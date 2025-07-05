import sys
import os
from flask import Flask, render_template
import secrets
from importlib import import_module
from app.api_routes import api_blueprint, get_api_list
from app.apiinfo_routes import apiinfo_blueprint

#https://github.com/lionsoul2014/ip2region
#https://github.com/yescallop/areacodes
#https://mega.nz/folder/ewNxmbyT#toMSJLz44mpmQOO6W7j3Kg

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 从app包中导入create_app函数
from app import create_app

# 创建Flask应用实例
app = create_app()
# 设置密钥，用于会话和消息闪现
app.secret_key = secrets.token_hex(16)

# 插件系统
class PluginSystem:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self):
        """动态加载所有插件"""
        plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
        for item in os.listdir(plugin_dir):
            if not item.startswith('_') and item.endswith('.py'):
                plugin_name = item[:-3]
                try:
                    # 修改导入路径
                    module = import_module(f".plugins.{plugin_name}", package="app")
                    if hasattr(module, 'Plugin'):
                        plugin = module.Plugin()
                        self.plugins[plugin_name] = plugin
                        # 注册蓝图
                        if hasattr(plugin, 'blueprint'):
                            app.register_blueprint(plugin.blueprint)
                            print(f"加载插件 {plugin_name} 成功")
                except Exception as e:
                    print(f"加载插件 {plugin_name} 失败: {e}")

    def get_plugins(self):
        """获取所有已加载插件信息"""
        result = []
        for name, plugin in self.plugins.items():
            # 从蓝图中获取路由前缀
            route_name = plugin.blueprint.name if hasattr(plugin, 'blueprint') else name
            result.append({
                'name': route_name,  # 使用蓝图名称作为路由
                'title': plugin.title if hasattr(plugin, 'title') else name,
                'description': plugin.description if hasattr(plugin, 'description') else ''
            })
        return result

# 初始化插件系统
plugin_system = PluginSystem()
plugin_system.load_plugins()

app.register_blueprint(api_blueprint)
app.register_blueprint(apiinfo_blueprint)


# 全局上下文处理器，为所有模板提供插件列表
@app.context_processor
def inject_plugins():
    return {'plugins': plugin_system.get_plugins()}

@app.route('/')
def index():
    """首页显示所有可用工具"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=7001)

