import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
SUPPORT_CHAT = os.getenv('SUPPORT_CHAT', 'YOUR_SUPPORT_CHAT_ID_HERE')

# Bot Information
BOT_NAME = "Media Downloader Bot"
BOT_OWNER = "Your Name"
BOT_VERSION = "1.0.0"
HOSTED_AT = "Sevalla Platform"

# Download Settings
DOWNLOAD_TIMEOUT = 30  # seconds to wait for user response
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB max file size
TEMP_DIR = "downloads"

# YouTube Quality Options
YOUTUBE_QUALITIES = {
    "144p": "worst[height<=144]",
    "240p": "worst[height<=240]", 
    "360p": "worst[height<=360]",
    "480p": "worst[height<=480]",
    "720p": "best[height<=720]",
    "1080p": "best[height<=1080]",
    "Best": "best"
}

# Instagram Settings
INSTAGRAM_SESSION_FILE = "instagram_session"

