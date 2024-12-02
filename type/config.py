VERSION = '3.3.19'
DB_PATH = 'data/data_v2.db'

# 新版本配置文件，摈弃旧版本令人困惑的配置项 :D
DEFAULT_CONFIG_VERSION_2 = {
    "config_version": 2,
    "platform": [
        {
            "id": "default",
            "name": "qq_official",
            "enable": False,
            "appid": "",
            "secret": "",
            "enable_group_c2c": True,
            "enable_guild_direct_message": True,
        },
        {
            "id": "default",
            "name": "nakuru",
            "enable": False,
            "host": "172.0.0.1",
            "port": 5700,
            "websocket_port": 6700,
            "enable_group": True,
            "enable_guild": True,
            "enable_direct_message": True,
            "enable_group_increase": True,
        },
        {
            "id": "default",
            "name": "aiocqhttp",
            "enable": False,
            "ws_reverse_host": "",
            "ws_reverse_port": 6199,
        }
    ],
    "platform_settings": {
        "unique_session": False,
        "rate_limit": {
            "time": 60,
            "count": 30,
        },
        "reply_prefix": "",
        "forward_threshold": 200, # 转发消息的阈值
    },
    "llm": [
        {
            "id": "default",
            "name": "openai",
            "enable": True,
            "key": [],
            "api_base": "",
            "prompt_prefix": "",
            "default_personality": "",
            "model_config": {
                "model": "gpt-4o",
                "max_tokens": 6000,
                "temperature": 0.9,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
            },
            "image_generation_model_config": {
                "enable": True,
                "model": "dall-e-3",
                "size": "1024x1024",
                "style": "vivid",
                "quality": "standard",
            }
        },
    ],
    "llm_settings": {
        "wake_prefix": "",
        "web_search": False,
        "identifier": False,
    },
    "content_safety": {
        "baidu_aip": {
            "enable": False,
            "app_id": "",
            "api_key": "",
            "secret_key": "",
        },
        "internal_keywords": {
            "enable": True,
            "extra_keywords": [],
        }
    },
    "wake_prefix": ["/"],
    "t2i": True,
    "dump_history_interval": 10,
    "admins_id": [],
    "https_proxy": "",
    "http_proxy": "",
    "dashboard": {
        "enable": True,
        "username": "",
        "password": "",
    },
    "log_level": "INFO",
    "t2i_endpoint": "",
    "pip_install_arg": "",
    "plugin_repo_mirror": "default",
}

