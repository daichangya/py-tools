from flask import request
from app.utils.ip_utils import ip_utils

class IPService():
    """IP信息服务"""

    @staticmethod
    def get_client_ip() -> str:
        """获取客户端真实IP"""
        # 处理代理服务器情况
        if 'X-Forwarded-For' in request.headers:
            ips = request.headers['X-Forwarded-For'].split(',')
            return ips[0].strip()
        return request.remote_addr

    @staticmethod
    def query_ip(ip: str) -> dict:
        """查询IP信息

        Args:
            ip: IP地址字符串

        Returns:
            包含IP信息的字典或None
        """
        try:
            # 验证IP格式
            if not ip_utils.is_valid_ip(ip):
                return None

            # 查询IP信息
            result = ip_utils.search(ip)
            if not result:
                return None

            # 添加IP地址到结果中
            result['ip'] = ip
            return result

        except Exception:
            return None
