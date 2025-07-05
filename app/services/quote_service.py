import json
import random
import os
from typing import Dict, Optional

class QuoteService:
    """本地每日一言服务"""

    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'quote')

    def get_quote(self) -> Optional[Dict]:
        """
        从本地JSON文件随机获取一条名言

        Returns:
            Dict: 包含content, author, category字段
            None: 如果读取失败
        """
        try:
            # 随机选择一个字母文件
            letter = random.choice('abcdefghijkl')
            file_path = os.path.join(self.base_path, 'sentences', f'{letter}.json')

            with open(file_path, 'r', encoding='utf-8') as f:
                quotes = json.load(f)
                quote = random.choice(quotes)

                # 读取分类信息
                with open(os.path.join(self.base_path, 'categories.json'), 'r', encoding='utf-8') as cf:
                    categories = json.load(cf)

                categorie_map = {categorie["key"]: categorie for categorie in categories}
                return {
                    'content': quote['hitokoto'],
                    'author': quote['creator'],
                    'category': categorie_map.get(quote['type'])['name']
                }

        except Exception as e:
            print(f"读取本地名言失败: {str(e)}")
            return None
