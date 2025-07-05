from flask import Blueprint, render_template, request, flash
from app.services.identity_service import IdentityService

class Plugin:
    """身份证查询插件"""
    def __init__(self):
        self.title = "身份证查询"
        self.description = "验证身份证号码的有效性并解析信息"
        self.blueprint = Blueprint('identity', __name__, template_folder='../templates')
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/identity', methods=['GET', 'POST'])
        def identity_check():
            result = None
            if request.method == 'POST':
                id_number = request.form.get('id_number', '').strip()
                if IdentityService.validate_id(id_number):
                    result = IdentityService.parse_id(id_number)
                else:
                    flash('无效的身份证号码，请检查号码格式和校验位', 'danger')
            return render_template('plugins/identity.html', result=result)
