import asyncio
from typing import Optional
import discord
from discord.ext import commands, tasks
from . import storage
from .config import ALERT_CHANNEL_ID, POLL_INTERVAL, RECURRING, log
from .prices import fetch_price, is_triggered


class PricePoller(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.price_poller.start()

    def cog_unload(self) -> None:
        self.price_poller.cancel()

    @tasks.loop(seconds=POLL_INTERVAL)
    async def price_poller(self) -> None:
        if not self.bot.watchlist:
            return

        channel = self.bot.get_channel(ALERT_CHANNEL_ID)
        if channel is None:
            log.error("Alert channel %s not found; is ALERT_CHANNEL_ID correct?", ALERT_CHANNEL_ID)
            return

        tickers = {a["ticker"] for a in self.bot.watchlist}
        prices: dict[str, Optional[float]] = {}
        for ticker in tickers:
            prices[ticker] = await asyncio.to_thread(fetch_price, ticker)

        survivors: list[dict] = []
        changed = False
        for alert in self.bot.watchlist:
            price = prices.get(alert["ticker"])
            if price is None:
                survivors.append(alert)
                continue

            if is_triggered(alert["direction"], alert["price"], price):
                await self._send_alert(channel, alert, price)
                if RECURRING:
                    survivors.append(alert)
                else:
                    changed = True
            else:
                survivors.append(alert)

        self.bot.watchlist = survivors
        if changed:
            storage.save_watchlist(self.bot.watchlist)

    @price_poller.before_loop
    async def before_poller(self) -> None:
        await self.bot.wait_until_ready()

    async def _send_alert(
        self, channel: discord.abc.Messageable, alert: dict, price: float
    ) -> None:
        arrow = "📈" if alert["direction"] == "above" else "📉"
        try:
            await channel.send(
                f"{arrow} **{alert['ticker']}** is now **{price:.2f}**, "
                f"crossing your **{alert['direction']} {alert['price']:g}** alert."
            )
        except discord.DiscordException as exc:
            log.error("Failed to send alert for %s: %s", alert["ticker"], exc)
