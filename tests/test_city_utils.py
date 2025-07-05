import sys
import os
# 将项目根目录添加到模块搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.city_utils import city_utils

def test_get_area_by_code():
    """测试根据代码查询区域"""
    print("\n=== 测试根据代码查询区域 ===")

    # 测试有效的区域代码
    test_codes = ['110000', '110100', '110101']  # 北京市-北京市-东城区
    for code in test_codes:
        result = city_utils.get_area_by_code(code)
        print(f"\n查询代码 {code}:")
        if result:
            print(f"完整名称: {result['full_name']}")
            print(f"省份: {result['province']}")
            print(f"城市: {result['city']}")
            print(f"区县: {result['district']}")
        else:
            print("未找到区域信息")

    # 测试无效的区域代码
    invalid_code = '999999'
    result = city_utils.get_area_by_code(invalid_code)
    print(f"\n查询无效代码 {invalid_code}:")
    print("结果:", "未找到" if result is None else result)

def test_search_area():
    """测试区域搜索"""
    print("\n=== 测试区域搜索 ===")

    # 测试常见地名搜索
    test_keywords = ['朝阳', '海淀', '南山']
    for keyword in test_keywords:
        results = city_utils.search_area(keyword)
        print(f"\n搜索关键词 '{keyword}':")
        for item in results:
            print(f"- {item['full_name']} (代码: {item['code']})")

def test_parent_areas():
    """测试获取上级区域"""
    print("\n=== 测试获取上级区域 ===")

    # 测试区县级区域的上级查询
    test_code = '110101'  # 北京市东城区
    parents = city_utils.get_parent_areas(test_code)
    print(f"\n区域 {test_code} 的上级区域:")
    for area in parents:
        print(f"- 级别{area['level']}: {area['name']} (代码: {area['code']})")

def test_sub_areas():
    """测试获取下级区域"""
    print("\n=== 测试获取下级区域 ===")

    # 测试获取省份列表
    provinces = city_utils.get_sub_areas()
    print("\n省份列表:")
    for province in provinces[:3]:  # 只显示前3个省份
        print(f"- {province['name']} (代码: {province['code']})")

        # 获取该省份的城市
        cities = city_utils.get_sub_areas(province['code'])
        if cities:
            print("  城市列表:")
            for city in cities[:2]:  # 只显示前2个城市
                print(f"  - {city['name']} (代码: {city['code']})")

                # 获取该城市的区县
                districts = city_utils.get_sub_areas(city['code'])
                if districts:
                    print("    区县列表:")
                    for district in districts[:2]:  # 只显示前2个区县
                        print(f"    - {district['name']} (代码: {district['code']})")

def main():
    """运行所有测试"""
    print("开始测试城市代码工具类...")

    test_get_area_by_code()
    test_search_area()
    test_parent_areas()
    test_sub_areas()

    print("\n测试完成!")

if __name__ == '__main__':
    main()
