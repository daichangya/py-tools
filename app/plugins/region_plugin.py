from flask import Blueprint, render_template, request, flash, jsonify
from app.services.region_service import RegionService

class Plugin:
    """省市区查询插件"""
    def __init__(self):
        self.title = "省市区查询"
        self.description = "查询行政区划代码与名称的对应关系"
        self.blueprint = Blueprint('region', __name__, template_folder='../templates')
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/region', methods=['GET', 'POST'])
        def region_query():
            results = []
            if request.method == 'POST':
                query_type = request.form.get('query_type', 'name')
                query_value = request.form.get('query_value', '').strip()

                if query_value:
                    if query_type == 'name':
                        # 按名称查询
                        results = RegionService.search_by_name(query_value)
                    else:
                        # 按代码查询
                        result = RegionService.search_by_code(query_value)
                        if result:
                            results = [result]

                if not results:
                    flash('未找到匹配的行政区划信息', 'warning')

            # 获取省份列表用于下拉选择
            provinces = RegionService.get_provinces()
            return render_template('plugins/region.html',
                                results=results,
                                provinces=provinces)

        @self.blueprint.route('/api/areas')
        def get_areas():
            """获取下级区域列表"""
            parent_code = request.args.get('parent_code')
            areas = RegionService.get_sub_areas(parent_code)
            return jsonify(areas)

        @self.blueprint.route('/api/area_details')
        def get_area_details():
            """获取区域详细信息"""
            code = request.args.get('code')
            if not code:
                return jsonify({'error': '缺少区域代码'}), 400

            area_details = RegionService.get_area_details(code)
            if not area_details:
                return jsonify({'error': '未找到区域信息'}), 404

            return jsonify(area_details)
