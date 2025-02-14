import pandas as pd

# 读取数据
df = pd.read_csv("/Users/sara/Downloads/weatherHistory.csv")

# 转换日期格式
df['Formatted Date'] = pd.to_datetime(df['Formatted Date'], utc=True, errors='coerce')

# 删除无用列（Loud Cover 只有 0）
if 'Loud Cover' in df.columns:
    df.drop(columns=['Loud Cover'], inplace=True)

# 处理缺失值：填充 Precip Type 缺失值（修复 FutureWarning）
if 'Precip Type' in df.columns:
    df.loc[:, 'Precip Type'] = df['Precip Type'].fillna('unknown')

# 过滤掉 Pressure (millibars) = 0 的异常值
df = df[df['Pressure (millibars)'] > 800]

# 移除重复数据
df.drop_duplicates(inplace=True)

# 显示数据概览
#print(df.info())
#print(df.head())

# 检查缺失值
#print(df.isnull().sum())

# 统计信息
#print(df.describe())

import matplotlib.pyplot as plt
import seaborn as sns

# 设置全局风格
plt.style.use('seaborn-v0_8-darkgrid')

# 提取月份
df['Month'] = df['Formatted Date'].dt.month

# 计算每月平均温度
monthly_avg_temp = df.groupby('Month')['Temperature (C)'].mean()

# 计算不同降水类型的温度差异
precip_temp = df.groupby('Precip Type')['Temperature (C)'].mean()

# 计算温度与湿度的关系
humidity_temp_data = df[['Humidity', 'Temperature (C)']]

# 每月平均温度折线图
plt.figure(figsize=(10, 5))
plt.plot(monthly_avg_temp.index, monthly_avg_temp.values, marker='o', linestyle='-', linewidth=2, color='orange')
plt.xlabel("Month")
plt.ylabel("Average Temperature (°C)")
plt.title("Average Monthly Temperature")
plt.xticks(range(1, 13))
plt.grid(True)
plt.show()

# 降水类型对温度影响的柱状图 #
plt.figure(figsize=(8, 5))
sns.barplot(x=precip_temp.index, y=precip_temp.values, color="blue")
plt.xlabel("Precipitation Type")
plt.ylabel("Average Temperature (°C)")
plt.title("Average Temperature by Precipitation Type")
plt.show()

# 温度 vs. 湿度 散点图 #
plt.figure(figsize=(8, 5))
sns.scatterplot(x=df['Humidity'], y=df['Temperature (C)'], alpha=0.5)
plt.xlabel("Humidity")
plt.ylabel("Temperature (°C)")
plt.title("Temperature vs. Humidity")
plt.show()

# 风速直方图 #
plt.figure(figsize=(8, 5))
plt.hist(df['Wind Speed (km/h)'], bins=30, edgecolor='black', alpha=0.7)
plt.xlabel("Wind Speed (km/h)")
plt.ylabel("Frequency")
plt.title("Wind Speed Distribution")
plt.show()

# 气压的 KDE 分布曲线 #
plt.figure(figsize=(8, 5))
sns.kdeplot(df['Pressure (millibars)'], fill=True, color="blue", alpha=0.5)
plt.xlabel("Pressure (millibars)")
plt.ylabel("Density")
plt.title("Pressure Distribution")
plt.show()

# 温度相关性的热力图 #
plt.figure(figsize=(8, 5))
sns.heatmap(df[['Temperature (C)', 'Apparent Temperature (C)', 'Humidity', 'Wind Speed (km/h)', 'Visibility (km)', 'Pressure (millibars)']].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
