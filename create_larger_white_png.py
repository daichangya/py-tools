from PIL import Image
import os

# 创建一个80x100像素的白色图片
width, height = 60, 80
white_image = Image.new('RGB', (width, height), color='white')

# 保存图片
output_path = "app/static/images/white.png"
white_image.save(output_path)

print(f"更大的白色PNG图片已创建: {os.path.abspath(output_path)}")
print(f"尺寸: {width}x{height} 像素")
