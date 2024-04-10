# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# -- СРЕДНЕМЕСЯЧНАЯ ЗП --
#zp_data = pd.read_excel('/content/sample_data/zp_srmes_rab.xlsx', index_col=0)
zp_data = pd.read_excel('https://raw.githubusercontent.com/qd217/DS_project/main/zp_srmes_rab.xlsx', index_col=0)
zp_data.head()

# -- ИНФЛЯЦИЯ --
#infl_data = pd.read_excel('/content/sample_data/infl_rab.xlsx', index_col=0)
infl_data = pd.read_excel('https://raw.githubusercontent.com/qd217/DS_project/main/infl_rab.xlsx', index_col=0)
infl_data.head(13)

# --ГРАФИКИ--
mask1 = zp_data.index == 'рыболовство и рыбоводство'
mask2 = infl_data.index == 'Всего'
mask3 = zp_data.index == 'образование'
mask4 = zp_data.index == 'добыча металлических руд'

plt.figure(figsize=(5, 5))
plt.plot(zp_data.columns, zp_data[mask1].values[0], color = 'Blue')
plt.plot(zp_data.columns, zp_data[mask3].values[0], color = 'Green')
plt.plot(zp_data.columns, zp_data[mask4].values[0], color = 'Brown')
plt.title("ЗП без учета инфляции")
plt.legend(['Рыболовство и рыбоводство','Образование','Добыча металлических руд'])
plt.show()

plt.figure(figsize=(5, 5))
plt.bar(infl_data.columns, infl_data[mask2].values[0], color = 'Red')
plt.title("Инфляция")
plt.legend(['Инфляция'])
plt.xlabel('Год');
plt.ylabel('%.');
plt.show()

plt.figure(figsize=(5, 5))
plt.plot(zp_data.columns, zp_data[mask1].values[0], color = 'Blue')
plt.plot(infl_data.columns, (1-infl_data[mask2].values[0]/100)*zp_data[mask1].values[0], color = 'Red')
plt.bar(zp_data.columns,zp_data[mask1].values[0]-(1-infl_data[mask2].values[0]/100)*zp_data[mask1].values[0], color = 'Black')
plt.title("Рыболовство и рыбоводство")
plt.legend(['ЗП без учета инфляции','ЗП с учетом инфляции','delta'])
plt.xlabel('Год');
plt.ylabel('тыс. руб.');
plt.show()

plt.figure(figsize=(5, 5))
plt.plot(zp_data.columns, zp_data[mask3].values[0], color = 'Green')
plt.plot(infl_data.columns, (1-infl_data[mask2].values[0]/100)*zp_data[mask3].values[0], color = 'Red')
plt.bar(zp_data.columns,zp_data[mask3].values[0]-(1-infl_data[mask2].values[0]/100)*zp_data[mask3].values[0], color = 'Black')
plt.title("Образование")
plt.legend(['ЗП без учета инфляции','ЗП с учетом инфляции','delta'])
plt.xlabel('Год');
plt.ylabel('тыс. руб.');
plt.show()

plt.figure(figsize=(5, 5))
plt.plot(zp_data.columns, zp_data[mask4].values[0], color = 'Brown')
plt.plot(infl_data.columns, (1-infl_data[mask2].values[0]/100)*zp_data[mask4].values[0], color = 'Red')
plt.bar(zp_data.columns,zp_data[mask4].values[0]-(1-infl_data[mask2].values[0]/100)*zp_data[mask4].values[0], color = 'Black')
plt.title("Добыча металлических руд")
plt.legend(['ЗП без учета инфляции','ЗП с учетом инфляции','delta'])
plt.xlabel('Год');
plt.ylabel('тыс. руб.');
plt.show()

# -- ТЕМП --
zp_infl_data = zp_data.T
zp_infl_data = zp_infl_data[['рыболовство и рыбоводство', 'добыча металлических руд', 'образование']].shift(1).rename(columns={'рыболовство и рыбоводство':'рыболовство и рыбоводство_см','добыча металлических руд':'добыча металлических руд_см','образование': 'образование_см' })
zp_infl_data = pd.concat([zp_data.T, zp_infl_data, infl_data.T['Всего']], axis=1).rename(columns={'Всего':'инфляция'})
zp_infl_data['рыболовство и рыбоводство_реал'] = zp_infl_data['рыболовство и рыбоводство']*(1-zp_infl_data['инфляция']/100)
zp_infl_data['добыча металлических руд_реал'] = zp_infl_data['добыча металлических руд']*(1-zp_infl_data['инфляция']/100)
zp_infl_data['образование_реал'] = zp_infl_data['образование']*(1-zp_infl_data['инфляция']/100)
zp_infl_data_full = zp_infl_data[['рыболовство и рыбоводство_реал', 'добыча металлических руд_реал', 'образование_реал']].shift(1).rename(columns={'рыболовство и рыбоводство_реал':'рыболовство и рыбоводство_реал_см','добыча металлических руд_реал':'добыча металлических руд_реал_см','образование_реал': 'образование_реал_см' })
zp_infl_data = pd.concat([zp_infl_data, zp_infl_data_full], axis=1)
zp_infl_data['темп_обр_р'] = (1-(zp_infl_data['образование_реал_см']/zp_infl_data['образование_реал']))*100
zp_infl_data['темп_доб_р'] = (1-(zp_infl_data['добыча металлических руд_реал_см']/zp_infl_data['добыча металлических руд_реал']))*100
zp_infl_data['темп_рыб_р'] = (1-(zp_infl_data['рыболовство и рыбоводство_реал_см']/zp_infl_data['рыболовство и рыбоводство_реал']))*100

