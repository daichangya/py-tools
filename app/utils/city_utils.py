import json
import os
from typing import Dict, List, Optional, Union

class CityUtils:
    """城市代码工具类"""
    
    def __init__(self):
        self._city_data = None
        self._code_map = {}
        self._name_map = {}
        self._load_city_data()
    
    def _load_city_data(self):
        """加载城市数据"""
        try:
            # 获取项目根目录（即test目录的父目录）
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(project_root,'static', 'citycodes.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 获取items数组
                self._city_data = data.get('items', [])
            self._build_maps(self._city_data)
        except Exception as e:
            print(f"加载城市数据失败: {e}")
            self._city_data = []
    
    def _build_maps(self, data: List[dict], parent_info: tuple = None):
        """构建代码和名称映射"""
        for item in data:
            code = str(item.get('code', ''))  # 转换为字符串
            name = item.get('name', '')
            children = item.get('children', [])
            successors = item.get('successors', [])
            
            if parent_info:
                parent_codes, parent_names = parent_info
                current_codes = parent_codes + [code]
                current_names = parent_names + [name]
            else:
                current_codes = [code]
                current_names = [name]
            
            # 存储完整的层级信息
            if code:
                self._code_map[code] = {
                    'codes': current_codes,
                    'names': current_names,
                    'level': len(current_codes),
                    'start': item.get('start'),
                    'successors': successors
                }
            
            # 构建名称到代码的映射
            if name:
                if name not in self._name_map:
                    self._name_map[name] = []
                self._name_map[name].append({
                    'code': code,
                    'full_name': '/'.join(current_names),
                    'level': len(current_codes)
                })
            
            # 递归处理子区域
            if children:
                self._build_maps(children, (current_codes, current_names))
    
    def get_area_by_code(self, code: str) -> Optional[Dict]:
        """根据区域代码获取信息
        
        Args:
            code: 区域代码
            
        Returns:
            包含区域信息的字典，包括:
            - province: 省份名称
            - city: 城市名称
            - district: 区县名称（如果有）
            - code: 完整区域代码
            - full_name: 完整区域名称
        """
        if not code or code not in self._code_map:
            return None
        
        info = self._code_map[code]
        names = info['names']
        result = {
            'code': code,
            'full_name': '/'.join(names),
            'province': names[0] if len(names) > 0 else '',
            'city': names[1] if len(names) > 1 else '',
            'district': names[2] if len(names) > 2 else ''
        }
        return result
    
    def search_area(self, keyword: str) -> List[Dict]:
        """搜索区域
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的区域列表，每个元素包含:
            - code: 区域代码
            - full_name: 完整区域名称
            - level: 区域级别（1：省，2：市，3：区县）
        """
        results = []
        for name, areas in self._name_map.items():
            if keyword in name:
                results.extend(areas)
        return sorted(results, key=lambda x: (x['level'], x['full_name']))
    
    def get_parent_areas(self, code: str) -> List[Dict]:
        """获取指定区域的所有上级区域
        
        Args:
            code: 区域代码
            
        Returns:
            上级区域列表，从省份到当前区域，每个元素包含:
            - code: 区域代码
            - name: 区域名称
            - level: 区域级别(1:省, 2:市, 3:区县)
            - full_name: 完整区域名称
        """
        if not code or code not in self._code_map:
            return []
        
        info = self._code_map[code]
        codes = info['codes']
        names = info['names']
        
        results = []
        for i in range(len(codes)):
            results.append({
                'code': codes[i],
                'name': names[i],
                'level': i + 1,
                'full_name': '/'.join(names[:i+1])
            })
        return results

    def get_admin_level(self, code: str) -> int:
        """
        根据行政区划代码判断级别

        参数:
            code (str): 行政区划代码，如 "110000" 表示北京市

        返回:
            int: 级别，1表示省级，2表示市级，3表示区县级，0表示无效编码
        """
        code = str(code).strip()

        # 检查是否为纯数字
        if not code.isdigit():
            return 0

        length = len(code)

        # 省级 (2位数字)
        if length != 6:
            return 0
        # 省级扩展形式 (6位数字，后四位为0000)
        elif code[2:] == "0000":
            return 1
        # 市级 (6位数字，后二位为0000)
        elif code[2:] == "00":
            return 2
        # 区县级 (6位数字)
        elif length == 6:
            return 3
        else:
            return 0  # 其他长度的编码无效
    
    def get_sub_areas(self, code: str = None) -> List[Dict]:
        """获取指定区域的下级区域列表
        
        Args:
            code: 区域代码，如果为None则返回所有省份
            
        Returns:
            下级区域列表
        """
        def find_node(data: List[dict], target_code: str) -> Optional[dict]:
            for item in data:
                if str(item.get('code', '')) == target_code:
                    return item
                children = item.get('children', [])
                if children:
                    result = find_node(children, target_code)
                    if result:
                        return result
            return None
        
        if code is None:
            # 返回所有省份
            return [{'code': str(item.get('code', '')), 'name': item.get('name', '')} 
                    for item in self._city_data]
        
        node = find_node(self._city_data, code)
        if node:
            # 优先使用children字段
            if 'children' in node and node['children']:
                return [{'code': str(item.get('code', '')), 'name': item.get('name', '')} 
                        for item in node['children']]
            # 其次使用successors字段
            elif 'successors' in node and node['successors']:
                return [{'code': str(item.get('code', '')), 'name': item.get('name', '')} 
                        for item in node['successors']]
        return []

# 创建单例实例
city_utils = CityUtils()

if __name__ == '__main__':
    # 使用示例
    
    # 1. 根据代码查询区域信息
    area = city_utils.get_area_by_code('110101')
    if area:
        print(f"区域信息: {area}")
    
    # 2. 搜索区域
    results = city_utils.search_area('朝阳')
    print(f"\n搜索'朝阳':")
    for item in results:
        print(f"- {item['full_name']} ({item['code']})")
    
    # 3. 获取上级区域
    parents = city_utils.get_parent_areas('110101')
    print(f"\n区域'110101'的上级区域:")
    for item in parents:
        print(f"- {item['name']} ({item['code']})")
    
    # 4. 获取下级区域
    subs = city_utils.get_sub_areas('110100')
    print(f"\n区域'110100'的下级区域:")
    for item in subs:
        print(f"- {item['name']} ({item['code']})")
