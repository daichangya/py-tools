from typing import List, Dict, Any, Optional
from app.utils.city_utils import city_utils

class RegionService():
    """区域信息服务"""

    @staticmethod
    def search_by_name(name: str) -> List[Dict[str, Any]]:
        """按名称搜索区域

        Args:
            name: 区域名称关键词

        Returns:
            匹配的区域列表
        """
        return city_utils.search_area(name)

    @staticmethod
    def search_by_code(code: str) -> Optional[Dict[str, Any]]:
        """按代码搜索区域

        Args:
            code: 区域代码

        Returns:
            区域信息或None
        """
        area_info = city_utils.get_area_by_code(code)
        if area_info:
            level = city_utils.get_admin_level(area_info['code'])
            return {
                'code': code,
                'full_name': area_info['full_name'],
                'level': level
            }
        return None

    @staticmethod
    def get_provinces() -> List[Dict[str, str]]:
        """获取所有省份列表

        Returns:
            省份列表
        """
        return city_utils.get_sub_areas()

    @staticmethod
    def get_sub_areas(parent_code: Optional[str] = None) -> List[Dict[str, str]]:
        """获取下级区域列表

        Args:
            parent_code: 父级区域代码，为None时获取省份列表

        Returns:
            下级区域列表
        """
        return city_utils.get_sub_areas(parent_code)

    @staticmethod
    def get_area_details(code: str) -> Optional[Dict[str, Any]]:
        """获取区域详细信息

        Args:
            code: 区域代码

        Returns:
            区域详细信息或None
        """
        # 获取区域基本信息
        area_info = city_utils.get_area_by_code(code)
        if not area_info:
            return None

        # 获取层级关系
        hierarchy = city_utils.get_parent_areas(code)

        # 获取下级区域
        sub_areas = city_utils.get_sub_areas(code)

        # 确定行政级别名称
        level_names = ['省级', '市级', '区县级']
        level = len(hierarchy)
        level_name = level_names[level - 1] if level <= len(level_names) else f'级别{level}'

        return {
            'code': code,
            'name': area_info['full_name'],
            'level': level,
            'level_name': level_name,
            'hierarchy': hierarchy,
            'sub_areas': sub_areas
        }
