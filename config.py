from robyn import logger

DEFAULT_DIR_NAME = '整理完成'
FAIL_DIR = '整理失败'


class GlobalConfig:
    _config = {}
    __proxies = None

    @classmethod
    def set(cls, key, value):
        cls._config[key] = value

    @classmethod
    def get(cls, key, default=None):
        v = cls._config.get(key)
        if v is None:
            logger.info(f"settings {key} not found, use default value {default}")
        return v

    @classmethod
    def get_all(cls):
        return cls._config

    @classmethod
    def update_all(cls, json):
        cls.__proxies = None
        return cls._config.update(json)

    @classmethod
    def get_proxy(cls):
        if cls.__proxies is None and cls._config.get("useProxy"):
            cls.__proxies = {"http": cls._config.get("httpProxy"), "https": cls._config.get("httpsProxy")}
        return cls.__proxies
