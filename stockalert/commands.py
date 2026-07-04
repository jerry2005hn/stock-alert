import asyncio
from discord.ext import commands
from . import storage
from .config import VALID_DIRECTIONS, log
from .prices import fetch_price


class StockCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="watch")
    async def watch(self, ctx: commands.Context, ticker: str, direction: str, price: str) -> None:
        ticker = ticker.upper().strip()
        direction = direction.lower().strip()

        if direction not in VALID_DIRECTIONS:
            await ctx.send(f"Direction must be one of {VALID_DIRECTIONS}, got `{direction}`.")
            return

        try:
            threshold = float(price)
            if threshold <= 0:
                raise ValueError
        except ValueError:
            await ctx.send(f"`{price}` is not a valid positive price.")
            return

        await ctx.send(f"Checking `{ticker}`…")
        current = await asyncio.to_thread(fetch_price, ticker)
        if current is None:
            await ctx.send(f"Couldn't fetch a price for `{ticker}` — is it a valid ticker?")
            return

        self.bot.watchlist.append(
            {"ticker": ticker, "direction": direction, "price": threshold}
        )
        storage.save_watchlist(self.bot.watchlist)
        await ctx.send(
            f"✅ Watching **{ticker}** for price **{direction} {threshold:g}** "
            f"(current: {current:.2f})."
        )

    @commands.command(name="alerts")
    async def alerts(self, ctx: commands.Context) -> None:
        if not self.bot.watchlist:
            await ctx.send("No active alerts. Add one with `!watch AAPL above 200`.")
            return
        lines = [
            f"• **{a['ticker']}** {a['direction']} {a['price']:g}"
            for a in self.bot.watchlist
        ]
        await ctx.send("**Active alerts:**\n" + "\n".join(lines))

    @commands.command(name="clear")
    async def clear(self, ctx: commands.Context, ticker: str) -> None:
        ticker = ticker.upper().strip()
        before = len(self.bot.watchlist)
        self.bot.watchlist = [a for a in self.bot.watchlist if a["ticker"] != ticker]
        removed = before - len(self.bot.watchlist)
        storage.save_watchlist(self.bot.watchlist)
        if removed:
            await ctx.send(f"🗑️ Removed {removed} alert(s) for **{ticker}**.")
        else:
            await ctx.send(f"No alerts found for **{ticker}**.")

    @watch.error
    @clear.error
    async def command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "Usage:\n"
                "`!watch <TICKER> <above|below> <price>`\n"
                "`!clear <TICKER>`"
            )
        else:
            log.exception("Command error: %s", error)
            await ctx.send("Something went wrong handling that command.")
