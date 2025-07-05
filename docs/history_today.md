# 历史上的今天工具

## 体验地址

您可以在以下地址体验此工具：[http://api.zthinker.com/](http://api.zthinker.com/)

## 功能概述

"历史上的今天"工具是一个用于展示历史上同一天发生的重要事件的应用。用户可以查看当天或选择特定日期，了解历史上这一天发生的重大历史事件、名人诞生或逝世等信息。

## 主要功能

- 自动展示当天历史上发生的重要事件
- 支持选择特定日期查询历史事件
- 按年份排序展示历史事件
- 提供丰富的历史事件数据库

## 使用方法

### Web界面使用

1. 访问历史上的今天工具页面：`/history`
2. 默认显示当天日期的历史事件
3. 使用日期选择器选择其他日期（月-日）
4. 点击"查询"按钮获取选定日期的历史事件
5. 浏览按年份排序的历史事件列表

### 日期选择

- 可以选择任意月份和日期（1月1日至12月31日）
- 日期格式为：YYYY-MM-DD（年份可任意，只使用月日部分）
- 点击"今天"按钮可快速返回当天的历史事件

## 技术实现

### 核心功能

1. **数据存储**：使用JSON文件存储按月份和日期组织的历史事件数据
2. **日期处理**：处理用户输入的日期并转换为查询格式
3. **数据查询**：根据月份和日期从数据库中检索历史事件
4. **结果展示**：按年份排序展示历史事件

### 数据结构

历史事件数据按月份存储在JSON文件中，每个文件包含该月所有日期的历史事件：

```json
{
  "01": {
    "0101": [
      {"year": "1912", "event": "中华民国成立，孙中山就任临时大总统"},
      {"year": "1863", "event": "林肯发布《解放黑奴宣言》"},
      {"year": "1958", "event": "欧洲经济共同体成立"}
    ],
    "0102": [
      // 1月2日的历史事件
    ]
    // 更多日期...
  }
}
```

### 数据查询流程

```python
def get_events_by_date(self, month: int = None, day: int = None) -> List[Dict]:
    """
    获取指定日期的历史事件
    
    Args:
        month: 月份 (1-12)，默认为当前月
        day: 日期，默认为当天
        
    Returns:
        List[Dict]: 历史事件列表，每个事件包含year和event字段
    """
    try:
        # 如果没有提供日期，使用当天
        today = datetime.datetime.now()
        month = month or today.month
        day = day or today.day

        # 读取对应月份文件
        file_path = os.path.join(self.base_path, f"{month}月.json")

        with open(file_path, 'r', encoding='utf-8') as f:
            month_data = json.load(f)
            # 月份 天 补足两位
            month = f"{month:0>2}"
            day = f"{day:0>2}"
            month_data = month_data[month]
            # 查找当天事件
            daily_events = month_data[month+day]
            return daily_events

    except Exception as e:
        print(f"读取历史数据失败: {str(e)}")
        return []
```

## 数据来源

历史事件数据来源于百度百科"历史上的今天"栏目，数据存储在应用的静态文件目录中：

```
app/static/BaiduJson/
  ├── 1月.json
  ├── 2月.json
  ├── 3月.json
  ...
  └── 12月.json
```

## 文件结构

- `app/plugins/history_plugin.py`：插件主类，处理路由和请求
- `app/services/history_service.py`：服务类，实现核心功能
- `app/templates/plugins/history.html`：前端模板
- `app/static/BaiduJson/`：存放历史事件数据的JSON文件

## 注意事项

1. 历史事件数据库需要定期更新以包含最新的历史事件
2. 某些日期（如2月29日）只在闰年有效，但系统会提供该日期的历史事件
3. 历史事件数据主要关注重大历史事件、科技发明、文化事件和名人生卒
4. 数据主要来源于百度百科，可能存在一定的地域和文化偏好
5. 系统不支持按年份筛选，只能按月日查询

## 未来计划

1. 添加按类别筛选历史事件的功能（如政治、科技、文化等）
2. 实现历史事件的搜索功能
3. 为重要历史事件添加详细描述和相关图片
4. 支持用户贡献和补充历史事件
5. 添加历史上的今天API接口，方便第三方应用调用
