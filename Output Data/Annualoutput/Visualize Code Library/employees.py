import numpy as np
import pandas as pd
import pyproj
import os
import shutil
import re

import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime
from shapely.geometry import Point

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase

from Base_Map import base_map_path as other_base_map_path
#%%
#TitleSize修改标题大小
#    title = f"Residences Price Year:{year}"  调整标题在类似的格式中调整

years = list(range(2010, 2054))
output_folder = os.path.join(os.getcwd(), "csv街道图中转")
os.makedirs(output_folder, exist_ok=True)
TitleSize = 100
base_map_path = other_base_map_path

current_time = datetime.now()
plt.rcParams['font.sans-serif'] = 'Times new roman'#字体现在是中易黑体
plt.rcParams['font.weight'] = 'bold'#加粗
plt.rcParams['font.size'] = 40#总局字体大小，后面有单独标题大小

#folder_name = "shp_Result_output_time_" + current_time.strftime("%Y-%m-%d-%H-%M-%S")
folder_name = "employees result"
if not os.path.exists(os.path.join(folder_name, "Geometrically Spaced")):
    os.makedirs(os.path.join(folder_name, "Geometrically Spaced"))

if not os.path.exists(os.path.join(folder_name, "Equal Value")):
    os.makedirs(os.path.join(folder_name, "Equal Value"))

try:
    os.mkdir(folder_name)
    print(f"已创建文件夹：{folder_name}")
except FileExistsError:
    print(f"{folder_name} 文件夹已存在")

base_map_path = base_map_path
base_map = gpd.read_file(base_map_path)

#%%
employees_density = {}

years = list(range(2010, 2054))  


output_folder = os.path.join(os.getcwd(), "employees街道图中转")
os.makedirs(output_folder, exist_ok=True)


for year in years:
    csv_file_path = f"employees{year}year.csv"
    
    if os.path.isfile(csv_file_path): 
        df = pd.read_csv(csv_file_path)
        

        x = df['x-coordinate']
        y = df['y-coordinate']
        

        geometry = [Point(xy) for xy in zip(x, y)]
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
        

        output_shapefile = os.path.join(output_folder, f"employees {year} year.shp")
        
        gdf.to_file(output_shapefile)
        
        print(f"{year}已转换WGS84，保存在 {output_shapefile}。")
    else:
        print()


input_folder = "employees街道图中转"  
output_folder = "employees街道图中转/第一步图像相交结果"  


os.makedirs(output_folder, exist_ok=True)

base_map_path = base_map_path
base_map = gpd.read_file(base_map_path)


base_map['AREA'] = base_map['AREA'].astype(float)  

for filename in os.listdir(input_folder):
    if filename.endswith(".shp"):  
        input_file_path = os.path.join(input_folder, filename)
        gdf_points = gpd.read_file(input_file_path)
        gdf_points = gdf_points.reset_index(drop=True)
        joined_data = gpd.sjoin(gdf_points, base_map, how="left", op="within")
        

        unmatched_points = joined_data[joined_data['index_right'].isnull()]
        
        if not unmatched_points.empty:
            print(f"文件 {filename} 中有 {len(unmatched_points)} 个点没有面。")
        

        joined_data = joined_data.dropna(subset=['index_right'])

        result = joined_data.groupby('index_right')['people-ID'].count().reset_index()
        result_gdf = gpd.GeoDataFrame(result, geometry=base_map.geometry.loc[result['index_right']].reset_index(drop=True), crs=base_map.crs)
        

        missing_face_ids = set(base_map.index) - set(result_gdf['index_right'])
        missing_faces = gpd.GeoDataFrame({'index_right': list(missing_face_ids), 'people-ID': [0] * len(missing_face_ids)}, geometry=base_map.geometry.loc[list(missing_face_ids)].reset_index(drop=True), crs=base_map.crs)

        result_gdf = pd.concat([result_gdf, missing_faces])
        result_gdf['AREA'] = base_map['AREA'].loc[result_gdf['index_right']].reset_index(drop=True)
        result_gdf['Emomean'] = result_gdf['people-ID'] / result_gdf['AREA']
        output_file_path = os.path.join(output_folder, filename)
        result_gdf.to_file(output_file_path)

        print(f"处理完成：{filename}，结果已保存到 {output_file_path}")

