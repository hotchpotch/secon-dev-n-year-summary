import argparse
import os
from datetime import datetime

from secon_d_summary.chain import build_chain
from secon_d_summary.diary_retriever import Diary
from secon_d_summary.post_discord import post_discord


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
    print("summary:", summary)
    print("diaries:", [diary["url"] for diary in diaries])

    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    if webhook_url:
        post_discord(webhook_url, summary, diaries, dt)
