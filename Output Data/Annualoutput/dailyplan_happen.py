#%%
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image

years = list(range(2010, 2054))
output_folder = os.path.join(os.getcwd(), "weekday_dailyplan")
os.makedirs(output_folder, exist_ok=True)

max_count_all_years = 0

for year in years:
    csv_file_path = f"weekday{year}year.csv"
    if os.path.isfile(csv_file_path):
        
        df = pd.read_csv(csv_file_path, usecols=['firstbath-happen', 'secondbath-happen', 'breakfast-happen', 
                                                 'lunch-happen', 'dinner-happen', 'washclothes-happen', 
                                                 'clean-happen', 'footbath-happen'])

        data = df.to_dict(orient='list')

        half_hour_bins = range(0, 1441, 60)
        df_intervals = {activity: pd.cut(times, bins=half_hour_bins).value_counts().sort_index() for activity, times in data.items()}

        max_counts = max([len(counts) for counts in df_intervals.values()])
        max_count_all_years = max(max_count_all_years, max([counts.max() for counts in df_intervals.values()]))

for year in years:
    csv_file_path = f"weekday{year}year.csv"
    if os.path.isfile(csv_file_path):
        
        df = pd.read_csv(csv_file_path, usecols=['firstbath-happen', 'secondbath-happen', 'breakfast-happen', 
                                                 'lunch-happen', 'dinner-happen', 'washclothes-happen', 
                                                 'clean-happen', 'footbath-happen'])
        # 创建一个字典，用于将旧列名映射到新列名（去掉 "-happen" 后缀）
        new_columns = {col: col.replace('-happen', '') for col in df.columns}
        df = df.rename(columns=new_columns)

        data = df.to_dict(orient='list')

        half_hour_bins = range(0, 1441, 60)
        df_intervals = {activity: pd.cut(times, bins=half_hour_bins).value_counts().sort_index() for activity, times in data.items()}

        max_counts = max([len(counts) for counts in df_intervals.values()])

        for activity, counts in df_intervals.items():
            if len(counts) < max_counts:
                missing_intervals = pd.cut([], bins=half_hour_bins).value_counts().sort_index()
                df_intervals[activity] = counts.reindex(missing_intervals.index, fill_value=0)

        plt.rcParams['font.sans-serif'] = ['Times New Roman']

        fig, ax = plt.subplots()
        bottom = None
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray']

        for i, (activity, counts) in enumerate(df_intervals.items()):
            if bottom is None:
                bottom = pd.Series(0, index=counts.index)
            plt.bar(range(len(counts)), counts, width=0.8, alpha=0.7, label=activity, bottom=bottom, color=colors[i])
            bottom += counts

        x_labels = [f'{interval.left//60:02d}:{interval.left%60:02d}' if interval in counts.index else '...' for interval in df_intervals['firstbath'].index]
        ax.set_xticks(range(len(counts)))
        ax.set_xticklabels(x_labels, rotation=45)
        ax.set_xlabel('Time')
        ax.set_ylabel('Number')
        ax.set_title(f'Weekday Activities Happen Time ({year})')

        ax.set_ylim(0, max_count_all_years * 1.5)  # 使用所有年份中的最大计数作为纵坐标的上限

        ax.legend(loc='upper left', framealpha=0.3, prop={'size': 10})

        plt.tight_layout()
        
        output_filename = f"Weekday Activities Happen Time {year}.png"
        output_path = os.path.join(output_folder, output_filename)
        plt.savefig(output_path, dpi=300)
        plt.close()

# 生成 GIF
images = [img for img in os.listdir(output_folder) if img.endswith(".png")]

# 生成 GIF 图
gif_path = "weekday_dailyplan/output.gif"
with Image.open(os.path.join(output_folder, images[0])) as img:
    img.save(gif_path, save_all=True, append_images=[Image.open(os.path.join(output_folder, img)) for img in images[1:]], duration=800, loop=0)

print(f"成功生成 GIF 文件: {gif_path}")

