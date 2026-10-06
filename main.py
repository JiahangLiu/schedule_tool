# ========== 文件导入模块 ==========
from inputs import hand_input
from inputs import read_csv
from time_utils import to_minutes
from free_time import generate_weekly_free_time
from outputs import print_table
from outputs import print_free_time
from outputs import print_common_free_time  # 引入新的打印函数
from common_time import get_all_common_free_time # 引入求交集模块

# ========== 主函数 ==========
def main():
    print("请选择输入方式：")
    choice = input("手动输入请输入 0；CSV读入请输入 1：").strip()

    all_people_records: dict[str, list[dict]] = {}  # 存储所有人的课程表

    if choice == "0":
        number_of_people = int(input("请输入人数：").strip())
        for _ in range(number_of_people):
            name = input("请输入姓名：").strip()
            all_people_records[name] = hand_input() 
    elif choice == "1":
        number_of_people = int(input("请输入人数：").strip())
        for _ in range(number_of_people):
            name = input("请输入姓名：").strip()
            file_path = input(f"请输入 {name} 的CSV文件路径：").strip()
            all_people_records[name] = read_csv(file_path)
    else:
        print("选择错误，程序退出。")
        return

    # 检查是否读到了数据
    if not all_people_records:
        print("没有读到任何课程数据。")
        return

    # ========== 1. 打印每个人的课表 ==========
    for k, v in all_people_records.items():
        print_table(k, v)

    # ========== 2. 计算并打印每个人的空闲时间，并保存结果 ==========
    all_people_free_schedules = {} # 用来存 {姓名: [{"day":1, "free_slots":...}, ...]}
    for k, v in all_people_records.items():
        sorted_records = sorted(v, key=lambda x: (x["day"], to_minutes(x["start"])))
        free_time_result = generate_weekly_free_time(sorted_records)
        
        # 打印这个人的空闲时间
        print_free_time(k, v) 
        
        # 保存起来，给需求3用
        all_people_free_schedules[k] = free_time_result

    # ========== 3. 计算并打印所有人的共同空闲时间 ==========
    print("\n正在计算所有人的共同空闲时间...")
    common_free_schedule = get_all_common_free_time(all_people_free_schedules)
    print_common_free_time(common_free_schedule)

if __name__ == "__main__":
    main()