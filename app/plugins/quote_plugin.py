from flask import Blueprint, render_template
from app.services.quote_service import QuoteService

class Plugin:
    """每日一言插件(本地数据版)"""
    def __init__(self):
        self.title = "每日一言"
        self.description = "展示每日一句名言警句"
        self.blueprint = Blueprint('quote', __name__, url_prefix='/quote', template_folder='../templates')
        self.quote_service = QuoteService()
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/')
        def index():
            """每日一言页面"""
            quote_data = self.quote_service.get_quote()
            return render_template('plugins/quote.html', quote=quote_data)
