from PIL import Image, ImageDraw, ImageFont
import os
import random

# 确保目标目录存在
output_dir = "app/static/images/festivals"
os.makedirs(output_dir, exist_ok=True)

# 定义节日和对应的图片文件名
festivals = {
    "春节": ["spring_festival_1.jpg", "spring_festival_2.jpg", "spring_festival_3.jpg"],
    "元宵节": ["lantern_festival_1.jpg", "lantern_festival_2.jpg"],
    "清明节": ["qingming_1.jpg", "qingming_2.jpg"],
    "端午节": ["dragon_boat_1.jpg", "dragon_boat_2.jpg"],
    "中秋节": ["mid_autumn_1.jpg", "mid_autumn_2.jpg"],
    "国庆节": ["national_day_1.jpg", "national_day_2.jpg"],
    "元旦": ["new_year_1.jpg", "new_year_2.jpg"],
    "圣诞节": ["christmas_1.jpg", "christmas_2.jpg"]
}

# 定义颜色映射
festival_colors = {
    "春节": (255, 0, 0),      # 红色
    "元宵节": (255, 165, 0),  # 橙色
    "清明节": (0, 128, 0),    # 绿色
    "端午节": (0, 255, 0),    # 亮绿色
    "中秋节": (255, 215, 0),  # 金色
    "国庆节": (255, 0, 0),    # 红色
    "元旦": (0, 0, 255),      # 蓝色
    "圣诞节": (255, 0, 0)     # 红色
}

def generate_festival_image(festival, filename, width=800, height=600):
    """生成一个简单的节日图片"""
    # 创建一个彩色背景
    bg_color = festival_colors.get(festival, (200, 200, 200))
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # 添加一些随机装饰
    for _ in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=3)

    # 添加节日名称
    try:
        # 尝试加载一个字体，如果失败则使用默认字体
        font = ImageFont.truetype("Arial", 60)
    except IOError:
        font = ImageFont.load_default()

    # 计算文本位置使其居中
    text = festival
    text_width = draw.textlength(text, font=font)
    text_position = ((width - text_width) / 2, height / 2 - 30)

    # 绘制文本
    draw.text(text_position, text, fill=(255, 255, 255), font=font)

    # 保存图片
    output_path = os.path.join(output_dir, filename)
    image.save(output_path)
    print(f"生成图片: {output_path}")

# 为每个节日生成图片
for festival, filenames in festivals.items():
    for filename in filenames:
        generate_festival_image(festival, filename)

print("所有节日图片生成完成！")