#%%
# 清空全局命名空间中的所有变量
globals().clear()

#%%
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image

years = list(range(2010, 2054))
output_folder = os.path.join(os.getcwd(), "weekend_dailyplan")
os.makedirs(output_folder, exist_ok=True)

max_count_all_years = 0

for year in years:
    csv_file_path = f"weekend{year}year.csv"
    if os.path.isfile(csv_file_path):
        
        df = pd.read_csv(csv_file_path, usecols=['firstbath-happen', 'secondbath-happen', 'breakfast-happen', 
                                                 'lunch-happen', 'dinner-happen', 'washclothes-happen', 
                                                 'clean-happen', 'footbath-happen'])

        data = df.to_dict(orient='list')

        half_hour_bins = range(0, 1441, 60)
        df_intervals = {activity: pd.cut(times, bins=half_hour_bins).value_counts().sort_index() for activity, times in data.items()}

        max_counts = max([len(counts) for counts in df_intervals.values()])
        max_count_all_years = max(max_count_all_years, max([counts.max() for counts in df_intervals.values()]))

for year in years:
    csv_file_path = f"weekend{year}year.csv"
    if os.path.isfile(csv_file_path):
        
        df = pd.read_csv(csv_file_path, usecols=['firstbath-happen', 'secondbath-happen', 'breakfast-happen', 
                                                 'lunch-happen', 'dinner-happen', 'washclothes-happen', 
                                                 'clean-happen', 'footbath-happen'])
        # 创建一个字典，用于将旧列名映射到新列名（去掉 "-happen" 后缀）
        new_columns = {col: col.replace('-happen', '') for col in df.columns}
        df = df.rename(columns=new_columns)

        data = df.to_dict(orient='list')

        half_hour_bins = range(0, 1441, 60)
        df_intervals = {activity: pd.cut(times, bins=half_hour_bins).value_counts().sort_index() for activity, times in data.items()}

        max_counts = max([len(counts) for counts in df_intervals.values()])

        for activity, counts in df_intervals.items():
            if len(counts) < max_counts:
                missing_intervals = pd.cut([], bins=half_hour_bins).value_counts().sort_index()
                df_intervals[activity] = counts.reindex(missing_intervals.index, fill_value=0)

        plt.rcParams['font.sans-serif'] = ['Times New Roman']

        fig, ax = plt.subplots()
        bottom = None
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray']

        for i, (activity, counts) in enumerate(df_intervals.items()):
            if bottom is None:
                bottom = pd.Series(0, index=counts.index)
            plt.bar(range(len(counts)), counts, width=0.8, alpha=0.7, label=activity, bottom=bottom, color=colors[i])
            bottom += counts

        x_labels = [f'{interval.left//60:02d}:{interval.left%60:02d}' if interval in counts.index else '...' for interval in df_intervals['firstbath'].index]
        ax.set_xticks(range(len(counts)))
        ax.set_xticklabels(x_labels, rotation=45)
        ax.set_xlabel('Time')
        ax.set_ylabel('Number')
        ax.set_title(f'Weekend Activities Happen Time ({year})')

        ax.set_ylim(0, max_count_all_years * 1.5)  # 使用所有年份中的最大计数作为纵坐标的上限

        ax.legend(loc='upper left', framealpha=0.3, prop={'size': 10})

        plt.tight_layout()
        
        output_filename = f"Weekend Activities Happen Time {year}.png"
        output_path = os.path.join(output_folder, output_filename)
        plt.savefig(output_path, dpi=300)
        plt.close()

# 生成 GIF
images = [img for img in os.listdir(output_folder) if img.endswith(".png")]

# 生成 GIF 图
gif_path = "weekend_dailyplan/output.gif"
with Image.open(os.path.join(output_folder, images[0])) as img:
    img.save(gif_path, save_all=True, append_images=[Image.open(os.path.join(output_folder, img)) for img in images[1:]], duration=800, loop=0)

print(f"成功生成 GIF 文件: {gif_path}")
# %%
