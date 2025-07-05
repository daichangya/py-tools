#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from tabulate import tabulate

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.user_service import UserService
from app.database import init_db
from app.utils.import_users import import_users_from_file, import_users_from_static, format_import_results

def init_database():
    """初始化数据库"""
    try:
        init_db()
        print("数据库初始化成功")
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)

def list_users(args):
    """列出所有用户"""
    try:
        users = UserService.get_all_users()[:10]  # Get first 10 users
        if not users:
            print("没有找到任何用户")
            return

        # 准备表格数据
        headers = ["ID", "用户名", "邮箱","手机号","身份证", "全名","其他信息", "状态", "创建时间"]
        rows = []
        for user in users:
            rows.append([
                user.id,
                user.username,
                user.email,
                user.phone or "-",
                user.id_card or "-",
                user.full_name or "-",
                user.additional_info or "-",
                "激活" if user.is_active else "禁用",
                user.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

        # 打印表格
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    except Exception as e:
        print(f"列出用户失败: {e}")

def get_user(args):
    """获取用户信息"""
    try:
        users = None
        if args.id:
            users = UserService.get_user_by_id(args.id)
        elif args.username:
            users = UserService.get_user_by_username(args.username)
        elif args.email:
            users = UserService.get_user_by_email(args.email)
        else:
            print("请提供用户ID、用户名或邮箱")
            return

        if not users:
            print("未找到用户")
            return
        user = users[0]
        # 打印用户信息
        print("\n用户信息:")
        print(f"ID: {user.id}")
        print(f"用户名: {user.username}")
        print(f"邮箱: {user.email}")
        print(f"全名: {user.full_name or '-'}")
        print(f"状态: {'激活' if user.is_active else '禁用'}")
        print(f"创建时间: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"更新时间: {user.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"获取用户信息失败: {e}")

def create_user(args):
    """创建新用户"""
    try:
        user = UserService.create_user(
            username=args.username,
            password=args.password,
            email=args.email,
            full_name=args.full_name
        )
        print(f"用户创建成功: {user.username} (ID: {user.id})")
    except Exception as e:
        print(f"创建用户失败: {e}")

def update_user(args):
    """更新用户信息"""
    try:
        # 构建更新字段
        update_fields = {}
        if args.email:
            update_fields['email'] = args.email
        if args.full_name:
            update_fields['full_name'] = args.full_name
        if args.password:
            update_fields['password'] = args.password
        if args.active is not None:
            update_fields['is_active'] = args.active

        if not update_fields:
            print("没有提供要更新的字段")
            return

        # 更新用户
        user = UserService.update_user(args.id, **update_fields)
        if user:
            print(f"用户 {user.username} 更新成功")
        else:
            print(f"未找到ID为 {args.id} 的用户")
    except Exception as e:
        print(f"更新用户失败: {e}")

def delete_user(args):
    """删除用户"""
    try:
        result = UserService.delete_user(args.id)
        if result:
            print(f"用户 ID: {args.id} 删除成功")
        else:
            print(f"未找到ID为 {args.id} 的用户")
    except Exception as e:
        print(f"删除用户失败: {e}")

def authenticate(args):
    """验证用户凭据"""
    try:
        user = UserService.authenticate_user(args.username, args.password)
        if user:
            print(f"认证成功: {user.username} (ID: {user.id})")
        else:
            print("认证失败: 用户名或密码错误")
    except Exception as e:
        print(f"认证失败: {e}")

def import_users(args):
    """从文件导入用户"""
    try:
        result = import_users_from_static()

        # if args.file == 'default':
        #     result = import_users_from_static()
        #     print(result)
        # else:
        #     results = import_users_from_file(args.file)
        #     print(format_import_results(results))
    except Exception as e:
        print(f"导入用户失败: {e}")

def count_users(args):
    """获取用户总数"""
    try:
        count = UserService.count_users()
        print(f"用户总数: {count}")
    except Exception as e:
        print(f"获取用户数量失败: {e}")

def main():
    """主函数"""
    # 初始化数据库
    init_database()

    # 创建命令行解析器
    parser = argparse.ArgumentParser(description="用户管理命令行工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 列出所有用户
    list_parser = subparsers.add_parser("list", help="列出所有用户")

    # 获取用户信息
    get_parser = subparsers.add_parser("get", help="获取用户信息")
    get_parser.add_argument("--id", type=int, help="用户ID")
    get_parser.add_argument("--username", help="用户名")
    get_parser.add_argument("--email", help="邮箱")

    # 创建用户
    create_parser = subparsers.add_parser("create", help="创建新用户")
    create_parser.add_argument("--username", required=True, help="用户名")
    create_parser.add_argument("--password", required=True, help="密码")
    create_parser.add_argument("--email", required=True, help="邮箱")
    create_parser.add_argument("--full-name", help="全名")

    # 更新用户
    update_parser = subparsers.add_parser("update", help="更新用户信息")
    update_parser.add_argument("--id", type=int, required=True, help="用户ID")
    update_parser.add_argument("--email", help="新邮箱")
    update_parser.add_argument("--full-name", help="新全名")
    update_parser.add_argument("--password", help="新密码")
    update_parser.add_argument("--active", type=bool, help="是否激活")

    # 删除用户
    delete_parser = subparsers.add_parser("delete", help="删除用户")
    delete_parser.add_argument("--id", type=int, required=True, help="用户ID")

    # 认证用户
    auth_parser = subparsers.add_parser("auth", help="验证用户凭据")
    auth_parser.add_argument("--username", required=True, help="用户名")
    auth_parser.add_argument("--password", required=True, help="密码")
    
    # 导入用户
    import_parser = subparsers.add_parser("import", help="从文件导入用户")
    import_parser.add_argument("--file", default="default", help="用户数据文件路径（使用default表示从static/userinfo.txt导入）")
    
    # 获取用户总数
    count_parser = subparsers.add_parser("count", help="获取用户总数")

    # 解析命令行参数
    args = parser.parse_args()

    # 执行对应的命令
    if args.command == "list":
        list_users(args)
    elif args.command == "get":
        get_user(args)
    elif args.command == "create":
        create_user(args)
    elif args.command == "update":
        update_user(args)
    elif args.command == "delete":
        delete_user(args)
    elif args.command == "auth":
        authenticate(args)
    elif args.command == "import":
        import_users(args)
    elif args.command == "count":
        count_users(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
    # import_users(None)
