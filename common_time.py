# common_time.py
from time_utils import to_minutes, re_time

def get_intersection(slots_a, slots_b):
    """
    双指针法求两个空闲列表的交集。
    输入: [("10:00", "12:00"), ("14:00", "18:00")] 和 [("11:00", "13:00")]
    输出: [("11:00", "12:00")]
    """
    result = []
    i, j = 0, 0 # 双指针

    while i < len(slots_a) and j < len(slots_b):
        # 1. 把时间转成分钟，方便比较大小
        a_start, a_end = to_minutes(slots_a[i][0]), to_minutes(slots_a[i][1])
        b_start, b_end = to_minutes(slots_b[j][0]), to_minutes(slots_b[j][1])

        # 2. 求重叠区间：开始时间取更晚的，结束时间取更早的
        overlap_start = max(a_start, b_start)
        overlap_end = min(a_end, b_end)

        # 3. 如果有重叠（开始时间 < 结束时间），记录结果
        if overlap_start < overlap_end:
            result.append((re_time(overlap_start), re_time(overlap_end)))

        # 4. 双指针移动法则：谁的结束时间更早，谁就往后移动一格
        if a_end < b_end:
            i += 1
        else:
            j += 1

    return result


def get_all_common_free_time(all_people_free_schedules):
    """
    求多个人（N个人）的共同空闲时间。
    思路：A ∩ B ∩ C = (A ∩ B) ∩ C
    输入: {"张三": [{"day": 1, "free_slots": [("10:00", "12:00")]}], "李四": [...]}
    输出: [{"day": 1, "free_slots": [("11:00", "12:00")]}, ...]
    """
    if not all_people_free_schedules:
        return []

    # 获取人名列表
    people = list(all_people_free_schedules.keys())
    
    # 以第一人的时间表为基准
    common_schedule = all_people_free_schedules[people[0]]

    # 逐个与后面的每个人求交集
    for person in people[1:]:
        person_schedule = all_people_free_schedules[person]
        new_common_schedule = []

        # 遍历周一到周日
        for day in range(1, 8):
            # 找到当前人这一天的空闲列表
            day_slots = next((item["free_slots"] for item in person_schedule if item["day"] == day), [])
            # 找到共同空闲列表中这一天的空闲列表
            common_day_slots = next((item["free_slots"] for item in common_schedule if item["day"] == day), [])

            # 求这一天的交集
            day_slots.sort(key=lambda x: to_minutes(x[0]))
            common_day_slots.sort(key=lambda x: to_minutes(x[0]))#按开始时间重排,防止漏掉数据

            day_intersection = get_intersection(common_day_slots, day_slots)

            # 时长越长越靠前排序
            day_intersection.sort(key=lambda x: to_minutes(x[1]) - to_minutes(x[0]), reverse=True)

            new_common_schedule.append({
                "day": day,
                "free_slots": day_intersection
            })

        # 更新基准，继续和下一人求交集
        common_schedule = new_common_schedule

    return common_schedule