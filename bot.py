import os
import asyncio
import logging
import time
import re
from datetime import datetime, timedelta
from typing import Dict, Any
import psutil

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

import yt_dlp
import instaloader
from config import *

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variables to track user sessions
user_sessions: Dict[int, Dict[str, Any]] = {}

class MediaDownloaderBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
        
        # Create downloads directory
        os.makedirs(TEMP_DIR, exist_ok=True)
    
    def setup_handlers(self):
        """Setup all command and callback handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("download", self.download_command))
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        keyboard = [
            [InlineKeyboardButton("📋 About", callback_data="about")],
            [InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_message = f"""
🎉 *Welcome to {BOT_NAME}!*

Your ultimate media downloader bot for YouTube and Instagram content.

Choose an option below to get started:
        """
        
        await update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def download_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /download command"""
        keyboard = [
            [InlineKeyboardButton("🎥 YouTube", callback_data="download_youtube")],
            [InlineKeyboardButton("📸 Instagram", callback_data="download_instagram")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🔽 *Choose Platform to Download:*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        if data == "about":
            await self.show_about(query)
        elif data == "help":
            await self.show_help(query)
        elif data == "back_to_start":
            await self.back_to_start(query)
        elif data == "download_youtube":
            await self.start_youtube_download(query, user_id)
        elif data == "download_instagram":
            await self.start_instagram_download(query, user_id)
        elif data.startswith("yt_format_"):
            await self.handle_youtube_format_selection(query, user_id, data)
        elif data.startswith("yt_quality_"):
            await self.handle_youtube_quality_selection(query, user_id, data)
        elif data == "ig_confirm_profile":
            await self.handle_instagram_profile_confirm(query, user_id)
        elif data == "ig_cancel_profile":
            await self.cancel_instagram_profile(query, user_id)
    
    async def show_about(self, query):
        """Show about information"""
        uptime = self.get_uptime()
        about_text = f"""
ℹ️ *About {BOT_NAME}*

🤖 **Bot Name:** {BOT_NAME}
👨‍💻 **Owner:** {BOT_OWNER}
🏠 **Hosted at:** {HOSTED_AT}
📊 **Version:** {BOT_VERSION}
⏰ **Uptime:** {uptime}
🕐 **Started:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This bot helps you download media content from various social media platforms with ease and high quality.
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_help(self, query):
        """Show help information"""
        help_text = f"""
❓ *Help - {BOT_NAME}*

**🎯 Available Commands:**
• `/start` - Start the bot and show main menu
• `/download` - Start downloading media

**🎥 YouTube Downloads:**
• Send YouTube video/playlist URL
• Choose format: Video, Audio, or File
• Select quality from available options
• Download starts automatically

**📸 Instagram Downloads:**
• Send Instagram post or profile URL
• For profiles: Confirm to download all posts
• For posts: Direct download
• Supports photos and videos

**⚡ Features:**
• High-quality downloads
• Progress tracking with animations
• Multiple format options
• Batch downloads for profiles
• Error handling with support notifications

**⏱️ Session Timeout:**
• 30 seconds to send links after selection
• Sessions auto-expire for security

**🆘 Support:**
If you encounter any issues, they are automatically reported to our support team.
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def back_to_start(self, query):
        """Return to start menu"""
        keyboard = [
            [InlineKeyboardButton("📋 About", callback_data="about")],
            [InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_message = f"""
🎉 *Welcome to {BOT_NAME}!*

Your ultimate media downloader bot for YouTube and Instagram content.

Choose an option below to get started:
        """
        
        await query.edit_message_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def start_youtube_download(self, query, user_id):
        """Start YouTube download process"""
        user_sessions[user_id] = {
            'platform': 'youtube',
            'step': 'waiting_link',
            'timestamp': time.time(),
            'chat_id': query.message.chat_id,
            'message_id': query.message.message_id
        }
        
        await query.edit_message_text(
            "🎥 *YouTube Download*\n\n"
            "📎 Please send me a YouTube video URL\n"
            "⏰ You have 30 seconds to send the link...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Set timeout
        asyncio.create_task(self.session_timeout(user_id, 30))
    
    async def start_instagram_download(self, query, user_id):
        """Start Instagram download process"""
        user_sessions[user_id] = {
            'platform': 'instagram',
            'step': 'waiting_link',
            'timestamp': time.time(),
            'chat_id': query.message.chat_id,
            'message_id': query.message.message_id
        }
        
        await query.edit_message_text(
            "📸 *Instagram Download*\n\n"
            "📎 Please send me an Instagram post or profile URL\n"
            "⏰ You have 30 seconds to send the link...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Set timeout
        asyncio.create_task(self.session_timeout(user_id, 30))
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = update.message.from_user.id
        text = update.message.text
        
        if user_id not in user_sessions:
            await update.message.reply_text(
                "❌ No active session. Use /download to start downloading."
            )
            return
        
        session = user_sessions[user_id]
        
        # Check if session is expired
        if time.time() - session['timestamp'] > DOWNLOAD_TIMEOUT:
            del user_sessions[user_id]
            await update.message.reply_text(
                "⏰ Session expired. Please try again with /download"
            )
            return
        
        if session['platform'] == 'youtube' and session['step'] == 'waiting_link':
            await self.handle_youtube_link(update, user_id, text)
        elif session['platform'] == 'instagram' and session['step'] == 'waiting_link':
            await self.handle_instagram_link(update, user_id, text)
    
    async def handle_youtube_link(self, update: Update, user_id: int, url: str):
        """Handle YouTube URL"""
        if not self.is_youtube_url(url):
            await update.message.reply_text(
                "❌ Invalid YouTube URL. Please send a valid YouTube link."
            )
            return
        
        user_sessions[user_id]['url'] = url
        user_sessions[user_id]['step'] = 'choosing_format'
        
        keyboard = [
            [InlineKeyboardButton("🎥 Video", callback_data="yt_format_video")],
            [InlineKeyboardButton("🎵 Audio", callback_data="yt_format_audio")],
            [InlineKeyboardButton("📁 File", callback_data="yt_format_file")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "✅ *YouTube URL Received!*\n\n"
            "🎯 Choose download format:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def handle_instagram_link(self, update: Update, user_id: int, url: str):
        """Handle Instagram URL"""
        if not self.is_instagram_url(url):
            await update.message.reply_text(
                "❌ Invalid Instagram URL. Please send a valid Instagram link."
            )
            return
        
        user_sessions[user_id]['url'] = url
        
        # Check if it's a profile or post
        if '/p/' in url or '/reel/' in url or '/tv/' in url:
            # It's a post
            await self.start_instagram_post_download(update, user_id, url)
        else:
            # It's likely a profile
            await self.confirm_instagram_profile_download(update, user_id, url)
    
    async def confirm_instagram_profile_download(self, update: Update, user_id: int, url: str):
        """Confirm Instagram profile download"""
        keyboard = [
            [InlineKeyboardButton("✅ Yes, Download All", callback_data="ig_confirm_profile")],
            [InlineKeyboardButton("❌ Cancel", callback_data="ig_cancel_profile")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚠️ *Profile Link Detected*\n\n"
            "This appears to be an Instagram profile link.\n"
            "Do you want to download ALL posts from this account?\n\n"
            "⚡ This may take a while depending on the number of posts.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def handle_youtube_format_selection(self, query, user_id: int, data: str):
        """Handle YouTube format selection"""
        format_type = data.split('_')[-1]  # video, audio, or file
        user_sessions[user_id]['format'] = format_type
        user_sessions[user_id]['step'] = 'choosing_quality'
        
        # Get available qualities
        try:
            qualities = await self.get_youtube_qualities(user_sessions[user_id]['url'])
            keyboard = []
            
            for quality, ydl_format in qualities.items():
                keyboard.append([InlineKeyboardButton(
                    f"📺 {quality}", 
                    callback_data=f"yt_quality_{quality}"
                )])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"🎯 *Format: {format_type.title()}*\n\n"
                "📊 Choose quality:",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        except Exception as e:
            await self.handle_error(e, query.message.chat_id, "Failed to get YouTube qualities")
            del user_sessions[user_id]
    
    async def handle_youtube_quality_selection(self, query, user_id: int, data: str):
        """Handle YouTube quality selection"""
        quality = data.split('_')[-1]
        user_sessions[user_id]['quality'] = quality
        
        await query.edit_message_text(
            "🚀 *Starting Download...*\n\n"
            "⏳ Please wait while we process your request...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Start download
        asyncio.create_task(self.download_youtube_video(user_id, query.message.chat_id))
    
    async def download_youtube_video(self, user_id: int, chat_id: int):
        """Download YouTube video"""
        try:
            session = user_sessions[user_id]
            url = session['url']
            format_type = session['format']
            quality = session['quality']
            
            # Setup progress tracking
            progress_msg = await self.app.bot.send_message(
                chat_id,
                "📥 *Downloading...*\n\n"
                "🔄 Initializing download...\n"
                "📊 Progress: 0%",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Configure yt-dlp options
            ydl_opts = {
                'outtmpl': f'{TEMP_DIR}/%(title)s.%(ext)s',
                'progress_hooks': [lambda d: asyncio.create_task(
                    self.youtube_progress_hook(d, progress_msg, chat_id)
                )],
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/117.0 Safari/537.36'
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/117.0 Safari/537.36'
                },
                'nocheckcertificate': True,
                'ignoreerrors': True,
            }
            
            if format_type == 'audio':
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            elif format_type == 'video':
                ydl_opts['format'] = YOUTUBE_QUALITIES.get(quality, 'best')
            else:  # file
                ydl_opts['format'] = 'best'
            
            # Download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
                
                await self.app.bot.edit_message_text(
                    "📥 *Downloading...*\n\n"
                    f"🎬 Title: {info.get('title', 'Unknown')}\n"
                    f"⏱️ Duration: {self.format_duration(info.get('duration', 0))}\n"
                    "🔄 Starting download...",
                    chat_id,
                    progress_msg.message_id,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                ydl.download([url])
            
            # Upload file
            await self.upload_file_to_telegram(filename, chat_id, progress_msg)
            
            # Cleanup
            if os.path.exists(filename):
                os.remove(filename)
            
            del user_sessions[user_id]
            
        except Exception as e:
            await self.handle_error(e, chat_id, "YouTube download failed")
            if user_id in user_sessions:
                del user_sessions[user_id]
    
    async def start_instagram_post_download(self, update: Update, user_id: int, url: str):
        """Start Instagram post download"""
        try:
            progress_msg = await update.message.reply_text(
                "📥 *Instagram Download*\n\n"
                "🔄 Initializing download...\n"
                "📊 Progress: 0%",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Download Instagram post
            await self.download_instagram_content(url, update.message.chat_id, progress_msg, False)
            
            del user_sessions[user_id]
            
        except Exception as e:
            await self.handle_error(e, update.message.chat_id, "Instagram download failed")
            if user_id in user_sessions:
                del user_sessions[user_id]
    
    async def handle_instagram_profile_confirm(self, query, user_id: int):
        """Handle Instagram profile download confirmation"""
        url = user_sessions[user_id]['url']
        
        await query.edit_message_text(
            "📥 *Instagram Profile Download*\n\n"
            "🔄 Starting profile download...\n"
            "⚠️ This may take several minutes...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            await self.download_instagram_content(url, query.message.chat_id, query.message, True)
            del user_sessions[user_id]
        except Exception as e:
            await self.handle_error(e, query.message.chat_id, "Instagram profile download failed")
            if user_id in user_sessions:
                del user_sessions[user_id]
    
    async def cancel_instagram_profile(self, query, user_id: int):
        """Cancel Instagram profile download"""
        del user_sessions[user_id]
        await query.edit_message_text(
            "❌ *Download Cancelled*\n\n"
            "Use /download to start a new download.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def download_instagram_content(self, url: str, chat_id: int, progress_msg, is_profile: bool):
        """Download Instagram content"""
        L = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            dirname_pattern=TEMP_DIR
        )
        
        if is_profile:
            # Profile download
            profile_name = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
            profile = instaloader.Profile.from_username(L.context, profile_name)
            
            post_count = 0
            for post in profile.get_posts():
                post_count += 1
                await self.app.bot.edit_message_text(
                    f"📥 *Instagram Profile Download*\n\n"
                    f"👤 Profile: {profile.username}\n"
                    f"📊 Downloaded: {post_count} posts\n"
                    f"🔄 Downloading post {post_count}...",
                    chat_id,
                    progress_msg.message_id,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                L.download_post(post, target=profile.username)
                
                if post_count >= 50:  # Limit to prevent spam
                    break
        else:
            # Single post download
            shortcode = self.extract_instagram_shortcode(url)
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target="single_post")
        
        # Find and upload downloaded files
        await self.upload_instagram_files(chat_id, progress_msg)
    
    async def upload_instagram_files(self, chat_id: int, progress_msg):
        """Upload Instagram files to Telegram"""
        files_uploaded = 0
        
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.mp4')):
                    file_path = os.path.join(root, file)
                    files_uploaded += 1
                    
                    await self.app.bot.edit_message_text(
                        f"📤 *Uploading Files...*\n\n"
                        f"📊 Uploaded: {files_uploaded} files\n"
                        f"🔄 Uploading: {file}",
                        chat_id,
                        progress_msg.message_id,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    
                    await self.upload_file_to_telegram(file_path, chat_id, None)
                    os.remove(file_path)
        
        await self.app.bot.edit_message_text(
            f"✅ *Download Complete!*\n\n"
            f"📊 Total files uploaded: {files_uploaded}\n"
            f"🎉 All files have been sent successfully!",
            chat_id,
            progress_msg.message_id,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def upload_file_to_telegram(self, file_path: str, chat_id: int, progress_msg):
        """Upload file to Telegram"""
        try:
            file_size = os.path.getsize(file_path)
            
            if file_size > MAX_FILE_SIZE:
                await self.app.bot.send_message(
                    chat_id,
                    f"❌ File too large: {os.path.basename(file_path)}\n"
                    f"Size: {file_size / (1024*1024):.1f}MB (Max: {MAX_FILE_SIZE / (1024*1024):.0f}MB)"
                )
                return
            
            if progress_msg:
                await self.app.bot.edit_message_text(
                    "📤 *Uploading to Telegram...*\n\n"
                    f"📁 File: {os.path.basename(file_path)}\n"
                    f"📊 Size: {file_size / (1024*1024):.1f}MB\n"
                    "🔄 Uploading...",
                    chat_id,
                    progress_msg.message_id,
                    parse_mode=ParseMode.MARKDOWN
                )
            
            with open(file_path, 'rb') as file:
                if file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                    await self.app.bot.send_video(chat_id, file)
                elif file_path.lower().endswith(('.mp3', '.wav', '.m4a')):
                    await self.app.bot.send_audio(chat_id, file)
                else:
                    await self.app.bot.send_document(chat_id, file)
            
            if progress_msg:
                await self.app.bot.edit_message_text(
                    "✅ *Upload Complete!*\n\n"
                    f"📁 File: {os.path.basename(file_path)}\n"
                    "🎉 Successfully uploaded to Telegram!",
                    chat_id,
                    progress_msg.message_id,
                    parse_mode=ParseMode.MARKDOWN
                )
                
        except Exception as e:
            await self.handle_error(e, chat_id, f"Failed to upload {os.path.basename(file_path)}")
    
    async def youtube_progress_hook(self, d, progress_msg, chat_id):
        """YouTube download progress hook"""
        try:
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '0%')
                speed = d.get('_speed_str', 'Unknown')
                eta = d.get('_eta_str', 'Unknown')
                
                await self.app.bot.edit_message_text(
                    f"📥 *Downloading...*\n\n"
                    f"📊 Progress: {percent}\n"
                    f"🚀 Speed: {speed}\n"
                    f"⏱️ ETA: {eta}",
                    chat_id,
                    progress_msg.message_id,
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception:
            pass  # Ignore progress update errors
    
    async def get_youtube_qualities(self, url: str) -> dict:
        """Get available YouTube qualities"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                available_qualities = {}
                for quality, format_selector in YOUTUBE_QUALITIES.items():
                    available_qualities[quality] = format_selector
                
                return available_qualities
        except Exception:
            return {"Best": "best", "720p": "best[height<=720]", "480p": "best[height<=480]"}
    
    async def session_timeout(self, user_id: int, timeout: int):
        """Handle session timeout"""
        await asyncio.sleep(timeout)
        
        if user_id in user_sessions:
            session = user_sessions[user_id]
            if time.time() - session['timestamp'] >= timeout:
                del user_sessions[user_id]
                
                try:
                    await self.app.bot.send_message(
                        session['chat_id'],
                        "⏰ *Session Expired*\n\n"
                        "You took too long to respond. Please try again with /download",
                        parse_mode=ParseMode.MARKDOWN
                    )
                except Exception:
                    pass
    
    async def handle_error(self, error: Exception, chat_id: int, context: str):
        """Handle errors and send to support chat"""
        error_msg = f"❌ An error occurred. Our support team has been notified."
        
        try:
            await self.app.bot.send_message(chat_id, error_msg)
        except Exception:
            pass
        
        # Send error to support chat
        try:
            support_msg = (
                f"🚨 *Error Report*\n\n"
                f"**Context:** {context}\n"
                f"**Chat ID:** {chat_id}\n"
                f"**Error:** {str(error)}\n"
                f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            await self.app.bot.send_message(SUPPORT_CHAT, support_msg, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            logger.error(f"Failed to send error to support chat: {error}")
    
    def is_youtube_url(self, url: str) -> bool:
        """Check if URL is a valid YouTube URL"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
        ]
        return any(re.match(pattern, url) for pattern in youtube_patterns)
    
    def is_instagram_url(self, url: str) -> bool:
        """Check if URL is a valid Instagram URL"""
        instagram_patterns = [
            r'(?:https?://)?(?:www\.)?instagram\.com/p/[\w-]+',
            r'(?:https?://)?(?:www\.)?instagram\.com/reel/[\w-]+',
            r'(?:https?://)?(?:www\.)?instagram\.com/tv/[\w-]+',
            r'(?:https?://)?(?:www\.)?instagram\.com/[\w.-]+/?$',
        ]
        return any(re.match(pattern, url) for pattern in instagram_patterns)
    
    def extract_instagram_shortcode(self, url: str) -> str:
        """Extract Instagram shortcode from URL"""
        patterns = [
            r'/p/([^/?]+)',
            r'/reel/([^/?]+)',
            r'/tv/([^/?]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ""
    
    def format_duration(self, seconds: int) -> str:
        """Format duration in seconds to readable format"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m {seconds % 60}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def get_uptime(self) -> str:
        """Get system uptime"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_delta = timedelta(seconds=uptime_seconds)
            return str(uptime_delta).split('.')[0]  # Remove microseconds
        except Exception:
            return "Unknown"
    
    def run(self):
        """Run the bot"""
        logger.info(f"Starting {BOT_NAME}...")
        self.app.run_polling()

if __name__ == "__main__":
    bot = MediaDownloaderBot()
    bot.run()

