import argparse
import os
from datetime import datetime

import requests

from secon_d_summary.chain import build_chain
from secon_d_summary.diary_retriever import Diary


def post_discord(webhook_url: str, summary: str, diaries: list[Diary], dt: datetime):
    mmdd = dt.strftime("🗒️ %m月%d日の出来事")
    summary_data = {"content": mmdd + "\r" + summary}
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


def args_to_dt(args: argparse.Namespace) -> datetime:
    date = args.date
    # date を YYYYMMDD 形式に変換
    if date:
        # 柔軟にdatetimeに変換する
        dt = datetime.strptime(date, "%Y%m%d")
    else:
        dt = datetime.now()
        dt = dt.replace(year=dt.year - 1)
    return dt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date in YYYYMMDD format")
    args = parser.parse_args()
    dt = args_to_dt(args)
    date_ymd = dt.strftime("%Y/%m/%d")

    url = f"https://secon.dev/entry/{date_ymd}/210000/"

    print("target_url:", url)
    chain = build_chain()
    result = chain.invoke(url)
    diaries: list[Diary] = result["diaries"]
    summary: str = result["summary"]

    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    if webhook_url:
        post_discord(webhook_url, summary, diaries, dt)
