import re
from datetime import datetime
from typing import TypedDict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class Diary(TypedDict):
    title: str
    date: datetime
    url: str
    text: str
    image: str | None
    n_diary_urls: list[str]


def _get_image(soup: BeautifulSoup) -> str | None:
    if og_image := soup.find("meta", property="og:image"):
        image: str = og_image.get("content")  # type: ignore
        image = image.replace("medium", "xsmall")
        return image
    else:
        return None


def _get_target_link(soup: BeautifulSoup) -> str | None:
    if canonical_link := soup.find("link", rel="canonical"):
        return canonical_link.get("href")  # type: ignore
    else:
        return None


def _get_title(soup: BeautifulSoup) -> str | None:
    title_h1 = soup.select_one("div.entry h1.title a")
    if title_h1:
        return title_h1.text
    else:
        return None


def _get_text(soup: BeautifulSoup) -> str | None:
    entry_content = soup.select_one("div.entry-content")
    if entry_content:
        plain_text = entry_content.get_text(strip=False)
        plain_text = re.sub(r"\n+", "\n", plain_text)
        return plain_text
    else:
        return None


def _url_to_date(url: str) -> datetime:
    return datetime.strptime(url.split("/entry/")[1][:10], "%Y/%m/%d")


def _get_n_diary_urls(soup: BeautifulSoup) -> list[str]:
    hrefs = []
    for tag in soup.select(".similar-entries .similar-thumb-entry div > a"):
        href = tag.get("href")
        if href:
            hrefs.append(href)
    # unique
    hrefs = list(sorted(set(hrefs), reverse=True))
    return hrefs


def diary_retriever(url, n_diary_top_k=10) -> Diary | None:
    base_date = _url_to_date(url)
    parsed_url = urlparse(url)
    domain_url = parsed_url.scheme + "://" + parsed_url.netloc

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    target_link = _get_target_link(soup)
    title = _get_title(soup)
    text = _get_text(soup)
    if not title or not text or not target_link:
        return None

    image = _get_image(soup)
    n_diary_urls = []
    for n_diary_url in _get_n_diary_urls(soup):
        # base_date よりも 新しい n_diary_urls は削除
        n_diary_url_date = _url_to_date(n_diary_url)
        if n_diary_url_date < base_date:
            n_diary_urls.append(domain_url + n_diary_url)

    diary = Diary(
        title=title,
        date=base_date,
        url=target_link or url,
        text=text,
        image=image,
        n_diary_urls=n_diary_urls[:n_diary_top_k],
    )
    return diary
