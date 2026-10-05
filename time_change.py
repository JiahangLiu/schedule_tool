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