# 这个是用于迁移旧版本配置文件的映射表
MAPPINGS_1_2 = [
    [["qqbot", "enable"], ["platform", 0, "enable"]],
    [["qqbot", "appid"], ["platform", 0, "appid"]],
    [["qqbot", "token"], ["platform", 0, "secret"]],
    [["qqofficial_enable_group_message"], ["platform", 0, "enable_group_c2c"]],
    [["direct_message_mode"], ["platform", 0, "enable_guild_direct_message"]],
    [["gocqbot", "enable"], ["platform", 1, "enable"]],
    [["gocq_host"], ["platform", 1, "host"]],
    [["gocq_http_port"], ["platform", 1, "port"]],
    [["gocq_websocket_port"], ["platform", 1, "websocket_port"]],
    [["gocq_react_group"], ["platform", 1, "enable_group"]],
    [["gocq_react_guild"], ["platform", 1, "enable_guild"]],
    [["gocq_react_friend"], ["platform", 1, "enable_direct_message"]],
    [["gocq_react_group_increase"], ["platform", 1, "enable_group_increase"]],
    [["aiocqhttp", "enable"], ["platform", 2, "enable"]],
    [["aiocqhttp", "ws_reverse_host"], ["platform", 2, "ws_reverse_host"]],
    [["aiocqhttp", "ws_reverse_port"], ["platform", 2, "ws_reverse_port"]],
    [["uniqueSessionMode"], ["platform_settings", "unique_session"]],
    [["limit", "time"], ["platform_settings", "rate_limit", "time"]],
    [["limit", "count"], ["platform_settings", "rate_limit", "count"]],
    [["reply_prefix"], ["platform_settings", "reply_prefix"]],
    [["qq_forward_threshold"], ["platform_settings", "forward_threshold"]],
    
    [["openai", "key"], ["llm", 0, "key"]],
    [["openai", "api_base"], ["llm", 0, "api_base"]],
    [["openai", "chatGPTConfigs", "model"], ["llm", 0, "model_config", "model"]],
    [["openai", "chatGPTConfigs", "max_tokens"], ["llm", 0, "model_config", "max_tokens"]],
    [["openai", "chatGPTConfigs", "temperature"], ["llm", 0, "model_config", "temperature"]],
    [["openai", "chatGPTConfigs", "top_p"], ["llm", 0, "model_config", "top_p"]],
    [["openai", "chatGPTConfigs", "frequency_penalty"], ["llm", 0, "model_config", "frequency_penalty"]],
    [["openai", "chatGPTConfigs", "presence_penalty"], ["llm", 0, "model_config", "presence_penalty"]],    
    
    [["default_personality_str"], ["llm", 0, "default_personality"]],
    [["llm_env_prompt"], ["llm", 0, "prompt_prefix"]],
    [["openai_image_generate", "model"], ["llm", 0, "image_generation_model_config", "model"]],
    [["openai_image_generate", "size"], ["llm", 0, "image_generation_model_config", "size"]],
    [["openai_image_generate", "style"], ["llm", 0, "image_generation_model_config", "style"]],
    [["openai_image_generate", "quality"], ["llm", 0, "image_generation_model_config", "quality"]],
    
    [["llm_wake_prefix"], ["llm_settings", "wake_prefix"]],
    
    [["baidu_aip", "enable"], ["content_safety", "baidu_aip", "enable"]],
    [["baidu_aip", "app_id"], ["content_safety", "baidu_aip", "app_id"]],
    [["baidu_aip", "api_key"], ["content_safety", "baidu_aip", "api_key"]],
    [["baidu_aip", "secret_key"], ["content_safety", "baidu_aip", "secret_key"]],
    
    [["qq_pic_mode"], ["t2i"]],
    [["dump_history_interval"], ["dump_history_interval"]],
    [["other_admins"], ["admins_id"]],
    [["http_proxy"], ["http_proxy"]],
    [["https_proxy"], ["https_proxy"]],
    [["dashboard_username"], ["dashboard", "username"]],
    [["dashboard_password"], ["dashboard", "password"]],
    [["nick_qq"], ["wake_prefix"]],
]

