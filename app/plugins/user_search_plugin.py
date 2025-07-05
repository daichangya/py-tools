from flask import Blueprint, render_template, request, jsonify
from app.services.user_service import UserService

class Plugin:
    def __init__(self):
        self.blueprint = Blueprint('user_search', __name__, url_prefix='/user_search')
        self.title = "社工库查询"
        self.description = "通过用户名、邮箱、手机号或身份证号查询用户信息"
        self.user_service = UserService()

        @self.blueprint.route('/', methods=['GET'])
        def index():
            return render_template('plugins/user_search.html')

        @self.blueprint.route('/search', methods=['POST'])
        def search():
            query = request.form.get('query', '').strip()
            if not query:
                return jsonify({'error': '请输入查询内容'})

            results = []
            # 使用所有可用的查询方法
            # results.extend(self.user_service.get_user_by_username(query) or [])
            # results.extend(self.user_service.get_user_by_email(query) or [])
            results.extend(self.user_service.get_user_by_phone(query) or [])
            # results.extend(self.user_service.get_user_by_full_name(query) or [])
            # results.extend(self.user_service.get_user_by_id_card(query) or [])

            # 去重
            unique_results = []
            seen_ids = set()
            for user in results:
                if user.id not in seen_ids:
                    seen_ids.add(user.id)
                    unique_results.append({
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'phone': user.phone,
                        'full_name': user.full_name,
                        'id_card': user.id_card,
                        'address': user.get_additional_info('address', ''),
                        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None
                    })

            return jsonify({
                'success': True,
                'results': unique_results
            })