zp_infl_data = zp_infl_data.T

mask11 = zp_infl_data.index == 'рыболовство и рыбоводство_реал'
mask12 = zp_infl_data.index == 'рыболовство и рыбоводство_реал_см'
mask13 = zp_infl_data.index == 'добыча металлических руд_реал'
mask14 = zp_infl_data.index == 'добыча металлических руд_реал_см'
mask15 = zp_infl_data.index == 'образование_реал'
mask16 = zp_infl_data.index == 'образование_реал_см'

zp_infl_data.head(24)

# -- ТЕМП ГРАФИК --
plt.figure(figsize=(15, 5))

plt.plot(zp_infl_data.columns, (1-(zp_infl_data[mask12].values[0]/zp_infl_data[mask11].values[0]))*100, color = 'Blue')
plt.plot(zp_infl_data.columns, (1-(zp_infl_data[mask14].values[0]/zp_infl_data[mask13].values[0]))*100, color = 'Brown')
plt.plot(zp_infl_data.columns, (1-(zp_infl_data[mask16].values[0]/zp_infl_data[mask15].values[0]))*100, color = 'Green')
plt.bar(infl_data.columns, (infl_data[mask2].values[0]), color = 'Red', alpha = 0.3)
plt.title("Темп изменения реальных зарплат")
plt.legend(['Рыболовство и рыбоводство','Добыча металлических руд','Образование'])
plt.show()

#Вывод: При анализе представленных данных было установлено снижение инфляции и рост среднемесячных зарплат. Повышение зарплат обуславливает увеличение "разрыва" их номинальных и реальных значений. Темпы роста зарплат в стобильное время превышают инфляцию, что подтверждает повышение уровня дохода граждан.
#=== ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ ===
# -- ПОРОГ БЕДНОСТИ --
#bednost_data = pd.read_excel('/content/sample_data/bednost_rab.xlsx', index_col=0)
bednos_data = pd.read_excel('https://raw.githubusercontent.com/qd217/DS_project/main/bednost_rab.xlsx', index_col=0)
bednos_data.head()

# -- ИНДЕКС ПОТРЕБЛЕНИЯ --
#ind_potr_data = pd.read_excel('/content/sample_data/ind_potr_rab.xlsx', index_col=0)
ind_potr_data = pd.read_excel('https://raw.githubusercontent.com/qd217/DS_project/main/ind_potr_rab.xlsx', index_col=0)
ind_potr_data.head()

# -- ИНДЕКС СЧАСТЬЯ --
#ind_hap_data = pd.read_excel('/content/sample_data/ind_hap_rab.xlsx', index_col=0)
ind_hap_data = pd.read_excel('https://raw.githubusercontent.com/qd217/DS_project/main/ind_hap_rab.xlsx', index_col=0)
ind_hap_data.head()

# --ГРАФИКИ--
mask5 = bednos_data.index == 'В процентах от общей численности населения'
mask6 = ind_potr_data.index == 'Индекс потребительской уверенности'
mask7 = ind_hap_data.index == 'Индекс счастья'

plt.figure(figsize=(10, 10))
plt.bar(infl_data.columns, (infl_data[mask2].values[0]), color = 'Red', alpha = 0.3)
plt.plot(zp_data.columns, zp_data[mask1].values[0]/1000, color = 'Blue')
plt.plot(zp_data.columns, zp_data[mask3].values[0]/1000, color = 'Green')
plt.plot(zp_data.columns, zp_data[mask4].values[0]/1000, color = 'Brown')
plt.scatter(bednos_data.columns, bednos_data[mask5].values[0], color = 'Grey')
plt.bar(ind_potr_data.columns, ind_potr_data[mask6].values[0], color = 'Orange')
plt.scatter(ind_hap_data.columns, ind_hap_data[mask7].values[0], color = 'Yellow')
plt.xlabel('Год');
plt.ylabel('Абсолютныое значение');
plt.legend(['Средняя ЗП в сфере рыболовство и рыбоводство, тыс.руб.','Средняя ЗП в сфере образование, тыс.руб.','Средняя ЗП в сфере добыча металлических руд, тыс. руб.','Населения за чертой бедности, %','Индекс счастья, %','Инфляция, %','Индекс потребительской уверенности, %'])
plt.show()

