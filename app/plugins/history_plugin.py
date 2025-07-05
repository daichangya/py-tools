from flask import Blueprint, render_template
import datetime
from flask import request
from app.services.history_service import HistoryService

class Plugin:
    """历史上的今天插件"""
    def __init__(self):
        self.title = "历史上的今天"
        self.description = "展示历史上今天发生的重要事件"
        self.blueprint = Blueprint('history', __name__,  template_folder='../templates')
        self.history_service = HistoryService()
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/history')
        def index():
            """历史事件页面"""

            try:
                date_str = request.args.get('date')
                if date_str:
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    month = date_obj.month
                    day = date_obj.day
                    events = self.history_service.get_events_by_date(month, day)
                    query_date = f"{month}月{day}日"
                else:
                    events = self.history_service.get_today_events()
                    query_date = None
            except (ValueError, TypeError):
                events = self.history_service.get_today_events()
                query_date = None
                
            now = datetime.datetime.now()
            today = now.strftime('%Y-%m-%d')
            display_date = now.strftime('%m月%d日') if query_date is None else query_date
            return render_template('plugins/history.html', 
                                events=events,
                                query_date=query_date,
                                today=today,
                                display_date=display_date)

