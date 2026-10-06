

#下为检测输入格式的函数
def is_valid_time(t: str) -> bool:
    try:
        h, m = t.split(':')
        h, m = int(h), int(m)
        return 0 <= h <= 23 and 0 <= m <= 59
    except ValueError:
        return False




#下为将时间从分钟转换回 HH:MM 格式的函数
def to_minutes(t: str) -> int:
    try:
        t = t.strip().replace('：', ':')  # 处理中文全角冒号并去掉两端空格
        h, m = t.split(':')
        h, m = int(h), int(m)
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError("时间越界，小时应在 0-23，分钟应在 0-59")
        return h * 60 + m #将小时和分钟转换为总分钟数
    except (ValueError, IndexError):
        raise ValueError("有时间格式错误，请检查，应为 HH:MM 格式")    





# 下为将时间从分钟转换回 HH:MM 格式的函数
def re_time(minutes: int) -> str:
    """将分钟数转换回 HH:MM 字符串"""
    h = minutes // 60  # 整除了小时
    m = minutes % 60   # 取余得到分钟
    return f"{h:02d}:{m:02d}"  # 格式化为两位数，如 8 变成 08