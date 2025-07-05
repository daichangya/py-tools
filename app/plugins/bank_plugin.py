from flask import Blueprint, render_template, request, flash, jsonify
from ..services.bank_service import BankService

class Plugin:
    """银行卡查询插件"""
    def __init__(self):
        self.title = "银行卡查询"
        self.description = "查询银行卡类型、发卡行及验证有效性"
        self.blueprint = Blueprint('bank', __name__, template_folder='../templates/plugins')
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/bank', methods=['GET', 'POST'])
        def bank_query():
            result = None
            if request.method == 'POST':
                card_no = request.form.get('card_no', '').strip()
                if not card_no:
                    flash('请输入银行卡号', 'danger')
                else:
                    # 移除空格和破折号
                    card_no = card_no.replace(' ', '').replace('-', '')
                    if not card_no.isdigit():
                        flash('银行卡号只能包含数字', 'danger')
                    else:
                        result = BankService.get_card_info(card_no)
                        if not result:
                            flash('无法识别该银行卡信息', 'warning')
                        elif not result.get('valid'):
                            flash('银行卡号验证失败', 'warning')

            # 获取所有支持的银行列表
            banks = BankService.BANK_INFO
            return render_template('bank.html', result=result, banks=banks)

        @self.blueprint.route('/api/bank/query', methods=['POST'])
        def bank_query_api():
            """API接口，用于AJAX请求"""
            card_no = request.json.get('card_no', '').strip()
            if not card_no:
                return jsonify({'error': '请输入银行卡号'}), 400

            card_no = card_no.replace(' ', '').replace('-', '')
            if not card_no.isdigit():
                return jsonify({'error': '银行卡号只能包含数字'}), 400

            result = BankService.get_card_info(card_no)
            if not result:
                return jsonify({'error': '无法识别该银行卡信息'}), 404

            return jsonify(result)
