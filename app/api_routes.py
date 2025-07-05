from flask import Blueprint, jsonify, request
from app.services.bank_service import BankService

# API蓝图
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# API注册表
_api_registry = []

def register_api(endpoint, methods=['GET'], **kwargs):
    """API注册装饰器"""
    def decorator(f):
        # 添加到注册表
        _api_registry.append({
            'endpoint': endpoint,
            'function': f,
            'methods': methods,
            'metadata': kwargs
        })
        return f
    return decorator

# 示例API
@register_api('/identity', methods=['GET'],
              description="身份证信息查询API",
              params={"cardno": "身份证号码"})
def identity_query():
    """身份证信息查询"""
    cardno = request.args.get('cardno')
    if not cardno:
        return jsonify({
            "status": "error",
            "message": "缺少身份证号码参数"
        }), 400

    # 示例返回数据
    return jsonify({
        "status": "success",
        "data": {
            "cardno": cardno,
            "gender": "男" if int(cardno[-2]) % 2 else "女",
            "birthday": f"{cardno[6:10]}-{cardno[10:12]}-{cardno[12:14]}",
            "address": "北京市"
        }
    })

@register_api('/region/provinces', methods=['GET'],
             description="获取所有省份")
def get_provinces():
    """获取省份列表"""
    provinces = [
        {"code": "110000", "name": "北京市"},
        {"code": "310000", "name": "上海市"},
        # 可以添加更多省份数据
    ]
    return jsonify({
        "status": "success",
        "data": provinces
    })

@register_api('/bank', methods=['GET'],
             description="银行卡信息查询",
             params={"card_no": "银行卡号"})
def bank_query():
    """银行卡信息查询API"""
    card_no = request.args.get('card_no')
    if not card_no:
        return jsonify({
            "status": "error",
            "message": "缺少银行卡号参数"
        }), 400
    
    # 移除空格和破折号
    card_no = card_no.replace(' ', '').replace('-', '')
    
    if not card_no.isdigit():
        return jsonify({
            "status": "error",
            "message": "银行卡号只能包含数字"
        }), 400
    
    # 验证卡号
    if not BankService.validate_card(card_no):
        return jsonify({
            "status": "error",
            "message": "无效的银行卡号"
        }), 400
    
    # 获取卡片信息
    result = BankService.get_card_info(card_no)
    if not result:
        return jsonify({
            "status": "error",
            "message": "未找到该卡片信息"
        }), 404
    
    # 卡号脱敏处理
    result['masked_no'] = BankService.mask_card_no(card_no)
    
    return jsonify({
        "status": "success",
        "data": result
    })

# 注册所有API路由
for api in _api_registry:
    api_blueprint.route(api['endpoint'], methods=api['methods'])(api['function'])

def get_api_list():
    """获取所有API信息"""
    return [{
        'endpoint': api['endpoint'],
        'methods': api['methods'],
        'description': api['metadata'].get('description', ''),
        'params': api['metadata'].get('params', {})
    } for api in _api_registry]
