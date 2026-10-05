import csv

def read_csv(file_path):  #file_path为文件路径
    """读取CSV文件，返回课表列表（按输入顺序编成列表，元素为字典）"""
    records = []# 存储课表的列表（里面装的是字典）
    i = 0              #记数
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
                i += 1
            except (ValueError, KeyError) as e: 
                print(f"跳过一行异常数据，原因：{e}")
                continue  
                
    return records, i          #输出字典组成的列表和数据行数