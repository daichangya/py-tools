from flask import Blueprint, render_template, request, flash, jsonify
import requests
from urllib.parse import urljoin

class Plugin:
    """图书搜索插件"""
    def __init__(self, app=None):
        self.title = "图书搜索"
        self.description = "搜索图书信息，支持按书名、作者、出版社等条件查询"
        self.blueprint = Blueprint('book_search', __name__,
                                 template_folder='templates')
        self.api_base_url = "https://book.liangji.eu.org/search"
        self.white_pic = "/static/images/white.png"  # 默认白色图片路径
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/book_search', methods=['GET', 'POST'])
        def show_book_search():
            search_results = None
            search_params = {}

            # 根据请求方法获取参数
            if request.method == 'POST':
                param_source = request.form
            else:  # GET请求
                param_source = request.args
            
            # 获取搜索参数
            title = param_source.get('title', '').strip()
            author = param_source.get('author', '').strip()
            publisher = param_source.get('publisher', '').strip()
            extension = param_source.get('extension', '').strip()
            language = param_source.get('language', '').strip()
            isbn = param_source.get('isbn', '').strip()
            book_id = param_source.get('id', '').strip()
            limit = param_source.get('limit', '20').strip()
            offset = param_source.get('offset', '0').strip()

            # 构建搜索参数
            if title:
                search_params['title'] = title
            if author:
                search_params['author'] = author
            if publisher:
                search_params['publisher'] = publisher
            if extension:
                search_params['extension'] = extension
            if language:
                search_params['language'] = language
            if isbn:
                search_params['isbn'] = isbn
            if book_id:
                search_params['id'] = book_id

            search_params['limit'] = limit
            search_params['offset'] = offset

            # 如果有搜索参数，执行搜索
            if search_params and (title or author or publisher or extension or language or isbn or book_id):
                try:
                    # 调用搜索API
                    search_results = self._search_books(search_params)
                except Exception as e:
                    flash(f'搜索图书时出错: {str(e)}', 'danger')

            return render_template('plugins/book_search.html',
                                  search_results=search_results,
                                  search_params=search_params)

        @self.blueprint.route('/book_search/api', methods=['POST'])
        def api_search_books():
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'message': '请提供搜索参数'})

            search_params = {}

            # 提取搜索参数
            for param in ['title', 'author', 'publisher', 'extension', 'language', 'isbn', 'id']:
                if param in data and data[param].strip():
                    search_params[param] = data[param].strip()

            # 添加分页参数
            search_params['limit'] = data.get('limit', '20')
            search_params['offset'] = data.get('offset', '0')

            if not search_params:
                return jsonify({'success': False, 'message': '请至少提供一个搜索条件'})

            try:
                # 调用搜索API
                search_results = self._search_books(search_params)
                return jsonify({'success': True, 'results': search_results})
            except Exception as e:
                return jsonify({'success': False, 'message': f'搜索图书时出错: {str(e)}'})
                
        @self.blueprint.route('/book_search/detail', methods=['GET'])
        def show_book_detail():
            # 从会话中获取图书数据
            book_id = request.args.get('id')
            if not book_id:
                flash('未提供图书ID', 'danger')
                return render_template('plugins/book_detail.html', book=None, error='未提供图书ID')
            
            # 保存所有查询参数，用于返回按钮
            search_params = {}
            for param in ['title', 'author', 'publisher', 'extension', 'language', 'isbn', 'limit', 'offset']:
                value = request.args.get(param)
                if value:
                    search_params[param] = value
            
            # 从搜索结果中查找图书数据
            api_params = {'id': book_id}
            try:
                search_results = self._search_books(api_params)
                if search_results and 'books' in search_results and len(search_results['books']) > 0:
                    book_detail = search_results['books'][0]
                    return render_template('plugins/book_detail.html', book=book_detail, search_params=search_params)
                else:
                    flash('未找到图书信息', 'warning')
                    return render_template('plugins/book_detail.html', book=None, error='未找到图书信息', search_params=search_params)
            except Exception as e:
                flash(f'获取图书详情时出错: {str(e)}', 'danger')
                return render_template('plugins/book_detail.html', book=None, error=str(e), search_params=search_params)


    def _get_isbn_cover_image_url(self, isbn, size='M'):
        """
        根据ISBN获取Open Library的封面图片URL
        
        Args:
            isbn: 书籍的ISBN号，可能是单个ISBN或逗号分隔的多个ISBN
            size: 图片尺寸：S(小)、M(中)、L(大)，默认为M
            
        Returns:
            封面图片的URL
        """
        if not isbn or len(isbn) == 0:
            return self.white_pic
        
        # 如果包含逗号，取第一个ISBN
        if ',' in isbn:
            isbn = isbn.split(',')[0].strip()
            
            # 如果分割后的ISBN为空，返回白色图片
            if len(isbn) == 0:
                return self.white_pic
        
        # 移除ISBN中的连字符
        isbn = isbn.replace('-', '')
        return f"https://covers.openlibrary.org/b/isbn/{isbn}-{size}.jpg"

    def _search_books(self, params):
        """
        调用图书搜索API

        Args:
            params: 搜索参数字典

        Returns:
            搜索结果字典
        """
        try:
            response = requests.get(self.api_base_url, params=params, timeout=10)
            response.raise_for_status()  # 如果响应状态码不是200，抛出异常
            
            result = response.json()
            
            # 为每本书添加Open Library的封面图片URL
            if 'books' in result and isinstance(result['books'], list):
                for book in result['books']:
                    if 'isbn' in book and book['isbn']:
                        book['ol_cover_url'] = self._get_isbn_cover_image_url(book['isbn'])
                    else:
                        book['ol_cover_url'] = self.white_pic
            
            return result
        except requests.exceptions.RequestException as e:
            print(f"API请求错误: {e}")
            raise Exception(f"无法连接到图书搜索服务: {str(e)}")
        except ValueError as e:
            print(f"JSON解析错误: {e}")
            raise Exception("服务器返回的数据格式无效")
