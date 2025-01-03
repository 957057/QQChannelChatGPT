import threading
import traceback
from .route import Route, Response, RouteContext
from quart import request
from astrbot.core.updator import AstrBotUpdator
from astrbot.core import logger

class UpdateRoute(Route):
    def __init__(self, context: RouteContext, astrbot_updator: AstrBotUpdator) -> None:
        super().__init__(context)
        self.routes = {
            '/update/check': ('GET', self.check_update),
            '/update/do': ('POST', self.update_project),
        }
        self.astrbot_updator = astrbot_updator
        self.register_routes()
    
    async def check_update(self):
        try:
            ret = await self.astrbot_updator.check_update(None, None)
            return Response(
                status="success",
                message=str(ret) if ret is not None else "已经是最新版本了。",
                data={
                    "has_new_version": ret is not None
                }
            ).__dict__
        except Exception as e:
            logger.error(traceback.format_exc())
            return Response().error(e.__str__()).__dict__
    
    async def update_project(self):
        data = await request.json
        version = data.get('version', '')
        reboot = data.get('reboot', True)
        if version == "" or version == "latest":
            latest = True
            version = ''
        else:
            latest = False
        try:
            await self.astrbot_updator.update(latest=latest, version=version)
            if reboot:
                threading.Thread(target=self.astrbot_updator._reboot, args=(2, )).start()
                return Response().ok(None, "更新成功，AstrBot 将在 2 秒内全量重启以应用新的代码。").__dict__
            else:
                return Response().ok(None, "更新成功，AstrBot 将在下次启动时应用新的代码。").__dict__
        except Exception as e:
            logger.error(f"/api/update_project: {traceback.format_exc()}")
            return Response().error(e.__str__()).__dict__