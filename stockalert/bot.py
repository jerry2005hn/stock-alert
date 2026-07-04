import discord
from discord.ext import commands
from . import config, storage
from .commands import StockCommands
from .poller import PricePoller


class StockAlertBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.watchlist = storage.load_watchlist()

    async def setup_hook(self) -> None:
        """Register cogs before the gateway connection is established."""
        await self.add_cog(StockCommands(self))
        await self.add_cog(PricePoller(self))

    async def on_ready(self) -> None:
        config.log.info("Logged in as %s (id=%s)", self.user, self.user.id)
        config.log.info("Loaded %d alert(s) from watchlist", len(self.watchlist))
