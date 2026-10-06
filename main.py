# ========== 文件导入模块 ==========
from inputs import hand_input  # 引入 hand_input.py
from inputs import read_csv      # 引入 csv_input.py
from time_utils import to_minutes       # 引入 minute.py
from free_time import generate_weekly_free_time  # 引入 free_time.py

# ========== 主函数 ==========
def main():
    print("请选择输入方式：")
    choice = input("手动输入请输入 0；CSV读入请输入 1：").strip()

    # 准备空列表接收数据
    records: list[dict] = []

    if choice == "0":
        # 手动输入
        records = hand_input() 
    elif choice == "1":
        # CSV读入
        file_path = input("请输入CSV文件路径：").strip()
        records = read_csv(file_path) 
    else:
        print("选择错误，程序退出。")
        return

    # 如果读取失败或者是空数据，直接退出
    if not records:
        print("没有读到任何课程数据。")
        return

    # ========== 打印课表 ==========
    print("\n{:*^60}".format("课程表"))
    sorted_records = sorted(records, key=lambda x: (x["day"], to_minutes(x["start"])))#按开始时间和日期排序，方便正确调用
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
    free_time_result = generate_weekly_free_time(sorted_records)
    print("\n{:*^60}".format("本周空闲时间表"))
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

if __name__ == "__main__":
    main()                    #预防文件错误导入时运行出错