# 配置项的中文描述、值类型
CONFIG_METADATA_2 = {
    "config_version": {"description": "配置版本", "type": "int"},
    "platform": {
        "description": "平台配置",
        "type": "list",
        "items": {
            "id": {"description": "ID", "type": "string", "hint": "提供商 ID 名，用于在多实例下方便管理和识别。自定义，ID 不能重复。"},
            "name": {"description": "适配器类型", "type": "string", "hint": "当前版本下，支持 `qq_official`（QQ 官方机器人）, `aiocqhttp`(Onebot 适用), `nakuru` 三种适配器类型。", "options": ["qq_official", "aiocqhttp", "nakuru"]},
            "enable": {"description": "启用", "type": "bool", "hint": "是否启用该适配器。未启用的适配器对应的消息平台将不会接收到消息。"},
            "appid": {"description": "appid", "type": "string", "hint": "必填项。QQ 官方机器人平台的 appid。如何获取请参考文档。"},
            "secret": {"description": "secret", "type": "string", "hint": "必填项。QQ 官方机器人平台的 secret。如何获取请参考文档。"},
            "enable_group_c2c": {"description": "启用消息列表单聊", "type": "bool", "hint": "启用后，机器人可以接收到 QQ 消息列表中的私聊消息。你可能需要在 QQ 机器人平台上通过扫描二维码的方式添加机器人为你的好友。详见文档。"},
            "enable_guild_direct_message": {"description": "启用频道私聊", "type": "bool", "hint": "启用后，机器人可以接收到频道的私聊消息。"},
            "host": {"description": "主机地址", "type": "string", "hint": "Nakuru 适配器的服务器 IP 地址，不包含端口号。"},
            "port": {"description": "端口", "type": "int", "hint": "Nakuru 适配器的 HTTP 端口。"},
            "websocket_port": {"description": "Websocket 端口", "type": "int", "hint": "Nakuru 适配器的 Websocket 端口。"},
            "ws_reverse_host": {"description": "反向 Websocket 主机地址", "type": "string", "hint": "aiocqhttp 适配器的反向 Websocket 服务器 IP 地址，不包含端口号。"},
            "ws_reverse_port": {"description": "反向 Websocket 端口", "type": "int", "hint": "aiocqhttp 适配器的反向 Websocket 端口。"},
            "enable_group": {"description": "接收群组消息", "type": "bool", "hint": "启用后，机器人可以接收到群组消息。"},
            "enable_guild": {"description": "接收频道消息", "type": "bool", "hint": "启用后，机器人可以接收到频道消息。"},
            "enable_direct_message": {"description": "接收频道私聊", "type": "bool", "hint": "启用后，机器人可以接收到频道的私聊消息。"},
        }
    },
    "platform_settings": {
        "description": "平台设置",
        "type": "object",
        "items": {
            "unique_session": {"description": "会话隔离", "type": "bool", "hint": "启用后，在群组或者频道中，每个人的消息上下文都是独立的。"},
            "rate_limit": {
                "description": "速率限制",
                "hint": "每个会话在 `time` 秒内最多只能发送 `count` 条消息。",
                "type": "object",
                "items": {
                    "time": {"description": "消息速率限制时间", "type": "int"},
                    "count": {"description": "消息速率限制计数", "type": "int"},
                }
            },
            "reply_prefix": {"description": "回复前缀", "type": "string", "hint": "机器人回复消息时带有的前缀。"},
            "forward_threshold": {"description": "转发消息的字数阈值", "type": "int", "hint": "超过一定字数后，机器人会将消息折叠成 QQ 群聊的 “转发消息”，以防止刷屏。目前仅 QQ 平台适配器适用。"},
        }
    },
    "llm": {
        "description": "大语言模型配置",
        "type": "list",
        "items": {
            "id": {"description": "ID", "type": "string", "hint": "提供商 ID 名，用于在多实例下方便管理和识别。自定义，ID 不能重复。"},
            "name": {"description": "模型提供商类型", "type": "string", "hint": "当前版本下，支持 `openai` 一个模型提供商。", "options": ["openai"]},
            "enable": {"description": "启用", "type": "bool", "hint": "是否启用该模型。未启用的模型将不会被使用。"},
            "key": {"description": "API Key", "type": "list", "items": {"type": "string"}, "hint": "API Key 列表。填写好后输入回车即可添加 API Key。支持多个 API Key。"},
            "api_base": {"description": "API Base URL", "type": "string", "hint": "API Base URL 请在在模型提供商处获得。支持 Ollama 开放的 API 地址。如果您确认填写正确但是使用时出现了 404 异常，可以尝试在地址末尾加上 `/v1`。"},
            "prompt_prefix": {"description": "Prompt 前缀", "type": "text", "hint": "每次与 LLM 对话时在对话前加上的自定义文本。默认为空。"},
            "default_personality": {"description": "默认人格", "type": "text", "hint": "在当前版本下，默认人格文本会被添加到 LLM 对话的 `system` 字段中。"},
            "model_config": {
                "description": "模型配置",
                "type": "object",
                "items": {
                    "model": {"description": "模型名称", "type": "string", "hint": "大语言模型的名称，一般是小写的英文。如 gpt-4o-mini, deepseek-chat 等。"},
                    "max_tokens": {"description": "最大令牌数", "type": "int"},
                    "temperature": {"description": "温度", "type": "float"},
                    "top_p": {"description": "Top P值", "type": "float"},
                    "frequency_penalty": {"description": "频率惩罚", "type": "float"},
                    "presence_penalty": {"description": "存在惩罚", "type": "float"},
                }
            },
            "image_generation_model_config": {
                "description": "图像生成模型配置",
                "type": "object",
                "items": {
                    "enable": {"description": "启用", "type": "bool", "hint": "启用该功能需要提供商支持图像生成。如 dall-e-3"},
                    "model": {"description": "模型名称", "type": "string", "hint": "图像生成模型的名称，一般是小写的英文。如 dall-e-3"},
                    "size": {"description": "图像尺寸", "type": "string"},
                    "style": {"description": "图像风格", "type": "string"},
                    "quality": {"description": "图像质量", "type": "string"},
                }
            },
        }
    },
    "llm_settings": {
        "description": "大语言模型设置",
        "type": "object",
        "items": {
            "wake_prefix": {"description": "LLM 聊天额外唤醒前缀", "type": "string", "hint": "使用 LLM 聊天额外的触发条件。如填写 `chat`，则需要消息前缀加上 `/chat` 才能触发 LLM 聊天，是一个防止滥用的手段。"},
            "web_search": {"description": "启用网页搜索", "type": "bool", "hint": "能访问 Google 时效果最佳。如果 Google 访问失败，程序会依次访问 Bing, Sogo 搜索引擎。"},
            "identifier": {"description": "启动识别群员", "type": "bool", "hint": "在 Prompt 前加上群成员的名字以让模型更好地了解群聊状态。启用将略微增加 token 开销，"},
        }
    },
    "content_safety": {
        "description": "内容安全",
        "type": "object",
        "items": {
            "baidu_aip": {
                "description": "百度内容审核配置",
                "type": "object",
                "items": {
                    "enable": {"description": "启用百度内容审核", "type": "bool", "hint": "启用此功能前，您需要手动在设备中安装 baidu-aip 库。一般来说，安装指令如下: `pip3 install baidu-aip`"},
                    "app_id": {"description": "APP ID", "type": "string"},
                    "api_key": {"description": "API Key", "type": "string"},
                    "secret_key": {"description": "Secret Key", "type": "string"},
                }
            },
            "internal_keywords": {
                "description": "内部关键词过滤",
                "type": "object",
                "items": {
                    "enable": {"description": "启用内部关键词过滤", "type": "bool"},
                    "extra_keywords": {"description": "额外关键词", "type": "list", "items": {"type": "string"}, "hint": "额外的屏蔽关键词列表，支持正则表达式。"},
                }
            }
        }
    },
    "wake_prefix": {"description": "机器人唤醒前缀", "type": "list", "items": {"type": "string"}, "hint": "在不 @ 机器人的情况下，可以通过外加消息前缀来唤醒机器人。"},
    "t2i": {"description": "文本转图像", "type": "bool", "hint": "启用后，超出一定长度的文本将会通过 AstrBot API 渲染成 Markdown 图片发送。可以缓解审核和消息过长刷屏的问题，并提高 Markdown 文本的可读性。"},
    "dump_history_interval": {"description": "历史记录保存间隔", "type": "int", "hint": "每隔多少分钟将 LLM 聊天的历史记录转储到数据库。"},
    "admins_id": {"description": "管理员 ID", "type": "list", "items": {"type": "int"}, "hint": "管理员 ID 列表，管理员可以使用一些特权命令，如 `update`, `plugin` 等。ID 可以通过 `/myid` 指令获得。回车添加，可添加多个。"},
    "https_proxy": {"description": "HTTPS 代理", "type": "string", "hint": "启用后，会以添加环境变量的方式设置代理。格式为 `http://ip:port`"},
    "http_proxy": {"description": "HTTP 代理", "type": "string", "hint": "启用后，会以添加环境变量的方式设置代理。格式为 `http://ip:port`"},
    "dashboard": {
        "description": "管理面板配置",
        "type": "object",
        "items": {
            "enable": {"description": "启用", "type": "bool"},
            "username": {"description": "用户名", "type": "string"},
            "password": {"description": "密码", "type": "string"},
        }
    },
    "log_level": {"description": "控制台日志级别", "type": "string", "hint": "控制台输出日志的级别。", "options": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]},
    "t2i_endpoint": {"description": "文本转图像服务接口", "type": "string", "hint": "为空时使用 AstrBot API 服务"},
    "pip_install_arg": {"description": "pip 安装参数", "type": "string", "hint": "安装插件依赖时，会使用 Python 的 pip 工具。这里可以填写额外的参数，如 `--break-system-package` 等。"},
    "plugin_repo_mirror": {"description": "插件仓库镜像", "type": "string", "hint": "插件仓库的镜像地址，用于加速插件的下载。", "options": ["default", "https://github-mirror.us.kg/"]},
}
