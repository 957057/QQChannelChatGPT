import websockets
import json
import threading
import asyncio
import os
import uuid
import logging
import traceback

from . import DashBoardData, Response
from flask import Flask, request
from werkzeug.serving import make_server
from astrbot.persist.helper import dbConn
from type.types import Context
from typing import List
from SparkleLogging.utils.core import LogManager
from logging import Logger
from dashboard.helper import DashBoardHelper
from util.io import get_local_ip_addresses
from model.plugin.manager import PluginManager
from util.updator.astrbot_updator import AstrBotUpdator
from type.config import CONFIG_METADATA_2


logger: Logger = LogManager.GetLogger(log_name='astrbot')


class AstrBotDashBoard():
    def __init__(self, context: Context, plugin_manager: PluginManager, astrbot_updator: AstrBotUpdator):
        self.context = context
        self.plugin_manager = plugin_manager
        self.astrbot_updator = astrbot_updator
        self.dashboard_data = DashBoardData()
        self.dashboard_helper = DashBoardHelper(self.context)
        
        self.dashboard_be = Flask(__name__, static_folder="dist", static_url_path="/")
        self.dashboard_be.json.sort_keys=False # 不按照字典排序
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        self.dashboard_be.logger.setLevel(logging.ERROR)
        
        self.ws_clients = {}  # remote_ip: ws
        self.loop = asyncio.get_event_loop()
        
        self.http_server_thread: threading.Thread = None 

        @self.dashboard_be.get("/")
        def index():
            # 返回页面
            return self.dashboard_be.send_static_file("index.html")
        
        @self.dashboard_be.get("/auth/login")
        def _():
            return self.dashboard_be.send_static_file("index.html")

        @self.dashboard_be.get("/config")
        def rt_config():
            return self.dashboard_be.send_static_file("index.html")

        @self.dashboard_be.get("/logs")
        def rt_logs():
            return self.dashboard_be.send_static_file("index.html")
        
        @self.dashboard_be.get("/extension")
        def rt_extension():
            return self.dashboard_be.send_static_file("index.html")

        @self.dashboard_be.get("/dashboard/default")
        def rt_dashboard():
            return self.dashboard_be.send_static_file("index.html")

        @self.dashboard_be.post("/api/authenticate")
        def authenticate():
            username = self.context.config_helper.dashboard.username
            password = self.context.config_helper.dashboard.password
            # 获得请求体
            post_data = request.json
            if post_data["username"] == username and post_data["password"] == password:
                return Response(
                    status="success",
                    message="登录成功。",
                    data={
                        "token": "astrbot-test-token",
                        "username": username
                    }
                ).__dict__
            else:
                return Response(
                    status="error",
                    message="用户名或密码错误。",
                    data=None
                ).__dict__

        @self.dashboard_be.post("/api/change_password")
        def change_password():
            password = self.context.config_helper.dashboard.password
            # 获得请求体
            post_data = request.json
            if post_data["password"] == password:
                self.context.config_helper.put("dashboard_password", post_data["new_password"])
                return Response(
                    status="success",
                    message="修改成功。",
                    data=None
                ).__dict__
            else:
                return Response(
                    status="error",
                    message="原密码错误。",
                    data=None
                ).__dict__

        @self.dashboard_be.get("/api/stats")
        def get_stats():
            db_inst = dbConn()
            all_session = db_inst.get_all_stat_session()
            last_24_message = db_inst.get_last_24h_stat_message()
            # last_24_platform = db_inst.get_last_24h_stat_platform()
            platforms = db_inst.get_platform_cnt_total()
            self.dashboard_data.stats["session"] = []
            self.dashboard_data.stats["session_total"] = db_inst.get_session_cnt_total(
            )
            self.dashboard_data.stats["message"] = last_24_message
            self.dashboard_data.stats["message_total"] = db_inst.get_message_cnt_total(
            )
            self.dashboard_data.stats["platform"] = platforms

            return Response(
                status="success",
                message="",
                data=self.dashboard_data.stats
            ).__dict__

        @self.dashboard_be.get("/api/configs")
        def get_configs():
            # namespace 为空时返回 AstrBot 配置
            # 否则返回指定 namespace 的插件配置
            namespace = "" if "namespace" not in request.args else request.args["namespace"]
            if not namespace:
                return Response(
                    status="success",
                    message="",
                    data=self._get_astrbot_config()
                ).__dict__
            return Response(
                status="success",
                message="",
                data=self._get_extension_config(namespace)
            ).__dict__

        @self.dashboard_be.post("/api/astrbot-configs")
        def post_astrbot_configs():
            post_configs = request.json
            try:
                self.save_astrbot_configs(post_configs)
                return Response(
                    status="success",
                    message="保存成功~ 机器人将在 3 秒内重启以应用新的配置。",
                    data=None
                ).__dict__
            except Exception as e:
                return Response(
                    status="error",
                    message=e.__str__(),
                    data=None
                ).__dict__
                
        @self.dashboard_be.post("/api/extension-configs")
        def post_extension_configs():
            post_configs = request.json
            try:
                self.save_extension_configs(post_configs)
                return Response(
                    status="success",
                    message="保存成功~ 机器人将在 3 秒内重启以应用新的配置。",
                    data=None
                ).__dict__
            except Exception as e:
                return Response(
                    status="error",
                    message=e.__str__(),
                    data=None
                ).__dict__

        @self.dashboard_be.get("/api/extensions")
        def get_plugins():
            _plugin_resp = []
            for plugin in self.context.cached_plugins:
                _p = plugin.metadata
                _t = {
                    "name": _p.plugin_name,
                    "repo": '' if _p.repo is None else _p.repo,
                    "author": _p.author,
                    "desc": _p.desc,
                    "version": _p.version
                }
                _plugin_resp.append(_t)
            return Response(
                status="success",
                message="",
                data=_plugin_resp
            ).__dict__

        @self.dashboard_be.post("/api/extensions/install")
        def install_plugin():
            post_data = request.json
            repo_url = post_data["url"]
            try:
                logger.info(f"正在安装插件 {repo_url}")
                self.plugin_manager.install_plugin(repo_url)
                threading.Thread(target=self.astrbot_updator._reboot, args=(2, self.context)).start()
                logger.info(f"安装插件 {repo_url} 成功，2秒后重启")
                return Response(
                    status="success",
                    message="安装成功，机器人将在 2 秒内重启。",
                    data=None
                ).__dict__
            except Exception as e:
                logger.error(f"/api/extensions/install: {traceback.format_exc()}")
                return Response(
                    status="error",
                    message=e.__str__(),
                    data=None
                ).__dict__
            
        @self.dashboard_be.post("/api/extensions/upload-install")
        def upload_install_plugin():
            try:
                file = request.files['file']
                print(file.filename)
                logger.info(f"正在安装用户上传的插件 {file.filename}")
                # save file to temp/
                file_path = f"temp/{uuid.uuid4()}.zip"
                file.save(file_path)
                self.plugin_manager.install_plugin_from_file(file_path)
                logger.info(f"安装插件 {file.filename} 成功")
                return Response(
                    status="success",
                    message="安装成功~",
                    data=None
                ).__dict__
            except Exception as e:
                logger.error(f"/api/extensions/upload-install: {traceback.format_exc()}")
                return Response(
                    status="error",
                    message=e.__str__(),
                    data=None
                ).__dict__

        @self.dashboard_be.post("/api/extensions/uninstall")
        def uninstall_plugin():
            post_data = request.json
            plugin_name = post_data["name"]
            try:
                logger.info(f"正在卸载插件 {plugin_name}")
                self.plugin_manager.uninstall_plugin(plugin_name)
                logger.info(f"卸载插件 {plugin_name} 成功")
                return Response(
                    status="success",
                    message="卸载成功~",
                    data=None
                ).__dict__
            except Exception as e:
                logger.error(f"/api/extensions/uninstall: {traceback.format_exc()}")
                return Response(
                    status="error",
                    message=e.__str__(),
                    data=None
                ).__dict__

        @self.dashboard_be.post("/api/extensions/update")
        def update_plugin():
            post_data = request.json
            plugin_name = post_data["name"]
            try:
                logger.info(f"正在更新插件 {plugin_name}")
                self.plugin_manager.update_plugin(plugin_name)
                threading.Thread(target=self.astrbot_updator._reboot, args=(2, self.context)).start()
                logger.info(f"更新插件 {plugin_name} 成功，2秒后重启")
                return Response(
                    status="success",
                    message="更新成功，机器人将在 2 秒内重启。",
                    data=None
                ).__dict__
            except Exception as e:
                logger.error(f"/api/extensions/update: {traceback.format_exc()}")
                return Response(
                    status="error",
                    message=e.__str__(),
                    data=None
                ).__dict__

        @self.dashboard_be.post("/api/log")
        def log():
            for item in self.ws_clients:
                try:
                    asyncio.run_coroutine_threadsafe(
                        self.ws_clients[item].send(request.data.decode()), self.loop).result()
                except Exception as e:
                    pass
            return 'ok'

        @self.dashboard_be.get("/api/check_update")
        def get_update_info():
            try:
                ret = self.astrbot_updator.check_update(None, None)
                return Response(
                    status="success",
                    message=str(ret) if ret is not None else "已经是最新版本了。",
                    data={
                        "has_new_version": ret is not None
                    }
                ).__dict__
            except Exception as e:
                logger.error(f"/api/check_update: {traceback.format_exc()}")
                return Response(
                    status="error",
                    message=e.__str__(),
                    data=None
                ).__dict__

        @self.dashboard_be.post("/api/update_project")
        def update_project_api():
            version = request.json['version']
            if version == "" or version == "latest":
                latest = True
                version = ''
            else:
                latest = False
            try:
                self.astrbot_updator.update(latest=latest, version=version)
                threading.Thread(target=self.astrbot_updator._reboot, args=(2, self.context)).start()
                return Response(
                    status="success",
                    message="更新成功，机器人将在 3 秒内重启。",
                    data=None
                ).__dict__
            except Exception as e:
                logger.error(f"/api/update_project: {traceback.format_exc()}")
                return Response(
                    status="error",
                    message=e.__str__(),
                    data=None
                ).__dict__

        @self.dashboard_be.get("/api/llm/list")
        def llm_list():
            ret = []
            for llm in self.context.llms:
                ret.append(llm.llm_name)
            return Response(
                status="success",
                message="",
                data=ret
            ).__dict__

        @self.dashboard_be.get("/api/llm")
        def llm():
            text = request.args["text"]
            llm = request.args["llm"]
            for llm_ in self.context.llms:
                if llm_.llm_name == llm:
                    try:
                        ret = asyncio.run_coroutine_threadsafe(
                            llm_.llm_instance.text_chat(text), self.loop).result()
                        return Response(
                            status="success",
                            message="",
                            data=ret
                        ).__dict__
                    except Exception as e:
                        return Response(
                            status="error",
                            message=e.__str__(),
                            data=None
                        ).__dict__

            return Response(
                status="error",
                message="LLM not found.",
                data=None
            ).__dict__
        
    def save_astrbot_configs(self, post_configs: dict):
        try:
            self.dashboard_helper.save_astrbot_config(post_configs)
            threading.Thread(target=self.astrbot_updator._reboot, args=(3, self.context), daemon=True).start()
        except Exception as e:
            raise e
    
    def save_extension_configs(self, post_configs: dict):
        try:
            self.dashboard_helper.save_extension_config(post_configs)
            threading.Thread(target=self.astrbot_updator._reboot, args=(3, self.context), daemon=True).start()
        except Exception as e:
            raise e
        
    def _get_astrbot_config(self):
        config = self.context.config_helper.to_dict()
        for key in self.dashboard_helper.config_key_dont_show:
            if key in config:
                del config[key]
        return {
            "metadata": CONFIG_METADATA_2,
            "config": config,
        }

    def _get_extension_config(self, namespace: str):
        path = f"data/config/{namespace}.json"
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8-sig") as f:
            return [{
                "config_type": "group",
                "name": namespace + " 插件配置",
                "description": "",
                "body": list(json.load(f).values())
            },]

    async def get_log_history(self):
        try:
            with open("logs/astrbot/astrbot.log", "r", encoding="utf-8") as f:
                return f.readlines()[-100:]
        except Exception as e:
            logger.warning(f"读取日志历史失败: {e.__str__()}")
            return []

    async def __handle_msg(self, websocket, path):
        address = websocket.remote_address
        self.ws_clients[address] = websocket
        data = await self.get_log_history()
        data = ''.join(data).replace('\n', '\r\n')
        await websocket.send(data)
        while True:
            try:
                msg = await websocket.recv()
            except websockets.exceptions.ConnectionClosedError:
                # logger.info(f"和 {address} 的 websocket 连接已断开")
                del self.ws_clients[address]
                break
            except Exception as e:
                # logger.info(f"和 {path} 的 websocket 连接发生了错误: {e.__str__()}")
                del self.ws_clients[address]
                break

    async def ws_server(self):
        ws_server = websockets.serve(self.__handle_msg, "0.0.0.0", 6186)
        logger.info("WebSocket 服务器已启动。")
        await ws_server
        
    def http_server(self):
        http_server = make_server(
            '0.0.0.0', 6185, self.dashboard_be, threaded=True)
        http_server.serve_forever()

    def run_http_server(self):
        self.http_server_thread = threading.Thread(target=self.http_server, daemon=True).start()
        ip_address = get_local_ip_addresses()
        ip_str = f"http://{ip_address}:6185"
        logger.info(f"HTTP 服务器已启动，可访问: {ip_str} 等来登录可视化面板。")
