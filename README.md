# README

## 资源  

- 目前已经获得巨潮网、上交所官网和深交所官网的ESG报告以及相关信息(京交所的相关报告数量过少没有爬取)。采用精确搜索字符串 **“环境、社会及”** *(最后一个关键词表述不一致，不做限制以获取更多篇目)* 的方式，得到6000+篇。后续可以纳入更多的网站或优化搜索细节以丰富资源。

## 构成

- `get_data.py` 是爬虫的运行接口，调用其他库文件，使用时应与所有库文件在同一目录下。每个库文件是针对不同网页的爬取方法。

## 功能及使用方法

- 使用前在项目根目录输入 `pip install -r requirements.txt` 获得该项目依赖的非python内置库（srds这里只有一个库）

- 该爬虫程序会以 `json` 文件的形式收集每篇报告的基本信息，包括标题、发布日期、`pdf` 的 `url` 以及来源网站。具体地，该 `json` 若干个字典组成的列表。每个字典形如：`{'title': title, 'url': pdf_url,'publishdate': date_str,'src':source}`
- 在当前目录下运行 `python get_data.py -h` 可以得到详细的命令行参数使用说明。支持选择文章的网页来源（可选）、日期范围（可选）和 `json` 的下载路径（必选）:

```Python
参数选项:
  -h, --help            帮助信息
  --src SRC, -s SRC     信息来源，包括 1:cninfo(巨潮网), 2: shse(上交所), 3:szse(深交所), 0:all above. 使用时输入冒号前的编号即可，默认值为0
  --date DATE, -d DATE  需要输入如：2021-01-23 格式的日期字符串，表示从特定网站筛选报告的发布时间满足：[该指定日期,程序运行时刻的日期]，并将它们更新到本地。默认为不加时间限制。
  --path PATH, -p PATH  生成json文件的下载位置。无默认值，这是必需项。

  使用样例：python get_data.py -s 0 -d 2021-09-13  -p XXXXX

```
