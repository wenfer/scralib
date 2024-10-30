"""从dl.getchu官网抓取数据"""
import json
import re
import logging
from typing import Optional

from _scrape import MovieInfo
from scrapes.jav_base import BaseJavScrape

logger = logging.getLogger(__name__)

# https://dl.getchu.com/i/item4045373
# base_url = 'https://dl.getchu.com'
# dl.getchu用utf-8会乱码
base_encode = 'euc-jp'


def get_movie_title(html):
    container = html.xpath("//form[@action='https://dl.getchu.com/cart/']/div/table[2]")
    if len(container) > 0:
        container = container[0]
    rows = container.xpath('.//tr')
    title = ''
    for row in rows:
        for cell in row.xpath('.//td/div'):
            # 获取单元格文本内容
            if cell.text:
                title = str(cell.text).strip()
    return title


def get_movie_img(html, getchu_id):
    img_src = ''
    container = html.xpath(f'//img[contains(@src, "{getchu_id}top.jpg")]')
    if len(container) > 0:
        container = container[0]
        img_src = container.get('src')
    return img_src


def get_movie_preview(html, getchu_id):
    preview_pics = []
    container = html.xpath(f'//img[contains(@src, "{getchu_id}_")]')
    if len(container) > 0:
        for c in container:
            preview_pics.append(c.get('src'))
    return preview_pics


DURATION_PATTERN = re.compile(r'(?:動画)?(\d+)分')


class DlGetchuScrape(BaseJavScrape):
    def __init__(self, target_dir, timeout=30, create_nfo=True, translator=None):
        super().__init__(target_dir=target_dir, timeout=timeout, create_nfo=create_nfo, translator=translator)
        self.base_url = 'https://dl.getchu.com'

    def site_url(self) -> str:
        return self.base_url

    def _scrape_by_num(self, num) -> Optional[MovieInfo]:
        """解析指定番号的影片数据"""
        # 去除番号中的'GETCHU'字样
        id_uc = num.upper()
        if not id_uc.startswith('GETCHU-'):
            return None
        getchu_id = id_uc.replace('GETCHU-', '')
        # 抓取网页
        url = f'{self.base_url}/i/item{getchu_id}'
        html = self.get_html(url, delay_raise=True, encoding=base_encode)
        container = html.xpath("//form[@action='https://dl.getchu.com/cart/']/div/table[3]")
        if len(container) > 0:
            container = container[0]
        # 将表格提取为键值对
        rows = container.xpath('.//table/tr')
        kv_rows = [i for i in rows if len(i) == 2]
        data = {}
        movie = MovieInfo()
        for row in kv_rows:
            # 获取单元格文本内容
            key = row.xpath("td[@class='bluetext']/text()")[0]
            # 是否包含a标签: 有的属性是用<a>表示的，不是text
            a_tags = row.xpath("td[2]/a")
            if a_tags:
                value = [i.text for i in a_tags]
            else:
                # 获取第2个td标签的内容（下标从1开始计数）
                value = row.xpath("td[2]/text()")
            data[key] = value

        for key, value in data.items():
            if key == 'サークル':
                movie.producer = value[0]
            elif key == '作者':
                # 暂时没有在getchu找到多个actress的片子
                movie.actress = [i.strip() for i in value]
            elif key == '画像数&ページ数':
                match = DURATION_PATTERN.search(' '.join(value))
                if match:
                    movie.duration = match.group(1)
            elif key == '配信開始日':
                movie.publish_date = value[0].replace('/', '-')
            elif key == '趣向':
                movie.genre = value
            elif key == '作品内容':
                idx = -1
                for i, line in enumerate(value):
                    if line.lstrip().startswith('※'):
                        idx = i
                        break
                movie.plot = ''.join(value[:idx])

        movie.title = get_movie_title(html)
        movie.cover = get_movie_img(html, getchu_id)
        movie.preview_pics = get_movie_preview(html, getchu_id)
        movie.dvdid = id_uc
        movie.url = url
        return movie

    def test(self, num):
        return self._scrape_by_num(num)


if __name__ == '__main__':
    spider = DlGetchuScrape("")
    m = spider.test("getchu-4041026")
    print(json.dumps(m.get_info_dic(), ensure_ascii=False))
