from flask import Blueprint, request, jsonify, current_app, render_template
import os
from typing import Dict, Any, List, Optional
import logging
from app.services.email_service import EmailService

# 创建日志记录器
logger = logging.getLogger(__name__)


# 插件类定义
class Plugin:
    def __init__(self):
        self.title = "邮件工具"
        self.description = "发送邮件、验证邮箱地址等功能"
        # 创建蓝图
        self.blueprint = Blueprint('email', __name__, url_prefix='/email' ,template_folder='../templates')
        self._register_routes()

    def _register_routes(self):
        # 路由：邮件工具首页
        @self.blueprint.route('/', methods=['GET'])
        def index():
            return render_template('plugins/email.html')

        # 路由：发送邮件
        @self.blueprint.route('/send', methods=['POST'])
        def send_email():
            try:
                data = request.json

                # 获取SMTP配置
                smtp_server = data.get('smtp_server')
                smtp_port = int(data.get('smtp_port', 587))
                username = data.get('username')
                password = data.get('password')

                # 获取邮件内容
                to_emails = data.get('to_emails', [])
                if isinstance(to_emails, str):
                    to_emails = [email.strip() for email in to_emails.split(',')]

                cc_emails = data.get('cc_emails', [])
                if isinstance(cc_emails, str):
                    cc_emails = [email.strip() for email in cc_emails.split(',')]

                bcc_emails = data.get('bcc_emails', [])
                if isinstance(bcc_emails, str):
                    bcc_emails = [email.strip() for email in bcc_emails.split(',')]

                subject = data.get('subject', '')
                body = data.get('body', '')
                is_html = data.get('is_html', False)
                send_individually = data.get('send_individually', False)

                # 验证必填字段
                if not all([smtp_server, username, password, to_emails, subject, body]):
                    return jsonify({
                        "success": False,
                        "message": "缺少必要参数，请检查SMTP配置和邮件内容"
                    }), 400

                # 创建邮件服务并发送邮件
                email_service = EmailService(smtp_server, smtp_port, username, password)
                result = email_service.send_email(
                    to_emails=to_emails,
                    subject=subject,
                    body=body,
                    cc_emails=cc_emails,
                    bcc_emails=bcc_emails,
                    is_html=is_html,
                    send_individually=send_individually
                )

                if result["success"]:
                    return jsonify(result), 200
                else:
                    return jsonify(result), 500

            except Exception as e:
                error_msg = f"发送邮件时出错: {str(e)}"
                logger.error(error_msg)
                return jsonify({"success": False, "message": error_msg}), 500

        # 路由：验证邮箱
        @self.blueprint.route('/validate', methods=['POST'])
        def validate_email():
            try:
                data = request.json
                email = data.get('email', '')

                if not email:
                    return jsonify({
                        "success": False,
                        "message": "请提供邮箱地址"
                    }), 400

                # 创建邮件服务并验证邮箱
                email_service = EmailService("", 0, "", "")  # 验证邮箱不需要SMTP配置
                is_valid = email_service.validate_email(email)

                return jsonify({
                    "success": True,
                    "is_valid": is_valid,
                    "message": "邮箱格式正确" if is_valid else "邮箱格式不正确"
                }), 200

            except Exception as e:
                error_msg = f"验证邮箱时出错: {str(e)}"
                logger.error(error_msg)
                return jsonify({"success": False, "message": error_msg}), 500
