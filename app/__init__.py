from flask import Flask, request, render_template
from app.commands.import_users_command import import_users_command
from app.commands.import_csdn_users_command import import_csdn_users_command
from app.services.ip_limit_service import IpLimitService
from app.services.ip_service import IPService
from app.config.email_config import EMAIL_CONFIG

# 创建全局服务实例
ip_limit_service = IpLimitService()
ip_service = IPService()

def create_app():
    """
    创建并配置Flask应用
    """
    app = Flask(__name__)
    
    # 添加邮件配置
    app.config.update(EMAIL_CONFIG)

    # 注册CLI命令
    app.cli.add_command(import_users_command)
    app.cli.add_command(import_csdn_users_command)

    # 添加请求前处理函数，检查IP访问限制
    @app.before_request
    def check_ip_limit():
        # 获取客户端IP
        ip = ip_service.get_client_ip()
        print(ip)

        # 跳过静态文件请求
        if request.path.startswith('/static'):
            return None

        # 检查IP是否可以访问
        if not ip_limit_service.can_access(ip):
            remaining_visits = ip_limit_service.get_remaining_visits(ip)
            # 获取IP详细信息
            ip_info = ip_service.query_ip(ip)
            return render_template('error/too_many_requests.html', 
                                  remaining_visits=remaining_visits, 
                                  ip_address=ip,
                                  ip_info=ip_info), 429
            
        return None

    return app
