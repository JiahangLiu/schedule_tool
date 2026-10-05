# ========== 文件导入模块 ==========
from hand_input import start_input  # 引入 hand_input.py
from csv_input import read_csv      # 引入 csv_input.py
from time_change import to_minutes       # 引入 minute.py

# ========== 主函数 ==========
def main():
    print("请选择输入方式：")
    choice = input("手动输入请输入 0；CSV读入请输入 1：").strip()

    # 准备空列表接收数据
    records = []

    if choice == "0":
        # 手动输入
        records = start_input() 
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
    sorted_records = sorted(records, key=lambda x: to_minutes(x["start"]))#按开始时间排序，方便打印
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

if __name__ == "__main__":
    main()                    #预防文件错误导入时运行出错