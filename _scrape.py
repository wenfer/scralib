import json
import logging
import os.path
import shutil
from pathlib import Path
from typing import Optional

import lxml.html
import requests

import xml.etree.ElementTree as ET

from requests import ConnectTimeout

import config


def default_dir():
    return os.path.join(config.SCAN_DIR, config.DEFAULT_DIR_NAME)


class MovieInfo:
    title: str = ""
    url: str = ""
    dvdid: str = ""
    rating: str = ""
    cover: str = ""
    preview_pics: str = ""
    publish_date: str = ""
    genre: list = []
    genre_id: list = []
    actress: list = []
    actress_pics: dict = {}
    plot: str = ""
    runtime: str = ""
    mpaa: str = ""
    cid: str = ""
    num: str = ""
    tag: str = ""
    country: str = ""
    director: str = ""
    premiered: str = ""
    studio: str = ""
    actor: str = ""

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'dvdid': self.dvdid,
            'rating': self.rating,
            'cover': self.cover,
            'preview_pics': self.preview_pics,
            'publish_date': self.publish_date,
            'genre': self.genre,
            'genre_id': self.genre_id,
            'actress': self.actress,
            'actress_pics': self.actress_pics,
            'plot': self.plot,
            'runtime': self.runtime,
            'mpaa': self.mpaa,
            'cid': self.cid,
            'num': self.num,
            'tag': self.tag,
            'country': self.country,
            'director': self.director,
            'premiered': self.premiered,
            'studio': self.studio,
            'actor': self.actor
        }


class Scrape:

    def __init__(self, timeout):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36',
            "sec-ch-ua-platform": "macos",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"'
        }
        self.timeout = timeout

    def site_url(self) -> str:
        pass

    def min_size(self) -> int:
        pass

    def match_name(self, file_name):
        pass

    def _scrape_data(self, name) -> Optional[str]:
        """
        :param name: 正则匹配后的番号
        :return: 刮削成功的元信息所在目录
        """
        pass

    def scrape(self, file_path: Path):
        matched_name = self.match_name(file_path.name)
        if matched_name is not None and matched_name != "":
            try:
                new_dir = self._scrape_data(matched_name)
                if new_dir:
                    shutil.move(file_path, new_dir)
                    return new_dir
            except ConnectTimeout:
                logging.error(f"请求{self.site_url()}超时")

    def scrape_type(self) -> str:
        pass

    def download_img(self, url, save_dir, name, refer):
        img_path = os.path.join(save_dir, name)
        if os.path.exists(img_path):
            return
        logging.info(f"start download to {os.path.join(save_dir, name)}")
        response = self.get(url, headers={
            "Referer": refer,
        })
        if response.status_code == 200:
            # 以二进制模式打开文件并写入内容
            with open(os.path.join(save_dir, name), 'wb') as file:
                file.write(response.content)
            logging.info(f"image downloaded to {os.path.join(save_dir, name)}")

    # url, cookies=None, timeout=None, delay_raise=False
    def get(self, url, cookies=None, timeout=None, delay_raise=False, headers=None):
        """获取指定url的原始请求"""
        if headers is None:
            headers = self.headers
        else:
            headers.update(self.headers)
        if cookies is None:
            cookies = {}
        if timeout is None:
            timeout = self.timeout
        if config.USE_PROXY == "true":
            proxies = {"http": config.HTTP_PROXY, "https": config.HTTPS_PROXY}
        else:
            proxies = None
        logging.info(f"proxies is {json.dumps(proxies)}")
        r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout)
        if not delay_raise:
            if r.status_code == 403 and b'>Just a moment...<' in r.content:
                # raise SiteBlocked(f"403 Forbidden: 无法通过CloudFlare检测: {url}")
                raise RuntimeError(f"403 Forbidden: 无法通过CloudFlare检测: {url}")
            else:
                r.raise_for_status()
        return r

    def post(self, url, data, cookies=None, timeout=None, delay_raise=False):
        """向指定url发送post请求"""
        if timeout is None:
            timeout = self.timeout
        try:
            if config.USE_PROXY == "true":
                proxies = {"http": config.HTTP_PROXY, "https": config.HTTPS_PROXY}
            else:
                proxies = None
            r = requests.post(url, data=data,
                              headers=self.headers,
                              cookies=cookies,
                              proxies=proxies,
                              timeout=timeout)
        except requests.exceptions.ConnectionError:
            raise RuntimeError("网络不通，建议使用代理")
        if not delay_raise:
            r.raise_for_status()
        return r

    def post_html(self, url, data, cookies=None):
        resp = self.post(url, data, cookies=cookies)
        text = resp.text
        html = lxml.html.fromstring(text)
        # jav321提供ed2k形式的资源链接，其中的非ASCII字符可能导致转换失败，因此要先进行处理
        ed2k_tags = html.xpath("//a[starts-with(@href,'ed2k://')]")
        for tag in ed2k_tags:
            tag.attrib['ed2k'], tag.attrib['href'] = tag.attrib['href'], ''
        html.make_links_absolute(url, resolve_base_href=True)
        for tag in ed2k_tags:
            tag.attrib['href'] = tag.attrib['ed2k']
            tag.attrib.pop('ed2k')
        return html

    def get_html(self, url, cookies=None, timeout=None, delay_raise=False, encoding=None):
        resp = self.get(url, cookies=cookies, timeout=timeout, delay_raise=delay_raise)
        if encoding:
            resp.encoding = encoding
        else:
            resp.encoding = resp.apparent_encoding
        if resp.history and resp.history[0].status_code == 302:
            logging.info("发生302重定向")
            resp_body = resp.history[0].text
        else:
            resp_body = resp.text
        html = lxml.html.fromstring(resp_body)
        html.make_links_absolute(url, resolve_base_href=True)
        return html

    def support_suffix(self) -> list:
        pass


