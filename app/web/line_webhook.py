"""
LINE Webhook Handler
Receives and processes LINE webhook events
"""
from fastapi import FastAPI, Request, HTTPException
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import config
from app.pipeline.run_pipeline import VideoPipeline

app = FastAPI()

parser = WebhookParser(config.LINE_CHANNEL_SECRET)
api_client = ApiClient()
api_client.configuration.access_token = config.LINE_CHANNEL_ACCESS_TOKEN
messaging_api = MessagingApi(api_client)


@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle LINE webhook events"""
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()
    body = body.decode('utf-8')

    try:
        events = parser.parse(body, signature)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            user_id = event.source.user_id
            text = event.message.text.lower().strip()

            # Handle commands
            if text == 'run':
                # Start video generation pipeline
                await handle_run_command(user_id)
            elif text == 'status':
                # Check status (not implemented yet)
                await handle_status_command(user_id)
            else:
                # Echo back
                await reply_message(event.reply_token, f"受信: {text}\n\nコマンド: 'run' または 'status'")

    return {"status": "ok"}


async def handle_run_command(user_id: str):
    """Handle 'run' command to start pipeline"""
    try:
        pipeline = VideoPipeline(user_id=user_id)
        # Run pipeline in background (for now, run synchronously)
        result = pipeline.run()
        print(f"Pipeline completed for user {user_id}")
    except Exception as e:
        print(f"Pipeline failed for user {user_id}: {e}")


async def handle_status_command(user_id: str):
    """Handle 'status' command"""
    from linebot.v3.messaging import PushMessageRequest, TextMessage

    messaging_api.push_message(
        PushMessageRequest(
            to=user_id,
            messages=[TextMessage(text="ステータス確認機能は開発中です")]
        )
    )


async def reply_message(reply_token: str, text: str):
    """Reply to LINE message"""
    from linebot.v3.messaging import ReplyMessageRequest, TextMessage

    messaging_api.reply_message(
        ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=text)]
        )
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "YouTube Auto Generator"}
