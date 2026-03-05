# Perfect Stranger Twitch Bot

A Twitch chat bot that tracks chatter activity, builds leaderboard rankings, and posts periodic updates in chat.

## Features

- Tracks points per chatter during stream chat.
- Applies custom point adjustments based on message content.
- Supports subscriber bonus logic.
- Posts leaderboard updates on a schedule.
- Generates final leaderboard output files.
- Includes runtime control:
  - Default run time is 12 hours.
  - Auto-shuts down when timer expires.
  - Host/mod can restart the timer from chat.

## Project Structure

- Main bot file: `Perfectstranger.py`
- Auth token import: `clientshit.py` (expects `access_token`)
- Output files:
  - `Total_Chatter.csv`
  - `Rank_User.csv`
  - `Perfectstranger.txt`
  - `user1.txt`, `user2.txt`, `user3.txt`

## Requirements

- Python 3.10+
- Packages:
  - twitchio
  - pandas

Install dependencies:

```bash
pip install twitchio pandas
```

## Configuration

1. Put your Twitch OAuth token in `clientshit.py` as:

```python
access_token = "oauth:your_token_here"
```

2. Confirm channel and nick values in `Perfectstranger.py` are correct for your stream.

## Run the Bot

From the `perfectstrangerbot` folder:

```bash
python Perfectstranger.py
```

### Optional Runtime Argument

You can pass a custom runtime in minutes (minimum enforced is 720 minutes / 12 hours):

```bash
python Perfectstranger.py --runtime-minutes 900
```

## In-Chat Timer Commands

Host/mod only:

- `!restarttimer=`
  - Restarts timer to default 12 hours.
- `!restarttimer(x)`
  - Restarts timer to `x` hours.
  - Example: `!restarttimer(16)`

Also accepted:

- `!restarttimer=16`
- `!restarttimer 16`

## Stopping Early

- You can stop the bot early at any time with `Ctrl+C` in the running terminal.

## Notes

- The bot currently sends leaderboard messages to `codingwithstrangers` channel as configured in code.
- If you move folders, update hardcoded file paths in `Perfectstranger.py`.
