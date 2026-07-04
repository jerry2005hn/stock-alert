# Stock Alert Discord Bot

A Discord bot that monitors stock prices with [yfinance](https://pypi.org/project/yfinance/)
and posts a message to a channel when a price threshold is crossed. The watchlist
is persisted to a local JSON file, so your alerts survive restarts.

## Commands

| Command | Description | Example |
| --- | --- | --- |
| `!watch <TICKER> <above\|below> <price>` | Add an alert | `!watch AAPL above 200` |
| `!alerts` | List all active alerts | `!alerts` |
| `!clear <TICKER>` | Remove all alerts for a ticker | `!clear AAPL` |

By default an alert **fires once and auto-removes**. Set `RECURRING=true` in your
`.env` to make alerts re-fire on every crossing instead.