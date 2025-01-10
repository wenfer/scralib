import os
from pathlib import Path

import config
from log_config import log
from models.models import Settings


def handle_file(file_path: Path):
    log.info(f"开始处理文件{file_path}")


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
            scan_dir(child)
