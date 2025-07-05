from app.models.user import User
from app.database import db_session
from typing import List, Dict
import os

def import_users_from_file(file_path: str) -> Dict[str, List[str]]:
    """
    从文本文件导入用户数据到数据库
    :param file_path: 用户数据文件的路径
    :return: 导入结果统计，包含成功和失败的用户列表
    """
    results = {
        'success': [],
        'failed': []
    }

    try:
        # 添加日志，10000条记录一次日志，并提交一次
        start = 137180000
        index = 0
        count = 20000
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    if index % count == 0:
                        print(f"当前进度: {index} success: {len(results['success']) }")

                    index += 1
                    if index < start:
                        continue

                    # 分割行数据
                    data = line.strip().split('---')
                    if len(data) != 7:
                        continue
                        # raise ValueError(f"Invalid data format: {line}")

                    full_name, username, password_hash, email, id_card, phone, backup_phone = data

                    # 处理特殊值 \N
                    id_card = None if id_card == '\\N' else id_card
                    phone = None if phone == '\\N' else phone
                    backup_phone = None if backup_phone == '\\N' else backup_phone

                    # 创建附加信息字典
                    additional_info = {}
                    if backup_phone:
                        additional_info['backup_phone'] = backup_phone

                    # 创建用户对象
                    user = User(
                        username=username,
                        password=None,  # 注意：这里直接使用hash值
                        email=email,
                        phone=phone,
                        id_card=id_card,
                        full_name=full_name,
                        additional_info=additional_info
                    )
                    if not user.phone:
                        continue
                    # # 检查用户是否已存在
                    existing_user = User.query.filter(
                        (User.phone == user.phone)
                    ).first()
                    #
                    if existing_user:
                        results['failed'].append(f"{username}  {email} {phone} (已存在)")
                        continue

                    # 保存到数据库
                    db_session.add(user)
                    results['success'].append(username)
                    if len(results['success']) > count:
                        # 提交一次
                        db_session.commit()
                        # 打印results信息 和 index，并清空 results
                        print(f"成功导入: {len(results['success'])} 个用户")
                        print(f"失败导入: {len(results['failed'])} 个用户")
                        print(results['failed'])
                        print(f"当前进度: {index}")
                        results = {
                            'success': [],
                            'failed': []
                            }

                except Exception as e:
                    db_session.rollback()
                    print(f"导入用户失败: {data[1] if len(data) > 1 else '未知'} ({str(e)})")
                    # results['failed'].append(f"{data[1] if len(data) > 1 else '未知'} ({str(e)})")
                    continue

            # 提交一次
            db_session.commit()
            # 打印results信息 和 index，并清空 results
            print(f"成功导入: {len(results['success'])} 个用户")
            print(f"失败导入: {len(results['failed'])} 个用户")

    except Exception as e:
        raise Exception(f"文件读取错误: {str(e)}")

    return results

def format_import_results(results: Dict[str, List[str]]) -> str:
    """
    格式化导入结果
    :param results: 导入结果字典
    :return: 格式化的结果字符串
    """
    output = []
    output.append("用户导入完成\n")
    output.append(f"成功导入: {len(results['success'])} 个用户")
    if results['success']:
        output.append("成功列表:")
        for username in results['success']:
            output.append(f"  - {username}")

    if results['failed']:
        output.append(f"\n导入失败: {len(results['failed'])} 个用户")
        output.append("失败列表:")
        for fail_info in results['failed']:
            output.append(f"  - {fail_info}")

    return "\n".join(output)

def import_users_from_static():
    """
    从static目录导入用户数据的便捷方法
    """
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, 'static', 'jdcominfo12g.txt')

    try:
        results = import_users_from_file(file_path)
        return format_import_results(results)
    except Exception as e:
        return f"导入失败: {str(e)}"

if __name__ == '__main__':
    print(import_users_from_static())