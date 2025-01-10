import logging
import os

config_path = None

if os.name == "nt":
    base_path = os.getenv("APPDATA")
elif os.name == "posix":
    base_path = os.path.expanduser("~/.config/")
else:
    logging.info(f"unknown os {os.name}")
    base_path = '.config'
config_path = os.path.join(base_path, "scrapelib")
if not os.path.exists(config_path):
    os.mkdir(config_path)
logging.info(f"init config_path is {config_path}")

