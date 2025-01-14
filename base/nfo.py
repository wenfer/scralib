import xml.etree.ElementTree as ET


class Movie:
    def __init__(self):
        self.title = ""  # 电影标题
        self.originaltitle = ""  # 电影原始标题
        self.sorttitle = ""  # 排序标题
        self.ratings = []  # 评分信息
        self.userrating = 0  # 用户评分
        self.top250 = 0  # 是否为Top250电影
        self.outline = ""  # 简要概述
        self.plot = ""  # 剧情简介
        self.tagline = ""  # 电影标语
        self.runtime = 0  # 电影时长（分钟）
        self.thumbs = []  # 电影封面图片列表
        self.fanart = None  # 电影艺术图
        self.mpaa = ""  # MPAA评级
        self.playcount = 0  # 播放次数
        self.lastplayed = ""  # 最后播放时间
        self.id = 0  # 电影ID
        self.uniqueid = {"imdb": "", "tmdb": ""}  # 唯一标识符
        self.genre = []  # 电影类型
        self.country = []  # 国家/地区
        self.set = None  # 电影合集
        self.tags = []  # 电影标签
        self.credits = []  # 编剧和制片人列表
        self.director = ""  # 导演
        self.premiered = ""  # 首映时间
        self.year = 0  # 电影上映年份
        self.status = ""  # 电影状态
        self.code = ""  # 电影代码
        self.aired = ""  # 播放时间
        self.studio = ""  # 电影制片厂
        self.trailer = ""  # 电影预告片文件
        self.fileinfo = None  # 文件信息
        self.actors = []  # 演员列表


class Rating:
    def __init__(self, name="", max_rating=10, default=False):
        self.name = name  # 评分来源名称
        self.max = max_rating  # 评分最高值
        self.default = default  # 是否为默认评分
        self.value = 0.0  # 评分值
        self.votes = 0  # 评分人数


class Thumb:
    def __init__(self, aspect="", preview=""):
        self.aspect = aspect  # 封面图片类型（如poster、landscape等）
        self.preview = preview  # 图片URL


class Fanart:
    def __init__(self, preview=""):
        self.preview = preview  # 艺术图URL


class Actor:
    def __init__(self, name="", role="", order=0, thumb=""):
        self.name = name  # 演员名字
        self.role = role  # 演员角色
        self.order = order  # 演员顺序
        self.thumb = thumb  # 演员头像URL


# 解析XML数据并填充实体类
def parse_nfo(file_path):
    # 解析XML
    root = ET.parse(file_path)
    # 创建Movie实例
    movie = Movie()

    movie.title = root.find('title').text  # 电影标题
    movie.originaltitle = root.find('originaltitle').text  # 电影原始标题
    movie.sorttitle = root.find('sorttitle').text  # 排序标题

    # 解析评分信息
    ratings = root.find('ratings')
    for rating in ratings.findall('rating'):
        rating_obj = Rating()
        rating_obj.name = rating.get('name')
        rating_obj.max = int(rating.get('max'))
        rating_obj.default = rating.get('default') == "true"
        rating_obj.value = float(rating.find('value').text)
        rating_obj.votes = int(rating.find('votes').text)
        movie.ratings.append(rating_obj)

    movie.userrating = int(root.find('userrating').text)  # 用户评分
    movie.top250 = int(root.find('top250').text)  # 是否为Top250电影
    movie.outline = root.find('outline').text or ""  # 简要概述
    movie.plot = root.find('plot').text  # 剧情简介
    movie.tagline = root.find('tagline').text  # 电影标语
    movie.runtime = int(root.find('runtime').text)  # 电影时长

    # 解析封面图
    thumbs = root.findall('thumb')
    for thumb in thumbs:
        thumb_obj = Thumb(aspect=thumb.get('aspect'), preview=thumb.get('preview'))
        movie.thumbs.append(thumb_obj)

    # 解析艺术图
    fanart_elem = root.find('fanart')
    if fanart_elem is not None:
        movie.fanart = Fanart(preview=fanart_elem.find('thumb').get('preview'))

    movie.mpaa = root.find('mpaa').text  # MPAA评级
    movie.playcount = int(root.find('playcount').text)  # 播放次数
    movie.lastplayed = root.find('lastplayed').text  # 最后播放时间
    movie.id = int(root.find('id').text)  # 电影ID
    movie.uniqueid['imdb'] = root.find('uniqueid[@type="imdb"]').text  # IMDB唯一标识
    movie.uniqueid['tmdb'] = root.find('uniqueid[@type="tmdb"]').text  # TMDB唯一标识

    # 解析其他字段
    movie.genre = [genre.text for genre in root.findall('genre')]  # 电影类型
    movie.country = [country.text for country in root.findall('country')]  # 国家/地区
    movie.set = root.find('set')  # 电影合集

    # 解析标签
    movie.tags = [tag.text for tag in root.findall('tag')]  # 电影标签

    # 解析导演、编剧等
    movie.credits = [credit.text for credit in root.findall('credits')]  # 编剧和制片人列表
    movie.director = root.find('director').text  # 导演
    movie.premiered = root.find('premiered').text  # 首映时间
    movie.year = int(root.find('year').text)  # 电影上映年份
    movie.status = root.find('status').text or ""  # 电影状态
    movie.code = root.find('code').text or ""  # 电影代码
    movie.aired = root.find('aired').text or ""  # 播放时间
    movie.studio = root.find('studio').text  # 电影制片厂
    movie.trailer = root.find('trailer').text  # 电影预告片文件

    # 解析演员信息
    actors = root.findall('actor')
    for actor_elem in actors:
        actor = Actor(
            name=actor_elem.find('name').text,
            role=actor_elem.find('role').text,
            order=int(actor_elem.find('order').text),
            thumb=actor_elem.find('thumb').text
        )
        movie.actors.append(actor)

    return movie


m = parse_nfo("movie.nfo")
print(m.id)
