import logging
import os
import re
from typing import Optional

from _scrape import MovieInfo, MovieScrape


class BaseJavScrape(MovieScrape):
    __name_regex = ["[a-z|A-Z]{3,4}-[0-9]{3,4}"]

    def __init__(self, target_dir, timeout, create_nfo, translator):
        super().__init__(timeout=timeout, create_nfo=create_nfo)
        self.__target_dir = target_dir
        self.__translator = translator

    def match_name(self, file_name):
        for regex in self.__name_regex:
            result = re.match(regex, file_name)
            if result:
                return result.group()
        return None

    def save_img(self, movie: MovieInfo, save_dir):
        logging.info(f"cover  :{movie.cover}    {len(movie.cover)}")
        if len(movie.cover) > 0:
            self.download_img(movie.cover, save_dir, "cover.jpg", movie.url)
        if len(movie.preview_pics) > 0:
            name_count = 1
            for preview_pic in movie.preview_pics:
                self.download_img(preview_pic, save_dir, f"preview_{name_count}.jpg", movie.url)
                name_count += 1
        logging.info(f"{len(movie.actress_pics)}")
        if len(movie.actress_pics) > 0:
            for actor in movie.actress_pics:
                self.download_img(movie.actress_pics[actor], save_dir, f"{actor}.jpg", movie.url)

    def __append_regex(self, regex):
        self.__name_regex.append(regex)

    def scrape_type(self) -> str:
        return "movie"

    def _scrape_by_num(self, num) -> Optional[MovieInfo]:
        pass

    def _scrape_data(self, name, parent_dir) -> Optional[str]:
        movie = self._scrape_by_num(name)
        if movie is None:
            return None
        if self.__translator is not None:
            res = self.__translator.translate(movie.title)
            if res:
                movie.title = res
        if movie.actor is None or movie.actor == "":
            movie.actor = "未知演员"
        base_dir = os.path.join(self.__target_dir if self.__target_dir else parent_dir, movie.actor, movie.title)
        os.makedirs(base_dir, exist_ok=True)
        self.save_img(movie, base_dir)
        return base_dir
