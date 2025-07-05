import os
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops


class IdCardMakerService:
    def __init__(self, app):
        self.app = app
        # 设置目录路径
        self.uploads_dir = os.path.join(app.static_folder, 'uploads', 'id_cards')
        self.usedres_dir = os.path.join(app.static_folder, 'idcard')

        # 确保目录存在
        os.makedirs(self.uploads_dir, exist_ok=True)
        os.makedirs(self.usedres_dir, exist_ok=True)

        # 设置字体路径
        self.name_font_path = os.path.join(self.usedres_dir, 'hei.ttf')
        self.other_font_path = os.path.join(self.usedres_dir, 'hei.ttf')
        self.bdate_font_path = os.path.join(self.usedres_dir, 'fzhei.ttf')
        self.id_font_path = os.path.join(self.usedres_dir, 'ocrb10bt.ttf')

    def _save_uploaded_file(self, file):
        """保存上传的文件"""
        if not file:
            return None

        # 生成唯一文件名
        unique_id = uuid.uuid4()
        filename = f"photo_{unique_id}.png"
        file_path = os.path.join(self.uploads_dir, filename)

        # 保存文件
        file.save(file_path)

        return file_path

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
                diff = sum(abs(pixel[i] - background_color[i]) for i in range(3))  # 只比较RGB通道
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

    def _create_id_card(self, name, gender, nationality, birth_year, birth_month, birth_day,
                        address, id_number, issue_authority, valid_period, photo_path, auto_cutout=False):
        """创建身份证（使用单一模板，上半部分是正面，下半部分是背面）"""
        # 加载empty.png作为模板
        empty_png_path = os.path.join(self.usedres_dir, 'empty.png')
        if not os.path.exists(empty_png_path):
            # 如果找不到empty.png，复制一份到usedres目录
            source_empty_png = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'empty.png')
            if os.path.exists(source_empty_png):
                import shutil
                shutil.copy(source_empty_png, empty_png_path)
            else:
                # 如果找不到empty.png，创建一个空白模板
                template = Image.new('RGB', (2000, 3000), (255, 255, 255))
                draw = ImageDraw.Draw(template)
                # 绘制边框
                draw.rectangle([(0, 0), (1999, 2999)], outline=(0, 0, 0), width=5)
                template.save(empty_png_path)

        # 打开模板 - 假设empty.png已经包含了正面和背面的布局
        id_card = Image.open(empty_png_path)

        # 添加标签
        draw = ImageDraw.Draw(id_card)
        font = ImageFont.truetype(self.other_font_path, 40) if self.other_font_path else ImageFont.load_default()
        # 假设模板的上半部分是正面，下半部分是背面
        height = id_card.height
        draw.text((20, height // 2 - 60), "正面", fill=(0, 0, 0), font=font)
        draw.text((20, height // 2 + 60), "反面", fill=(0, 0, 0), font=font)

        # 设置字体
        name_font = ImageFont.truetype(self.name_font_path, 72) if self.name_font_path else ImageFont.load_default()
        other_font = ImageFont.truetype(self.other_font_path, 60) if self.other_font_path else ImageFont.load_default()
        bdate_font = ImageFont.truetype(self.bdate_font_path, 60) if self.bdate_font_path else ImageFont.load_default()
        id_font = ImageFont.truetype(self.id_font_path, 72) if self.id_font_path else ImageFont.load_default()

        # 绘制正面信息（上半部分）
        draw.text((630, 690), name, fill=(0, 0, 0), font=name_font)
        draw.text((630, 840), gender, fill=(0, 0, 0), font=other_font)
        draw.text((1030, 840), nationality, fill=(0, 0, 0), font=other_font)

        # 绘制出生日期（添加年月日单位）
        draw.text((630, 980), birth_year, fill=(0, 0, 0), font=bdate_font)
        draw.text((950, 980), birth_month, fill=(0, 0, 0), font=bdate_font)
        draw.text((1150, 980), birth_day, fill=(0, 0, 0), font=bdate_font)

        # 绘制地址，每行最多11个字符
        start = 0
        loc = 1120
        while start + 11 < len(address):
            draw.text((630, loc), address[start:start + 11], fill=(0, 0, 0), font=other_font)
            start += 11
            loc += 100
        draw.text((630, loc), address[start:], fill=(0, 0, 0), font=other_font)

        # 绘制身份证号码
        draw.text((950, 1475), id_number, fill=(0, 0, 0), font=id_font)

        # 添加照片
        if photo_path:
            try:
                photo = Image.open(photo_path)

                if auto_cutout:
                    # 使用自动抠图功能
                    photo = photo.convert('RGBA')
                    id_card = self._change_background(photo, id_card, (500, 670), (690, 1500))
                else:
                    # 调整照片大小并直接粘贴
                    photo = photo.resize((500, 670))
                    photo = photo.convert('RGBA')
                    id_card.paste(photo, (1500, 690), mask=photo)

            except Exception as e:
                self.app.logger.error(f"添加照片失败: {str(e)}")

        # 由于_change_background方法现在只处理照片区域，不会影响其他部分，
        # 所以可以将背面信息的绘制移回到照片处理之后
        # 重新获取绘图对象，确保在最新的图像上绘制
        draw = ImageDraw.Draw(id_card)

        # 绘制背面信息（下半部分）
        # 假设模板的下半部分已经是背面的布局，直接使用gui.py中的坐标
        draw.text((1050, 2750), issue_authority, fill=(0, 0, 0), font=other_font)
        draw.text((1050, 2895), valid_period, fill=(0, 0, 0), font=other_font)

        return id_card

    def generate_id_card(self, name, gender, nationality, birth_date, address, id_number, issue_authority, valid_period,
                         photo, auto_cutout=False):
        """生成身份证"""
        try:
            # 解析出生日期，格式为"1990年01月01日"
            import re
            birth_match = re.match(r'(\d{4})年(\d{2})月(\d{2})日', birth_date)
            if birth_match:
                birth_year = birth_match.group(1)
                birth_month = birth_match.group(2)
                birth_day = birth_match.group(3)
            else:
                # 尝试其他格式，如果不匹配则分割
                birth_parts = birth_date.split('-')
                birth_year = birth_parts[0] if len(birth_parts) > 0 else ""
                birth_month = birth_parts[1] if len(birth_parts) > 1 else ""
                birth_day = birth_parts[2] if len(birth_parts) > 2 else ""

            # 保存上传的照片
            photo_path = self._save_uploaded_file(photo) if photo else None

            # 使用单一模板创建身份证
            id_card = self._create_id_card(
                name, gender, nationality, birth_year, birth_month, birth_day,
                address, id_number, issue_authority, valid_period, photo_path, auto_cutout
            )

            # 生成唯一文件名
            unique_id = uuid.uuid4()
            id_card_filename = f"id_card_{unique_id}.png"

            # 保存生成的身份证图像
            id_card_path = os.path.join(self.uploads_dir, id_card_filename)
            id_card.save(id_card_path)

            # 生成URL
            id_card_url = f"/static/uploads/id_cards/{id_card_filename}"

            return {
                'success': True,
                'preview': {
                    'combined': id_card_url
                },
                'message': '身份证生成成功，仅供预览'
            }
        except Exception as e:
            self.app.logger.error(f"生成身份证失败: {str(e)}")
            return {
                'success': False,
                'message': f'生成身份证失败: {str(e)}'
            }