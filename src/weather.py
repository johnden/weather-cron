import requests
import os

def get_weather(city: str = "Guangzhou") -> str:
 url = f"https://wttr.in/{city}?format=j1"
 resp = requests.get(url, timeout=10)
 data = resp.json()
 c = data["current_condition"][0]
 return (
 f"📍 {city}\n"
 f"🌤 天气：{c['weatherDesc'][0]['value']}\n"
 f"🌡 气温：{c['temp_C']}°C\n"
 f"💧 湿度：{c['humidity']}%\n"
 f"🌬 风速：{c['windspeedKmph']} km/h"
 )

def send_feishu(message: str):
 webhook = os.environ.get("FEISHU_WEBHOOK_URL")
 if not webhook:
 print("⚠️ 未配置飞书 Webhook，仅打印结果：")
 print(message)
 return

 payload = {
 "msg_type": "text",
 "content": {"text": f"🌤️ 天气播报\n\n{message}"}
 }
 resp = requests.post(webhook, json=payload, timeout=10)
 if resp.status_code != 200:
 print(f"❌ 飞书推送失败：{resp.text}")

if __name__ == "__main__":
 city = os.environ.get("CITY", "Beijing")
 result = get_weather(city)
 print(result)
 send_feishu(result)

 # 输出供 GitHub Actions 捕获
 with open(os.environ["GITHUB_OUTPUT"], "a") as f:
 f.write(f"weather_result={result}")
