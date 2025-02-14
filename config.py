app = None

DEFAULT_DIR_NAME = '整理完成'
FAIL_DIR = '整理失败'
SCAN_DIR = ""
TMDB_API_KEY = "c06c581794e148e16461150d2320a13a"
MOVIE_TARGET_DIR = ""
DOWNLOAD_IMAGE = False  # 是否下载图片
USE_PROXY = None
HTTP_PROXY = ""
HTTPS_PROXY = ""

# 默认支持的文件后缀
SUPPORT_SUFFIX = ['.mp4', '.mkv']

REMOVE_REGEX = [
    "萝莉视频989pa.com-",
    "阳光电影dygod.org",
    "【.+】",
    "梦幻天堂·龙网\\(www.321n.net\\)",
    "[国|中|英][\u4e00-\u9fa5a]+[中|双|英|无]字",
    "(mkv|mp4)",
    "(19[0-9]{2}|20[0-9]{2})",
    "(DTS-SONYHD|DDP5|BD|HD|DSNP|AAC|2Audio|DreamHD|Atmos)",
    "((1080|2160)[p|P])",
    "([H|X]26[4|5])",
    "WEB-DL",
]

IGNORE_NAMES = []
SCRAPE_LIST = []

MOVIE_MINSIZE = 10
MUSIC_MINSIZE = 1

# 请求超时时间，默认30
TIMEOUT = 30

# 翻译引擎
TRANSLATE_ENGINE = None

# bing翻译
BING_APP_ID = None
BING_API_KEY = None

# 大模型翻译
OPENAI_API_URL = None
OPENAI_API_KEY = None
OPENAI_MODEL = None

# claude 翻译
CLAUDE_API_KEY = None

# 百度翻译
BAIDU_APP_ID = None
BAIDU_API_KEY = None


def update_settings(settings):
    global DEFAULT_DIR_NAME, FAIL_DIR, SCAN_DIR, MOVIE_TARGET_DIR, USE_PROXY, HTTP_PROXY, HTTPS_PROXY, MUSIC_TARGET_DIR, \
        IGNORE_NAMES, SCRAPE_LIST, MOVIE_MINSIZE, MUSIC_MINSIZE, TIMEOUT, TRANSLATE_ENGINE, BING_APP_ID, BING_API_KEY, \
        OPENAI_API_URL, OPENAI_API_KEY, OPENAI_MODEL, CLAUDE_API_KEY, BAIDU_APP_ID, BAIDU_API_KEY
    DEFAULT_DIR_NAME = settings.get("defaultDirName", DEFAULT_DIR_NAME)
    BAIDU_APP_ID = settings.get("baiduAppId", BAIDU_APP_ID)
    BAIDU_API_KEY = settings.get("baiduApiKey", BAIDU_API_KEY)
    FAIL_DIR = settings.get("failDir", FAIL_DIR)
    SCAN_DIR = settings.get("scanDir", SCAN_DIR)
    MOVIE_TARGET_DIR = settings.get("movieTargetDir", MOVIE_TARGET_DIR)
    # MUSIC_TARGET_DIR = settings.get("musicTargetDir", MUSIC_TARGET_DIR)
    USE_PROXY = settings.get("useProxy", USE_PROXY)
    HTTP_PROXY = settings.get("httpProxy", HTTP_PROXY)
    HTTPS_PROXY = settings.get("httpsProxy", HTTPS_PROXY)
    IGNORE_NAMES = settings.get("ignoreNames", IGNORE_NAMES)
    SCRAPE_LIST = settings.get("scrapeList", SCRAPE_LIST)
    MOVIE_MINSIZE = settings.get("movieMinSize", MOVIE_MINSIZE)
    MUSIC_MINSIZE = settings.get("musicMinSize", MUSIC_MINSIZE)
    TIMEOUT = settings.get("timeout", TIMEOUT)
    TRANSLATE_ENGINE = settings.get("translateEngine", TRANSLATE_ENGINE)
    BING_APP_ID = settings.get("bingAppId", BING_APP_ID)
    BING_API_KEY = settings.get("bingApiKey", BING_API_KEY)
    OPENAI_API_URL = settings.get("openaiApiUrl", OPENAI_API_URL)
    OPENAI_API_KEY = settings.get("openaiApiKey", OPENAI_API_KEY)
    OPENAI_MODEL = settings.get("openaiModel", OPENAI_MODEL)
    CLAUDE_API_KEY = settings.get("claudeApiKey", CLAUDE_API_KEY)
    if settings.get("ignoreNames"):
        IGNORE_NAMES = settings.get("ignoreNames").split(":")
    if settings.get("scrapeList"):
        SCRAPE_LIST = settings.get("scrapeList").split(":")
