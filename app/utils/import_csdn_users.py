from app.models.user import User
from app.database import db_session
from typing import List, Dict
import os

def import_users_from_csdn_file(file_path: str) -> Dict[str, List[str]]:
    """
    从CSDN CSV文件导入用户数据到数据库
    :param file_path: CSDN用户数据文件的路径
    :return: 导入结果统计，包含成功和失败的用户列表
    """
    results = {
        'success': [],
        'failed': []
    }

    try:
        # 添加日志，1000条记录一次日志，并提交一次
        index = 0
        batch_size = 1000
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    if index % batch_size == 0:
                        print(f"当前进度: {index} success: {len(results['success'])}")

                    index += 1

                    # 分割行数据 (格式: username # password # email)
                    line = line.strip()
                    if not line:
                        continue

                    data = line.split(' # ')
                    if len(data) != 3:
                        results['failed'].append(f"格式错误: {line}")
                        continue

                    username, password, email = data

                    # 创建用户对象
                    user = User(
                        username=username,
                        password=password,  # 直接使用密码
                        email=email,
                        phone=None,
                        id_card=None,
                        full_name=None,
                        additional_info={"source": "csdn"}
                    )

                    # 检查用户是否已存在
                    existing_user = User.query.filter(
                        (User.username == username) | (User.email == email)
                    ).first()

                    if existing_user:
                        results['failed'].append(f"{username} (已存在)")
                        continue

                    # 保存到数据库
                    db_session.add(user)
                    results['success'].append(username)

                    # 每批次提交一次
                    if len(results['success']) % batch_size == 0:
                        db_session.commit()
                        print(f"成功导入: {len(results['success'])} 个用户")
                        print(f"失败导入: {len(results['failed'])} 个用户")

                except Exception as e:
                    db_session.rollback()
                    print(f"导入用户失败: {line} ({str(e)})")
                    results['failed'].append(f"{line} ({str(e)})")
                    continue

            # 最后提交一次
            db_session.commit()
            print(f"成功导入: {len(results['success'])} 个用户")
            print(f"失败导入: {len(results['failed'])} 个用户")

    except Exception as e:
        db_session.rollback()
        raise Exception(f"文件读取错误: {str(e)}")

    return results

def format_import_results(results: Dict[str, List[str]]) -> str:
    """
    格式化导入结果
    :param results: 导入结果字典
    :return: 格式化的结果字符串
    """
    output = []
    output.append("CSDN用户导入完成\n")
    output.append(f"成功导入: {len(results['success'])} 个用户")

    if results['failed']:
        output.append(f"\n导入失败: {len(results['failed'])} 个用户")
        if len(results['failed']) <= 10:
            output.append("失败列表:")
            for fail_info in results['failed']:
                output.append(f"  - {fail_info}")
        else:
            output.append(f"失败列表过长，仅显示前10条:")
            for fail_info in results['failed'][:10]:
                output.append(f"  - {fail_info}")

    return "\n".join(output)

def import_csdn_users():
    """
    从static目录导入CSDN用户数据的便捷方法
    """
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, 'static', 'csdn.csv')

    try:
        results = import_users_from_csdn_file(file_path)
        return format_import_results(results)
    except Exception as e:
        return f"导入失败: {str(e)}"

if __name__ == '__main__':
    print(import_csdn_users())
