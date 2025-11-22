import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#感染者数データを読み込む
file_path = 'WHO_malaria_data.xlsx'
df = pd.read_excel(file_path, header=2)
df.to_csv("WHO_malaria_data.csv", index=False)


df = df[df['IndicatorCode'] == 'MALARIA_EST_CASES']
df['FactValueNumeric'] = pd.to_numeric(df['FactValueNumeric'], errors='coerce')

df = df.dropna(subset=['FactValueNumeric', 'Period', 'Location'])

# 気候データ読み込み＆CSV化
def read_and_csv(excel_file, csv_file):
    pd.read_excel(excel_file).to_csv(csv_file, index=False)
    return pd.read_csv(csv_file)

df_temp = read_and_csv('気温月次データ.xlsx', '気温月次データ.csv')
df_rain = read_and_csv('降水量月次データ.xlsx', '降水量月次データ.csv')
df_humidity = read_and_csv('相対湿度月次データ.xlsx', '相対湿度月次データ.csv')

# 月次→年次に変換
def monthly_to_yearly(df, agg="mean"):
    month_cols = [col for col in df.columns if "-" in col]
    years = sorted({col.split("-")[0] for col in month_cols})
    out = df[["code", "name"]].copy()
    for year in years:
        cols = [c for c in month_cols if c.startswith(year)]
        if agg == "mean":
            out[year] = df[cols].mean(axis=1, skipna=True)
        elif agg == "sum":
            out[year] = df[cols].sum(axis=1, skipna=True)
    return out

yearly_temp = monthly_to_yearly(df_temp, agg="mean")
yearly_rain = monthly_to_yearly(df_rain, agg="mean")
yearly_humidity = monthly_to_yearly(df_humidity, agg="mean")

# 2000～2023年だけ抽出-
def filter_2000_2023(df):
    year_cols = [col for col in df.columns if col.isdigit()]
    target = [c for c in year_cols if 2000 <= int(c) <= 2023]
    return df[["code", "name"] + target]

temp_2000_2023 = filter_2000_2023(yearly_temp)
rain_2000_2023 = filter_2000_2023(yearly_rain)
humidity_2000_2023 = filter_2000_2023(yearly_humidity)

# ナイジェリアだけ抽出して転置（年を行に）
years = [str(y) for y in range(2000, 2024)]

temp_nigeria = temp_2000_2023[temp_2000_2023['code']=='NGA'][years].T
temp_nigeria.columns = ['AvgTemp']
rain_nigeria = rain_2000_2023[rain_2000_2023['code']=='NGA'][years].T
rain_nigeria.columns = ['AvgRain']
humidity_nigeria = humidity_2000_2023[humidity_2000_2023['code']=='NGA'][years].T
humidity_nigeria.columns = ['AvgHumidity']

# 年をindexに揃える
temp_nigeria.index = temp_nigeria.index.astype(int)
rain_nigeria.index = rain_nigeria.index.astype(int)
humidity_nigeria.index = humidity_nigeria.index.astype(int)

# マージ
malaria_nigeria = df[(df['Location']=='Nigeria') & (df['Period'].isin(range(2000,2024)))][['Period','FactValueNumeric']].set_index('Period')
merged_df = malaria_nigeria.join([temp_nigeria, rain_nigeria, humidity_nigeria])

# 確認
print(merged_df)

#グラフ化
years = merged_df.index

#1感染者数と気温
fig, ax1 = plt.subplots(figsize=(10,5))

# 左軸：感染者数（百万単位）
ax1.set_xlabel('Year')
ax1.set_ylabel('Malaria Cases (million)', color='tab:red')
ax1.plot(years, merged_df['FactValueNumeric']/1e6, color='tab:red', marker='o', label='Malaria Cases')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True)

# 右軸：気温
ax2 = ax1.twinx()
ax2.set_ylabel('Average Temperature (°C)', color='tab:blue')
ax2.plot(years, merged_df['AvgTemp'], color='tab:blue', marker='s', label='Average Temp')
ax2.tick_params(axis='y', labelcolor='tab:blue')

# 凡例をまとめる
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.title('Malaria Cases vs Temperature in Nigeria (2000-2023)')
plt.tight_layout()
plt.show()

#2感染者数と湿度
fig, ax1 = plt.subplots(figsize=(10,5))

# 左軸：感染者数
ax1.set_xlabel('Year')
ax1.set_ylabel('Malaria Cases (million)', color='tab:red')
ax1.plot(years, merged_df['FactValueNumeric']/1e6, color='tab:red', marker='o', label='Malaria Cases')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True)

# 右軸：湿度
ax2 = ax1.twinx()
ax2.set_ylabel('Average Humidity (%)', color='tab:green')
ax2.plot(years, merged_df['AvgHumidity'], color='tab:green', marker='x', label='Average Humidity')
ax2.tick_params(axis='y', labelcolor='tab:green')

# 凡例をまとめる
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.title('Malaria Cases vs Relative Humidity in Nigeria (2000-2023)')
plt.tight_layout()
plt.show()

#3感染者数と降水量（棒グラフ）
fig, ax1 = plt.subplots(figsize=(10,5))

ax1.plot(merged_df.index, merged_df['FactValueNumeric']/1e6, color='tab:blue', marker='o', label='Malaria Cases (million)')
ax1.set_xlabel('Year')
ax1.set_ylabel('Malaria Cases (million)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()  
ax2.bar(merged_df.index, merged_df['AvgRain'], alpha=0.3, color='tab:green', label='Average Rain (mm)')
ax2.set_ylabel('Average Rain (mm)', color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:green')

plt.title('Malaria Cases vs Rainfall in Nigeria (2000-2023)')
fig.tight_layout()
plt.show()

# X軸：気候要因、Y軸：感染者数（百万単位）
cases = merged_df['FactValueNumeric'] / 1e6

# 1. 感染者数 vs 気温
plt.figure(figsize=(7,5))
plt.scatter(merged_df['AvgTemp'], cases, color='red')
plt.xlabel('Average Temperature (°C)')
plt.ylabel('Malaria Cases (million)')
plt.title('Malaria Cases vs Temperature in Nigeria (2000-2023)')
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. 感染者数 vs 降水量
plt.figure(figsize=(7,5))
plt.scatter(merged_df['AvgRain'], cases, color='blue')
plt.xlabel('Average Rainfall (mm)')
plt.ylabel('Malaria Cases (million)')
plt.title('Malaria Cases vs Rainfall in Nigeria (2000-2023)')
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. 感染者数 vs 相対湿度
plt.figure(figsize=(7,5))
plt.scatter(merged_df['AvgHumidity'], cases, color='green')
plt.xlabel('Average Relative Humidity (%)')
plt.ylabel('Malaria Cases (million)')
plt.title('Malaria Cases vs Relative Humidity in Nigeria (2000-2023)')
plt.grid(True)
plt.tight_layout()
plt.show()


# 相関行列を計算
corr = merged_df.corr()

# ヒートマップ描画
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Correlation Matrix: Malaria Cases and Climate Factors (Nigeria 2000-2023)")
plt.tight_layout()
plt.show()