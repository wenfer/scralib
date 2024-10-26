import json
import logging
import random
import time
import uuid
from hashlib import md5
from typing import Optional

import requests

import config
from _scrape import MovieInfo


class TranslateEngine:

    def translate(self, text):
        pass

    def auto_translate(self, movie_info: MovieInfo):
        new_title = self.translate(movie_info.title)
        if new_title:
            movie_info.title = new_title


class GoogleTranslateEngine(TranslateEngine):
    def __init__(self):
        super().__init__()
        self.to = 'zh_CN'
        self._google_trans_wait = 60

    def translate(self, text):
        """使用Google翻译文本（默认翻译为简体中文）"""
        # API: https://www.jianshu.com/p/ce35d89c25c3
        # client参数的选择: https://github.com/lmk123/crx-selection-translate/issues/223#issue-184432017
        url = f"https://translate.google.com.hk/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl={self.to}&q={text}"
        r = requests.get(url)
        while r.status_code == 429:
            logging.warning(
                f"HTTP {r.status_code}: {r.reason}: Google翻译请求超限，将等待{self._google_trans_wait}秒后重试")
            time.sleep(self._google_trans_wait)
            r = requests.get(url)
            if r.status_code == 429:
                self._google_trans_wait += random.randint(60, 90)
        if r.status_code == 200:
            result = r.json()
        else:
            result = {'error_code': r.status_code, 'error_msg': r.reason}
        time.sleep(4)  # Google翻译的API有QPS限制，因此需要等待一段时间
        return result


class ClaudeTranslateEngine(TranslateEngine):
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.to = 'zh_CN'
        self.api_url = "https://api.anthropic.com/v1/messages"

    def translate(self, text):
        """使用Claude翻译文本（默认翻译为简体中文）"""
        headers = {
            "x-api-key": self.api_key,
            "context-type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        data = {
            "model": "claude-3-haiku-20240307",
            "system": f"Translate the following Japanese paragraph into {self.to}, while leaving non-Japanese text, "
                      f"names, or text that does not look like Japanese untranslated. Reply with the translated text "
                      f"only, do not add any text that is not in the original content.",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": text}],
        }
        r = requests.post(self.api_url, headers=headers, json=data)
        if r.status_code == 200:
            result = r.json().get("content", [{}])[0].get("text", "").strip()
        else:
            result = {
                "error_code": r.status_code,
                "error_msg": r.json().get("error", {}).get("message", r.reason),
            }
        return result


class OpenAITranslateEngine(TranslateEngine):
    def __init__(self, url: str, api_key: str, model: str):
        super().__init__()
        self.api_key = api_key
        self.api_url = url
        self.model = model
        self.to = 'zh_CN'

    def translate(self, text):
        """使用 OpenAI 翻译文本（默认翻译为简体中文）"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": f"Translate the following Japanese paragraph into {self.to}, while leaving "
                               f"non-Japanese text, names, or text that does not look like Japanese untranslated. "
                               f"Reply with the translated text only, do not add any text that is not in the original "
                               f"content."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            "model": self.model,
            "temperature": 0,
            "max_tokens": 1024,
        }
        r = requests.post(self.api_url, headers=headers, json=data)
        if r.status_code == 200:
            if 'error' in r.json():
                result = {
                    "error_code": r.status_code,
                    "error_msg": r.json().get("error", {}).get("message", ""),
                }
            else:
                result = r.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        else:
            result = {
                "error_code": r.status_code,
                "error_msg": r.reason,
            }
        return result


class BingTranslateEngine(TranslateEngine):
    def __init__(self, api_id: str, api_key: str):
        super().__init__()
        self.app_id = api_id
        self.api_key = api_key
        self.api_url = "https://api.cognitive.microsofttranslator.com/translate"
        self.to = 'zh-Hans'

    def translate(self, text):
        """使用Bing翻译文本（默认翻译为简体中文）"""
        params = {'api-version': '3.0', 'to': self.to, 'includeSentenceLength': True}
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': 'global',
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        body = [{'text': text}]
        r = requests.post(self.api_url, params=params, headers=headers, json=body)
        result = r.json()
        return result


class BaiduTranslateEngine(TranslateEngine):
    def __init__(self, app_id, app_key):
        super().__init__()
        self.app_id = app_id
        self.api_key = app_key
        self.to = "zh"
        self._last_access = -1

    def translate(self, text):
        """使用百度翻译文本（默认翻译为简体中文）"""
        api_url = "https://api.fanyi.baidu.com/api/trans/vip/translate"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        salt = random.randint(0, 0x7FFFFFFF)
        sign_input = self.app_id + text + str(salt) + self.api_key
        sign = md5(sign_input.encode('utf-8')).hexdigest()
        payload = {'appid': self.app_id, 'q': text, 'from': 'auto', 'to': self.to, 'salt': salt, 'sign': sign}
        # 由于百度标准版限制QPS为1，连续翻译标题和简介会超限，因此需要添加延时
        now = time.perf_counter()
        wait = 1.0 - (now - self._last_access)
        if wait > 0:
            time.sleep(wait)
        r = requests.post(api_url, params=payload, headers=headers)

        result = r.json()
        self._last_access = time.perf_counter()
        if result.get("error_code") is not None:
            logging.error(f"百度翻译失败，错误代码为:{result['error_code']}  错误信息为:{result['error_msg']}")
            return None
        logging.info(f"百度翻译完成，识别到的语言为:{result['from']}  翻译为:{result['to']}  原文为:{text}")
        return result['trans_result'][0]['dst']


def get_translate() -> Optional[TranslateEngine]:
    engine = config.TRANSLATE_ENGINE
    if engine == 'bing':
        return BingTranslateEngine(config.BING_APP_ID, config.BING_API_KEY)
    elif engine == 'openai':
        return OpenAITranslateEngine(config.OPENAI_API_URL, config.OPENAI_API_KEY,
                                     config.OPENAI_MODEL)
    elif engine == 'claude':
        return ClaudeTranslateEngine(config.CLAUDE_API_KEY)
    elif engine == 'baidu':
        return BaiduTranslateEngine(config.BAIDU_APP_ID, config.BAIDU_API_KEY)
    return None
