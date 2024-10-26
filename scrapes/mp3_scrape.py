import logging
import os.path
import shutil
from pathlib import Path
from typing import Optional

import config
from _scrape import MusicScrape, default_dir
from config import FAIL_DIR


class Mp3Scrape(MusicScrape):

    def __init__(self, target_dir):
        super().__init__(0)
        self.__target_dir = target_dir
        if self.__target_dir is not None and not os.path.exists(self.__target_dir):
            os.makedirs(self.__target_dir, exist_ok=True)

    def scrape(self, file_path: Path) -> Optional[str]:
        from mutagen.easyid3 import EasyID3
        # 加载MP3文件
        try:
            audio = EasyID3(file_path)
        except:
            logging.error(f"文件解析失败，文件名:{file_path.name}")
            fail_dir = str(os.path.join(self.__target_dir if self.__target_dir else config.SCAN_DIR, FAIL_DIR))
            if not os.path.exists(fail_dir):
                os.makedirs(fail_dir, exist_ok=True)
            try:
                logging.error(f"文件{file_path}  移动到  {fail_dir}")
                shutil.move(file_path, fail_dir)
            except:
                pass
            return fail_dir
        # 打印所有可用的元数据标签
        # print(audio.keys())
        # 访问特定的元数据标签
        artist = audio.get('artist', [])
        title = audio.get('title', [])
        album = audio.get('album', [])
        print('Title:', title)
        # print('Album:', audio.get('album', ['N/A'])[0])
        # print('Track Number:', audio.get('tracknumber', ['N/A'])[0])
        # print('Date:', audio.get('date', ['N/A'])[0])
        # print('Genre:', audio.get('genre', ['N/A'])[0])
        # print('Composer:', audio.get('composer', ['N/A'])[0])
        # print('Disc Number:', audio.get('discnumber', ['N/A'])[0])
        # print('Publisher:', audio.get('publisher', ['N/A'])[0])
        # print('Comment:', audio.get('comment', ['N/A'])[0])
        # print('Copyright:', audio.get('copyright', ['N/A'])[0])
        # print('BPM:', audio.get('bpm', ['N/A'])[0])
        # print('Encoded By:', audio.get('encodedby', ['N/A'])[0])
        # print('Length:', audio.get('length', ['N/A'])[0])
        # print('Lyrics:', audio.get('lyrics', ['N/A'])[0])
        # print('URL:', audio.get('website', ['N/A'])[0])
        # print('Rating:', audio.get('rating', ['N/A'])[0])
        if len(artist) > 0 and len(title) > 0:
            if self.__target_dir:
                base_dir = self.__target_dir
            else:
                base_dir = default_dir()
                if not os.path.exists(base_dir):
                    os.makedirs(base_dir, exist_ok=True)
            new_path = os.path.join(base_dir, f"{artist[0]} - {title[0]}.{file_path.name.split('.')[-1]}")
            shutil.move(file_path, new_path)
            logging.info(f"文件{file_path.name}  移动到 {new_path}")
            return new_path
