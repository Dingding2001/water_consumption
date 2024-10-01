import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

# 读取坐标数据.xlsx
coordinates_data_yuan = pd.read_excel('坐标.xlsx', engine='openpyxl')

# 导入坐标数据.xlsx
coordinates_data_need = pd.read_excel('输入数据.xlsx', engine='openpyxl')

# 提取第一组、第二组
who1 = coordinates_data_yuan['who'].values
xcor1 = coordinates_data_yuan['xcor'].values
ycor1 = coordinates_data_yuan['ycor'].values
long2 = coordinates_data_yuan['long'].values
lat2 = coordinates_data_yuan['lat'].values

#导入第三组坐标数据
who2 = coordinates_data_need['who'].values
xcor3 = coordinates_data_need['xcor'].values
ycor3 = coordinates_data_need['ycor'].values

# 定义多项式函数 使用curve_fit拟合多项式
def polynomial_function(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

params_x, _ = curve_fit(polynomial_function, xcor1, long2)
params_y, _ = curve_fit(polynomial_function, ycor1, lat2)

# 根据拟合的多项式生成第四组坐标数据
long4 = polynomial_function(xcor3, *params_x)
lat4 = polynomial_function(ycor3, *params_y)

#定义表头
data = {
    'who': who2,
    'xcor': xcor3,
    'ycor': ycor3,
    'long': long4,
    'lat': lat4
}

df = pd.DataFrame(data)
df.to_csv('坐标转换result.csv', index=False)

# 输出结果
print("转换成果")
