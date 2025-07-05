from flask import Blueprint, render_template, request, jsonify
from app.services.greeting_card_service import GreetingCardService

class Plugin:
    """贺卡生成插件"""
    def __init__(self):
        self.title = "贺卡生成"
        self.description = "生成节日贺卡"
        self.blueprint = Blueprint('greeting_card', __name__, template_folder='../templates')
        self.service = GreetingCardService()
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/greeting_card', methods=['GET'])
        def greeting_card():
            festivals = self.service.get_all_festivals()
            festival = self.service.get_next_festival()
            return render_template('plugins/greeting_card.html', festivals=festivals,festival= festival)

        @self.blueprint.route('/greeting_card/generate', methods=['POST'])
        def generate_greeting():
            data = request.get_json()
            festival = data.get('festival')
            sender = data.get('sender')
            receiver = data.get('receiver')
            
            if not all([festival, sender, receiver]):
                return jsonify({
                    'success': False,
                    'message': '请填写完整信息'
                }), 400
            
            card_data = self.service.generate_greeting_card(festival, sender, receiver)
            
            if not card_data:
                return jsonify({
                    'success': False,
                    'message': '生成贺卡失败，请重试'
                }), 500
            
            return jsonify({
                'success': True,
                'data': card_data
            })