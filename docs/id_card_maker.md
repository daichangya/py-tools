# 身份证制作工具

## 体验地址

您可以在以下地址体验此工具：[http://api.zthinker.com/](http://api.zthinker.com/)

## 功能概述

身份证制作工具是一个用于生成模拟身份证图像的应用。用户可以输入个人信息和上传照片，系统会自动生成一张包含正面和背面的身份证图像。该工具仅供学习和娱乐使用，不得用于任何非法用途。

## 主要功能

- 生成身份证正面和背面图像
- 支持自定义姓名、性别、民族、出生日期等信息
- 支持上传照片并自动调整大小
- 提供自动抠图功能，去除照片背景
- 生成高清身份证预览图

## 使用方法

### Web界面使用

1. 访问身份证制作工具页面：`/id_card_maker`
2. 填写身份证信息：
   - 姓名
   - 性别
   - 民族（默认为"汉"）
   - 出生日期（格式：YYYY年MM月DD日）
   - 住址
   - 身份证号码
   - 签发机关
   - 有效期限
3. 上传证件照片（可选）
4. 选择是否启用自动抠图功能
5. 点击"生成身份证"按钮
6. 查看生成的身份证预览图

## 技术实现

### 核心功能

1. **表单处理**：收集用户输入的身份证信息
2. **图像处理**：使用PIL库处理上传的照片和生成身份证图像
3. **自动抠图**：使用纯PIL实现的背景去除算法
4. **文字渲染**：在身份证模板上渲染各种信息

### 自动抠图算法

系统使用纯PIL实现的自动抠图功能，不依赖OpenCV或NumPy：

```python
def _change_background(self, img, img_back, zoom_size, center):
    """更改背景（自动抠图）- 使用纯PIL实现，不依赖numpy和opencv"""
    # 缩放图像
    img = img.resize(zoom_size)
    
    # 获取左上角像素作为背景色参考
    background_color = img.getpixel((0, 0))
    
    # 创建掩码图像
    mask = Image.new('L', img.size, 0)  # 'L'是8位灰度图，0是黑色
    width, height = img.size
    
    # 设置颜色差异阈值
    threshold = 50  # 可以根据需要调整
    
    # 遍历图像像素，标记背景区域
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            # 计算与背景色的差异
            diff = sum(abs(pixel[i] - background_color[i]) for i in range(3))
            if diff < threshold:
                mask.putpixel((x, y), 255)  # 255是白色，表示背景
    
    # 模拟腐蚀和膨胀操作
    mask = mask.filter(ImageFilter.MinFilter(3))  # 腐蚀
    mask = mask.filter(ImageFilter.MaxFilter(3))  # 膨胀
    
    # 创建前景掩码（反转背景掩码）
    foreground_mask = ImageChops.invert(mask)
    
    # 将前景与透明背景合成
    transparent = Image.new('RGBA', img.size, (0, 0, 0, 0))
    transparent.paste(img, (0, 0), foreground_mask)
    
    # 将合成后的图像粘贴到目标图像上
    result = img_back.copy()
    result.paste(transparent, (center[1], center[0]), transparent)
    
    return result
```

### 身份证生成流程

1. 加载身份证模板（empty.png）
2. 在模板上绘制用户提供的个人信息
3. 处理并添加用户上传的照片
4. 生成并保存最终的身份证图像
5. 返回图像URL供用户预览

## 文件结构

- `app/plugins/id_card_maker_plugin.py`：插件主类，处理路由和请求
- `app/services/id_card_maker_service.py`：服务类，实现核心功能
- `app/templates/plugins/id_card_maker.html`：前端模板
- `app/static/idcard/`：存放身份证模板和字体文件
- `app/static/uploads/id_cards/`：存放生成的身份证图像和上传的照片

## 资源文件

系统需要以下资源文件：

1. **身份证模板**：
   - `empty.png`：包含身份证正反面布局的模板图像

2. **字体文件**：
   - `hei.ttf`：用于渲染姓名和其他信息
   - `fzhei.ttf`：用于渲染出生日期
   - `ocrb10bt.ttf`：用于渲染身份证号码

## 注意事项

1. 该工具生成的身份证图像仅供学习和娱乐使用，不具有任何法律效力
2. 禁止使用该工具生成虚假证件或进行任何违法活动
3. 上传的照片和生成的身份证图像会保存在服务器上，请确保不含敏感信息
4. 自动抠图功能对于背景简单、对比度高的照片效果较好
5. 系统会为每个生成的身份证图像分配唯一的文件名，以避免冲突
6. 生成的身份证图像包含正面和背面在同一张图片中

## API接口

### 生成身份证

**请求**：
```
POST /id_card_maker/generate
Content-Type: multipart/form-data
```

**参数**：
- `name`：姓名
- `gender`：性别
- `nationality`：民族（默认为"汉"）
- `birth_date`：出生日期（格式：YYYY年MM月DD日）
- `address`：住址
- `id_number`：身份证号码
- `issue_authority`：签发机关
- `valid_period`：有效期限
- `photo`：照片文件（可选）
- `auto_cutout`：是否启用自动抠图（true/false）

**响应**：
```json
{
  "success": true,
  "preview": {
    "combined": "/static/uploads/id_cards/id_card_12345678-1234-1234-1234-123456789012.png"
  },
  "message": "身份证生成成功，仅供预览"
}
```

## 未来计划

1. 添加更多身份证模板样式
2. 优化自动抠图算法，提高准确性
3. 支持分别生成正面和背面图像
4. 添加水印功能，防止滥用
5. 支持调整照片亮度、对比度等参数
