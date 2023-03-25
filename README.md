# ESG报告爬虫说明文档

## 简介  

本爬虫程序是用于爬取巨潮网、上交所官网和深交所官网的ESG报告及相关信息的Python程序。本程序可以在指定时间范围内收集报告的基本信息，包括标题、发布日期、PDF的URL以及来源网站。本文档将提供有关程序的基本信息，如运行环境、使用方法和参数选项等。

## 资源  

目前已经获得巨潮网、上交所官网和深交所官网的ESG报告以及相关信息(京交所的相关报告数量过少没有爬取)。采用精确搜索字符串 **“环境、社会及”** *(最后一个关键词表述不一致，不做限制以获取更多篇目)* 的方式，经过文章去重（以MD5码为基准）后，得到近5000篇精选文本。

## 运行环境

本程序需要`Python 3.9`版本。运行程序之前，请确保已安装以下`Python`库：

- `requests==2.28.1`

- 使用以下命令安装：

```Python
pip install -r requirements.txt
```  

## 构成

- `get_data.py`：是爬虫的运行接口，调用其他库文件。使用时应与所有库文件在同一目录下。
- `cninfo.py`：针对巨潮网的爬取方法。
- `shse.py`：针对上交所官网的爬取方法。
- `szse.py`：针对深交所官网的爬取方法。

## 功能及使用方法

使用前请确保已经安装上述库文件，并保证它们在同一目录下。运行以下命令以了解命令行参数的使用方法：

```Pyhon
python get_data.py -h
```

命令行参数如下：

- `-src SRC 或 -s SRC`：信息来源。可选项包括：1（巨潮网）、2（上交所）、3（深交所）或0（所有）。默认值为0。
- `-date DATE 或 -d DATE`：日期范围。需要输入形如2021-01-23的日期字符串，表示从特定网站筛选报告的发布时间满足：[该指定日期,程序运行时刻的日期]，并将它们更新到本地。默认为不加时间限制。
- `-path PATH 或 -p PATH`：JSON文件的下载路径。必需项，没有默认值。

运行以下命令以启动程序：

```Python
python get_data.py --src SRC --date DATE --path PATH
```

注意：这里的`SRC`、`DATE`和`PATH`分别指用户提供的参数值。

本爬虫程序会以`JSON`文件的形式收集每篇报告的基本信息，包括标题、发布日期、报告的`URL`以及来源网站。具体地，该`JSON`由若干个字典组成的列表构成。每个字典形如：`{'title': title, 'url': pdf_url,'publishdate': date_str,'src':source}`。
