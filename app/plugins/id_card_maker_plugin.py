from flask import Blueprint, render_template, request, jsonify, current_app
import os
from app.services.id_card_maker_service import IdCardMakerService

class Plugin:
    """身份证制作插件"""

    def __init__(self):
        self.title = "身份证制作"
        self.description = "制作身份证正面和背面图像"
        self.blueprint = Blueprint('id_card_maker', __name__, template_folder='../templates')
        self._register_routes()
        
    def init_app(self, app):
        """在应用上下文中初始化插件"""
        # 确保上传目录存在
        uploads_dir = os.path.join(app.static_folder, 'uploads', 'id_cards')
        os.makedirs(uploads_dir, exist_ok=True)

        # 确保身份证模板目录存在
        templates_dir = os.path.join(app.static_folder, 'images', 'id_cards')
        os.makedirs(templates_dir, exist_ok=True)

    def _register_routes(self):
        """注册路由"""

        @self.blueprint.route('/id_card_maker', methods=['GET'])
        def index():
            """渲染插件首页"""
            return render_template('plugins/id_card_maker.html')

        @self.blueprint.route('/id_card_maker/generate', methods=['POST'])
        def generate_id_card():
            """生成身份证图像"""
            try:
                # 获取表单数据
                name = request.form.get('name', '')
                gender = request.form.get('gender', '')
                nationality = request.form.get('nationality', '汉')
                birth_date = request.form.get('birth_date', '')
                address = request.form.get('address', '')
                id_number = request.form.get('id_number', '')
                issue_authority = request.form.get('issue_authority', '')
                valid_period = request.form.get('valid_period', '')
                
                # 获取自动抠图选项
                auto_cutout = request.form.get('auto_cutout') == 'true'

                # 获取上传的照片
                photo = request.files.get('photo')

                # 创建服务实例
                service = IdCardMakerService(current_app)

                # 生成身份证
                result = service.generate_id_card(
                    name=name,
                    gender=gender,
                    nationality=nationality,
                    birth_date=birth_date,
                    address=address,
                    id_number=id_number,
                    issue_authority=issue_authority,
                    valid_period=valid_period,
                    photo=photo,
                    auto_cutout=auto_cutout
                )

                return jsonify(result)

            except Exception as e:
                current_app.logger.error(f"生成身份证失败: {str(e)}")
                return jsonify({
                    'success': False,
                    'message': f"生成身份证失败: {str(e)}"
                }), 500
