import inspect
import functools
import os
import sys
import traceback
import yaml
import logging
from types import ModuleType
from typing import List
from pip import main as pip_main
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core import logger
from .context import Context
from . import StarMetadata
from .updator import PluginUpdator
from astrbot.core.utils.io import remove_dir
from .star import star_registry, star_map
from .star_handler import star_handlers_registry
from astrbot.core.provider.register import llm_tools

class PluginManager:
    def __init__(
        self, 
        context: Context,
        config: AstrBotConfig    
    ):
        self.updator = PluginUpdator(config['plugin_repo_mirror'])
        
        self.context = context
                
        self.config = config
        self.plugin_store_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../data/plugins"))
        self.reserved_plugin_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../packages"))

    def _get_classes(self, arg: ModuleType):
        classes = []
        clsmembers = inspect.getmembers(arg, inspect.isclass)
        for (name, _) in clsmembers:
            if name.lower().endswith("plugin") or name.lower() == "main":
                classes.append(name)
                break
        return classes

    def _get_modules(self, path):
        modules = []

        dirs = os.listdir(path)
        # 遍历文件夹，找到 main.py 或者和文件夹同名的文件
        for d in dirs:
            if os.path.isdir(os.path.join(path, d)):
                if os.path.exists(os.path.join(path, d, "main.py")):
                    module_str = 'main'
                elif os.path.exists(os.path.join(path, d, d + ".py")):
                    module_str = d
                else:
                    print(f"插件 {d} 未找到 main.py 或者 {d}.py，跳过。")
                    continue
                if os.path.exists(os.path.join(path, d, "main.py")) or os.path.exists(os.path.join(path, d, d + ".py")):
                    modules.append({
                        "pname": d,
                        "module": module_str,
                        "module_path": os.path.join(path, d, module_str)
                    })
        return modules
    
    def _get_plugin_modules(self) -> List[dict]:
        plugins = []
        if os.path.exists(self.plugin_store_path):
            plugins.extend(self._get_modules(self.plugin_store_path))
        if os.path.exists(self.reserved_plugin_path):
            _p = self._get_modules(self.reserved_plugin_path)
            for p in _p:
                p['reserved'] = True
            plugins.extend(_p)
        return plugins
        
    def _check_plugin_dept_update(self, target_plugin: str = None):
        '''检查插件的依赖
        如果 target_plugin 为 None，则检查所有插件的依赖
        '''
        plugin_dir = self.plugin_store_path
        if not os.path.exists(plugin_dir):
            return False
        to_update = []
        if target_plugin:
            to_update.append(target_plugin)
        else:
            for p in self.context.get_all_stars():
                to_update.append(p.root_dir_name)
        for p in to_update:
            plugin_path = os.path.join(plugin_dir, p)
            if os.path.exists(os.path.join(plugin_path, "requirements.txt")):
                pth = os.path.join(plugin_path, "requirements.txt")
                logger.info(f"正在检查插件 {p} 的依赖: {pth}")
                try:
                    self._update_plugin_dept(os.path.join(plugin_path, "requirements.txt"))
                except Exception as e:
                    logger.error(f"更新插件 {p} 的依赖失败。Code: {str(e)}")

    def _update_plugin_dept(self, path):
        '''更新插件的依赖'''
        args = ['install', '-r', path, '--trusted-host', 'mirrors.aliyun.com', '-i', 'https://mirrors.aliyun.com/pypi/simple/']
        if self.config.pip_install_arg:
            args.extend(self.config.pip_install_arg)
        result_code = pip_main(args)
        if result_code != 0:
            raise Exception(str(result_code))  

    def _load_plugin_metadata(self, plugin_path: str, plugin_obj = None) -> StarMetadata:
        '''v3.4.0 以前的方式载入插件元数据
        
        先寻找 metadata.yaml 文件，如果不存在，则使用插件对象的 info() 函数获取元数据。
        '''
        metadata = None
        
        if not os.path.exists(plugin_path):
            raise Exception("插件不存在。")
        
        if os.path.exists(os.path.join(plugin_path, "metadata.yaml")):
            with open(os.path.join(plugin_path, "metadata.yaml"), "r", encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
        elif plugin_obj:
            # 使用 info() 函数
            metadata = plugin_obj.info()
        
        if isinstance(metadata, dict):
            if 'name' not in metadata or 'desc' not in metadata or 'version' not in metadata or 'author' not in metadata:
                raise Exception("插件元数据信息不完整。")
            metadata = StarMetadata(
                name=metadata['name'],
                author=metadata['author'],
                desc=metadata['desc'],
                version=metadata['version'],
                repo=metadata['repo'] if 'repo' in metadata else None
            )
            
        return metadata
    
    def reload(self):
        '''扫描并加载所有的 Star'''
        for smd in star_registry:
            logger.debug(f"尝试终止插件 {smd.name} ...")
            if hasattr(smd.star_cls, "__del__"):
                smd.star_cls.__del__()
            
        star_handlers_registry.clear()
        star_handlers_registry.star_handlers_map.clear()
        star_map.clear()
        star_registry.clear()
        for key in list(sys.modules.keys()):
            if key.startswith("data.plugins") or key.startswith("packages"):
                del sys.modules[key]
        
        plugin_modules = self._get_plugin_modules()
        if plugin_modules is None:
            return False, "未找到任何插件模块"
        fail_rec = ""
        
        # 导入 Star 模块，并尝试实例化 Star 类
        for plugin_module in plugin_modules:
            try:
                module_str = plugin_module['module']
                # module_path = plugin_module['module_path']
                root_dir_name = plugin_module['pname']
                reserved = plugin_module.get('reserved', False)
                
                logger.info(f"正在载入插件 {root_dir_name} ...")
                
                # 尝试导入模块
                path = "data.plugins." if not reserved else "packages."
                path += root_dir_name + "." + module_str
                try:
                    module = __import__(path, fromlist=[module_str])
                except (ModuleNotFoundError, ImportError):
                    # 尝试安装依赖
                    self._check_plugin_dept_update(target_plugin=root_dir_name)
                    module = __import__(path, fromlist=[module_str])
                except Exception as e:
                    logger.error(traceback.format_exc())
                    logger.error(f"插件 {root_dir_name} 导入失败。原因：{str(e)}")
                    continue

                if path in star_map:
                    # 通过装饰器的方式注册插件
                    star_metadata = star_map[path]
                    star_metadata.star_cls = star_metadata.star_cls_type(context=self.context)
                    star_metadata.module = module
                    star_metadata.root_dir_name = root_dir_name
                    star_metadata.reserved = reserved
                    
                    related_handlers = star_handlers_registry.get_handlers_by_module_name(star_metadata.module_path)
                    for handler in related_handlers:
                        logger.debug(f"bind handler {handler.handler_name} to {star_metadata.name}")
                        # handler.handler.__self__ = star_metadata.star_cls # 绑定 handler 的 self
                        handler.handler = functools.partial(handler.handler, star_metadata.star_cls)
                    # llm_tool
                    for func_tool in llm_tools.func_list:
                        if func_tool.handler.__module__ == star_metadata.module_path:
                            func_tool.handler = functools.partial(func_tool.handler, star_metadata.star_cls)
                    
                else:
                    # v3.4.0 以前的方式注册插件
                    logger.debug(f"插件 {path} 未通过装饰器注册。尝试通过旧版本方式载入。")
                    classes = self._get_classes(module)
                    try:
                        obj = getattr(module, classes[0])(context=self.context)
                    except BaseException as e:
                        logger.error(f"插件 {root_dir_name} 实例化失败。")
                        raise e
                    
                    metadata = None
                    plugin_path = os.path.join(self.plugin_store_path, root_dir_name) if not reserved else os.path.join(self.reserved_plugin_path, root_dir_name)
                    metadata = self._load_plugin_metadata(plugin_path=plugin_path, plugin_obj=obj)
                    metadata.star_cls = obj
                    metadata.module = module
                    metadata.root_dir_name = root_dir_name
                    metadata.reserved = reserved
                    metadata.star_cls_type = obj.__class__
                    metadata.module_path = path
                    star_map[path] = metadata
                    star_registry.append(metadata)
                    logger.debug(f"插件 {root_dir_name} 载入成功。")
                    
            except BaseException as e:
                traceback.print_exc()
                fail_rec += f"加载 {path} 插件时出现问题，原因 {str(e)}\n"

        # 清除 pip.main 导致的多余的 logging handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        if not fail_rec:
            return True, None
        else:
            return False, fail_rec
        
    async def install_plugin(self, repo_url: str):
        plugin_path = await self.updator.install(repo_url)
        # reload the plugin
        self.reload()
        return plugin_path
    
    async def uninstall_plugin(self, plugin_name: str):
        plugin = self.context.get_registered_star(plugin_name)
        if not plugin:
            raise Exception("插件不存在。")
        if plugin.reserved:
            raise Exception("该插件是 AstrBot 保留插件，无法卸载。")
        root_dir_name = plugin.root_dir_name
        ppath = self.plugin_store_path
        
        # 从 star_registry 和 star_map 中删除
        del star_map[plugin.module_path]
        for i, p in enumerate(star_registry):
            if p.name == plugin_name:
                del star_registry[i]
                break
        for handler in star_handlers_registry.get_handlers_by_module_name(plugin.module_path):
            logger.debug(f"unbind handler {handler.handler_name} from {plugin_name}")
            star_handlers_registry.remove(handler)
        keys_to_delete = [k for k, v in star_handlers_registry.star_handlers_map.items() if k.startswith(plugin.module_path)]
        for k in keys_to_delete:
            v = star_handlers_registry.star_handlers_map[k]
            logger.debug(f"unbind handler {v.handler_name} from {plugin_name} (map)")
            del star_handlers_registry.star_handlers_map[k]
        
        if not remove_dir(os.path.join(ppath, root_dir_name)):
            raise Exception("移除插件成功，但是删除插件文件夹失败。您可以手动删除该文件夹，位于 addons/plugins/ 下。")

    async def update_plugin(self, plugin_name: str):
        plugin = self.context.get_registered_star(plugin_name)
        if not plugin:
            raise Exception("插件不存在。")
        if plugin.reserved:
            raise Exception("该插件是 AstrBot 保留插件，无法更新。")
        
        await self.updator.update(plugin)
        self.reload()
        
    def install_plugin_from_file(self, zip_file_path: str):
        desti_dir = os.path.join(self.plugin_store_path, os.path.basename(zip_file_path))
        self.updator.unzip_file(zip_file_path, desti_dir)

        # remove the zip
        try:
            os.remove(zip_file_path)
        except BaseException as e:
            logger.warning(f"删除插件压缩包失败: {str(e)}")
        
        self._check_plugin_dept_update()

