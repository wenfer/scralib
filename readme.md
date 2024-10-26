## 从[javsp](https://github.com/Yuukiy/JavSP)项目中改造来的刮削工具
- 目前只支持两个jav抓取源，可以自己添加
- 准备再加一个mp3音频的刮削器，还未完成
- 依赖很轻，可以放到青龙面板中运行，也可以自己做成docker镜像

### 青龙面板配置
#### 1.添加依赖
* requests
* lxml

#### 2.添加订阅
```shell
ql repo https://github.com/wenfer/scralib.git "scrapejob" "" "scrapes|translate|config|_scrape"

```


#### 3.配置环境变量
```shell
# 网络不通的话建议配个代理
export SCRALIB_USE_PROXY="true"
export SCRALIB_HTTP_PROXY="http://xxx:xxx@192.168.1.1:7890"
export SCRALIB_HTTPS_PROXY="http://xxx:xxx@192.168.1.1:7890"
# 最小文件大小，单位MB
export SCRALIB_MOVIE_MINSIZE=10
# 刮削源 目前实现的有javbus和jav321
export SCRALIB_SCRAPE_LIST=javbus:jav321

# 翻译引擎 
export SCRALIB_TRANSLATE_ENGINE="baidu"

# baidu的配置
export SCRALIB_BAIDU_API_KEY=""
export SCRALIB_BAIDU_APP_ID=""

# bing 配置
export SCRALIB_BING_API_ID=""
export SCRALIB_BING_API_KEY=""

# openai配置
export SCRALIB_OPENAI_API_URL=""
export SCRALIB_OPENAI_API_KEY=""
export SCRALIB_OPENAI_MODEL=""

# claude
export SCRALIB_CLAUDE_API_KEY=""


# 忽略的文件名  支持* 通配符
export SCRALIB_IGNORE=""

# 扫描目录
export SCRALIB_SCAN_DIR="/ql/media"

# 输出目录 不设置就会在扫描目录下生成一个【整理完成】的文件夹
export SCRALIB_MOVIE_TARGET_DIR=""
```