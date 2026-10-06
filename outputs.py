from time_utils import to_minutes
from free_time import generate_weekly_free_time




    # ========== 打印课表 ==========
def print_table(k,v):
    print("\n{:*^60}".format("{}课程表".format(k)))
    sorted_records = sorted(v, key=lambda x: (x["day"], to_minutes(x["start"])))#按开始时间和日期排序，方便正确调用
    # 外层循环：按星期几（1-7）遍历
    for day in range(1, 8):
        print("{:*^60}".format(f"星期{day}"))
        
        has_course = False # 用来记录今天有没有课
        # 内层循环：遍历所有课程，找出属于当前 day 的课
        for course in sorted_records: # 这里要遍历 sorted_records 列表
            if course["day"] == day: # 判断这门课是不是今天的
                has_course = True
                
                # 数据间用 | 隔开
                print(f"  {course['start']} - {course['end']}  |  {course['name']}")
        
        if not has_course:
            print("  无课程安排")
            
    print("\n{:*^60}".format("课表结束"))















    # ========== 计算并打印空闲时间 ==========
    # 获取所有天的空闲时间数据
def print_free_time(k,v):
    sorted_records = sorted(v, key=lambda x: (x["day"], to_minutes(x["start"])))#按开始时间和日期排序，方便正确调用
    free_time_result = generate_weekly_free_time(sorted_records)
    print("\n{:*^60}".format("{}本周空闲时间表".format(k)))
    for item in free_time_result:
        day = item["day"]
        free_slots = item["free_slots"]
        
        print(f"\n【星期{day}】")
        if not free_slots:
            print("  今日无空闲")
        else:
            for start, end in free_slots:
                # 计算时长（分钟）并在打印时展示
                duration = to_minutes(end) - to_minutes(start)
                print(f"  {start} - {end}   (时长: {duration} 分钟)")
                
    print("\n{:*^60}".format("空闲时间表结束"))













# ===========打印共同空闲时间============
from time_utils import to_minutes

def print_common_free_time(common_schedule):
    """打印所有人的共同空闲时间"""
    print("\n{:*^60}".format("所有人共同空闲时间表"))
    
    for item in common_schedule:
        day = item["day"]
        free_slots = item["free_slots"]
        
        print(f"\n【星期{day}】")
        if not free_slots:
            print("  今日无共同空闲")
        else:
            for start, end in free_slots:
                duration = to_minutes(end) - to_minutes(start)
                print(f"  {start} - {end}   (时长: {duration} 分钟)")
                
    print("\n{:*^60}".format("共同空闲时间表结束"))