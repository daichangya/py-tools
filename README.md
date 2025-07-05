# PyTools

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

PyTools是一个功能丰富的Python工具集合，提供多种实用功能的Web界面和API接口。采用插件化架构设计，易于扩展和定制。

## 体验地址

您可以在以下地址体验此工具：[http://api.zthinker.com/](http://api.zthinker.com/)

## 功能特点

### 主要工具

- **身份证制作**：生成逼真的身份证正反面图像，支持自定义信息和照片自动抠图
- **银行卡信息**：银行卡号验证、银行识别等功能
- **快递查询**：支持多家快递公司单号查询
- **贺卡制作**：自定义电子贺卡生成
- **历史上的今天**：查询历史上同一天发生的重要事件
- **IP地址工具**：IP信息查询、归属地显示
- **随机音乐**：获取随机音乐推荐
- **名言引用**：随机名言展示
- **地区信息**：中国行政区划查询

### 技术特点

- 基于Flask的轻量级Web框架
- 插件化设计，便于功能扩展
- RESTful API支持
- 响应式Web界面，支持移动设备
- 命令行工具支持

## 安装指南

### 环境要求

- Python 3.8+
- pip包管理器

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/daichangya/py-tools.git
cd py-tools
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，设置必要的环境变量
```

4. 初始化数据库（如需要）
```bash
flask db init
flask db migrate
flask db upgrade
```

5. 运行应用
```bash
flask run
```

访问 http://127.0.0.1:7001 即可使用Web界面

## 使用说明

### Web界面

启动应用后，通过浏览器访问主页，可以看到所有可用工具的列表。点击相应工具进入功能页面。

### API接口

所有功能均提供API接口，可通过HTTP请求调用：

```bash
# 示例：获取身份证信息
curl -X POST http://localhost:5000/api/id_card_maker/generate \
  -F "name=张三" \
  -F "gender=男" \
  -F "nationality=汉" \
  -F "birth_date=1990年01月01日" \
  -F "address=北京市海淀区中关村南大街5号" \
  -F "id_number=110101199001010123" \
  -F "issue_authority=北京市公安局海淀分局" \
  -F "valid_period=2020.01.01-2030.01.01" \
  -F "photo=@/path/to/photo.jpg"
```

详细API文档可访问 `/apiinfo` 路径查看。

## 项目结构

```
py-tools/
├── app/                    # 应用主目录
│   ├── cli/                # 命令行工具
│   ├── commands/           # 自定义命令
│   ├── config/             # 配置文件
│   ├── database/           # 数据库相关
│   ├── models/             # 数据模型
│   ├── plugins/            # 插件目录
│   ├── services/           # 服务层
│   ├── static/             # 静态资源
│   ├── templates/          # HTML模板
│   ├── api_routes.py       # API路由
│   └── main.py             # 应用入口
├── .env.example            # 环境变量示例
├── .gitignore              # Git忽略文件
├── CHANGELOG.md            # 变更日志
├── LICENSE                 # 许可证文件
├── Makefile                # 构建脚本
├── README.md               # 项目说明
└── requirements.txt        # 依赖列表
```

## 插件系统

PyTools采用插件化设计，每个功能模块都是独立的插件。要添加新插件，只需在`app/plugins/`目录下创建新的插件文件，并实现必要的接口。

### 插件结构

每个插件需要包含以下组件：
- 插件类（继承自基础插件类或实现相同接口）
- 对应的服务类（实现业务逻辑）
- 前端模板（如需Web界面）

### 示例插件

```python
# app/plugins/example_plugin.py
from flask import Blueprint, render_template

class ExamplePlugin:
    def __init__(self):
        self.title = "示例插件"
        self.description = "这是一个示例插件"
        self.blueprint = Blueprint('example', __name__, template_folder='../templates/plugins')
        self._register_routes()
    
    def _register_routes(self):
        @self.blueprint.route('/example')
        def index():
            return render_template('example.html')
```

## 贡献指南

欢迎贡献代码、报告问题或提出新功能建议！

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请见[LICENSE](LICENSE)文件

## 免责声明

本工具集中的身份证制作等功能仅供学习、测试和研究使用，不得用于任何非法用途。使用者需自行承担因不当使用而产生的一切法律责任。
