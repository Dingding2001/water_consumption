import pandas as pd
import glob
import os

# 设置"Daily Plan"文件夹的路径
daily_plan_folder = os.path.join('.', 'Daily Plan')

# 确保文件夹存在
if not os.path.exists(daily_plan_folder):
    print("The 'Daily Plan' folder does not exist.")
    # 可以选择在这里创建文件夹，但在这个场景中我们假设它已经存在
    # os.makedirs(daily_plan_folder)
    exit()  # 或者你可以选择退出程序

# 查找"Daily Plan"文件夹中匹配的文件
matching_files = glob.glob(os.path.join(daily_plan_folder, 'emigration????year.csv'))
if matching_files:
    latest_file = max(matching_files, key=os.path.getmtime)  # 使用修改时间找到最新的

    # 加载CSV文件
    df_emigration = pd.read_csv(latest_file, usecols=['PID'])

    # 加载daily plan.csv（也假设它在"Daily Plan"文件夹中）
    df_daily_plan = pd.read_csv(os.path.join(daily_plan_folder, 'daily plan.csv'))

    # 找到并删除emigration文件中PID也在daily plan中的行
    mask = ~df_daily_plan['PID'].isin(df_emigration['PID'])
    filtered_df = df_daily_plan[mask]

    # 保存结果到"Daily Plan"文件夹下的daily plan.csv（覆盖原文件）
    filtered_df.to_csv(os.path.join(daily_plan_folder, 'daily plan.csv'), index=False)

    print(f"Processed data saved to {os.path.join(daily_plan_folder, 'daily plan.csv')}")
else:
    print("No matching emigration files found in the 'Daily Plan' folder.")