# -- СВОДНАЯ ТАБЛИЦА ДЛЯ АНАЛИЗА --
data_full = pd.concat([zp_data,infl_data.tail(1),bednos_data.tail(2).head(1),ind_potr_data,ind_hap_data,zp_infl_data.tail(3)])
data = data_full.T
data = data.rename(columns={'рыболовство и рыбоводство': 'Ср.ЗП рыб.','добыча металлических руд': 'Ср.ЗП доб.металл.руд', 'образование' : 'Ср.ЗП образование', 'Всего':'% инфл.', 'В процентах от общей численности населения':'% за черт.бедн.','Индекс потребительской уверенности':'Инд.потр.увер.','Индекс счастья':'Инд.счастья','темп_обр_р':'Темп.Обр.р.','темп_доб_р':'Темп.Доб.р.','темп_рыб_р':'Темп.Рыб.р.'})

data['Ср.ЗП рыб.'] = data['Ср.ЗП рыб.'].astype(float)
data['Ср.ЗП доб.металл.руд'] = data['Ср.ЗП доб.металл.руд'].astype(float)
data['Ср.ЗП образование'] = data['Ср.ЗП образование'].astype(float)
data['% инфл.'] = data['% инфл.'].astype(np.float16)
data['% за черт.бедн.'] = data['% за черт.бедн.'].astype(np.float16)
data['Инд.потр.увер.'] = data['Инд.потр.увер.'].astype(np.float16)
data['Инд.счастья'] = data['Инд.счастья'].astype(np.float16)
data['Темп.Обр.р.'] = data['Темп.Обр.р.'].astype(np.float16)
data['Темп.Доб.р.'] = data['Темп.Доб.р.'].astype(np.float16)
data['Темп.Рыб.р.'] = data['Темп.Рыб.р.'].astype(np.float16)

#data

# -- КОРРЕЛЯЦИЯ СПИРМЕНА--
corr = data.corr(method='spearman', numeric_only=True)
sns.heatmap(corr, cmap="Greens", annot=True)


#Вывод:
#Инфляция "отзеркаливает" индекс потребительской уверенности (не берем во внимание кризисы и мировую обстановку) - граждане следят за обстановкой в мире и ощущяют инфляцию.
#С увеличение зарплат снизилось количество граждан за чертой бедности, а так же увеличился индекс счастья. Последнее свидетельствует о том, что зарплата граждан отражает их внутреннее состояние;
#Про инфляцию и зарплаты описано ранее.

# -- STREAMLIT --
txt = ('Среднемесячная номинальная начисленная заработная плата работников организаций по видам экономической деятельности в Российской Федерации за 2000-2023 гг.')
st.header(txt)
st.dataframe(zp_data)

txt = ('Динамика номинальных зарплат')
st.header(txt)
st.image('sr_zp.png')

txt = ('Уровень инфляции в Российской Федерации за 2000-2023 гг.')
st.header(txt)
st.dataframe(infl_data)

txt = ('Динамика инфляции')
st.header(txt)
st.image('infl.png')

txt = ('Сравнение номинальных и реальных запрлат по отрослям')
st.header(txt)
# Select box!!!
option = st.selectbox(
     'Выбирите отрасль',
     ('Рыболовство и рыбоводство', 'Добыча металлических руд','Образование'))
if option == 'Рыболовство и рыбоводство':
    st.image('rib.png')
elif option == 'Добыча металлических руд':
    st.image('dob.png')
elif option == 'Образование':
    st.image('obr.png')

txt = ('Темп изменения реальных зарплат')
st.header(txt)
st.image('temp.png')

# Button!!!
if st.button('Отобразить сводную таблицу c расчетными показателями'):
    st.dataframe(zp_infl_data)

st.header('Промежуточный вывод:')
txt = ('При анализе представленных данных было установлено снижение инфляции и рост среднемесячных зарплат. Повышение зарплат обуславливает увеличение "разрыва" их номинальных и реальных значений. Темпы роста зарплат в стобильное время превышают инфляцию, что подтверждает повышение уровня дохода граждан.')
st.write(txt)


txt = ('В качестве дополниельных рассмотрим "Процент населения за чертой бедности","Индекс потребительской уверенности","Индекс счастья".')
st.caption(txt)

txt = ('Динамика показателей')
st.header(txt)
st.image('res_gr.png')

# Button!!!
if st.button('Отобразить сводную таблицу'):
    st.dataframe(data)

# Button!!!
if st.button('Отобразить таблицы дополнительных показателей'):
    st.dataframe(bednos_data)
    st.dataframe(ind_potr_data)
    st.dataframe(ind_hap_data)

txt = ('Корреляция Спирмена')
st.header(txt)
st.image('cor.png')
st.header('Вывод:')
txt = ('Инфляция "отзеркаливает" индекс потребительской уверенности (не берем во внимание кризисы и мировую обстановку (2008г, 2014г, 2022г)) - граждане следят за обстановкой в мире и ощущяют инфляцию; С увеличение зарплат снизилось количество граждан за чертой бедности, а так же увеличился индекс счастья. Последнее свидетельствует о том, что зарплата граждан отражает их внутреннее состояние; Анализ инфляция-зарплата представлен в промежуточном выводе.')
st.write(txt)



