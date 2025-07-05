# IP地址查询工具

## 体验地址

您可以在以下地址体验此工具：[http://api.zthinker.com/](http://api.zthinker.com/)

## 体验地址

您可以在以下地址体验此工具：[http://api.zthinker.com/](http://api.zthinker.com/)

## 功能概述

IP地址查询工具是一个用于查询IP地址地理位置和相关信息的应用。用户可以输入IP地址，系统会自动查询该IP的归属地、运营商等信息，并提供可视化的地理位置展示。

## 主要功能

- 查询IP地址的地理位置信息
- 获取IP地址的运营商信息
- 支持IPv4地址查询
- 提供本地IP库和在线API双重查询方式
- 支持查询本机公网IP地址

## 使用方法

### Web界面使用

1. 访问IP地址查询页面
2. 输入要查询的IP地址（如不输入则默认查询当前用户的公网IP）
3. 点击"查询"按钮
4. 查看返回的IP地址详细信息

### API调用

```
GET /api/ip/query?ip=114.114.114.114
```

## 技术实现

### 核心功能

1. **IP地址验证**：验证输入的IP地址格式是否有效
2. **本地IP库查询**：使用ip2region库在本地快速查询IP地址信息
3. **在线API查询**：当本地库无法提供详细信息时，使用在线API进行补充查询
4. **本机IP获取**：通过多种方式获取用户的真实公网IP地址

### IP地址验证

使用socket库验证IP地址格式：

```python
def is_valid_ip(ip: str) -> bool:
    """验证IP地址格式是否有效"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
```

### IP地址查询流程

1. 验证IP地址格式
2. 从本地IP库查询基本信息（国家、地区、省份、城市、ISP）
3. 如果需要更详细的信息，调用在线API进行查询
4. 合并本地库和在线API的查询结果
5. 返回完整的IP地址信息

### IP2Region库

系统使用开源的IP2Region库作为本地IP地址查询的基础。IP2Region是一个高效的IP地址定位库，具有以下特点：

1. **高性能**：查询速度快，平均查询时间小于1ms
2. **低内存**：整个库只有几MB大小，可以完全加载到内存中
3. **高准确性**：数据定期更新，保持较高的准确度

IP2Region使用的是xdb格式的数据文件，查询算法采用了前缀索引和二分查找相结合的方式，保证了查询的高效性。

### XdbSearcher实现

XdbSearcher是IP2Region的核心查询类，实现了对xdb文件的读取和查询：

1. **向量索引**：使用二维向量索引加速查询
2. **内存缓存**：支持将整个数据库加载到内存中，提高查询速度
3. **二分查找**：在索引块中使用二分查找算法定位IP信息

## 数据结构

### IP地址信息

系统返回的IP地址信息包含以下字段：

| 字段 | 说明 |
|------|------|
| ip | 查询的IP地址 |
| country | 国家 |
| region | 区域 |
| province | 省份 |
| city | 城市 |
| isp | 互联网服务提供商 |
| asn | 自治系统号 |
| timezone | 时区 |
| is_local | 是否为局域网IP |

### IP地址类型

系统可以识别以下几种IP地址类型：

1. **公网IP**：可在互联网上路由的IP地址
2. **局域网IP**：内部网络使用的私有IP地址（如192.168.x.x）
3. **保留IP**：特殊用途的保留IP地址（如127.0.0.1）
4. **特殊IP**：具有特殊用途的IP地址（如广播地址）

## 文件结构

- `app/plugins/ip_plugin.py`：插件主类，处理路由和请求
- `app/services/ip_service.py`：服务类，实现IP地址查询的核心功能
- `app/utils/ip_utils.py`：IP工具类，封装IP2Region查询功能
- `app/utils/xdbSearcher.py`：XDB搜索器，实现对xdb文件的读取和查询
- `app/static/ip2region.xdb`：IP2Region数据文件

## API接口

### 查询IP地址信息

**请求**：
```
GET /api/ip/query?ip={IP地址}
```

**参数**：
- `ip`：要查询的IP地址，如不提供则查询用户当前的公网IP

**响应**：
```json
{
  "success": true,
  "data": {
    "ip": "114.114.114.114",
    "country": "中国",
    "region": "华东",
    "province": "江苏省",
    "city": "南京市",
    "isp": "南京信风网络科技有限公司",
    "asn": "AS17638",
    "timezone": "UTC+8",
    "is_local": false
  }
}
```

### 获取当前用户的公网IP

**请求**：
```
GET /api/ip/myip
```

**响应**：
```json
{
  "success": true,
  "data": {
    "ip": "123.123.123.123"
  }
}
```

### 批量查询IP地址

**请求**：
```
POST /api/ip/batch
Content-Type: application/json

{
  "ips": ["114.114.114.114", "8.8.8.8"]
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "114.114.114.114": {
      "country": "中国",
      "region": "华东",
      "province": "江苏省",
      "city": "南京市",
      "isp": "南京信风网络科技有限公司"
    },
    "8.8.8.8": {
      "country": "美国",
      "region": "北美洲",
      "province": "加利福尼亚州",
      "city": "山景城",
      "isp": "Google LLC"
    }
  }
}
```

## 注意事项

1. IP地址查询结果的准确性取决于IP库的更新频率和数据质量
2. 本地IP库可能不如在线API准确，但查询速度更快且不依赖网络
3. 某些IP地址（如内网IP）无法获取准确的地理位置信息
4. 系统不会记录用户的查询历史，保护用户隐私
5. IP地址的地理位置信息仅供参考，不应用于需要高精度定位的场景

## 未来计划

1. 支持IPv6地址查询
2. 添加IP地址的地图可视化展示
3. 提供更多IP相关信息，如网络安全评估
4. 增加IP地址历史记录和变更追踪功能
5. 支持导出IP查询结果为多种格式（CSV、Excel等）
