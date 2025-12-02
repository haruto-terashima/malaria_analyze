# マラリア感染者数分析

# 概要
　graph.pyでは2000年から2023年までの年次感染者数データから最も感染者数の多い10か国を取り出して分析した。
  graph2.pyではナイジェリアの感染者数データと気候データ（降水量、気温、湿度）の関係を調べた。
  
# 使用技術
　python 3.11.13
  numpy 2.3.3
　pandas 2.3.3
　matplotlib 3.10.6
　seaborn 0.13.2
　scikit-learn 1.7.2

# 使用データ
  気候データ　world bankのclimate change knowledge portal
  https://climateknowledgeportal.worldbank.org/?utm_source=chatgpt.com
  マラリア感染データ　WHO　Global Health Observatory（GHO）
  https://www.who.int/data/gho/data/indicators/indicator-details/GHO/estimated-number-of-malaria-cases?utm_source=chatgpt.com
  
## graph.py
# 折れ線グラフ（トップ10感染者数国の2000年から2023年の推移）
<img width="1014" height="672" alt="スクリーンショット 2025-11-23 235921" src="https://github.com/user-attachments/assets/7088dd96-370a-459d-9fb0-d4c51696241e" />

# 棒グラフ（最新年の感染者数が多い国）
<img width="1011" height="673" alt="スクリーンショット 2025-11-23 235934" src="https://github.com/user-attachments/assets/5329bd9e-e5b0-4d4e-9f82-8b8329ad2b4d" />

# 前年比増減率の折れ線グラフ
<img width="1211" height="673" alt="スクリーンショット 2025-11-23 235945" src="https://github.com/user-attachments/assets/2104e761-f08e-4df3-bf86-e3b9e3e0220e" />

# クラスタ（10か国の中で傾向の類似性から3つに分類する）
<img width="1215" height="678" alt="スクリーンショット 2025-11-23 235955" src="https://github.com/user-attachments/assets/ba34d7fc-fe5d-431c-a63f-8b9a8266e8d1" />

# ナイジェリアとコンゴを除いた折れ線グラフ（この二か国の感染者数が多すぎるため）
<img width="1209" height="670" alt="スクリーンショット 2025-11-24 000005" src="https://github.com/user-attachments/assets/9c979841-d1eb-4814-8d66-b34d5b654b9b" />

## graph2.py
# 折れ線グラフ（感染者数と気温のそれぞれの推移）
<img width="1013" height="565" alt="スクリーンショット 2025-11-24 001120" src="https://github.com/user-attachments/assets/6a32c041-57f6-4f8c-895f-0e103b70bf7b" />

# 折れ線グラフ（感染者数と湿度のそれぞれの推移）
<img width="1006" height="565" alt="スクリーンショット 2025-11-24 001128" src="https://github.com/user-attachments/assets/0a63fe9c-0b79-4fdc-b759-80142c3bcf89" />

# 折れ線グラフと棒グラフ（感染者数、降水量（棒グラフ）でそれぞれの推移）
<img width="1009" height="571" alt="スクリーンショット 2025-11-24 001140" src="https://github.com/user-attachments/assets/df979ff9-c8a8-4a8d-8bce-968d1d8c469f" />

# 散布図（感染者数と気温）
<img width="715" height="571" alt="スクリーンショット 2025-11-24 001149" src="https://github.com/user-attachments/assets/3845095f-361c-47d6-8348-f5bdd84cdf1e" />


# 散布図（感染者数と降水量）
<img width="707" height="567" alt="スクリーンショット 2025-11-24 001156" src="https://github.com/user-attachments/assets/03b28614-0d72-4aa6-b305-c90d16bd2ead" />


# 散布図（感染者数と湿度）
<img width="717" height="572" alt="スクリーンショット 2025-11-24 001204" src="https://github.com/user-attachments/assets/5fbc02f0-6fe4-44b4-8d45-ef41e999006f" />


# 相関図
<img width="817" height="677" alt="スクリーンショット 2025-11-24 001213" src="https://github.com/user-attachments/assets/13f9a9cd-9f7d-418c-8fcc-2d3e2cd654d2" />








