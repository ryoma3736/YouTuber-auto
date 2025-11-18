"""
LINE Notification Module
Sends messages to LINE users
"""
from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)
from config import config

class LineNotifier:
    """LINE notification sender"""

    def __init__(self):
        self.api_client = ApiClient()
        self.api_client.configuration.access_token = config.LINE_CHANNEL_ACCESS_TOKEN
        self.messaging_api = MessagingApi(self.api_client)

    def send_message(self, user_id: str, message: str):
        """
        Send text message to LINE user
        Args:
            user_id: LINE user ID
            message: Text message to send
        """
        try:
            self.messaging_api.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=[TextMessage(text=message)]
                )
            )
            return True
        except Exception as e:
            print(f"Failed to send LINE message: {e}")
            return False

    def notify_start(self, user_id: str):
        """Notify pipeline start"""
        message = "🚀 動画生成を開始しました"
        return self.send_message(user_id, message)

    def notify_success(self, user_id: str, title: str, url: str):
        """Notify successful video generation"""
        message = f"✅ 動画生成が完了しました！\n\n📹 {title}\n🔗 {url}"
        return self.send_message(user_id, message)

    def notify_error(self, user_id: str, step: str, error: str):
        """Notify error during pipeline"""
        message = f"❌ エラーが発生しました\n\nステップ: {step}\nエラー: {error}"
        return self.send_message(user_id, message)
