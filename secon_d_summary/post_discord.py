from datetime import datetime

import requests

from .diary_retriever import Diary


def post_discord(
    webhook_url: str, summary: str, diaries: list[Diary], dt: datetime
) -> bool:
    mmdd = dt.strftime("🗒️ %m月%d日の出来事")
    summary_data = {"content": mmdd + "\r" + summary}
    res = requests.post(webhook_url, json=summary_data)
    if res.status_code == 204:
        fields = []
        for diary in diaries:
            fields.append(
                {
                    "name": "",
                    "value": f"[{diary['title']}]({diary['url']})",
                    "inline": True,
                }
            )
        data = {"embeds": [{"fields": fields}]}
        res = requests.post(webhook_url, json=data)
        if res.status_code == 204:
            print("successfully posted summary")
            return True
    print("failed to post summary")
    print(res.status_code)
    print(res.text)
    return False
