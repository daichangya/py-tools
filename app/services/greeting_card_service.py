from datetime import datetime
import random
from zhdate import ZhDate



class GreetingCardService:
    def __init__(self):
        self.festivals = {
            "春节": {"month": 1, "day": 1, "lunar": True},
            "元宵节": {"month": 1, "day": 15, "lunar": True},
            "情人节": {"month": 2, "day": 14, "lunar": False},
            "清明节": {"month": 4, "day": 5, "lunar": False},
            "端午节": {"month": 5, "day": 5, "lunar": True},
            "中秋节": {"month": 8, "day": 15, "lunar": True},
            "国庆节": {"month": 10, "day": 1, "lunar": False},
            "元旦": {"month": 1, "day": 1, "lunar": False},
            "圣诞节": {"month": 12, "day": 25, "lunar": False}
        }

        self.greetings = {
            "春节": [
                "愿新春佳节带给你幸福安康，阖家欢乐！",
                "祝您春节快乐，万事如意，阖家幸福！",
                "新年新气象，祝您事业腾飞，家庭美满！",
                "恭贺新春，万事大吉，阖家幸福安康！",
                "金牛贺岁迎新春，万事如意展宏图。祝您新春快乐！",
                "爆竹声中一岁除，春风送暖入屠苏。祝您春节快乐！",
                "春回大地，万象更新，祝您新春吉祥，阖家欢乐！"
            ],
            "元宵节": [
                "元宵节快乐，愿您与家人团团圆圆！",
                "花好月圆人团圆，祝您元宵节快乐！",
                "明月照人心，祝您元宵佳节快乐！",
                "月上柳梢头，人约黄昏后。祝您元宵节快乐！",
                "火树银花合，星桥铁锁开。愿您元宵佳节阖家欢乐！",
                "东风夜放花千树，更吐明月千江水。祝您元宵节快乐！"
            ],
            "清明节": [
                "清明时节雨纷纷，愿您平安度佳节。",
                "寄托哀思，愿逝者安息，生者坚强。",
                "春和景明，愿您清明节安康。",
                "清明祭扫，慎终追远，愿逝者安息，生者康泰。",
                "细雨清明，缅怀追思，愿您平安喜乐。",
                "清明时节，寄托哀思，愿逝者安息，生者坚强。"
            ],
            "端午节": [
                "端午安康，愿您粽香情浓！",
                "五月初五，祝您端午节快乐！",
                "龙舟竞渡，粽香四溢，祝您端午安康！",
                "艾叶飘香，粽叶飘香，祝您端午节安康！",
                "五月榴花妖艳烘，绿扬才子有骚情。端午安康！",
                "午日龙舟竞渡，粽香情意绵绵，祝您端午节快乐！"
            ],
            "中秋节": [
                "但愿人长久，千里共婵娟。中秋快乐！",
                "月圆人团圆，祝您中秋节快乐！",
                "花好月圆，愿您中秋佳节阖家欢乐！",
                "海上生明月，天涯共此时。祝您中秋节快乐！",
                "明月几时有，把酒问青天。愿您中秋佳节阖家团圆！",
                "月到中秋分外明，人到中秋情更浓。祝您中秋快乐！"
            ],
            "国庆节": [
                "祝您国庆节快乐，祖国繁荣昌盛！",
                "欢度国庆，祝您假期愉快！",
                "金秋送爽，祝您国庆节快乐！",
                "举国同庆，普天同乐，祝您国庆节快乐！",
                "祖国生日，举国欢庆，愿您假期愉快！",
                "金风送爽，丹桂飘香，祝您国庆节快乐！"
            ],
            "元旦": [
                "新年新气象，祝您元旦快乐！",
                "辞旧迎新，愿您新年快乐！",
                "元旦佳节，祝您万事如意！",
                "新年伊始，万象更新，祝您元旦快乐！",
                "辞旧迎新之际，祝您新年快乐，万事如意！",
                "元旦钟声敲响，愿您新的一年事事顺心！"
            ],
            "圣诞节": [
                "Merry Christmas! 圣诞快乐！",
                "愿圣诞带给您温暖与祝福！",
                "圣诞快乐，愿您心想事成！",
                "铃儿响叮当，圣诞节快乐！愿您佳节愉快！",
                "平安夜的钟声即将敲响，愿您圣诞快乐，新年吉祥！",
                "白雪纷飞的季节，为您送上最温暖的圣诞祝福！"
            ],
            "情人节": [
                "愿爱情如玫瑰绽放，祝您情人节快乐！",
                "有你的日子里，每天都是情人节。情人节快乐！",
                "愿您的爱情甜蜜浪漫，情人节快乐！",
                "爱情是生命中最美的风景，祝您情人节快乐！",
                "让我们一起谱写爱的篇章，情人节快乐！",
                "愿天下有情人终成眷属，情人节快乐！"
            ]
        }

        # 图片库（实际使用时需要确保这些图片存在）
        self.images = {
            "春节": [
                "spring_festival_1.jpg",  # 红灯笼和春联
                "spring_festival_2.jpg",  # 烟花绽放
                "spring_festival_3.jpg",  # 福字和年画
                "spring_festival_4.jpg",  # 新春花卉
                "spring_festival_5.jpg"   # 喜庆场景
            ],
            "元宵节": [
                "lantern_festival_1.jpg", # 花灯展示
                "lantern_festival_2.jpg", # 元宵汤圆
                "lantern_festival_3.jpg", # 灯会场景
                "lantern_festival_4.jpg"  # 月夜花灯
            ],
            "情人节": [
                "valentine_1.jpg",        # 红玫瑰
                "valentine_2.jpg",        # 心形装饰
                "valentine_3.jpg",        # 浪漫场景
                "valentine_4.jpg",        # 礼物盒
                "valentine_5.jpg"         # 烛光晚餐
            ],
            "清明节": [
                "qingming_1.jpg",        # 春雨景色
                "qingming_2.jpg",        # 柳枝新芽
                "qingming_3.jpg",        # 踏青场景
                "qingming_4.jpg"         # 春日花卉
            ],
            "端午节": [
                "dragon_boat_1.png",     # 龙舟竞渡
                "dragon_boat_2.png",     # 香粽特写
                "dragon_boat_3.png",     # 艾草和菖蒲
                "dragon_boat_4.png",     # 传统习俗
                "dragon_boat_5.png"      # 节日美食
            ],
            "中秋节": [
                "mid_autumn_1.jpg",      # 圆月夜景
                "mid_autumn_2.jpg",      # 月饼特写
                "mid_autumn_3.jpg",      # 花好月圆
                "mid_autumn_4.jpg",      # 团圆场景
                "mid_autumn_5.jpg"       # 赏月图景
            ],
            "国庆节": [
                "national_day_1.jpg",    # 天安门广场
                "national_day_2.jpg",    # 五星红旗
                "national_day_3.jpg",    # 烟花绽放
                "national_day_4.jpg",    # 节日庆典
                "national_day_5.jpg"     # 欢庆场景
            ],
            "元旦": [
                "new_year_1.jpg",        # 跨年烟花
                "new_year_2.jpg",        # 新年钟声
                "new_year_3.jpg",        # 庆祝场景
                "new_year_4.jpg",        # 新年装饰
                "new_year_5.jpg"         # 倒计时场景
            ],
            "圣诞节": [
                "christmas_1.jpg",       # 圣诞树
                "christmas_2.jpg",       # 圣诞老人
                "christmas_3.jpg",       # 礼物盒
                "christmas_4.jpg",       # 圣诞装饰
                "christmas_5.jpg"        # 雪景场景
            ]
        }

    def get_next_festival(self):
        """获取下一个即将到来的节日"""
        today = datetime.now().date()
        current_year = today.year
        current_month = today.month
        current_day = today.day

        next_festival = None
        min_days_diff = float('inf')

        for festival, info in self.festivals.items():
            month = info['month']
            day = info['day']
            lunar = info['lunar']

            # 处理公历节日
            if not lunar:
                festival_date = datetime(current_year, month, day).date()
                if festival_date < today:
                    festival_date = datetime(current_year + 1, month, day).date()
                days_diff = (festival_date - today).days
            else:
                # 处理农历节日
                try:
                    # 尝试获取今年的农历节日对应的公历日期
                    lunar_date = ZhDate(current_year, month, day)
                    solar_date = lunar_date.to_datetime().date()

                    # 如果今年的农历节日已经过去，则计算明年的
                    if solar_date < today:
                        lunar_date = ZhDate(current_year + 1, month, day)
                        solar_date = lunar_date.to_datetime().date()

                    days_diff = (solar_date - today).days
                except ValueError:
                    # 处理特殊情况，如农历没有对应的日期（如闰月问题）
                    print(f"警告: 农历 {current_year}年{month}月{day}日不存在，跳过 {festival}")
                    continue

            if days_diff < min_days_diff:
                min_days_diff = days_diff
                next_festival = festival

        return next_festival

    def get_festival_date(self, festival):
        """获取指定节日的日期信息"""
        if festival not in self.festivals:
            return None
            
        info = self.festivals[festival]
        month = info['month']
        day = info['day']
        lunar = info.get('lunar', False)
        
        today = datetime.now().date()
        current_year = today.year
        
        # 处理公历节日
        if not lunar:
            festival_date = datetime(current_year, month, day).date()
            if festival_date < today:
                festival_date = datetime(current_year + 1, month, day).date()
        else:
            # 处理农历节日
            try:
                # 尝试获取今年的农历节日对应的公历日期
                lunar_date = ZhDate(current_year, month, day)
                festival_date = lunar_date.to_datetime().date()

                # 如果今年的农历节日已经过去，则计算明年的
                if festival_date < today:
                    lunar_date = ZhDate(current_year + 1, month, day)
                    festival_date = lunar_date.to_datetime().date()
            except ValueError:
                # 处理特殊情况，如农历没有对应的日期
                return None
        
        days_until = (festival_date - today).days
        
        return {
            "date": festival_date,
            "is_lunar": lunar,
            "days_until": days_until
        }
        
    def generate_greeting_card(self, festival=None, sender=None, receiver=None):
        """
        生成节日贺卡
        
        Args:
            festival: 节日名称，如果为None则使用下一个节日
            sender: 发送者姓名
            receiver: 接收者姓名
        """
        if festival is None:
            festival = self.get_next_festival()

        if festival not in self.greetings:
            return None

        greeting = random.choice(self.greetings[festival])
        image = random.choice(self.images[festival])

        # 获取节日日期信息
        festival_date_info = self.get_festival_date(festival)
        
        # 添加当前日期
        now = datetime.now()

        # 不再在greeting中包含发送者和接收者信息，而是作为单独的字段返回
        card_data = {
            "festival": festival,
            "greeting": greeting,
            "image": image,
            "is_next_festival": festival == self.get_next_festival(),
            "now": now,  # 当前日期
            "sender": sender,
            "receiver": receiver,
            "layout": {
                "image_layer": 0,  # 图片在底层
                "text_layer": 1    # 文字在上层
            }
        }
        
        # 添加节日日期信息
        if festival_date_info:
            card_data.update({
                "festival_date": festival_date_info["date"],
                "is_lunar": festival_date_info["is_lunar"],
                "days_until": festival_date_info["days_until"]
            })
            
        return card_data

    def get_all_festivals(self):
        """获取所有节日列表"""
        return list(self.festivals.keys())
