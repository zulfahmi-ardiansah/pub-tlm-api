import requests

from bs4 import BeautifulSoup
from util_config import scrap_config


def get_article(link):
    html = requests.get(link).content
    html = BeautifulSoup(html, "html.parser")
    art_title = html.select_one("header.td-post-title h1.entry-title").text
    art_author = html.select_one("header.td-post-title .td-module-meta-info .td-post-author-name a").text
    art_date = html.select_one("header.td-post-title .td-module-meta-info time.entry-date")["datetime"]
    art_category = []
    art_content = []
    for category in html.select(".td-post-header .td-category li a"):
        art_category.append(category.text)
    for element in html.select_one(".td-post-content").select("h1, h1, h2, h3, h4, h5, h6, p, img, ul, ol"):
        content = {
            "type": element.name
        }
        if content["type"] == "ol" or content["type"] == "ul":
            content["value"] = []
            for sub_element in element.select("li"):
                text = sub_element.text.strip()
                if len(text) > 0:
                    content["value"].append(text)
        else:
            content["value"] = element["src"] if element.name == "img" else element.text
        if len(content["value"]) > 0:
            art_content.append(content)
    return {
        "title": art_title,
        "author": art_author,
        "date": art_date,
        "category": art_category,
        "content": art_content
    }


def get_list_article_by_keyword(keyword):
    print(scrap_config["base_url"] + "?s=" + keyword)
    html = requests.get(scrap_config["base_url"] + "?s=" + keyword).content
    html = BeautifulSoup(html, "html.parser")
    result = {
        "data": []
    }
    for article_element in html.select("div.td_module_16.td_module_wrap.td-animation-stack"):
        art_title = article_element.select_one("h3.entry-title.td-module-title a").text
        art_link = article_element.select_one("h3.entry-title.td-module-title a")["href"]
        art_author = article_element.select_one("span.td-post-author-name a").text
        art_date = article_element.select_one("time.entry-date.updated.td-module-date")["datetime"]
        art_thumbnail = article_element.select_one("img.entry-thumb")["src"]
        result["data"].append({
            "title": art_title,
            "author": art_author,
            "date": art_date,
            "thumbnail": art_thumbnail,
            "link": art_link
        })
    return result


def get_list_article_by_category(category, page):
    html = requests.get(scrap_config["base_url"] + scrap_config["category"][category] + str(page)).content
    html = BeautifulSoup(html, "html.parser")
    result = {
        "totalPage": int(html.select_one("div.page-nav span.pages").text.split("of ")[-1]),
        "page": page,
        "data": []
    }
    for article_element in html.select("div.td_module_10.td_module_wrap.td-animation-stack"):
        art_title = article_element.select_one("h3.entry-title.td-module-title a").text
        art_link = article_element.select_one("h3.entry-title.td-module-title a")["href"]
        art_author = article_element.select_one("span.td-post-author-name a").text
        art_date = article_element.select_one("time.entry-date.updated.td-module-date")["datetime"]
        art_thumbnail = article_element.select_one("img.entry-thumb")["src"]
        result["data"].append({
            "title": art_title,
            "author": art_author,
            "date": art_date,
            "thumbnail": art_thumbnail,
            "link": art_link
        })
    return result
