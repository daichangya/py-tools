# Copyright 2022 The Ip2Region Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#

from app.utils import XdbSearcher
import os

def searchWithFile():
    # 1. 创建查询对象
    project_root = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(project_root, 'static', 'ip2region.xdb')
    
    # 2. 执行查询
    ip = "1.2.3.4"
    region_str = searcher.searchByIPStr(ip)
    print(region_str)
    
    # 3. 关闭searcher
    searcher.close()

def searchWithVectorIndex():
     # 1. 预先加载整个 xdb
    project_root = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(project_root, 'static', 'ip2region.xdb')

    # 2. 使用上面的缓存创建查询对象, 同时也要加载 xdb 文件
    searcher = XdbSearcher(dbfile=dbPath, vectorIndex=vi)
    
    # 3. 执行查询
    ip = "1.2.3.4"
    region_str = searcher.search(ip)
    print(region_str)

    # 4. 关闭searcher
    searcher.close()
    
def searchWithContent():
    # 1. 预先加载整个 xdb
    project_root = os.path.dirname(os.path.abspath(__file__))
    dbPath = os.path.join(project_root, 'static', 'ip2region.xdb')
    cb = XdbSearcher.loadContentFromFile(dbfile=dbPath)
    
    # 2. 仅需要使用上面的全文件缓存创建查询对象, 不需要传源 xdb 文件
    searcher = XdbSearcher(contentBuff=cb)
    
    # 3. 执行查询
    ip = "1.2.3.4"
    region_str = searcher.search(ip)
    print(region_str)

    # 4. 关闭searcher
    searcher.close()
    
    
if __name__ == '__main__':
    searchWithContent()
    
