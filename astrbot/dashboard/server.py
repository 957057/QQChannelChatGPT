import logging
import asyncio
from quart import Quart
from quart.logging import default_handler
from core.core_lifecycle import AstrBotCoreLifecycle
from .routes import *
from core import logger
from core.db import BaseDatabase
from core.plugin.plugin_manager import PluginManager
from core.updator import AstrBotUpdator
from core.utils.io import get_local_ip_addresses
from core.config import AstrBotConfig
from core.db import BaseDatabase

class AstrBotDashboard():
    def __init__(self, core_lifecycle: AstrBotCoreLifecycle, db: BaseDatabase) -> None:
        self.core_lifecycle = core_lifecycle
        self.config = core_lifecycle.astrbot_config
        self.app = Quart("dashboard", static_folder="dist", static_url_path="/")
        self.app.json.sort_keys = False
        
        logging.getLogger(self.app.name).removeHandler(default_handler)
        
        self.ar = AuthRoute(self.config, self.app)
        self.ur = UpdateRoute(self.config, self.app, core_lifecycle.astrbot_updator)
        self.sr = StatRoute(self.config, self.app, db, core_lifecycle)
        self.pr = PluginRoute(self.config, self.app, core_lifecycle, core_lifecycle.plugin_manager)
        self.cr = ConfigRoute(self.config, self.app, core_lifecycle)
        self.lr = LogRoute(self.config, self.app, core_lifecycle.log_broker)
        self.sfr = StaticFileRoute(self.config, self.app)
    
    async def shutdown_trigger_placeholder(self):
        while not self.core_lifecycle.event_queue.closed:
            await asyncio.sleep(1)
        logger.info("管理面板已关闭。")
        
    def run(self):
        ip_addr = get_local_ip_addresses()
        logger.info(f"\n-----\n🌈 管理面板已启动，可访问 \n1. http://{ip_addr}:6185\n2. http://localhost:6185 登录。\n------")
        return self.app.run_task(host="0.0.0.0", port=6185, shutdown_trigger=self.shutdown_trigger_placeholder)