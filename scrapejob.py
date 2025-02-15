import fnmatch
import logging
import os
import shutil
from pathlib import Path

import config
import translate
from config import GlobalConfig
from scrapes.airav import AiravScrape
from scrapes.arzon import ArzonScrape
from scrapes.avsox import AvsoxScrape
from scrapes.avwiki import AvwikiScrape
from scrapes.dl_getchu import DlGetchuScrape
from scrapes.fanza import FanzaScrape
from scrapes.jav321 import Jav321Scrape
from scrapes.javbus import JavBusScrape


def match_ignores(string, patterns):
    """
    尝试用多个通配符模式匹配一个字符串，一旦匹配成功就立即返回True。

    :param string: 要匹配的字符串
    :param patterns: 通配符模式列表
    :return: 如果匹配成功，返回True；否则返回False
    """
    for pattern in patterns:
        if fnmatch.fnmatch(string, pattern):
            return True
    return False


def handle_file(file_path: Path):
    for scrape in scrapes:
        if (file_path.stat().st_size > scrape.min_size() and
                any(file_path.name.endswith(suffix) for suffix in scrape.support_suffix())):
            logging.info(f"开始使用{scrape.site_url()}刮削文件:{file_path.name}")
            try:
                new_path = scrape.scrape(file_path)
                if new_path:
                    logging.info(f"{file_path.name}刮削成功，文件已经移动到{new_path}")
                    break
            except BaseException as e:
                logging.error(f"请求 {scrape.site_url()} 失败，可以尝试配置代理")
                logging.exception(e)


def is_directory_empty(directory):
    return len(os.listdir(directory)) == 0


def scan_dir(directory_path):
    if match_ignores(directory_path.name, GlobalConfig.get("ignoreNames")):
        return
    logging.info(f"开始扫描目录{directory_path.name}")
    for child in os.scandir(directory_path):
        if match_ignores(child.name, GlobalConfig.get("ignoreNames")):
            logging.info(f"ignore:{child.name}")
            continue
        if child.is_file():
            handle_file(Path(child))
        elif child.is_dir():
            scan_dir(child)
    if is_directory_empty(directory_path):
        shutil.rmtree(directory_path)


def read_config_env():
    env = os.environ
    scandir = env.get("SCRALIB_SCAN_DIR")
    if scandir is None or scandir == "":
        raise RuntimeError("未配置扫描目录")
    GlobalConfig.set("scanDir", scandir)
    GlobalConfig.set("targetDir", env.get("SCRALIB_TARGET_DIR", config.DEFAULT_DIR_NAME))
    ignore_names = env.get("SCRALIB_IGNORE", "").split(":")
    ignore_names.append(config.DEFAULT_DIR_NAME)
    ignore_names.append(config.FAIL_DIR)
    GlobalConfig.set("ignoreNames", ignore_names)
    GlobalConfig.set("minsize", int(env.get("SCRALIB_MOVIE_MINSIZE", 10)) * 1024)
    GlobalConfig.set("translateEngine", env.get("SCRALIB_TRANSLATE_ENGINE", "google"))
    GlobalConfig.set("bingApiId", env.get("SCRALIB_BING_API_ID"))
    GlobalConfig.set("bingApiKey", env.get("SCRALIB_BING_API_KEY"))
    GlobalConfig.set("openaiApiUrl", env.get("SCRALIB_OPENAI_API_URL"))
    GlobalConfig.set("openaiApiKey", env.get("SCRALIB_OPENAI_API_KEY"))
    GlobalConfig.set("openaiApiModel", env.get("SCRALIB_OPENAI_MODEL"))
    GlobalConfig.set("claudeApiKey", env.get("SCRALIB_CLAUDE_API_KEY"))
    GlobalConfig.set("baiduAppId", env.get("SCRALIB_BAIDU_APP_ID"))
    GlobalConfig.set("baiduApiKey", env.get("SCRALIB_BAIDU_API_KEY"))
    GlobalConfig.set("scrapeList", env.get("SCRALIB_SCRAPE_LIST", "").split(":"))
    GlobalConfig.set("useProxy", env.get("SCRALIB_USE_PROXY"))
    GlobalConfig.set("httpProxy", env.get("SCRALIB_HTTP_PROXY"))
    GlobalConfig.set("httpsProxy", env.get("SCRALIB_HTTPS_PROXY"))


if __name__ == '__main__':
    read_config_env()
    scrapes = []
    translator = translate.get_translate()
    target_dir = GlobalConfig.get("targetDir")
    for scrape_name in GlobalConfig.get("scrapeList"):
        if scrape_name == "javbus":
            scrapes.append(JavBusScrape(target_dir=target_dir, translator=translator))
        elif scrape_name == "jav321":
            scrapes.append(Jav321Scrape(target_dir=target_dir, translator=translator))
        elif scrape_name == "airav":
            scrapes.append(AiravScrape(target_dir=target_dir, translator=translator))
        elif scrape_name == "arzon":
            scrapes.append(ArzonScrape(target_dir=target_dir, translator=translator))
        elif scrape_name == "avsox":
            scrapes.append(AvsoxScrape(target_dir=target_dir, translator=translator))
        elif scrape_name == "avwiki":
            scrapes.append(AvwikiScrape(target_dir=target_dir, translator=translator))
        elif scrape_name == "dl_getchu":
            scrapes.append(DlGetchuScrape(target_dir=target_dir, translator=translator))
        elif scrape_name == "fanza":
            scrapes.append(FanzaScrape(target_dir=target_dir, translator=translator))
    for file in os.scandir(GlobalConfig.get("scanDir")):
        if file.is_file():
            handle_file(Path(file.path))
        elif file.is_dir():
            scan_dir(file)
