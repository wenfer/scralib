from tortoise import Model, fields


class Movie(Model):
    """
        电影
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    path = fields.CharField(50)
    plot = fields.CharField(1000)  # 故事情节
    source = fields.CharField(50)  # 来源
    cover = fields.CharField(100)  # 封面图片（URL）
    high_cover = fields.CharField(100)  # 高清封面图片（URL）
    genre = fields.CharField(50)  # 影片分类的标签
    genre_id = fields.CharField(50)  # 影片分类的标签的ID，用于解决部分站点多个genre同名的问题，也便于管理多语言的genre
    genre_norm = fields.CharField(50)  # 统一后的影片分类的标签
    score = fields.CharField(50)  # 评分（10分制，为方便提取写入和保持统一，应以字符串类型表示）
    title = fields.CharField(50)  # 影片标题（不含番号）
    ori_title = fields.CharField(50)  # 原始影片标题，仅在标题被处理过时才对此字段赋值
    serial = fields.CharField(100)  # 系列
    actress = fields.CharField(100)  # 出演女优
    actor_pics = fields.CharField(100)  # 出演女优的头像。单列一个字段，便于满足不同的使用需要
    director = fields.CharField(100)  # 导演
    duration = fields.CharField(50)  # 影片时长
    producer = fields.CharField(100)  # 制作商
    publisher = fields.CharField(100)  # 发行商
    uncensored = fields.CharField(50)  # 是否为无码影片
    publish_date = fields.CharField(50)  # 发布日期
    cid = fields.CharField(50)  # 番号
    preview_pics = fields.CharField(100)  # 预览图片（URL）

    def __str__(self):
        return f"Movie {self.id}: {self.name}"


class Settings(Model):
    """
        扫描scrapes目录下的刮削脚本
    """
    id = fields.IntField(primary_key=True)
    name = fields.CharField(50,unique=True)
    value = fields.CharField(50)


class Scrape(Model):
    """
        扫描scrapes目录下的刮削脚本
    """
    id = fields.IntField(primary_key=True)
    name = fields.CharField(50)
    path = fields.CharField(50)
    status = fields.CharField(50)


class Task(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(50)
    cron = fields.CharField(50)

    def __str__(self):
        return f"Task {self.id}: {self.name}"
