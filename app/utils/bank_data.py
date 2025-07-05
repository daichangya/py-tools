import csv
import json
import os
from typing import Dict, Optional

class BankData:
    """银行卡数据管理类"""
    
    def __init__(self):
        self.bank_list: Dict[str, str] = {}
        self.bank_info: Dict[str, dict] = {}
        self.bin_info: Dict[str, dict] = {}
        self.binex_info: Dict[str, dict] = {}
        
        # 设置基础路径
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'bank'))
        
        # 确保目录存在
        os.makedirs(self.base_path, exist_ok=True)
        
        # 加载数据
        self.load_bank_list()
        self.load_bank_info()
        self.load_bin_info()
        self.load_binex_info()
    
    def load_bank_list(self, file_path: str = None) -> None:
        """加载银行列表数据"""
        file_path = file_path or os.path.join(self.base_path, 'bank_list.csv')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['BankTypeCode'] and row['BankName']:
                        self.bank_list[row['BankTypeCode']] = row['BankName']
        except Exception as e:
            print(f'加载银行列表数据失败: {e}')
    
    def load_bank_info(self, file_path: str = None) -> None:
        """加载银行详细信息"""
        file_path = file_path or os.path.join(self.base_path, 'bank.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.bank_info = json.load(f)
        except Exception as e:
            print(f'加载银行详细信息失败: {e}')
    
    def load_bin_info(self, file_path: str = None) -> None:
        """加载银行卡BIN信息"""
        file_path = file_path or os.path.join(self.base_path, 'bin.csv')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['bin'] and row['bank']:
                        self.bin_info[row['bin']] = {
                            'bank': row['bank'],
                            'type': row['type'],
                            'length': int(row['length'])
                        }
        except Exception as e:
            print(f'加载银行卡BIN信息失败: {e}')
    
    def load_binex_info(self, file_path: str = None) -> None:
        """加载扩展BIN信息"""
        file_path = file_path or os.path.join(self.base_path, 'binex.csv')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['bin'] and row['bank']:
                        self.binex_info[row['bin']] = {
                            'bank': row['bank'],
                            'type': row['type'],
                            'length': int(row['length'])
                        }
        except Exception as e:
            print(f'加载扩展BIN信息失败: {e}')
    
    def save_binex_info(self, file_path: str = None) -> None:
        """保存扩展BIN信息"""
        file_path = file_path or os.path.join(self.base_path, 'binex.csv')
        try:
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['bin', 'bank', 'type', 'length'])
                writer.writeheader()
                for bin_code, info in self.binex_info.items():
                    writer.writerow({
                        'bin': bin_code,
                        'bank': info['bank'],
                        'type': info['type'],
                        'length': info['length']
                    })
        except Exception as e:
            print(f'保存扩展BIN信息失败: {e}')
    
    def get_bank_name(self, bank_code: str) -> str:
        """根据银行编码获取银行名称"""
        return self.bank_list.get(bank_code, '未知银行')
    
    def get_bank_info(self, bank_code: str) -> Optional[dict]:
        """根据银行编码获取银行详细信息"""
        for bank in self.bank_info:
            if bank.get('名称', '').startswith(self.get_bank_name(bank_code)):
                return bank
        return None
    
    def get_card_info(self, card_no: str) -> Optional[dict]:
        """根据卡号获取银行卡信息"""
        # 先查找扩展BIN信息
        for length in range(8, 5, -1):
            if len(card_no) >= length:
                bin_code = card_no[:length]
                if bin_code in self.binex_info:
                    return self.binex_info[bin_code]
        
        # 再查找标准BIN信息
        for length in range(8, 5, -1):
            if len(card_no) >= length:
                bin_code = card_no[:length]
                if bin_code in self.bin_info:
                    return self.bin_info[bin_code]
        
        return None

# 创建单例实例
bank_data = BankData()