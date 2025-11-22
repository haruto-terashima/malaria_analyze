import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

file_path = 'WHO_malaria_data.xlsx'
df = pd.read_excel(file_path, header=2)
df.to_csv("WHO_malaria_data.csv", index=False)


df = df[df['IndicatorCode'] == 'MALARIA_EST_CASES']
df['FactValueNumeric'] = pd.to_numeric(df['FactValueNumeric'], errors='coerce')

df = df.dropna(subset=['FactValueNumeric', 'Period', 'Location'])

all_years = sorted(df['Period'].unique())


complete_countries = [
    country for country, group in df.groupby('Location')
    if set(group['Period']) == set(all_years)
]


df = df[df['Location'].isin(complete_countries)]

latest_year = df['Period'].max()
top_countries = (
    df[df['Period'] == latest_year]
    .groupby('Location')['FactValueNumeric']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index.tolist()
)


plt.figure(figsize=(10,6))

for country in top_countries:
    subset = df[df['Location'] == country].sort_values('Period')
    plt.plot(subset['Period'], subset['FactValueNumeric'], marker='o', label=country)

plt.title(f'Estimated Malaria Cases (Top 10 Countries, up to {latest_year})')
plt.xlabel('Year')
plt.ylabel('Estimated Cases')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



# ② 最新年の棒グラフ（今一番深刻な国）

latest_data = (
    df[df['Period'] == latest_year]
    .groupby('Location')['FactValueNumeric']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))
latest_data.plot(kind='bar', color='salmon')
plt.title(f'Estimated Malaria Cases by Country (Top 10 in {latest_year})', fontsize=16)
plt.ylabel('Estimated Cases')
plt.xlabel('Country')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ③ 前年比増減率の折れ線グラフ

trend_df = df[df['Location'].isin(top_countries)].sort_values(['Location', 'Period'])

trend_df['PrevYear'] = trend_df.groupby('Location')['FactValueNumeric'].shift(1)
trend_df['ChangeRate'] = (trend_df['FactValueNumeric'] - trend_df['PrevYear']) / trend_df['PrevYear'] * 100
trend_df = trend_df.dropna(subset=['ChangeRate'])

plt.figure(figsize=(12,6))
for country in top_countries:
    subset = trend_df[trend_df['Location'] == country]
    plt.plot(subset['Period'], subset['ChangeRate'], marker='o', label=country)

plt.axhline(0, color='black', linestyle='--') 
plt.title(f'Year-on-Year Change Rate of Malaria Cases (Top 10 Countries)', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Change Rate (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


#クラスタ
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
time_series_df = df[df['Location'].isin(top_countries)].pivot_table(
    index='Location',
    columns='Period',
    values='FactValueNumeric'
)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(time_series_df)

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

time_series_df['Cluster'] = clusters

plt.figure(figsize=(12,6))
for cluster in sorted(time_series_df['Cluster'].unique()):
    cluster_data = time_series_df[time_series_df['Cluster'] == cluster].drop('Cluster', axis=1)
    mean_trend = cluster_data.mean(axis=0)
    plt.plot(mean_trend.index, mean_trend.values, marker='o', label=f'Cluster {cluster}')

plt.title('Average Trend by Cluster (Top 10 Countries)', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Estimated Cases (Standardized)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
print(time_series_df[['Cluster']])


# ⑤ ナイジェリアとコンゴを除いた折れ線グラフ

exclude_countries = ['Nigeria', 'Democratic Republic of the Congo']

filtered_countries = [c for c in top_countries if c not in exclude_countries]

plt.figure(figsize=(12,6))

for country in filtered_countries:
    subset = df[df['Location'] == country].sort_values('Period')
    plt.plot(subset['Period'], subset['FactValueNumeric'], marker='o', label=country)

plt.title('Estimated Malaria Cases (Excluding Nigeria & DR Congo)')
plt.xlabel('Year')
plt.ylabel('Estimated Cases')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

