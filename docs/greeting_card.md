# 贺卡生成工具

## 体验地址

您可以在以下地址体验此工具：[http://api.zthinker.com/](http://api.zthinker.com/)

## 功能概述

贺卡生成工具是一个用于创建和发送节日贺卡的应用。用户可以选择不同的节日，输入发送者和接收者信息，系统会自动生成一张精美的电子贺卡，包含节日祝福语和相应的节日图片。

## 主要功能

- 支持多种中国传统节日和国际节日
- 自动识别并推荐即将到来的节日
- 提供丰富的节日祝福语库
- 为每个节日提供多种精美图片背景
- 显示节日倒计时
- 支持农历和公历节日日期计算

## 使用方法

### Web界面使用

1. 访问贺卡生成工具页面：`/greeting_card`
2. 从下拉菜单中选择一个节日（默认为最近即将到来的节日）
3. 输入发送者姓名
4. 输入接收者姓名
5. 点击"生成贺卡"按钮
6. 查看生成的贺卡，可以保存或分享

### API接口使用

```bash
curl -X POST http://your-server/greeting_card/generate \
  -H "Content-Type: application/json" \
  -d '{
    "festival": "春节",
    "sender": "张三",
    "receiver": "李四"
  }'
```

#### 返回结果示例

```json
{
  "success": true,
  "data": {
    "festival": "春节",
    "greeting": "恭贺新春，万事大吉，阖家幸福安康！",
    "image": "spring_festival_3.jpg",
    "is_next_festival": true,
    "now": "2023-01-15T10:30:45.123456",
    "sender": "张三",
    "receiver": "李四",
    "festival_date": "2023-01-22",
    "is_lunar": true,
    "days_until": 7,
    "layout": {
      "image_layer": 0,
      "text_layer": 1
    }
  }
}
```

## 技术实现

### 核心功能

1. **节日管理**：维护农历和公历节日数据库
2. **日期计算**：使用zhdate库计算农历节日的公历日期
3. **贺卡生成**：根据节日随机选择祝福语和图片
4. **倒计时计算**：计算距离下一个节日的天数

### 农历日期转换

系统使用zhdate库处理农历日期的转换：

```python
from zhdate import ZhDate

# 农历日期转公历日期
lunar_date = ZhDate(2023, 1, 1)  # 农历2023年正月初一
solar_date = lunar_date.to_datetime().date()  # 转换为公历日期
```

### 下一个节日计算

系统会计算最近即将到来的节日，并作为默认选项：

```python
def get_next_festival(self):
    """获取下一个即将到来的节日"""
    today = datetime.now().date()
    current_year = today.year
    
    next_festival = None
    min_days_diff = float('inf')

    for festival, info in self.festivals.items():
        # 计算节日日期（处理农历和公历）
        # ...
        
        # 找出距离今天最近的未来节日
        if days_diff < min_days_diff:
            min_days_diff = days_diff
            next_festival = festival

    return next_festival
```

## 支持的节日

系统支持以下节日的贺卡生成：

| 节日名称 | 日期类型 | 日期 |
|---------|---------|------|
| 春节 | 农历 | 正月初一 |
| 元宵节 | 农历 | 正月十五 |
| 情人节 | 公历 | 2月14日 |
| 清明节 | 公历 | 4月5日 |
| 端午节 | 农历 | 五月初五 |
| 中秋节 | 农历 | 八月十五 |
| 国庆节 | 公历 | 10月1日 |
| 元旦 | 公历 | 1月1日 |
| 圣诞节 | 公历 | 12月25日 |

## 祝福语库

系统为每个节日提供多种祝福语，以下是部分示例：

### 春节祝福语

- 愿新春佳节带给你幸福安康，阖家欢乐！
- 祝您春节快乐，万事如意，阖家幸福！
- 新年新气象，祝您事业腾飞，家庭美满！
- 恭贺新春，万事大吉，阖家幸福安康！
- 金牛贺岁迎新春，万事如意展宏图。祝您新春快乐！

### 中秋节祝福语

- 但愿人长久，千里共婵娟。中秋快乐！
- 月圆人团圆，祝您中秋节快乐！
- 花好月圆，愿您中秋佳节阖家欢乐！
- 海上生明月，天涯共此时。祝您中秋节快乐！
- 明月几时有，把酒问青天。愿您中秋佳节阖家团圆！

## 图片资源

系统为每个节日提供多张精美图片作为贺卡背景：

- 春节：红灯笼、春联、烟花、福字、年画等
- 元宵节：花灯、汤圆、灯会场景等
- 中秋节：圆月、月饼、团圆场景等
- 圣诞节：圣诞树、圣诞老人、礼物、雪景等
- 其他节日：各具特色的节日元素和场景

## 文件结构

- `app/plugins/greeting_card_plugin.py`：插件主类，处理路由和请求
- `app/services/greeting_card_service.py`：服务类，实现核心功能
- `app/templates/plugins/greeting_card.html`：前端模板
- `app/static/images/greeting_cards/`：存放贺卡背景图片

## 注意事项

1. 农历日期计算依赖zhdate库，确保正确安装
2. 图片资源需要预先准备并放置在正确的目录中
3. 农历节日日期每年会有所变化，系统会自动计算
4. 贺卡生成是随机选择祝福语和图片，每次生成的结果可能不同
5. 系统会自动识别并推荐最近的节日，但用户也可以手动选择其他节日
