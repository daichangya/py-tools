from datetime import datetime, timedelta
from typing import Dict, Tuple

class IpLimitService:
    def __init__(self):
        # 存储格式: {ip: (访问次数, 最后访问日期)}
        self._ip_records: Dict[str, Tuple[int, datetime]] = {}
        self.max_visits = 100

    def can_access(self, ip: str) -> bool:
        """
        检查IP是否可以访问
        :param ip: 访问者IP
        :return: 是否允许访问
        """
        now = datetime.now()

        # 如果IP不在记录中，添加记录并允许访问
        if ip not in self._ip_records:
            self._ip_records[ip] = (1, now)
            return True

        visits, last_visit = self._ip_records[ip]

        # 如果是新的一天，重置计数
        if last_visit.date() < now.date():
            self._ip_records[ip] = (1, now)
            return True

        # 如果是同一天，检查访问次数
        if visits >= self.max_visits:
            return False

        # 更新访问记录
        self._ip_records[ip] = (visits + 1, now)
        print(self._ip_records)
        return True

    def get_remaining_visits(self, ip: str) -> int:
        """
        获取IP今天剩余的访问次数
        :param ip: 访问者IP
        :return: 剩余访问次数
        """
        if ip not in self._ip_records:
            return self.max_visits

        visits, last_visit = self._ip_records[ip]

        # 如果是新的一天，返回最大访问次数
        if last_visit.date() < datetime.now().date():
            return self.max_visits

        return max(0, self.max_visits - visits)
