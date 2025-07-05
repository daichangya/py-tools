from flask import Blueprint, render_template, request, flash
from app.services.ip_service import IPService
from app.utils.ip_utils import ip_utils

class Plugin:
    """IP查询插件"""
    def __init__(self):
        self.title = "IP查询"
        self.description = "查询IP地址的地理位置"
        self.blueprint = Blueprint('ip', __name__, template_folder='../templates')
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/ip', methods=['GET', 'POST'])
        def ip_query():
            result = None
            if request.method == 'POST':
                ip_address = request.form.get('ip_address', '').strip()
                if ip_address:
                    result = IPService.query_ip(ip_address)
                    if not result:
                        flash('IP查询失败', 'danger')
                else:
                    # 查询本机IP
                    client_ip = IPService.get_client_ip()
                    result = IPService.query_ip(client_ip)

            return render_template('plugins/ip.html', result=result)

    def __del__(self):
        """清理资源"""
        if hasattr(self, 'ip_utils') and ip_utils:
            ip_utils.close()
