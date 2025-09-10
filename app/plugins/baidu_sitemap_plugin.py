from flask import Blueprint, request, jsonify, current_app, render_template
import os
from typing import Dict, Any, List, Optional
import logging
from app.services.baidu_sitemap_service import BaiduSitemapService

# 创建日志记录器
logger = logging.getLogger(__name__)


# 插件类定义
class Plugin:
    def __init__(self):
        self.title = "百度sitemap推送工具"
        self.description = "从sitemap URL获取内容并推送到百度搜索资源平台"
        # 创建蓝图
        self.blueprint = Blueprint('baidu_sitemap', __name__, url_prefix='/baidu_sitemap', template_folder='../templates')
        self._register_routes()

    def _register_routes(self):
        # 路由：工具首页
        @self.blueprint.route('/', methods=['GET'])
        def index():
            return render_template('plugins/baidu_sitemap.html')

        # 路由：处理sitemap推送
        @self.blueprint.route('/push', methods=['POST'])
        def push_sitemap():
            try:
                data = request.json

                # 获取必填参数
                sitemap_url = data.get('sitemap_url', '').strip()
                api_key = data.get('api_key', '').strip()

                # 验证必填字段
                if not all([sitemap_url, api_key]):
                    return jsonify({
                        "success": False,
                        "message": "缺少必要参数，请填写sitemap URL和API密钥"
                    }), 400

                # 验证URL格式
                if not (sitemap_url.startswith('http://') or sitemap_url.startswith('https://')):
                    return jsonify({
                        "success": False,
                        "message": "sitemap URL必须以http://或https://开头"
                    }), 400

                # 创建服务并处理sitemap
                sitemap_service = BaiduSitemapService(api_key)
                result = sitemap_service.process_sitemap(sitemap_url)

                return jsonify(result), 200 if result["success"] else 500

            except Exception as e:
                error_msg = f"处理sitemap推送时出错: {str(e)}"
                logger.error(error_msg)
                return jsonify({"success": False, "message": error_msg}), 500

        # 路由：批量推送URL列表
        @self.blueprint.route('/push-urls', methods=['POST'])
        def push_urls():
            try:
                data = request.json

                # 获取参数
                api_key = data.get('api_key', '').strip()
                urls = data.get('urls', [])
                
                # 处理字符串格式的URL列表
                if isinstance(urls, str):
                    urls = [url.strip() for url in urls.split('\n') if url.strip()]

                # 验证必填字段
                if not api_key:
                    return jsonify({
                        "success": False,
                        "message": "请提供API密钥"
                    }), 400

                if not urls:
                    return jsonify({
                        "success": False,
                        "message": "请提供要推送的URL列表"
                    }), 400

                # 验证URL格式
                invalid_urls = []
                for url in urls:
                    if not (url.startswith('http://') or url.startswith('https://')):
                        invalid_urls.append(url)
                
                if invalid_urls:
                    return jsonify({
                        "success": False,
                        "message": f"以下URL格式不正确（必须以http://或https://开头）: {', '.join(invalid_urls[:5])}{'...' if len(invalid_urls) > 5 else ''}"
                    }), 400

                # 创建服务并推送URL
                sitemap_service = BaiduSitemapService(api_key)
                result = sitemap_service.push_to_baidu(urls)

                return jsonify(result), 200 if result["success"] else 500

            except Exception as e:
                error_msg = f"推送URL列表时出错: {str(e)}"
                logger.error(error_msg)
                return jsonify({"success": False, "message": error_msg}), 500

        # 路由：验证sitemap URL（只解析不推送）
        @self.blueprint.route('/validate', methods=['POST'])
        def validate_sitemap():
            try:
                data = request.json
                sitemap_url = data.get('sitemap_url', '').strip()

                if not sitemap_url:
                    return jsonify({
                        "success": False,
                        "message": "请提供sitemap URL"
                    }), 400

                # 验证URL格式
                if not (sitemap_url.startswith('http://') or sitemap_url.startswith('https://')):
                    return jsonify({
                        "success": False,
                        "message": "sitemap URL必须以http://或https://开头"
                    }), 400

                # 创建服务并解析sitemap（不使用API密钥）
                sitemap_service = BaiduSitemapService("dummy_token")
                sitemap_content = sitemap_service.fetch_sitemap_content(sitemap_url)
                
                if not sitemap_content:
                    return jsonify({
                        "success": False,
                        "message": "无法获取sitemap内容，请检查URL是否正确"
                    }), 400

                # 解析URL但不推送
                urls = sitemap_service.parse_sitemap(sitemap_content)

                return jsonify({
                    "success": True,
                    "message": f"成功解析sitemap，找到 {len(urls)} 个URL",
                    "url_count": len(urls),
                    "sample_urls": urls[:10] if urls else [],
                    "sitemap_url": sitemap_url
                }), 200

            except Exception as e:
                error_msg = f"验证sitemap时出错: {str(e)}"
                logger.error(error_msg)
                return jsonify({"success": False, "message": error_msg}), 500