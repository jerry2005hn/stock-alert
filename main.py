import logging
from stockalert import config
from stockalert.bot import StockAlertBot


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    if not config.DISCORD_TOKEN:
        raise SystemExit("DISCORD_TOKEN is not set. Copy .env.example to .env and fill it in.")
    if not config.ALERT_CHANNEL_ID:
        raise SystemExit("ALERT_CHANNEL_ID is not set (env var or config.json).")

    config.log.info(
        "Starting bot (poll every %ss, recurring=%s)",
        config.POLL_INTERVAL,
        config.RECURRING,
    )

    bot = StockAlertBot()
    bot.run(config.DISCORD_TOKEN, log_handler=None) 


if __name__ == "__main__":
    main()
