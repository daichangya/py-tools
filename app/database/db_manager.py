#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config.database import DATABASE_URL

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # 允许在多线程中使用同一个连接
    echo=False  # 设置为True可以看到SQL语句
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建线程安全的会话
db_session = scoped_session(SessionLocal)

# 创建基类
Base = declarative_base()
Base.query = db_session.query_property()

def get_db():
    """获取数据库会话"""
    db = db_session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库"""
    # 导入所有模型，确保它们在创建表之前被定义
    from .. import models

    # 创建所有表
    Base.metadata.create_all(bind=engine)
