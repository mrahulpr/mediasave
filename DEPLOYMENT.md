# 🚀 Sevalla Platform Deployment Guide

This guide provides step-by-step instructions for deploying the Telegram Media Downloader Bot on Sevalla Platform.

## 📋 Prerequisites

Before deploying, ensure you have:
- Sevalla Platform account
- Telegram Bot Token (from @BotFather)
- Support Chat ID (for error reporting)
- Basic knowledge of environment variables

## 🎯 Deployment Methods

### Method 1: Direct Python Deployment (Recommended)

#### Step 1: Prepare Your Sevalla Instance
1. Log into your Sevalla dashboard
2. Create a new Python application
3. Choose Python 3.11+ runtime
4. Set up your domain/subdomain

#### Step 2: Upload Project Files
```bash
# Clone or download the project
git clone <your-repository-url>
cd telegram-media-bot

# Upload files to Sevalla (via FTP, Git, or dashboard)
# Ensure all files are in the root directory of your app
```

#### Step 3: Configure Environment Variables
In Sevalla dashboard, set these environment variables:
```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
SUPPORT_CHAT=-1001234567890
BOT_NAME=Media Downloader Bot
BOT_OWNER=Your Name
HOSTED_AT=Sevalla Platform
```

#### Step 4: Install Dependencies
In Sevalla terminal or via SSH:
```bash
pip install -r requirements.txt
```

#### Step 5: Start the Bot
```bash
python bot.py
```

### Method 2: Docker Deployment

#### Step 1: Prepare Docker Environment
1. Enable Docker support in Sevalla
2. Upload project files including Dockerfile
3. Configure environment variables

#### Step 2: Build and Deploy
```bash
# Build the Docker image
docker build -t telegram-media-bot .

# Run the container
docker run -d --name media-bot \
  -e BOT_TOKEN="your_token_here" \
  -e SUPPORT_CHAT="your_chat_id" \
  telegram-media-bot
```

#### Step 3: Using Docker Compose
```bash
# Configure .env file
cp .env.example .env
nano .env

# Deploy with docker-compose
docker-compose up -d
```

## ⚙️ Sevalla-Specific Configuration

### Environment Variables Setup
1. Go to Sevalla Dashboard → Your App → Environment
2. Add the following variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | `1234567890:ABC...` |
| `SUPPORT_CHAT` | Chat ID for error reporting | `-1001234567890` |
| `BOT_NAME` | Display name for your bot | `Media Downloader Bot` |
| `BOT_OWNER` | Your name or organization | `Your Name` |
| `HOSTED_AT` | Platform identifier | `Sevalla Platform` |

### Resource Requirements
- **RAM**: Minimum 512MB, Recommended 1GB+
- **Storage**: 2GB+ (for temporary downloads)
- **CPU**: 1 vCPU minimum
- **Network**: Unlimited bandwidth recommended

### File Permissions
Ensure the following directories are writable:
```bash
chmod 755 downloads/
chmod 755 logs/
chmod +x start.sh
```

## 🔧 Sevalla-Specific Features

### Auto-Restart Configuration
Add to your Sevalla app configuration:
```json
{
  "restart_policy": "always",
  "health_check": {
    "enabled": true,
    "interval": 30,
    "timeout": 10,
    "retries": 3
  }
}
```

### Log Management
Configure log rotation in Sevalla:
```bash
# Create logs directory
mkdir -p logs

# Set up log rotation (if supported)
logrotate -f /etc/logrotate.conf
```

### Monitoring Setup
Enable Sevalla monitoring for:
- CPU usage
- Memory consumption
- Network traffic
- Application uptime

## 🚨 Troubleshooting

### Common Sevalla Issues

#### Bot Not Starting
```bash
# Check Python version
python --version

# Verify dependencies
pip list | grep telegram

# Check environment variables
env | grep BOT_
```

#### Permission Errors
```bash
# Fix file permissions
chmod -R 755 /path/to/your/app
chmod +x start.sh

# Check directory ownership
ls -la
```

#### Memory Issues
```bash
# Monitor memory usage
free -h

# Check process memory
ps aux | grep python
```

#### Network Connectivity
```bash
# Test Telegram API
curl -X GET "https://api.telegram.org/bot${BOT_TOKEN}/getMe"

# Test external connectivity
ping google.com
```

### Log Analysis
Check application logs in Sevalla dashboard:
```bash
# View recent logs
tail -f logs/bot.log

# Search for errors
grep -i error logs/bot.log

# Monitor in real-time
journalctl -f -u your-app-name
```

## 📊 Performance Optimization

### Sevalla Optimization Tips

#### 1. Resource Allocation
- Monitor CPU and RAM usage
- Scale resources based on usage patterns
- Use Sevalla's auto-scaling features

#### 2. Caching Strategy
```python
# Add to config.py
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour
```

#### 3. Database Optimization
If using database:
- Use connection pooling
- Implement query optimization
- Regular maintenance tasks

#### 4. File Management
```bash
# Clean up old downloads
find downloads/ -type f -mtime +1 -delete

# Monitor disk usage
df -h
```

## 🔒 Security Best Practices

### Environment Security
1. **Never expose sensitive data**:
   - Keep `.env` file secure
   - Use Sevalla's environment variable system
   - Rotate tokens regularly

2. **Network Security**:
   - Use HTTPS for all communications
   - Implement rate limiting
   - Monitor for suspicious activity

3. **File Security**:
   - Validate all uploaded content
   - Implement file size limits
   - Clean temporary files regularly

### Access Control
```bash
# Restrict file access
chmod 600 .env
chmod 700 downloads/

# Set up proper user permissions
chown -R app:app /path/to/app
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use Sevalla's load balancing
- Implement session sharing
- Database clustering if needed

### Vertical Scaling
- Monitor resource usage
- Upgrade instance size as needed
- Optimize memory usage

### Performance Monitoring
Set up alerts for:
- High CPU usage (>80%)
- Memory usage (>90%)
- Disk space (>85%)
- Error rates (>5%)

## 🆘 Support and Maintenance

### Regular Maintenance Tasks
1. **Weekly**:
   - Check error logs
   - Monitor resource usage
   - Update dependencies

2. **Monthly**:
   - Review performance metrics
   - Update bot features
   - Security audit

3. **Quarterly**:
   - Full system backup
   - Disaster recovery test
   - Performance optimization

### Getting Help
1. **Sevalla Support**: Use platform support channels
2. **Bot Issues**: Check error logs and support chat
3. **Community**: GitHub issues and discussions

---

**🎉 Your Telegram Media Downloader Bot is now ready for production on Sevalla Platform!**

For additional support, refer to the main README.md or contact the development team.

