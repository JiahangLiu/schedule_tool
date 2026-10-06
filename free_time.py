

from time_utils import is_valid_time
from time_utils import to_minutes
from time_utils import re_time



# 一天内合并相邻课的并输出空闲时间的函数
def merge_slots(busy_slots):
    """
    busy_slots: 一个包含 (开始分钟, 结束分钟) 元组的列表
    返回: 合并后的连续忙碌时间段列表
    """
    if not busy_slots:
        return []

    # 1. 按开始时间排序
    busy_slots.sort(key=lambda x: x[0])
    
    # 2. 核心合并逻辑：把第一个当作基准，后续的尝试合并到最后一个元素上
    merged = [busy_slots[0]]  # 放入第一个元素作为初始基准
    
    for current_start, current_end in busy_slots[1:]:
        last_start, last_end = merged[-1]  # 取出已合并列表的最后一个
        
        # 如果当前课的开始时间 和 上一节课的结束时间 间隔 <= 20 分钟
        if current_start - last_end <= 20:
            # 合并：新的结束时间是这两个的最大值（防止出现包含关系）
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # 不能合并，直接作为一个新时间段追加
            merged.append((current_start, current_end))
            
    return merged


# 算一天内所有人的空闲时间（结合合并后的忙碌时间段）
def calculate_free_time(busy_slots, day_start=480, day_end=1320):
    """
    busy_slots: 已经合并过的忙碌时间段列表 [(480, 650), (800, 900)]
    day_start: 每天可用总范围的开始（默认 08:00 = 480）
    day_end: 每天可用总范围的结束（默认 22:00 = 1320）
    返回: 空闲时间段列表
    """
    free_slots = []
    
    # 1. 处理第一节课之前的空闲（day_start 到 第一个忙碌块的开始）
    if busy_slots[0][0] > day_start:
        free_slots.append((day_start, busy_slots[0][0]))
        
    # 2. 处理忙碌块之间的空闲
    for i in range(len(busy_slots) - 1):
        prev_end = busy_slots[i][1]
        next_start = busy_slots[i+1][0]
        if next_start > prev_end:  # 确实有空白
            free_slots.append((prev_end, next_start))
            
    # 3. 处理最后一节课之后的空闲（最后一个忙碌块的结束 到 day_end）
    if day_end > busy_slots[-1][1]:
        free_slots.append((busy_slots[-1][1], day_end))
        
    return free_slots


# 整合所有天数的入口函数
def generate_weekly_free_time(sorted_records, day_start=480, day_end=1320):
    """
    sorted_records: 经过整体排序的课程列表（包含所有天）
    返回: 一个包含每一天空闲时间表的大列表
    """
    final_result = []
    
    # 遍历周一到周日
    for day in range(1, 8):
        day_course_list = []
        for course in sorted_records:
            if course["day"] == day:
                # 提取这门课的开始和结束分钟，存入临时列表
                start_min = to_minutes(course["start"])
                end_min = to_minutes(course["end"])
                day_course_list.append((start_min, end_min))
                
        # 如果今天有课，就算空闲时间；今天没课，全天都是空闲
        if day_course_list:
            merged_busy = merge_slots(day_course_list)
            free_slots = calculate_free_time(merged_busy, day_start, day_end) # 传进去
        else:
            free_slots = [(day_start, day_end)] # 直接用变量，不再写死
            
        # 把分钟数转回 HH:MM 格式，方便打印
        formatted_free = [(re_time(s), re_time(e)) for s, e in free_slots]
        
        # 按照空闲时长从长到短排序（题目要求：越长越靠前）
        formatted_free.sort(key=lambda x: to_minutes(x[1]) - to_minutes(x[0]), reverse=True)
        
        final_result.append({"day": day, "free_slots": formatted_free})
        
    return final_result