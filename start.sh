export SCRALIB_USE_PROXY=false
export SCRALIB_HTTP_PROXY="http://xxx:xxx@127.0.0.1:7890"
export SCRALIB_HTTPS_PROXY="http://xxx:xxx@127.0.0.1:7890"

export SCRALIB_MOVIE_MINSIZE=1
export SCRALIB_SCRAPE_LIST=javbus:jav321


export SCRALIB_TRANSLATE_ENGINE="baidu"
export SCRALIB_BAIDU_API_KEY=""
export SCRALIB_BAIDU_APP_ID=""
export SCRALIB_IGNORE=""
export SCRALIB_SCAN_DIR=$HOME/test/
python3 scrapejob.py