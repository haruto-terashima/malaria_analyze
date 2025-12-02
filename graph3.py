import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# マラリアデータの読み込み・整形
df = pd.read_excel('WHO_malaria_data.xlsx', header=2)
df = df[df['IndicatorCode'] == 'MALARIA_EST_CASES']
df['FactValueNumeric'] = pd.to_numeric(df['FactValueNumeric'], errors='coerce')
df = df.dropna(subset=['FactValueNumeric', 'Period', 'Location'])

malaria_nigeria = df[df['Location'] == 'Nigeria'][['Period', 'FactValueNumeric']].set_index('Period')
malaria_nigeria.columns = ['MalariaCases']

# マクロデータ定義 (2000-2023)
years = list(range(2000, 2024))

gdp_values = [
    69448756933, 74030364472, 95385819321, 1.04912E+11, 1.36386E+11, 1.76134E+11,
    2.36104E+11, 2.75626E+11, 3.37036E+11, 2.9188E+11, 3.6336E+11, 4.10335E+11,
    4.59376E+11, 5.14966E+11, 5.68499E+11, 4.94583E+11, 4.0465E+11, 3.75745E+11,
    3.9719E+11, 4.4812E+11, 4.32199E+11, 4.40839E+11, 4.77403E+11, 3.63846E+11
]
df_gdp = pd.DataFrame({'Period': years, 'GDP': gdp_values}).set_index('Period')

pop_values = [
    122283850, 125394046, 128596076, 131900631, 135320422, 138865016,
    142538308, 146339977, 150269623, 154324933, 158503197, 162805071,
    167228767, 171765769, 176404902, 181137448, 185960289, 190873311,
    195874740, 200963603, 208327405, 213401323, 223150896, 227882945
]
df_pop = pd.DataFrame({'Period': years, 'Population': pop_values}).set_index('Period')

urban_values = [
    34.84, 35.67, 36.51, 37.36, 38.21, 39.07, 39.94, 40.82, 41.70, 42.59, 43.48, 44.37,
    45.25, 46.12, 46.98, 47.84, 48.68, 49.52, 50.34, 51.16, 51.96, 52.75, 53.52, 54.28
]
df_urban = pd.DataFrame({'Period': years, 'Urbanization': urban_values}).set_index('Period')

health_values = [
    3.20, 3.19, 2.49, 5.05, 4.63, 4.47, 4.26, 3.91, 3.70, 3.58, 3.30, 3.32, 3.36, 3.42, 3.35,
    3.58, 3.65, 3.75, 3.09, 2.99, 3.38, 4.08, 4.27, np.nan
]
df_health = pd.DataFrame({'Period': years, 'HealthExpenditureGDP': health_values}).set_index('Period')
df_health['HealthExpenditureGDP'] = df_health['HealthExpenditureGDP'].ffill()

# 結合と出力
merged_df = malaria_nigeria.join([df_gdp, df_pop, df_urban, df_health])
merged_df.to_csv('Nigeria_malaria_with_macro.csv')

print(merged_df)


# 相関をとるカラム
cols = ['MalariaCases', 'GDP', 'Population', 'Urbanization', 'HealthExpenditureGDP']

# 相関行列の計算
corr = merged_df[cols].corr()

# ヒートマップ描画
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix: Malaria Cases and Macro Variables (Nigeria 2000-2023)")
plt.tight_layout()
plt.show()
