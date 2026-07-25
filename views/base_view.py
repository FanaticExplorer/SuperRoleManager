import discord


class BaseEphemeralView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=5 * 60)  # 5 minutes
        self.message = None

    async def on_timeout(self):
        if self.message:
            try:
                await self.message.delete()
            except (discord.NotFound, discord.HTTPException):
                pass
