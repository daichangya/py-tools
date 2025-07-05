from flask import Blueprint, render_template, flash
import requests

class Plugin:
    """随机小姐姐视频插件"""
    def __init__(self, app=None):
        self.title = "随机小姐姐视频"
        self.description = "展示随机小姐姐视频"
        self.blueprint = Blueprint('pretty_girl_video', __name__,
                                 template_folder='templates')
        self._register_routes()

    def _register_routes(self):
        """注册路由"""
        @self.blueprint.route('/pretty_girl_video', methods=['GET', 'POST'])
        def show_pretty_girl_video():
            # 使用视频API
            try:
                response = requests.get('https://api.kuleu.com/api/MP4_xiaojiejie?type=json')
                if response.status_code == 200:
                    video_url = response.json()['mp4_video']
                else:
                    video_url = None
                    flash('视频API请求失败', 'warning')
            except Exception as e:
                video_url = None
                flash(f'视频加载出错: {str(e)}', 'danger')

            return render_template('plugins/pretty_girl_video.html',
                                video_url=video_url)
