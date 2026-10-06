
#下为读取CSV文件的函数
import csv

def read_csv(file_path):  #file_path为文件路径
    """读取CSV文件，返回课表列表（按输入顺序编成列表，元素为字典）"""
    records = []# 存储课表的列表（里面装的是字典）
  
    with open(file_path, 'r', encoding='utf-8-sig') as f:#打开路径的文件，utf-8-sig是为了防止中文乱码 
        reader = csv.DictReader(f)           #读取为字典
        
        for row in reader:                   #循环按行读取

            try:
                day = int(row['星期几'])         
                course_name = row['课程名']      
                start_time = row['开始时间']       
                end_time = row['结束时间']    #从提取的一行的字典中提取数据并转换格式
                
                record = {
                    "day": day,
                    "name": course_name,
                    "start": start_time,
                    "end": end_time
                }                         #组织成一个字典
                records.append(record)    #加到records列表中
              
            except (ValueError, KeyError) as e: 
                print(f"跳过一行异常数据，原因：{e}")
                continue  
                
    return records      #输出字典组成的列表













#下为手动输入课程信息的函数
from time_utils import is_valid_time 
def hand_input():
    """手动录入课程信息，返回一个人的课表列表"""
    # 存储课表的列表（里面装的是字典）
    

    records = [] 
    
    print("请输入课程信息，格式为：星期几,课程名,开始时间,结束时间")
    print("例如：1,高等数学,08:00,09:40")
    print("输入 q 结束录入。")
    while True:
        # 1. 获取输入并去掉两端空格
        user_in = input("请输入: ").strip()
        
        # 2. 判断结束
        if user_in.lower() == 'q':
            print("录入结束。")
            break
            
        # 3. 解析输入（核心逻辑）
        # 防止用户输入错误，比如忘了加逗号
        parts = user_in.split(',')  # 用逗号切割
        
        if len(parts) != 4:
            print("格式错误！请确保用英文逗号分隔，且只有4个部分。请重新输入。")
            continue # 跳过本次循环，让用户重新输入
            
        try:
            day = int(parts[0])         # 星期几转成整数
            course_name = parts[1]      # 课程名
            start_time = parts[2]       # 开始时间
            end_time = parts[3]         # 结束时间
            if not is_valid_time(start_time) or not is_valid_time(end_time):
                print("时间格式错误！请确保时间为 HH:MM 格式（如 08:00），且小时在 0-23，分钟在 0-59。")
                continue
            # 4. 存入列表（这里用字典存，你也可以用 Course 对象）
            record = {
                "day": day,
                "name": course_name,
                "start": start_time,
                "end": end_time
            }
            records.append(record)
            print("添加成功！")
            
        except ValueError:
            print("格式错误！星期几必须是数字。请重新输入。")
            continue # 跳过本次循环，让用户重新输入
    return records