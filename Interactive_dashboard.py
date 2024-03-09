import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px

st.title('Proyek Analisis Data: [E-Commerce Public Dataset]')
st.markdown("""
- **Nama:** [Rohmatul Ummah]
- **Email:** [rohmatulemma1@gmail.com]
- **ID Dicoding:** [rohmatulummahemma]
""")

#url = 'https://drive.google.com/drive/folders/1zgc5W-5ibHmGFW_BLJ_Hu65P9ZWTh1vV?usp=drive_link'
#hour = pd.read_csv(url)

# Function to load data
#@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

# Load datasets
customer_df = load_data('https://drive.google.com/uc?id=19WRdPaov3Z__BlQqHGWkB5yz2GnTtD71')
order_item_df = load_data('https://drive.google.com/uc?id=1rSVQabuRsgzHEjfRaKRhT9yOZOMfQVhT')
order_payment_df = load_data('https://drive.google.com/uc?id=1nWhQhe0p5vv6FOeEHnBckNH9iCRZbpIb')
orders_df = load_data('https://drive.google.com/uc?id=1-cgj3PSXCw3GHROE8cPUTGt06NL89tGx')
kategori_df = load_data('https://drive.google.com/uc?id=1JSjk_UyHQenJYJ90PACweb6_AOSMYMvp')
products_df = load_data('https://drive.google.com/uc?id=18MQoUu3tXFJdG0jcY_U1HIDvXK6a95SK')
seller_df = load_data('https://drive.google.com/uc?id=1Awh_mQp3HRUuRyzD3ObXKtOLFcfGlacU')

# Display data frames
st.subheader("Customer Data")
st.write(customer_df)

st.subheader("Order Item Data")
st.write(order_item_df)

st.subheader("Order Payment Data")
st.write(order_payment_df)

st.subheader("Orders Data")
st.write(orders_df)

st.subheader("Product Category Data")
st.write(kategori_df)

st.subheader("Products Data")
st.write(products_df)

st.subheader("Seller Data")
st.write(seller_df)

# Mengecek missing Values
customer_df.isna().sum()
order_item_df.isna().sum()
order_payment_df.isna().sum()
orders_df.isna().sum()
kategori_df.isna().sum()
products_df.isna().sum()
seller_df.isna().sum()

#"""### Cleaning Data

#Handling data type
order_item_df['shipping_limit_date'] = pd.to_datetime(order_item_df['shipping_limit_date'])

#"""**Cleaning tabel orders_df**"""

orders_df.isna().sum()

orders_df.dropna(axis=0, inplace=True)

orders_df.isna().sum()

orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
orders_df['order_approved_at'] = pd.to_datetime(orders_df ['order_approved_at'])
orders_df['order_delivered_carrier_date'] = pd.to_datetime(orders_df['order_delivered_carrier_date'])
orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
orders_df['order_estimated_delivery_date'] = pd.to_datetime(orders_df['order_estimated_delivery_date'])



products_df.isna().sum()

# menangani missing values dengan method ffill (mengisi nilai yang hilang dengan nilai dari baris sebelumnya)

products_df['product_weight_g'].fillna(method='ffill', inplace=True)
products_df['product_length_cm'].fillna(method='ffill', inplace=True)
products_df['product_height_cm'].fillna(method='ffill', inplace=True)
products_df['product_width_cm'].fillna(method='ffill', inplace=True)
products_df['product_name_lenght'].fillna(method='ffill', inplace=True)
products_df['product_description_lenght'].fillna(method='ffill', inplace=True)
products_df['product_photos_qty'].fillna(method='ffill', inplace=True)

mode_category = products_df['product_category_name'].mode()[0]
products_df['product_category_name'].fillna(value=mode_category, inplace=True)

products_df.isna().sum()

# EDA
#"""## Exploratory Data Analysis (EDA)

### Explore Tabel

#** products_df dan order_item_df**
infoCategory = pd.merge(products_df[['product_id', 'product_category_name']], order_item_df[['order_id','order_item_id','product_id','shipping_limit_date']], on='product_id', how='inner')

#"""**infoCategory & kategori_df**"""
infoCategory = pd.merge(infoCategory,kategori_df[['product_category_name', 'product_category_name_english']], on='product_category_name', how='inner')

# Menghapus kategori yang bahasa asing
infoCategory = infoCategory.drop('product_category_name',axis=1)

# Mengubah nama kolom kategori dan order item id
infoCategory = infoCategory.rename(columns={'product_category_name_english': 'product_category'})
infoCategory = infoCategory.rename(columns={'order_item_id': 'jumlah_terjual'})


st.subheader("Mengidentifikasi produk-produk terlaris (populer) dan produk-produk terbawah (kurang populer")

# Ambil data count_kategori
count_kategori = infoCategory['product_category'].value_counts()

# Tampilkan data frame di dashboard
st.write("Jumlah Produk per Kategori:")
st.write(count_kategori)

