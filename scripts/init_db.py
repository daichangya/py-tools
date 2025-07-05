#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db
from app.services.user_service import UserService

def init_database():
    """初始化数据库"""
    print("正在初始化数据库...")

    # 创建数据库表
    init_db()
    print("数据库表创建完成")

    # 创建测试用户
    try:
        test_user = UserService.create_user(
            username="admin",
            password="admin123",
            email="admin@example.com",
            full_name="Administrator"
        )
        print(f"测试用户创建成功: {test_user.username}")
    except ValueError as e:
        print(f"测试用户已存在: {e}")
    except Exception as e:
        print(f"创建测试用户时出错: {e}")

def main():
    """主函数"""
    try:
        init_database()
        print("数据库初始化完成")
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
