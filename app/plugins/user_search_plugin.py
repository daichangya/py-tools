from flask import Blueprint, render_template, request, jsonify
from app.services.user_service import UserService
import random

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
            
        @self.blueprint.route('/random_emails', methods=['GET'])
        def random_emails():
            """随机提取100个用户的邮箱信息"""
            try:
                # 直接在数据库层面随机选择100个用户，避免加载所有用户数据
                from app.models.user import User
                from sqlalchemy.sql.expression import func
                from app.database.db_manager import db_session
                
                # 获取用户总数
                total_users = 50000000
                
                # 确定要获取的用户数量
                limit = min(100, total_users)

                # 如果上述方法都失败，使用备用方法
                # 获取一个随机偏移量
                if total_users > limit:
                    offset = random.randint(0, total_users - limit)
                    random_users = db_session.query(User).filter(User.email != None).offset(offset).limit(limit).all()
                else:
                    random_users = db_session.query(User).filter(User.email != None).limit(limit).all()
                
                # 提取邮箱信息
                email_list = [
                    {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username
                    }
                    for user in random_users if user.email
                ]
                
                return jsonify({
                    'success': True,
                    'count': len(email_list),
                    'emails': email_list
                })
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                return jsonify({
                    'success': False,
                    'error': f"获取随机邮箱失败: {str(e)}",
                    'details': error_details
                }), 500
