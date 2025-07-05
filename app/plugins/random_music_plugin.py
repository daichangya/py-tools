from flask import Blueprint, render_template, flash
import requests


class Plugin:
    def __init__(self):
        self.title = "随机音乐"
        self.description = "随机播放一首热门歌曲，支持在线试听"
        self.blueprint = Blueprint('random_music', __name__,
                                 template_folder='templates')
        self._register_routes()

    def _register_routes(self):
        """注册路由"""

        @self.blueprint.route('/random_music')
        def random_music():
            try:
                # 调用随机音乐API
                response = requests.get('http://api.uomg.com/api/rand.music?sort=热歌榜&format=json')
                data = response.json()

                if data['code'] == 1:
                    music_data = data['data']
                    return render_template('plugins/random_music.html',
                                           music_url=music_data['url'],
                                           music_name=music_data['name'],
                                           artist_name=music_data['artistsname'],
                                           cover_url=music_data['picurl'])
                else:
                    return render_template('plugins/random_music.html', error="获取音乐失败")

            except Exception as e:
                return render_template('plugins/random_music.html', error=f"发生错误: {str(e)}")

