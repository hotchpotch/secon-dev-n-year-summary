import json
import os
from urllib.request import Request, urlopen

import requests

from secon_d_summary.chain import build_chain
from secon_d_summary.diary_retriever import Diary


def post_discord(webhook_url: str, summary: str, diaries: list[Diary]):
    summary_data = {"content": summary}
    summary_res = requests.post(webhook_url, json=summary_data)
    if summary_res.status_code == 204:
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


if __name__ == "__main__":
    url = "https://secon.dev/entry/2023/01/13/210000/"
    chain = build_chain()
    result = chain.invoke(url)
    diaries: list[Diary] = result["diaries"]
    summary: str = result["summary"]

    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    if webhook_url:
        post_discord(webhook_url, summary, diaries)