# Mencari kategori teratas (top 10)
kategori_head = count_kategori.head(10)
st.write("Kategori Teratas (Top 10):")
st.dataframe(pd.DataFrame(kategori_head))

# Mencari kategori dengan penjualan paling sedikit (top 10 terbawah)
kategori_tail = count_kategori.tail(10)
st.write("Kategori Terbawah (Top 10):")
st.dataframe(pd.DataFrame(kategori_tail))

st.subheader("Menganalisis pola penjualan dari produk yang paling diminati selama beberapa tahun terakhir")

# Menentukan trend penjualan kategori terlaris
terlaris = count_kategori.head(10)
st.write("Trend Penjualan Kategori Terlaris:")
st.dataframe(pd.DataFrame(terlaris))



# Filter data untuk kategori paling banyak terjual

terlaris_1 = terlaris.index[0]
terlaris_1 = infoCategory[infoCategory['product_category'] == terlaris_1]

terlaris_2 = terlaris.index[1]
terlaris_2 = infoCategory[infoCategory['product_category'] == terlaris_2]

terlaris_3 = terlaris.index[2]
terlaris_3 = infoCategory[infoCategory['product_category'] == terlaris_3]

terlaris_4 = terlaris.index[3]
terlaris_4 = infoCategory[infoCategory['product_category'] == terlaris_4]

terlaris_5 = terlaris.index[4]
terlaris_5 = infoCategory[infoCategory['product_category'] == terlaris_5]

terlaris_6 = terlaris.index[5]
terlaris_6 = infoCategory[infoCategory['product_category'] == terlaris_6]

terlaris_7 = terlaris.index[6]
terlaris_7 = infoCategory[infoCategory['product_category'] == terlaris_7]

terlaris_8 = terlaris.index[7]
terlaris_8 = infoCategory[infoCategory['product_category'] == terlaris_8]

terlaris_9 = terlaris.index[8]
terlaris_9 = infoCategory[infoCategory['product_category'] == terlaris_9]

terlaris_10 = terlaris.index[9]
terlaris_10 = infoCategory[infoCategory['product_category'] == terlaris_10]

# Buat kolom 'month_year' untuk menyimpan bulan dan tahun menggunakan .loc[]

terlaris_1.loc[:, 'month_year'] = terlaris_1['shipping_limit_date'].dt.to_period('Y')
terlaris_2.loc[:, 'month_year'] = terlaris_2['shipping_limit_date'].dt.to_period('Y')
terlaris_3.loc[:, 'month_year'] = terlaris_3['shipping_limit_date'].dt.to_period('Y')
terlaris_4.loc[:, 'month_year'] = terlaris_4['shipping_limit_date'].dt.to_period('Y')
terlaris_5.loc[:, 'month_year'] = terlaris_5['shipping_limit_date'].dt.to_period('Y')
terlaris_6.loc[:, 'month_year'] = terlaris_6['shipping_limit_date'].dt.to_period('Y')
terlaris_7.loc[:, 'month_year'] = terlaris_7['shipping_limit_date'].dt.to_period('Y')
terlaris_8.loc[:, 'month_year'] = terlaris_8['shipping_limit_date'].dt.to_period('Y')
terlaris_9.loc[:, 'month_year'] = terlaris_9['shipping_limit_date'].dt.to_period('Y')
terlaris_10.loc[:, 'month_year'] = terlaris_10['shipping_limit_date'].dt.to_period('Y')

# trend penjualan top 10 kategori

sales_category1 = terlaris_1.groupby('month_year')['jumlah_terjual'].count()
sales_category2= terlaris_2.groupby('month_year')['jumlah_terjual'].count()
sales_category3= terlaris_3.groupby('month_year')['jumlah_terjual'].count()
sales_category4= terlaris_4.groupby('month_year')['jumlah_terjual'].count()
sales_category5 = terlaris_5.groupby('month_year')['jumlah_terjual'].count()
sales_category6= terlaris_6.groupby('month_year')['jumlah_terjual'].count()
sales_category7= terlaris_7.groupby('month_year')['jumlah_terjual'].count()
sales_category8= terlaris_8.groupby('month_year')['jumlah_terjual'].count()
sales_category9= terlaris_9.groupby('month_year')['jumlah_terjual'].count()
sales_category10= terlaris_10.groupby('month_year')['jumlah_terjual'].count()

## Visualization & Explanatory Analysis

st.header('Visualisasi Data')

#sidebar
st.sidebar.header('Settiing Visualisasi Data')


st.subheader('Pertanyaan 1: Apa saja produk-produk terlaris (populer) dan produk-produk terbawah (kurang populer)?')

# Warna untuk plot
color1 = ["#B0C5A4","#6196A6","#6196A6","#6196A6","#6196A6"]
color2 = ["#6196A6","#6196A6","#6196A6","#6196A6","#D37676"]
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# Plot pertama (kategori_head)
axes[0].bar(kategori_head.index, kategori_head.values, color=color1)
axes[0].set_xticks(kategori_head.index)
axes[0].tick_params(axis='x', rotation=90)
axes[0].set_title('Kategori terlaris (banyak diminati)')

