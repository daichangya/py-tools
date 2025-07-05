import os
import socket
from typing import Dict, Optional
from threading import Lock
from app.utils.xdbSearcher import XdbSearcher

class Ip2Region:
    """IP地址查询工具类"""

    def __init__(self, db_path: str = None):
        """初始化IP2Region查询对象

        Args:
            db_path: xdb文件路径，默认为static/ip2region.xdb
        """
        if db_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(project_root,'static', 'ip2region.xdb')

        self.db_path = db_path
        self.searcher = None
        self._cache = {}
        self._lock = Lock()

        # 加载数据文件
        self._init_searcher()

    def _init_searcher(self):
        """初始化搜索器"""
        try:
            # 检查文件是否存在
            if not os.path.exists(self.db_path):
                raise FileNotFoundError(f"xdb file not found: {self.db_path}")

            # 初始化搜索器
            self.searcher = XdbSearcher(dbfile=self.db_path)
        except Exception as e:
            raise RuntimeError(f"failed to initialize ip2region: {e}")

    def search(self, ip: str) -> Dict[str, str]:
        """查询IP地址信息

        Args:
            ip: IP地址字符串

        Returns:
            包含地区信息的字典:
            - country: 国家
            - region: 区域
            - province: 省份
            - city: 城市
            - isp: 运营商
            - asn: 自治系统号
            - timezone: 时区
        """
        # 检查缓存
        with self._lock:
            if ip in self._cache:
                return self._cache[ip]

        # 验证IP格式
        if not self.is_valid_ip(ip):
            return self._unknown_result()

        try:
            # 查询地区信息
            region_str = self.searcher.search(ip)
            if not region_str:
                return self._unknown_result()

            # 解析地区信息
            parts = region_str.split('|')
            result = {
                'country': parts[0] if len(parts) > 0 else '未知',
                'region': parts[1] if len(parts) > 1 else '未知',
                'province': parts[2] if len(parts) > 2 else '未知',
                'city': parts[3] if len(parts) > 3 else '未知',
                'isp': parts[4] if len(parts) > 4 else '未知',
                'asn': '未知',
                'timezone': '未知'
            }

            # 更新缓存
            with self._lock:
                self._cache[ip] = result

            return result
        except Exception:
            return self._unknown_result()

    def _unknown_result(self) -> Dict[str, str]:
        """返回未知结果"""
        return {
            'country': '未知',
            'region': '未知',
            'province': '未知',
            'city': '未知',
            'isp': '未知',
            'asn': '未知',
            'timezone': '未知'
        }

    def is_valid_ip(self, ip: str) -> bool:
        """验证IP地址格式是否有效

        Args:
            ip: IP地址字符串

        Returns:
            True表示有效，False表示无效
        """
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def close(self):
        """关闭搜索器"""
        if self.searcher:
            self.searcher.close()
        self.searcher = None

    def __del__(self):
        """析构函数"""
        self.close()

# 创建单例实例
ip_utils = Ip2Region()


if __name__ == '__main__':
    # 使用示例
    ip_util = ip_utils
    if ip_util:
        test_ips = [
            '1.1.1.1',
            '114.114.114.114',
            '223.5.5.5',
            '8.8.8.8'
        ]

        for ip in test_ips:
            try:
                result = ip_util.search(ip)
                print(f"\nIP: {ip}")
                for key, value in result.items():
                    print(f"{key}: {value}")
            except Exception as e:
                print(f"查询IP {ip} 失败: {e}")
        ip_util.close()
