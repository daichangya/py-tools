#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent.parent

# 数据库配置
DATABASE = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    }
}

# 数据库连接字符串
DATABASE_URL = f"sqlite:///{os.path.join(ROOT_DIR, 'db.sqlite3')}"