# Plot kedua (kategori_tail)
axes[1].bar(kategori_tail.index, kategori_tail.values, color=color2)
axes[1].set_xticks(kategori_tail.index)
axes[1].tick_params(axis='x', rotation=90)
axes[1].set_title('Kategori terbawah (kurang diminati)')

# Menampilkan plot
st.write('Grafik Produk terlaris dan ter-tidak laris')
st.pyplot(fig)

st.subheader('Pertanyaan 2: Bagaimana pola penjualan dari produk yang paling diminati selama beberapa tahun terakhir?')
# Plot kategori trend
plt.figure(figsize=(9, 6))

#pilih warna gemoy
color1 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 1',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category1.plot(kind='line', marker='o', color=color1, markerfacecolor='black', markersize=8, label='Bed & Bath')

color2 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 2',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category2.plot(kind='line', marker='o', color=color2, markerfacecolor='black', markersize=8, label='Health & Beauty')

color3 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 3',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category3.plot(kind='line', marker='o', color=color3, markerfacecolor='black', markersize=8, label='Sports & Leisure')

color4 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 4',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category4.plot(kind='line', marker='o', color=color4, markerfacecolor='black', markersize=8, label='Furniture & Decor')

color5 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 5',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category5.plot(kind='line', marker='o', color=color5, markerfacecolor='black', markersize=8, label='Computers & Accessories')

color6 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 6',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category6.plot(kind='line', marker='o', color=color6, markerfacecolor='black', markersize=8, label='Housewares')

color7 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 7',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category7.plot(kind='line', marker='o', color=color7, markerfacecolor='black', markersize=8, label='waches gifts')

color8 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 8',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category8.plot(kind='line', marker='o', color=color8, markerfacecolor='black', markersize=8, label='telephony')

color9 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 9',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category9.plot(kind='line', marker='o', color=color9, markerfacecolor='black', markersize=8, label='garden tools')

color10 = st.sidebar.select_slider(
    'Pilih warna untuk kategori pola 10',
    options=['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'indigo', 'pink','violet','purple', 'grey']
)
sales_category10.plot(kind='line', marker='o', color=color10, markerfacecolor='black', markersize=8, label='auto')

plt.title('Pola Penjualan Kategori Produk Paling diminati')
plt.xlabel('Tahun')
plt.ylabel('Jumlah')
plt.grid(True)
plt.legend()

# Menampilkan plot
st.write('Trend Penjualan Kategori Produk Terlaris')
st.pyplot(plt)

st.header("Conclusion")
st.markdown(

"""
**Conclution pertanyaan 1**

Data menunjukkan bahwa item terlaris atau yang paling diminati berasal dari kategori seperti perlengkapan tidur dan mandi, kecantikan dan kesehatan, olahraga dan rekreasi, dekorasi dan perabotan, aksesori komputer, peralatan rumah tangga, jam dan hadiah, telepon, hadiah taman, dan otomotif. Produk paling populer berasal dari kategori perlengkapan tidur dan mandi dengan jumlah penjualan tertinggi mencapai 12.718 produk. Sementara itu, kategori dengan penjualan terendah adalah keamanan dan layanan, dengan hanya 2 produk terjual.

Untuk meningkatkan performa penjualan kategori-kategori ini, strategi penjualan perlu ditingkatkan. Ini termasuk melaksanakan kampanye pemasaran yang lebih agresif, melakukan riset pasar untuk mengetahui kebutuhan pelanggan yang lebih baik, serta memperluas variasi produk dan meninjau kembali stok yang ada. Dengan mengadopsi strategi ini, perusahaan dapat meningkatkan daya saingnya, meningkatkan pendapatan, dan memperkuat posisinya di pasar.

**Conclution pertanyaan 2**

Data penjualan menunjukkan bahwa produk perlengkapan tidur dan mandi menjadi yang paling diminati dan mengalami peningkatan signifikan dari tahun 2016 hingga 2018. Peningkatan ini mungkin disebabkan oleh faktor-faktor seperti tren gaya hidup yang berkembang, perubahan preferensi konsumen, atau strategi pemasaran yang berhasil dari produsen atau pengecer. Kemungkinan produk-produk dalam kategori ini menawarkan kualitas yang baik, harga yang terjangkau, atau fitur-fitur yang menarik bagi pelanggan.

Di sisi lain, kategori peralatan rumah tangga mengalami penurunan drastis dari tahun 2018 hingga 2020, meskipun mengalami kenaikan dari tahun 2016 hingga 2018. Penurunan ini mungkin disebabkan oleh beberapa faktor, seperti penurunan daya beli konsumen, perubahan tren gaya hidup, atau persaingan yang meningkat dari kategori produk lain. Produsen atau pengecer dalam kategori ini mungkin perlu mengevaluasi kembali strategi mereka, termasuk inovasi produk, harga, atau pemasaran, untuk memperbaiki kinerja penjualan mereka.
""")