class MovieScrape(Scrape):
    SUPPORT_SUFFIX = [".mp4", ".avi", ".mkv", ".wmv", ".rmvb", ".flv", ".mov"]
    MIN_SIZE = 100 * 1024 * 1024  # 100MB

    def __init__(self, create_nfo, timeout):
        super().__init__(timeout)
        self.__create_nfo = create_nfo

    def support_suffix(self) -> list:
        return self.SUPPORT_SUFFIX

    def min_size(self) -> int:
        return config.MOVIE_MINSIZE

    def __create_nfo(self, movie: MovieInfo, save_dir) -> None:
        """创建nfo文件"""

        # 创建根元素
        movie_tag = ET.Element("movie")

        # 创建并添加子元素
        ET.SubElement(movie_tag, "title").text = movie.title
        ET.SubElement(movie_tag, "sorttitle").text = "排序标题"
        ET.SubElement(movie_tag, "rating").text = "9.0"
        ET.SubElement(movie_tag, "votes").text = "投票数量"
        ET.SubElement(movie_tag, "plot").text = "剧情简介"
        ET.SubElement(movie_tag, "outline").text = "剧情概要"
        ET.SubElement(movie_tag, "runtime").text = "时长"
        ET.SubElement(movie_tag, "mpaa").text = "评级"
        ET.SubElement(movie_tag, "director").text = "导演"
        actor1 = ET.SubElement(movie_tag, "actor")
        ET.SubElement(actor1, "name").text = "演员1"
        ET.SubElement(actor1, "role").text = "角色"
        ET.SubElement(actor1, "order").text = "顺序"

        ET.SubElement(movie_tag, "genre").text = "影片类型1"
        ET.SubElement(movie_tag, "studio").text = "制作公司"
        ET.SubElement(movie_tag, "country").text = "国家地区"
        ET.SubElement(movie_tag, "premiered").text = "发布日期"
        ET.SubElement(movie_tag, "tag").text = "标签1"

        # 将XML树写入文件
        # tree = ET.ElementTree(movie_tag)
        # tree.write(output_path, encoding="utf-8", xml_declaration=True)
        #
        # print(f"NFO文件已生成：{output_path}")

    def save_img(self, movie: MovieInfo, save_dir):
        pass


class MusicScrape(Scrape):
    def __init__(self, timeout):
        super().__init__(timeout)

    def min_size(self) -> int:
        return config.MUSIC_MINSIZE

    def support_suffix(self) -> list:
        return [".mp3"]
