from dotenv import load_dotenv
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)

CHANNEL_ACCESS_TOKEN = "54uxdY5FzmNZZSe8uPtzyVn/o+iWpskiuGtNsrvw6gzTPCDjOmCprYpGsYT/FoVtmR/wMaclHp2T9nP/xMU4DvHpMgAjI4pH1uBGIAwGtadLjbGvuFIDySpb2Qu7uZ+28atyVb+Mnw4hnDkAZqjl5AdB04t89/1O/w1cDnyilFU="
TO_ID = "Ub79d770332dd2b228678faa227803d72"

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)


def send(message: str):
    try:
        with ApiClient(configuration) as api_client:
            line_api = MessagingApi(api_client)

            request = PushMessageRequest(to=TO_ID, messages=[TextMessage(text=message)])

            line_api.push_message(request)
            print("LINE通知送信完了 ✅")

    except Exception as e:
        print(f"LINE通知送信エラー ❌: {e}")
