#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:jack
# datetime:2019-04-01 12:37
# software: PyCharm


import importlib
import sys
from urllib.request import urlopen
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


'''
    url_path :需要访问的url
    result_path:保存结果的文件路径及文件名
    sensitive_words：敏感词数组
    '''


def parse(url_path, result_path, sensitive_words):

    '''解析PDF文本，（表格并不能完全解析）命中敏感词将保持到result_path中'''
    print(url_path)
    if r'://' in url_path:
        fp = urlopen(url_path)
    else:
        fp = open(url_path)
    # fp = open(url_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    check_raw = x.get_text()
                # print(check_raw)
                for word in sensitive_words:
                    if word in check_raw:
                        with open(result_path, 'a') as f:
                            print('Hit the sensitive word! url:'+url_path)
                            f.write(word + '------' + url_path + "\n")
                            return
                    else:
                        pass
                else:
                    pass





if __name__ == '__main__':
    parse('http://math.ecnu.edu.cn/~latex/docs/packages/fancyhdr_chs.pdf',
        r'./a.txt', ['升级'])

