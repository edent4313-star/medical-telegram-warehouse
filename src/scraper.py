
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
import os
import json
import logging
from pathlib import Path
from datetime import datetime

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise ValueError(
        "TELEGRAM_API_ID or TELEGRAM_API_HASH "
        "not found in .env file"
    )

# =====================================================
# Logging Configuration
# =====================================================

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/scraper.log"),
        logging.StreamHandler()
    ]
)

# =====================================================
# Telegram Client
# =====================================================

client = TelegramClient(
    "session",
    API_ID,
    API_HASH
)

# =====================================================
# Channels
# Replace these with actual Telegram usernames
# =====================================================

CHANNELS = [
    "CheMed123",
   "lobelia4cosmetics",
    "tikvahpharma",
    "Pharmaimportt",
    "medicalethiopia"
]

# =====================================================
# Data Lake Base Path
# =====================================================

BASE_PATH = Path("data/raw")

# =====================================================
# Scrape Single Channel
# =====================================================

async def scrape_channel(channel_name):

    try:

        logging.info(
            f"Starting scraping channel: {channel_name}"
        )

        entity = await client.get_entity(channel_name)

        messages_data = []

        async for msg in client.iter_messages(entity):

            try:

                record = {
                    "message_id": msg.id,
                    "channel_name": channel_name,
                    "message_date": str(msg.date),
                    "message_text": msg.message,
                    "views": msg.views,
                    "forwards": msg.forwards,
                    "has_media": msg.media is not None,
                    "image_path": None
                }

                # Download image if available

                if isinstance(
                    msg.media,
                    MessageMediaPhoto
                ):

                    image_dir = (
                        BASE_PATH /
                        "images" /
                        channel_name
                    )

                    image_dir.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    image_file = (
                        image_dir /
                        f"{msg.id}.jpg"
                    )

                    await client.download_media(
                        msg,
                        file=image_file
                    )

                    record["image_path"] = str(
                        image_file
                    )

                    logging.info(
                        f"Downloaded image "
                        f"{msg.id} "
                        f"from {channel_name}"
                    )

                messages_data.append(record)

            except Exception as e:

                logging.error(
                    f"Message processing error | "
                    f"Channel={channel_name} | "
                    f"Message={msg.id} | "
                    f"Error={e}"
                )

        # =================================================
        # Save JSON
        # =================================================

        date_folder = datetime.now().strftime(
            "%Y-%m-%d"
        )

        output_dir = (
            BASE_PATH /
            "telegram_messages" /
            date_folder
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            output_dir /
            f"{channel_name}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                messages_data,
                f,
                ensure_ascii=False,
                indent=4
            )

        logging.info(
            f"Saved {len(messages_data)} messages "
            f"to {output_file}"
        )

        logging.info(
            f"Completed channel: {channel_name}"
        )

    except Exception as e:

        logging.exception(
            f"Failed to scrape "
            f"{channel_name}: {e}"
        )

# =====================================================
# Main Function
# =====================================================

async def main():

    logging.info(
        "Telegram scraper started"
    )

    try:

        await client.start()

        for channel in CHANNELS:

            await scrape_channel(channel)

    except Exception as e:

        logging.exception(
            f"Fatal Error: {e}"
        )

    finally:

        await client.disconnect()

        logging.info(
            "Telegram scraper finished"
        )

# =====================================================
# Run Application
# =====================================================

with client:
    client.loop.run_until_complete(main())