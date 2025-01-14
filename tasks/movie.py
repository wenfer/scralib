import os
from pathlib import Path

import config
from log_config import log
from models.models import Settings
from scrapes.scrape import Scraper


def handle_file(file_path: Path, scrapes: list[Scraper]):
    log.info(f"开始处理文件{file_path}")
    if (file_path.stat().st_size > config.MOVIE_MINSIZE and
            any(file_path.name.endswith(suffix) for suffix in config.SUPPORT_SUFFIX)):
        for scrape in scrapes:
            log.info(f"开始使用{scrape.site_url()}刮削文件:{file_path.name}")
            try:
                new_path = scrape.scrape(file_path)
                if new_path:
                    log.info(f"{file_path.name}刮削成功，文件已经移动到{new_path}")
                    break
            except BaseException as e:
                log.error(f"请求 {scrape.site_url()} 失败，可以尝试配置代理")
                log.exception(e)


def scan_dir(dir_path: Path):
    for child in os.scandir(dir_path):
        if child.is_file():
            handle_file(Path(child))
        elif child.is_dir():
            scan_dir(Path(child))


async def scan_movie():
    base_dir = config.SCAN_DIR
    log.info(f"开始扫描电影 目录{base_dir}")
    for child in os.scandir(base_dir):
        if child.is_file():
            handle_file(Path(child))
        elif child.is_dir():
            scan_dir(Path(child))
