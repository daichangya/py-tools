from flask import Blueprint, render_template, request, flash
from app.services.express_service import ExpressService

class Plugin:
    """快递查询插件"""
    def __init__(self):
        self.title = "快递查询"
        self.description = "查询快递物流信息"
        self.blueprint = Blueprint('express', __name__, template_folder='../templates')
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/express', methods=['GET', 'POST'])
        def express_query():
            result = None
            if request.method == 'POST':
                express_no = request.form.get('express_no', '').strip()
                if express_no:
                    result = ExpressService.query_express(express_no)
                    if not result:
                        flash('未找到快递信息或查询失败', 'danger')
                else:
                    flash('请输入快递单号', 'danger')
            return render_template('plugins/express.html', result=result)