print("")



shp_folder = "employees街道图中转\第一步图像相交结果"  
gdf_list = []

shp_files = [f for f in os.listdir(shp_folder) if f.endswith('.shp')]

for shp_file in shp_files:
    shp_file_path = os.path.join(shp_folder, shp_file)
    gdf = gpd.read_file(shp_file_path)
    gdf_list.append(gdf)


all_employees_Emomean = []

for gdf in gdf_list:
    Emomean_column_name = "Emomean"  
    if Emomean_column_name in gdf.columns:
        all_employees_Emomean.extend(gdf[Emomean_column_name])

max_employees_Emomean_all_years = max(all_employees_Emomean)
min_employees_Emomean_all_years = min(all_employees_Emomean)

num_bins = 5
Emomean_range_all_years = [min_employees_Emomean_all_years + (max_employees_Emomean_all_years - min_employees_Emomean_all_years) * i / num_bins for i in range(num_bins + 1)]

all_employees_Emomean = []

for gdf in gdf_list:
    Emomean_column_name = "Emomean"  
    if Emomean_column_name in gdf.columns:
        all_employees_Emomean.extend(gdf[Emomean_column_name])


max_employees_Emomean_all_years = max(all_employees_Emomean)
min_employees_Emomean_all_years = min(all_employees_Emomean)


num_bins = num_bins
Emomean_range_all_years = [min_employees_Emomean_all_years + (max_employees_Emomean_all_years - min_employees_Emomean_all_years) * i / num_bins for i in range(num_bins + 1)]  # 不要改变这一行


for i, (shp_file, gdf) in enumerate(zip(shp_files, gdf_list)):
    year = re.search(r'\d+', shp_file).group()  # 从文件名中提取数字部分
    title = f"Year:{year}"  # 包含提取年份的标题
    fig, ax = plt.subplots(1, 1, figsize=(40, 40))

    cmap = plt.get_cmap('Purples', num_bins)

    gdf.plot(column=Emomean_column_name, ax=ax, cmap=cmap, legend=False)  
    base_map.plot(ax=ax, color='none', edgecolor='black', linewidth=2)


    for j in range(num_bins):
        ax.fill_between([], [], color=cmap(j), label=f'{int(Emomean_range_all_years[j])}-{int(Emomean_range_all_years[j+1])}')


    ax.legend(title=" Number of Employees\nUnit: 1000/KM2", loc='upper right',fontsize=35)#图块大小
    plt.title(title, fontsize=TitleSize, fontname='Times new roman', fontweight='bold')
    
    output_file_path = os.path.join(folder_name,'Equal Value', f"{os.path.splitext(shp_file)[0]}.png")
    plt.savefig(output_file_path, dpi=50, bbox_inches='tight')
    plt.close()
# 几何划分
percentiles = np.percentile(all_employees_Emomean, np.linspace(0, 100, num_bins + 1))

for i, (shp_file, gdf) in enumerate(zip(shp_files, gdf_list)):
    year = re.search(r'\d+', shp_file).group()  # 从文件名中提取数字部分
    title = f"Year:{year}"  # 包含提取年份的标题
    fig, ax = plt.subplots(1, 1, figsize=(40, 40))

    cmap = plt.get_cmap('Purples', num_bins)  

    # cut进行几何划分
    gdf['bin_Employees'] = pd.cut(gdf[Emomean_column_name], bins=percentiles, labels=range(num_bins))

    gdf.plot(column='bin_Employees', ax=ax, cmap=cmap, legend=False)  
    base_map.plot(ax=ax, color='none', edgecolor='black', linewidth=2)

    # 自定义块状图例
    for j in range(num_bins):
        ax.fill_between([], [], color=cmap(j), label=f'{int(percentiles[j])}-{int(percentiles[j+1])}')


    ax.legend(title="Number of People\nUnit: 1000/KM2", loc='upper right', fontsize=35)
    plt.title(title, fontsize=TitleSize, fontname='Times new roman', fontweight='bold')
    
    output_file_path = os.path.join(folder_name,'Geometrically Spaced', f"{os.path.splitext(shp_file)[0]}.png")
    plt.savefig(output_file_path, dpi=50, bbox_inches='tight')
    plt.close()


print("")