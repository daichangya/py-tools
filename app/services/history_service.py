import json
import os
import datetime
from typing import List, Dict

class HistoryService:
    """历史上的今天服务"""

    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'BaiduJson')

    def get_events_by_date(self, month: int = None, day: int = None) -> List[Dict]:
        """
        获取指定日期的历史事件
        
        Args:
            month: 月份 (1-12)，默认为当前月
            day: 日期，默认为当天
            
        Returns:
            List[Dict]: 历史事件列表，每个事件包含year和event字段
        """
        try:
            # 如果没有提供日期，使用当天
            today = datetime.datetime.now()
            month = month or today.month
            day = day or today.day

            # 读取对应月份文件
            file_path = os.path.join(self.base_path, f"{month}月.json")

            with open(file_path, 'r', encoding='utf-8') as f:
                month_data = json.load(f)
                # 月份 天 补足两位
                month = f"{month:0>2}"
                day = f"{day:0>2}"
                month_data = month_data[month]
                # 查找当天事件
                daily_events = month_data[month+day]
                return daily_events

        except Exception as e:
            print(f"读取历史数据失败: {str(e)}")
            return []

    def get_today_events(self) -> List[Dict]:
        """获取今天的历史事件(快捷方法)"""
        return self.get_events_by_date()

