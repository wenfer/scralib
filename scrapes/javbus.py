import logging
from typing import Union

from _scrape import MovieInfo
from scrapes.jav_base import BaseJavScrape

permanent_url = 'https://www.javbus.com'


class JavBusScrape(BaseJavScrape):

    def __init__(self, target_dir, timeout=30, create_nfo=True, translator=None):
        super().__init__(target_dir, timeout=timeout, create_nfo=create_nfo, translator=translator)
        self.base_url = 'https://www.javbus.com'

    def site_url(self) -> str:
        return self.base_url

    def _scrape_by_num(self, num) -> Union[MovieInfo, None]:
        url = f'{self.base_url}/{num}'
        html = self.get_html(url, delay_raise=True)

        # 引入登录验证后状态码不再准确，因此还要额外通过检测标题来确认是否发生了404
        page_title = html.xpath('/html/head/title/text()')
        if page_title and page_title[0].startswith('404 Page Not Found!'):
            # raise MovieNotFoundError(__name__, num)
            raise RuntimeError("movie not found")

        container = html.xpath("//div[@class='container']")[0]
        title = container.xpath("h3/text()")[0]
        cover = container.xpath("//a[@class='bigImage']/img/@src")[0]
        preview_pics = container.xpath("//div[@id='sample-waterfall']/a/@href")
        info = container.xpath("//div[@class='col-md-3 info']")[0]
        dvdid = info.xpath("p/span[text()='識別碼:']")[0].getnext().text
        publish_date = info.xpath("p/span[text()='發行日期:']")[0].tail.strip()
        duration = info.xpath("p/span[text()='長度:']")[0].tail.replace('分鐘', '').strip()
        director_tag = info.xpath("p/span[text()='導演:']")
        movie = MovieInfo()
        if director_tag:  # xpath没有匹配时将得到空列表
            movie.director = director_tag[0].getnext().text.strip()
        producer_tag = info.xpath("p/span[text()='製作商:']")
        if producer_tag:
            text = producer_tag[0].getnext().text
            if text:
                movie.producer = text.strip()
        publisher_tag = info.xpath("p/span[text()='發行商:']")
        if publisher_tag:
            movie.publisher = publisher_tag[0].getnext().text.strip()
        serial_tag = info.xpath("p/span[text()='系列:']")
        if serial_tag:
            movie.serial = serial_tag[0].getnext().text
        # genre, genre_id
        genre_tags = info.xpath("//span[@class='genre']/label/a")
        genre, genre_id = [], []
        for tag in genre_tags:
            tag_url = tag.get('href')
            pre_id = tag_url.split('/')[-1]
            genre.append(tag.text)
            if 'uncensored' in tag_url:
                movie.uncensored = True
                genre_id.append('uncensored-' + pre_id)
            else:
                movie.uncensored = False
                genre_id.append(pre_id)
        # JavBus的磁力链接是依赖js脚本加载的，无法通过静态网页来解析
        # actress, actress_pics
        actress, actress_pics = [], {}
        actress_tags = html.xpath("//a[@class='avatar-box']/div/img")
        for tag in actress_tags:
            name = tag.get('title')
            pic_url = tag.get('src')
            actress.append(name)
            if not pic_url.endswith('nowprinting.gif'):  # 略过默认的头像
                actress_pics[name] = pic_url
        # 整理数据并更新movie的相应属性
        movie.url = f'{permanent_url}/{movie.dvdid}'
        movie.dvdid = dvdid
        movie.title = title.replace(dvdid, '').strip()
        movie.cover = cover
        movie.preview_pics = preview_pics
        if publish_date != '0000-00-00':  # 丢弃无效的发布日期
            movie.publish_date = publish_date
        movie.duration = duration if int(duration) else None
        movie.genre = genre
        movie.genre_id = genre_id
        movie.actress = actress
        movie.actress_pics = actress_pics
        return movie
