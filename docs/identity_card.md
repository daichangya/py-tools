# 身份证信息查询工具

## 体验地址

您可以在以下地址体验此工具：[http://api.zthinker.com/](http://api.zthinker.com/)

## 功能概述

身份证信息查询工具是一个用于验证身份证号码有效性并解析身份证信息的应用。用户可以输入身份证号码，系统会自动验证其有效性，并提取出生日期、性别、地区信息、生肖和星座等信息。

## 主要功能

- 验证身份证号码的有效性
- 解析身份证号码中包含的信息
- 提取出生日期、性别和地区信息
- 计算生肖和星座
- 查询身份证号码对应的行政区划信息

## 使用方法

### Web界面使用

1. 访问身份证信息查询页面
2. 输入18位身份证号码
3. 点击"查询"按钮
4. 查看返回的身份证详细信息

### API调用

```
GET /api/identity/check?id_number=110101199001011234
```

## 技术实现

### 核心功能

1. **身份证验证**：验证身份证号码的格式和校验码
2. **信息提取**：从身份证号码中提取出生日期、性别和地区代码
3. **地区解析**：根据地区代码查询对应的省市区信息
4. **附加信息**：根据出生日期计算生肖和星座

### 身份证号码验证算法

身份证号码验证采用国家标准的校验算法：

```python
def validate_id(id_number):
    """验证身份证号码有效性"""
    if len(id_number) != 18:
        return False

    # 验证前6位是否为有效行政区划代码
    area_code = id_number[:6]
    if not city_utils.get_area_by_code(area_code):
        return False

    # 验证校验码
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    total = 0
    for i in range(17):
        try:
            total += int(id_number[i]) * factors[i]
        except ValueError:
            return False

    return id_number[-1].upper() == check_codes[total % 11]
```

### 身份证信息解析流程

1. 验证身份证号码的有效性
2. 提取出生日期（第7-14位）
3. 判断性别（第17位，奇数为男，偶数为女）
4. 提取地区代码（前6位）
5. 查询地区信息（省、市、区）
6. 根据出生年份计算生肖
7. 根据出生月日计算星座
8. 返回完整的身份证信息

### 生肖计算

根据出生年份计算生肖：

```python
def _get_zodiac(year):
    """根据年份计算属相"""
    zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇',
              '马', '羊', '猴', '鸡', '狗', '猪']
    offset = (year - 4) % 12
    return zodiacs[offset]
```

### 星座计算

根据出生月日计算星座：

```python
def _get_constellation(month, day):
    """根据月份和日期计算星座"""
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "水瓶座"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "双鱼座"
    # ... 其他星座判断逻辑
    else:
        return "摩羯座"
```

## 行政区划数据

系统使用全国行政区划数据来验证身份证号码中的地区代码并提供详细的地区信息。行政区划数据包含以下级别：

1. **省级**：包括省、直辖市、自治区、特别行政区
2. **市级**：包括地级市、地区、自治州、盟
3. **区县级**：包括市辖区、县级市、县、自治县、旗、自治旗、特区、林区

行政区划代码规则：
- 6位数字组成
- 前2位表示省级行政区
- 中间2位表示市级行政区
- 最后2位表示区县级行政区
- 如果后4位为0000，表示省级行政区
- 如果后2位为00，表示市级行政区

## 文件结构

- `app/plugins/identity_plugin.py`：插件主类，处理路由和请求
- `app/services/identity_service.py`：服务类，实现身份证验证和信息解析
- `app/utils/city_utils.py`：行政区划工具类，提供地区代码查询功能
- `app/static/citycodes.json`：行政区划数据文件

## API接口

### 验证并解析身份证信息

**请求**：
```
GET /api/identity/check?id_number={身份证号码}
```

**参数**：
- `id_number`：18位身份证号码

**响应**：
```json
{
  "success": true,
  "data": {
    "id_number": "110101199001011234",
    "valid": true,
    "birth_date": "1990-01-01",
    "gender": "男",
    "area_code": "110101",
    "area_info": {
      "province": "北京市",
      "city": "市辖区",
      "district": "东城区",
      "code": "110101",
      "full_name": "北京市/市辖区/东城区"
    },
    "zodiac": "马",
    "constellation": "摩羯座"
  }
}
```

### 查询行政区划信息

**请求**：
```
GET /api/identity/area?code={行政区划代码}
```

**参数**：
- `code`：6位行政区划代码

**响应**：
```json
{
  "success": true,
  "data": {
    "code": "110101",
    "full_name": "北京市/市辖区/东城区",
    "province": "北京市",
    "city": "市辖区",
    "district": "东城区"
  }
}
```

### 搜索行政区划

**请求**：
```
GET /api/identity/search?keyword={关键词}
```

**参数**：
- `keyword`：搜索关键词

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "code": "110101",
      "full_name": "北京市/市辖区/东城区",
      "level": 3
    },
    {
      "code": "120101",
      "full_name": "天津市/市辖区/和平区",
      "level": 3
    }
    // 更多匹配结果...
  ]
}
```

## 注意事项

1. 身份证信息查询仅用于验证身份证号码的有效性和解析其中包含的信息，不会验证身份证是否真实存在或可用
2. 系统不会存储用户输入的身份证号码，所有处理均在内存中完成
3. 行政区划数据可能会随着国家行政区划调整而变化，需要定期更新
4. 对于1999年之前的身份证号码，可能存在地区代码与现行行政区划不一致的情况
5. 系统不提供身份证号码生成功能，仅用于验证和解析

## 未来计划

1. 支持15位老身份证号码的验证和转换
2. 添加更多的身份证信息解析，如年龄、生日等
3. 提供行政区划历史变更查询功能
4. 增加身份证号码图像识别功能
5. 提供批量验证和解析功能
