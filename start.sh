#!/bin/bash

# Telegram Media Downloader Bot Startup Script

echo "🤖 Starting Telegram Media Downloader Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Please copy .env.example to .env and configure your settings:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create downloads directory
mkdir -p downloads
mkdir -p logs

# Check if BOT_TOKEN is set
source .env
if [ -z "$BOT_TOKEN" ] || [ "$BOT_TOKEN" = "your_bot_token_here" ]; then
    echo "❌ BOT_TOKEN is not configured!"
    echo "📝 Please set your bot token in the .env file"
    exit 1
fi

# Start the bot
echo "🚀 Starting bot..."
python3 bot.py

