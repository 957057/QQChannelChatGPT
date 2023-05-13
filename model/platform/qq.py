from nakuru.entities.components import Plain, At, Image

class QQ:
    def run_bot(self, gocq):
        self.client = gocq
        self.client.run()

    async def send_qq_msg(self, 
                          source, 
                          res, 
                          image_mode: bool = False):
        """
         res可以是一个数组，也就是gocq的消息链.
        """

        # print(res)
        print("[System-Info] 回复QQ消息中..."+str(res))

        if isinstance(res, list) and len(res) > 0:
            await self.client.sendGroupMessage(source.group_id, res)
            return
        # 通过消息链处理
        if not image_mode:
            if source.type == "GroupMessage":
                await self.client.sendGroupMessage(source.group_id, [
                    At(qq=source.user_id),
                    Plain(text=res)
                ])
            elif source.type == "FriendMessage":
                await self.client.sendFriendMessage(source.user_id, [
                    Plain(text=res)
                ])
        else:
            if source.type == "GroupMessage":
                await self.client.sendGroupMessage(source.group_id, [
                    At(qq=source.user_id),
                    Plain(text="好的，我根据你的需要为你生成了一张图片😊"),
                    Image.fromURL(url=res)
                ])
            elif source.type == "FriendMessage":
                await self.client.sendFriendMessage(source.user_id, [
                    Plain(text="好的，我根据你的需要为你生成了一张图片😊"),
                    Image.fromURL(url=res)
                ])