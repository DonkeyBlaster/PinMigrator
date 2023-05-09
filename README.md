# pin-migrator
Lightweight Discord bot that watches a server for pins, then immediately unpins that message and sends a link to it in some other channel.
Also works with the ⭐ and 📌 reactions.

## Usage
Clone the repo, then run `pip install -r requirements.txt` to install dependencies. 
Rename `.env_example` to `.env` and place bot token and pin channel ID there.
Then run `python3 main.py` to start the bot.

Built on Python 3.10, untested on other versions.