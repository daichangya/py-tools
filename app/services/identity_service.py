from app.utils.city_utils import city_utils

class IdentityService:
    """身份证信息服务"""
    
    @staticmethod
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

    @staticmethod
    def parse_id(id_number):
        """解析身份证信息"""
        # 提取出生日期
        year = int(id_number[6:10])
        month = int(id_number[10:12])
        day = int(id_number[12:14])
        birth_date = f"{year}-{month:02d}-{day:02d}"

        # 判断性别(奇数为男，偶数为女)
        gender = '男' if int(id_number[16]) % 2 else '女'

        # 获取地区代码
        area_code = id_number[:6]
        
        # 获取地区信息
        area_info = city_utils.get_area_by_code(area_code)

        # 计算属相和星座
        zodiac = IdentityService._get_zodiac(year)
        constellation = IdentityService._get_constellation(month, day)

        result = {
            'id_number': id_number,
            'birth_date': birth_date,
            'gender': gender,
            'area_code': area_code,
            'zodiac': zodiac,
            'constellation': constellation
        }

        if area_info:
            result['area_info'] = area_info

        return result

    @staticmethod
    def _get_zodiac(year):
        """根据年份计算属相"""
        zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇',
                  '马', '羊', '猴', '鸡', '狗', '猪']
        offset = (year - 4) % 12
        return zodiacs[offset]

    @staticmethod
    def _get_constellation(month, day):
        """根据月份和日期计算星座"""
        if (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "水瓶座"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "双鱼座"
        elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "白羊座"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "金牛座"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
            return "双子座"
        elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
            return "巨蟹座"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "狮子座"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "处女座"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
            return "天秤座"
        elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
            return "天蝎座"
        elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
            return "射手座"
        else:
            return "摩羯座"
