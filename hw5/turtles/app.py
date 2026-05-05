import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(
    page_title="пи",
    page_icon="пи",
    layout="wide"
)

def count_overlapping(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    cnt, start = 0, 0
    while True:
        start = text.find(pattern, start)
        if start == -1:
            break
        cnt += 1
        start += 1  
    return cnt

def most_frequent_enclosing_substring(text: str, pattern: str, k: int):
    if len(pattern) > k or k < 1:
        return None, 0
    counter = Counter()
    for i in range(len(text) - k + 1):
        sub = text[i:i + k]
        if pattern in sub:
            counter[sub] += 1
    if counter:
        return counter.most_common(1)[0]
    return None, 0

st.title("ЦЕЛЫЙ МИЛЛИОН ЗНАКОВ ЧИСЛА ПИ")



df_digits = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-24/pi_digits.csv")
pi_string = "".join(df_digits["digit"].astype(str).tolist())

col1, col2= st.columns(2)
query = col1.text_input("число:", value="228")
query = "".join(ch for ch in query if ch.isdigit())
k = col2.text_input("длина подстроки k:", value="10")
k = int(k)

occ = count_overlapping(pi_string, query)
freq_sub, freq_cnt = most_frequent_enclosing_substring(pi_string, query, k)

col1, col2= st.columns(2)
col1.metric("Сколько раз встречается число в 1М знаков?", f"{occ:,}")
col2.metric(f"Самая частая подстрока длины {k} - {freq_sub if len(freq_sub) <= 10 else f'{freq_sub[:5]}...{freq_sub[-5:]}'} - встречается", f"{freq_cnt:,}")

window_size = st.slider("длина окна для вычислений графиков", min_value=100, max_value=100000, value=10000, step=100)
window_size = int(window_size)  

positions = np.arange(0, len(pi_string), window_size)
densities = []
for start in positions:
    end = min(start + window_size, len(pi_string))
    densities.append(count_overlapping(pi_string[start:end], query))

df_density = pd.DataFrame({"позиция в пи": positions, "кол-во вхождений": densities})
fig_density = px.line(df_density, x="позиция в пи", y="кол-во вхождений",
                      title=f"плотность вхождений {query}")

fig_dist = px.histogram(x=densities, nbins=min(20, max(densities)+1),
                        title=f"распределение кол-ва вхождений {query} в окнах",
                        labels={"x": "кол-во вхождений", "y": "кол-во окон"})
fig_dist.update_layout(bargap=0.1)
st.plotly_chart(fig_density, use_container_width=True)
st.plotly_chart(fig_dist, use_container_width=True)
