from flask import Blueprint, render_template
from .api_routes import get_api_list

# Create a Blueprint for API routes
apiinfo_blueprint = Blueprint('apiinfo', __name__, url_prefix='/apiinfo')

@apiinfo_blueprint.route('/')
def api_list():
    """API列表页"""
    apis = get_api_list()
    return render_template('api_list.html', apis=apis)

@apiinfo_blueprint.route('/<path:api_path>')
def api_detail(api_path):
    """API详情页"""
    apis = get_api_list()
    api = next((a for a in apis if a['endpoint'] == f'/{api_path}'), None)
    if not api:
        return "API不存在", 404

    if api_path == 'identity':
        return render_template('api_detail_identity.html', api=api)
    elif api_path.startswith('region'):
        return render_template('api_detail_region.html', api=api)
    else:
        return render_template('api_detail_generic.html', api=api)