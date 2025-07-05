#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.services.bank_service import BankService

def test_bank_info():
    """测试银行信息是否正确加载"""
    # 打印加载的银行信息数量
    print(f"加载的银行数量: {len(BankService.BANK_INFO)}")

    # 打印部分银行信息
    banks = ["ICBC", "ABC", "BOC", "CCB", "CMB", "PSBC"]
    for code in banks:
        print(f"{code}: {BankService.BANK_INFO.get(code, '未找到')}")

    # 测试获取银行列表
    bank_list = BankService.get_bank_list()
    print(f"银行列表数量: {len(bank_list)}")

    # 测试卡号查询
    test_cards = [
        "6222021234567890123",  # 工商银行
        "6228481234567890123",  # 农业银行
        "6217001234567890123",  # 建设银行
        "6225761234567890123"   # 招商银行
    ]

    for card in test_cards:
        info = BankService.get_card_info(card)
        if info:
            print(f"卡号: {card}, 银行: {info.get('bank', '未知')}, 类型: {info.get('type', '未知')}")
        else:
            print(f"卡号: {card}, 无法识别")

if __name__ == "__main__":
    test_bank_info()
