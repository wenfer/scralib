"""从av-wiki抓取数据"""
import logging
from typing import Optional

from _scrape import MovieInfo
from scrapes.jav_base import BaseJavScrape

logger = logging.getLogger(__name__)
base_url = 'https://av-wiki.net'

ATTR_MAP = {'メーカー': 'producer', 'AV女優名': 'actress', 'メーカー品番': 'dvdid', 'シリーズ': 'serial',
            '配信開始日': 'publish_date'}


class AvwikiScrape(BaseJavScrape):
    def __init__(self, target_dir, timeout=30, create_nfo=True, translator=None):
        super().__init__(target_dir=target_dir, timeout=timeout, create_nfo=create_nfo, translator=translator)
        self.base_url = 'https://av-wiki.net'

    def site_url(self) -> str:
        return self.base_url

    def _scrape_by_num(self, num) -> Optional[MovieInfo]:
        """从网页抓取并解析指定番号的数据
        Args:
            movie (MovieInfo): 要解析的影片信息，解析后的信息直接更新到此变量内
        """
        url = url = f'{base_url}/{num}'
        html = self.get_html(url, delay_raise=True)
        cover_tag = html.xpath("//header/div/a[@class='image-link-border']/img")
        movie = MovieInfo()
        if cover_tag:
            try:
                srcset = cover_tag[0].get('srcset').split(', ')
                src_set_urls = {}
                for src in srcset:
                    url, width = src.split()
                    width = int(width.rstrip('w'))
                    src_set_urls[width] = url
                max_pic = sorted(src_set_urls.items(), key=lambda x: x[0], reverse=True)
                movie.cover = max_pic[0][1]
            except:
                movie.cover = cover_tag[0].get('src')
        body = html.xpath("//section[@class='article-body']")[0]
        title = body.xpath("div/p/text()")[0]
        title = title.replace(f"【{movie.dvdid}】", '')
        cite_url = body.xpath("div/cite/a/@href")[0]
        cite_url = cite_url.split('?aff=')[0]
        info = body.xpath("dl[@class='dltable']")[0]
        dt_txt_ls, dd_tags = info.xpath("dt/text()"), info.xpath("dd")
        data = {}
        for dt_txt, dd in zip(dt_txt_ls, dd_tags):
            dt_txt = dt_txt.strip()
            a_tag = dd.xpath('a')
            if len(a_tag) == 0:
                dd_txt = dd.text.strip()
            else:
                dd_txt = [i.text.strip() for i in a_tag]
            if isinstance(dd_txt, list) and dt_txt != 'AV女優名':  # 只有女优名以列表的数据格式保留
                dd_txt = dd_txt[0]
            data[dt_txt] = dd_txt

        for key, attr in ATTR_MAP.items():
            setattr(movie, attr, data.get(key))
        movie.title = title
        movie.uncensored = False  # 服务器在日本且面向日本国内公开发售，不会包含无码片
        return movie
