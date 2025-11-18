# Deployment Guide - YouTube Auto Generator

## Render Deployment

### Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **API Keys**: Obtain all required API keys
3. **GitHub Repository**: Connected to Render

### Step 1: Create Web Service

1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `youtube-auto-generator`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free (or paid for production)

### Step 2: Environment Variables

Add these environment variables in Render Dashboard:

#### Required API Keys

```bash
# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Google Gemini (for TTS)
GEMINI_API_KEY=xxxxx

# ElevenLabs (alternative TTS)
ELEVENLABS_API_KEY=xxxxx

# LINE Bot
LINE_CHANNEL_SECRET=xxxxx
LINE_CHANNEL_ACCESS_TOKEN=xxxxx

# YouTube API
YOUTUBE_CLIENT_ID=xxxxx.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=xxxxx
YOUTUBE_REFRESH_TOKEN=xxxxx

# Google Drive (optional)
GOOGLE_DRIVE_FOLDER_ID=xxxxx
```

#### Server Configuration

```bash
PORT=8000
HOST=0.0.0.0
```

### Step 3: Get API Keys

#### 1. Anthropic Claude API
1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Create API key
3. Copy to `ANTHROPIC_API_KEY`

#### 2. Google Gemini API
1. Go to [ai.google.dev](https://ai.google.dev/)
2. Get API key
3. Copy to `GEMINI_API_KEY`

#### 3. LINE Messaging API
1. Go to [LINE Developers Console](https://developers.line.biz/)
2. Create a Messaging API channel
3. Get Channel Secret → `LINE_CHANNEL_SECRET`
4. Issue Channel Access Token → `LINE_CHANNEL_ACCESS_TOKEN`

#### 4. YouTube Data API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Get refresh token (see below)

##### Getting YouTube Refresh Token

```bash
# Use OAuth Playground
# 1. Go to https://developers.google.com/oauthplayground/
# 2. Select YouTube Data API v3
# 3. Authorize and get refresh token
```

### Step 4: LINE Webhook Setup

1. Get your Render URL: `https://youtube-auto-generator.onrender.com`
2. Go to LINE Developers Console
3. Set Webhook URL: `https://youtube-auto-generator.onrender.com/webhook`
4. Enable "Use webhook"
5. Enable "Allow bot to join group chats" (optional)

### Step 5: Deploy

1. Click "Manual Deploy" → "Deploy latest commit"
2. Wait for deployment to complete
3. Check logs for errors
4. Visit `/health` endpoint to verify

### Step 6: Test

Send a message to your LINE Bot:

```
run
```

You should receive:
- Start notification
- Processing updates (if configured)
- Completion notification with YouTube URL

## Health Check

```bash
curl https://youtube-auto-generator.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "YouTube Auto Generator"
}
```

## Monitoring

### Logs

View logs in Render Dashboard or via CLI:

```bash
render logs -s youtube-auto-generator
```

### Common Issues

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **API Key Issues**: Double-check all environment variables
3. **LINE Webhook Fails**: Verify webhook URL and signature verification
4. **Memory Issues**: Upgrade to paid plan if needed

## Scaling

For production use:

- **Upgrade Plan**: Use Starter or higher for better performance
- **Background Workers**: Consider using Celery + Redis for async tasks
- **Database**: Add PostgreSQL for job queue and history
- **CDN**: Use CloudFlare for static assets

## Security

- ✅ Environment variables stored securely in Render
- ✅ LINE webhook signature verification
- ✅ HTTPS by default
- ⚠️ Add rate limiting for production
- ⚠️ Add authentication for admin endpoints

## Cost Estimate

**Free Tier**:
- Render: Free (with limitations)
- Anthropic Claude: Pay-as-you-go (~$0.01/video)
- Gemini API: Free tier available
- LINE Messaging: Free
- YouTube API: Free (10,000 quota/day)

**Total**: ~$0.01-0.05 per video generated

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
