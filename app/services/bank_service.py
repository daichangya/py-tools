from typing import Optional, Dict, Any
import requests
from app.utils.bank_data import bank_data

class BankService:
    """银行卡信息服务"""

    # 银行卡类型
    CARD_TYPE = {
        'CC': '信用卡',
        'DC': '储蓄卡',
        'DCC': '借记卡',
        'JC': '准贷记卡',
        'PC': '预付卡',
        'BC': '商务卡',
        'GC': '礼品卡',
        'SC': '学生卡',
        'EC': '电子现金卡',
        'ETC': 'ETC卡',
        'HC': '健康卡',
        'FC': '金融IC卡'
    }

    # 推荐银行列表
    BANK_INFO = {
        "ICBC": "中国工商银行",
        "ABC": "中国农业银行",
        "BOC": "中国银行",
        "CCB": "中国建设银行",
        "CMB": "招商银行",
        "CMBC": "中国民生银行",
        "PSBC": "中国邮政储蓄银行",
        "SPDB": "上海浦东发展银行",
        "COMM": "交通银行",
        "CIB": "兴业银行"
    }

    @staticmethod
    def get_bank_img(bank_code: str) -> str:
        """获取银行图标URL"""
        return f"https://apimg.alipay.com/combo.png?d=cashier&t={bank_code}"

    @staticmethod
    def get_bank_list() -> Dict[str, str]:
        """获取银行列表"""
        return bank_data.bank_list

    @staticmethod
    def validate_card(card_no: str) -> bool:
        """使用Luhn算法验证银行卡号"""
        if not card_no or not card_no.isdigit():
            return False

        digits = [int(x) for x in card_no]
        for i in range(len(digits)-2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        return sum(digits) % 10 == 0

    @staticmethod
    def query_alipay_api(card_no: str) -> Optional[Dict[str, Any]]:
        """查询支付宝接口获取银行卡信息"""
        try:
            url = 'https://ccdcapi.alipay.com/validateAndCacheCardInfo.json'
            params = {
                'cardNo': card_no,
                '_input_charset': 'utf-8',
                'cardBinCheck': 'true'
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('validated', False) and data.get('bank'):
                # 构建卡bin信息
                bin_prefix = card_no[:6]
                card_info = {
                    'bank': data['bank'],
                    'type': data.get('cardType', 'DC'),  # 默认为储蓄卡
                    'length': len(card_no)
                }
                # 保存到binex字典
                bank_data.binex_info[bin_prefix] = card_info
                # 确保保存到文件
                try:
                    bank_data.save_binex_info()
                    print(f'成功保存卡bin信息: {bin_prefix}')
                except Exception as e:
                    print(f'保存卡bin信息失败: {e}')
                return card_info
            return None
        except Exception as e:
            print(f'查询支付宝接口失败: {e}')
            return None

    @staticmethod
    def get_card_info(card_no: str) -> Optional[Dict[str, Any]]:
        """获取银行卡信息"""
        if not card_no or not card_no.isdigit():
            return None

        # 获取卡bin信息
        card_info = bank_data.get_card_info(card_no)
        valid = BankService.validate_card(card_no)
        if not card_info or not valid:
            # 尝试从支付宝接口获取信息
            card_info = BankService.query_alipay_api(card_no)
            if not card_info:
                return None
            else:
                valid = True

        # 获取银行信息
        bank_code = card_info['bank']
        bank_name = bank_data.get_bank_name(bank_code)
        bank_info = bank_data.get_bank_info(bank_code)

        return {
            'card_no': card_no,
            'masked_no': BankService.mask_card_no(card_no),
            'valid': valid,
            'bank_code': bank_code,
            'bank': bank_name,
            'type': BankService.CARD_TYPE.get(card_info['type'], '未知类型'),
            'length': card_info['length'],
            'bank_info': bank_info,
            'bank_img': BankService.get_bank_img(bank_code)
        }

    @staticmethod
    def mask_card_no(card_no: str) -> str:
        """银行卡号脱敏处理"""
        if not card_no or len(card_no) < 10:
            return card_no
        return f"{card_no[:6]}{'*'*(len(card_no)-10)}{card_no[-4:]}"
