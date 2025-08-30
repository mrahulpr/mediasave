# 🤖 Telegram Media Downloader Bot

A powerful Telegram bot for downloading media content from YouTube and Instagram with advanced features, progress tracking, and error handling.

## ✨ Features

### 🎥 YouTube Downloads
- **Multiple Formats**: Video, Audio (MP3), or File
- **Quality Selection**: Choose from available qualities (144p to 1080p, Best)
- **Progress Tracking**: Real-time download progress with ETA
- **Playlist Support**: Download entire YouTube playlists

### 📸 Instagram Downloads
- **Post Downloads**: Single posts, reels, and IGTV videos
- **Profile Downloads**: Download all posts from a profile (with confirmation)
- **Media Types**: Photos and videos
- **Batch Processing**: Efficient handling of multiple files

### 🚀 Advanced Features
- **Interactive UI**: Inline keyboards with intuitive navigation
- **Session Management**: 30-second timeout for user responses
- **Error Handling**: Automatic error reporting to support chat
- **Progress Animations**: Real-time progress updates with animations
- **File Size Limits**: Automatic handling of large files
- **Cross-Platform**: Works on all devices with Telegram

### 🛡️ Security & Reliability
- **Error Isolation**: All errors sent to support chat, users see friendly messages
- **Session Timeout**: Automatic cleanup of inactive sessions
- **File Cleanup**: Temporary files automatically removed after upload
- **Uptime Tracking**: Built-in system monitoring

## 📋 Requirements

- Python 3.11+
- FFmpeg (for audio conversion)
- Telegram Bot Token
- Support Chat ID (for error reporting)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd telegram-media-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
nano .env
```

Set the following variables in `.env`:
```env
BOT_TOKEN=your_bot_token_here
SUPPORT_CHAT=your_support_chat_id_here
BOT_NAME=Media Downloader Bot
BOT_OWNER=Your Name
HOSTED_AT=Sevalla Platform
```

### 4. Run the Bot
```bash
./start.sh
```

Or manually:
```bash
python bot.py
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
# Configure environment
cp .env.example .env
nano .env

# Start the bot
docker-compose up -d

# View logs
docker-compose logs -f
```

### Using Docker
```bash
# Build image
docker build -t telegram-media-bot .

# Run container
docker run -d --name media-bot --env-file .env telegram-media-bot
```

## ☁️ Sevalla Platform Deployment

### Method 1: Direct Deployment
1. Upload the project files to your Sevalla instance
2. Configure environment variables in Sevalla dashboard
3. Install dependencies: `pip install -r requirements.txt`
4. Start the bot: `python bot.py`

### Method 2: Docker Deployment
1. Upload project with Dockerfile
2. Configure environment variables
3. Deploy using Sevalla's Docker support

### Environment Variables for Sevalla
Set these in your Sevalla environment:
- `BOT_TOKEN`: Your Telegram bot token
- `SUPPORT_CHAT`: Chat ID for error reporting
- `BOT_NAME`: Name of your bot
- `BOT_OWNER`: Your name
- `HOSTED_AT`: "Sevalla Platform"

## 🎯 Bot Commands

### User Commands
- `/start` - Start the bot and show main menu
- `/download` - Begin media download process

### Menu Options
- **About** - Bot information, owner, uptime
- **Help** - Feature descriptions and commands
- **YouTube** - Download YouTube videos/audio
- **Instagram** - Download Instagram posts/profiles

## 📱 Usage Flow

### YouTube Download
1. Send `/download` command
2. Click "🎥 YouTube" button
3. Send YouTube URL within 30 seconds
4. Choose format: Video, Audio, or File
5. Select quality from available options
6. Wait for download and upload completion

### Instagram Download
1. Send `/download` command
2. Click "📸 Instagram" button
3. Send Instagram URL within 30 seconds
4. For profiles: Confirm bulk download
5. For posts: Automatic processing
6. Receive downloaded media files

## ⚙️ Configuration

### Bot Settings (`config.py`)
```python
# Timeout for user responses
DOWNLOAD_TIMEOUT = 30  # seconds

# Maximum file size for uploads
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Temporary download directory
TEMP_DIR = "downloads"
```

### YouTube Quality Options
- 144p, 240p, 360p, 480p, 720p, 1080p, Best
- Automatic format selection based on availability

### Instagram Settings
- Supports posts, reels, IGTV, and profiles
- Automatic media type detection
- Batch download with progress tracking

## 🔧 Troubleshooting

### Common Issues

**Bot not responding:**
- Check BOT_TOKEN in .env file
- Verify bot is running: `ps aux | grep python`
- Check logs for errors

**Download failures:**
- Ensure FFmpeg is installed
- Check internet connectivity
- Verify URL format is correct

**File upload errors:**
- Check file size (max 50MB)
- Verify Telegram API limits
- Check disk space

### Error Reporting
All errors are automatically sent to the configured support chat with:
- Error context and details
- User chat ID
- Timestamp
- Stack trace (for debugging)

## 📊 Monitoring

### Built-in Monitoring
- System uptime tracking
- Memory usage monitoring
- Download progress tracking
- Error rate monitoring

### Health Checks
Docker health check included:
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import requests; requests.get('https://api.telegram.org/bot${BOT_TOKEN}/getMe')"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🔒 Security Considerations

### Environment Variables
- Never commit `.env` file to version control
- Use strong, unique bot tokens
- Restrict support chat access

### File Handling
- Temporary files automatically cleaned up
- File size limits enforced
- Safe file type validation

### User Sessions
- 30-second timeout for security
- Session data automatically cleaned
- No persistent user data storage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and support:
1. Check the troubleshooting section
2. Review error messages in support chat
3. Create an issue on GitHub
4. Contact the bot owner

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [instaloader](https://github.com/instaloader/instaloader) - Instagram downloader
- [FFmpeg](https://ffmpeg.org/) - Media processing

---

**Made with ❤️ for the Telegram community**

