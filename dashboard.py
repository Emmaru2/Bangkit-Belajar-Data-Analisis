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

#"""**Cleaning tabel products_df**"""

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

#**Merge products_df dan order_item_df**
kategori_info = pd.merge(products_df[['product_id', 'product_category_name']], order_item_df[['order_id','order_item_id','product_id','shipping_limit_date']], on='product_id', how='inner')

#"""**Merge kategori_info & kategori_df**"""
kategori_info = pd.merge(kategori_info,kategori_df[['product_category_name', 'product_category_name_english']], on='product_category_name', how='inner')

# Menghapus kategori yang bahasa asing
kategori_info = kategori_info.drop('product_category_name',axis=1)

# Mengubah nama kolom kategori dan order item id
kategori_info = kategori_info.rename(columns={'product_category_name_english': 'product_category'})
kategori_info = kategori_info.rename(columns={'order_item_id': 'jumlah_terjual'})


#st.subheader("Mengidentifikasi produk-produk terlaris (populer) dan produk-produk terbawah (kurang populer"))

# Ambil data count_kategori
count_kategori = kategori_info['product_category'].value_counts()

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

# Menentukan trend penjualan kategori terlaris
terlaris = count_kategori.head(10)
st.write("Trend Penjualan Kategori Terlaris:")
st.dataframe(pd.DataFrame(terlaris))



# Filter data untuk kategori paling banyak terjual

terlaris_1 = terlaris.index[0]
terlaris_1 = kategori_info[kategori_info['product_category'] == terlaris_1]

terlaris_2 = terlaris.index[1]
terlaris_2 = kategori_info[kategori_info['product_category'] == terlaris_2]

terlaris_3 = terlaris.index[2]
terlaris_3 = kategori_info[kategori_info['product_category'] == terlaris_3]

terlaris_4 = terlaris.index[3]
terlaris_4 = kategori_info[kategori_info['product_category'] == terlaris_4]

terlaris_5 = terlaris.index[4]
terlaris_5 = kategori_info[kategori_info['product_category'] == terlaris_5]

terlaris_6 = terlaris.index[5]
terlaris_6 = kategori_info[kategori_info['product_category'] == terlaris_6]

terlaris_7 = terlaris.index[6]
terlaris_7 = kategori_info[kategori_info['product_category'] == terlaris_7]

terlaris_8 = terlaris.index[7]
terlaris_8 = kategori_info[kategori_info['product_category'] == terlaris_8]

terlaris_9 = terlaris.index[8]
terlaris_9 = kategori_info[kategori_info['product_category'] == terlaris_9]

terlaris_10 = terlaris.index[9]
terlaris_10 = kategori_info[kategori_info['product_category'] == terlaris_10]

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

sales_kategory1_trend = terlaris_1.groupby('month_year')['jumlah_terjual'].count()
sales_kategory2_trend = terlaris_2.groupby('month_year')['jumlah_terjual'].count()
sales_kategory3_trend = terlaris_3.groupby('month_year')['jumlah_terjual'].count()
sales_kategory4_trend = terlaris_4.groupby('month_year')['jumlah_terjual'].count()
sales_kategory5_trend = terlaris_5.groupby('month_year')['jumlah_terjual'].count()
sales_kategory6_trend = terlaris_6.groupby('month_year')['jumlah_terjual'].count()
sales_kategory7_trend = terlaris_7.groupby('month_year')['jumlah_terjual'].count()
sales_kategory8_trend = terlaris_8.groupby('month_year')['jumlah_terjual'].count()
sales_kategory9_trend = terlaris_9.groupby('month_year')['jumlah_terjual'].count()
sales_kategory10_trend = terlaris_10.groupby('month_year')['jumlah_terjual'].count()

#"""***Menganalisis profil pelanggan yang kita punya secara demografis***

#Merge products_df & product_category_df

products2_df = pd.merge(
    left=products_df,
    right=kategori_df,
    how='outer',
    left_on='product_category_name',
    right_on='product_category_name'
)
#"""Merge order_items_df & order_payment_df"""

orders2_df = pd.merge(
    left=order_item_df,
    right=order_payment_df,
    how='outer',
    left_on='order_id',
    right_on='order_id'
)

#"""Merge orders2_df & products2_df"""

gabungan1_df = pd.merge(
    left=orders2_df,
    right=products2_df,
    how='outer',
    left_on='product_id',
    right_on='product_id'
)

#"""Merge orders_df & customers_df"""

orders_customers_df = pd.merge(
    left=orders_df,
    right=customer_df,
    how='outer',
    left_on='customer_id',
    right_on='customer_id'
)

#"""Merge gabungan1_df & orders_customers_df"""
all_df = pd.merge(
    left=gabungan1_df,
    right=orders_customers_df,
    how='left',
    left_on='order_id',
    right_on='order_id'
)

all_df = all_df.dropna(subset='customer_zip_code_prefix')

all_df['customer_zip_code_prefix'] = all_df['customer_zip_code_prefix'].astype(int)

#"""Explore customer_df"""

orders_customers_df.dropna(axis=0, inplace=True)

delivery_time = orders_customers_df["order_delivered_customer_date"] - orders_customers_df["order_approved_at"]
delivery_time = delivery_time.apply(lambda x: x.total_seconds())
orders_customers_df["delivery_time"] = round(delivery_time/60)

orders_customers_df['delivery_time'].describe()
orders_customers_df = orders_customers_df.drop(orders_customers_df[orders_customers_df['delivery_time'] < 1].index)
orders_customers_df['delivery_time'].describe()
orders_customers_df.sort_values(by='delivery_time', ascending=True)
orders_customers_df["delivery_time"] = round(delivery_time/86400)
orders_customers_df['delivery_time'].describe()
orders_customers_df.sort_values(by='delivery_time', ascending=True)
orders_customers_df = orders_customers_df.dropna(subset=['delivery_time'])
orders_customers_df['delivery_time'] = orders_customers_df['delivery_time'].astype(int)
orders_customers_df.groupby(by='customer_city').customer_id.nunique().reset_index().sort_values(by='customer_id', ascending=False)
orders_customers_df.groupby(by='customer_state').customer_id.nunique().reset_index().sort_values(by='customer_id', ascending=False).head(5)

#"""Explore gabungan1_df"""

revenue_bycategory_df = gabungan1_df.groupby(by='product_category_name_english').agg({
    'payment_value':['sum','min','max','mean'],
    'order_item_id':'sum'
})
revenue_bycategory_df.rename(columns={
    'payment_value':'revenue',
    'order_item_id':'quantity'
}, inplace=True)
revenue_bycategory_df.sort_values(by=[('revenue', 'mean')], ascending=False).head(10)

price_bycategory_df = gabungan1_df.groupby(by='product_category_name_english').agg({
    'price':['min','max','mean']
})
price_bycategory_df.sort_values(by=[('price','mean')], ascending=False)


## Visualization & Explanatory Analysis

st.header('Visualisasi Data')
st.subheader('Pertanyaan 1: Apa saja produk-produk terlaris (populer) dan produk-produk terbawah (kurang populer)?')

color1 = ['green','blue','blue','blue','blue']
color2 = ['blue','blue','blue','blue','red']

# Plot pertama (kategori_head)
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
axes[0].bar(kategori_head.index, kategori_head.values, color=color1)
axes[0].set_xticks(kategori_head.index)
axes[0].tick_params(axis='x', rotation=90)
axes[0].set_title('Kategori terlaris (populer)')

# Plot kedua (kategori_tail)
axes[1].bar(kategori_tail.index, kategori_tail.values, color=color2)
axes[1].set_xticks(kategori_tail.index)
axes[1].tick_params(axis='x', rotation=90)
axes[1].set_title('Kategori terbawah (kurang populer)')

# Menampilkan plot
st.write('Grafik Produk terlaris dan ter-tidak laris')
st.pyplot(fig)

# Plot kategori trend
plt.figure(figsize=(9, 6))

# Plot kategori 1
sales_kategory1_trend.plot(kind='line', marker='o', color='blue', markerfacecolor='white', markersize=8, label='Bed & Bath')

# Plot kategori 2
sales_kategory2_trend.plot(kind='line', marker='o', color='red', markerfacecolor='white', markersize=8, label='Health & Beauty')

# Plot kategori 3
sales_kategory3_trend.plot(kind='line', marker='o', color='green', markerfacecolor='white', markersize=8, label='Sports & Leisure')

# Plot kategori 4
sales_kategory4_trend.plot(kind='line', marker='o', color='purple', markerfacecolor='white', markersize=8, label='Furniture & Decor')

# Plot kategori 5
sales_kategory5_trend.plot(kind='line', marker='o', color='yellow', markerfacecolor='white', markersize=8, label='Computers & Accessories')

# Plot kategori 6
sales_kategory6_trend.plot(kind='line', marker='o', color='blue', markerfacecolor='white', markersize=8, label='Bed & Bath')

# Plot kategori 7
sales_kategory7_trend.plot(kind='line', marker='o', color='red', markerfacecolor='white', markersize=8, label='Health & Beauty')

# Plot kategori 8
sales_kategory8_trend.plot(kind='line', marker='o', color='green', markerfacecolor='white', markersize=8, label='Sports & Leisure')

# Plot kategori 9
sales_kategory9_trend.plot(kind='line', marker='o', color='purple', markerfacecolor='white', markersize=8, label='Furniture & Decor')

# Plot kategori 10
sales_kategory10_trend.plot(kind='line', marker='o', color='yellow', markerfacecolor='white', markersize=8, label='Computers & Accessories')

plt.title('Trend Penjualan Kategori Produk Terlaris')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Penjualan')
plt.grid(True)
plt.legend()

# Menampilkan plot
st.write('Trend Penjualan Kategori Produk Terlaris')
st.pyplot(plt)

st.subheader('Pertanyaan 2: Bagaimana profil pelanggan yang kita punya secara demografis?')

# Hitung jumlah pelanggan berdasarkan negara bagian
customer_bystate = all_df.groupby(by='customer_state').customer_id.nunique().sort_values(ascending=False).reset_index()

# Hitung jumlah pelanggan berdasarkan kota
customer_bycity = all_df.groupby(by='customer_city').customer_id.nunique().sort_values(ascending=False).reset_index()

# Tampilkan grafik jumlah pelanggan berdasarkan negara bagian
plt.figure(figsize=(10, 5))
colors_ = ["#E1AFD1", "#FFE6E6", "#FFE6E6", "#FFE6E6", "#FFE6E6"]
sns.barplot(
    y='customer_state',
    x='customer_id',
    data=customer_bystate.head(5).sort_values(by="customer_id", ascending=False),
    palette=colors_
)
plt.title('Jumlah pelanggan berdasarkan negara bagian', loc='center', fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

# Menampilkan plot jumlah pelanggan berdasarkan negara bagian
st.write('Menampilkan plot jumlah pelanggan berdasarkan negara bagian')
st.pyplot(plt)

# Tampilkan grafik jumlah pelanggan berdasarkan kota
plt.figure(figsize=(10, 5))
colors_ = ["#E1AFD1", "#FFE6E6", "#FFE6E6", "#FFE6E6", "#FFE6E6"]
sns.barplot(
    y='customer_city',
    x='customer_id',
    data=customer_bycity.head(5).sort_values(by="customer_id", ascending=False),
    palette=colors_
)
plt.title('Jumlah pelanggan berdasarkan kota', loc='center', fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

# Menampilkan plot jumlah pelanggan berdasarkan kota
st.write('Menampilkan plot jumlah pelanggan berdasarkan kota')
st.pyplot(plt)

st.subheader('Pertanyaan 3: Berapa kisaran harga produk secara keseluruhan dalam setiap kategori?')


# Hitung harga rata-rata per kategori produk
price_bycategory = gabungan1_df.groupby(by='product_category_name_english').price.mean().sort_values(ascending=True).reset_index()

# Tampilkan lima kategori produk dengan harga rata-rata tertinggi
top_5_price_bycategory = price_bycategory.head(5).sort_values(by="price", ascending=False)

# Tampilkan grafik harga rata-rata per kategori produk
plt.figure(figsize=(10, 5))
colors_ = ["#E1AFD1", "#FFE6E6", "#FFE6E6", "#FFE6E6", "#FFE6E6"]
sns.barplot(
    y='product_category_name_english',
    x='price',
    data=top_5_price_bycategory,
    palette=colors_
)
plt.title('Harga rata-rata produk per kategori', loc='center', fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

# Menampilkan plot harga rata-rata per kategori produk
st.write('Menampilkan plot harga rata-rata per kategori produk')
st.pyplot(plt)

st.header("Conclusion")
st.markdown(

"""
**Conclution pertanyaan 1**

Analisis penjualan menunjukkan perbedaan yang signifikan di antara kategori produk, di mana beberapa kategori memiliki tingkat penjualan yang tinggi sementara yang lain rendah. Kategori seperti perabotan rumah tangga, produk kesehatan & kecantikan, serta perlengkapan olahraga menunjukkan minat yang besar dari pelanggan dan memegang posisi yang kuat di pasar.

Tren menunjukkan bahwa top 10 kategori teratas semakin diminati oleh konsumen seiring berjalannya waktu. Oleh karena itu, perusahaan dapat mempertimbangkan untuk meningkatkan stok produk dalam kategori-kategori ini atau mencari cara untuk meningkatkan penjualan, seperti dengan menjalankan promosi atau diskon khusus.

Di sisi lain, kategori seperti seni & kerajinan, hiburan seperti CD & DVD, dan produk keamanan & layanan menunjukkan tingkat minat yang lebih rendah dari konsumen.

Untuk meningkatkan performa penjualan kategori-kategori ini, strategi penjualan perlu ditingkatkan. Ini termasuk melaksanakan kampanye pemasaran yang lebih agresif, melakukan riset pasar untuk mengetahui kebutuhan pelanggan yang lebih baik, serta memperluas variasi produk dan meninjau kembali stok yang ada. Dengan mengadopsi strategi ini, perusahaan dapat meningkatkan daya saingnya, meningkatkan pendapatan, dan memperkuat posisinya di pasar.


**Conclution pertanyaan 2**

Pelanggan yang dimiliki tersebar di 26 negara bagian dan 4085 kota di seluruh wilayah. Kota Sao Paulo menjadi pusat perhatian dengan jumlah pelanggan tertinggi, mencapai 15044 orang, sementara negara bagian Sao Paulo (SP) memiliki jumlah pelanggan terbanyak, yaitu sebanyak 40489 orang. Sebaliknya, Roraima (RR) merupakan negara bagian dengan jumlah pelanggan paling sedikit, hanya mencapai 41 orang.

Dari data ini, dapat disimpulkan bahwa wilayah Sao Paulo memiliki minat yang signifikan terhadap layanan atau produk, dengan populasi pelanggan yang cukup besar. Sebaliknya, Roraima menunjukkan tingkat penerimaan yang lebih rendah terhadap produk atau layanan kami. Analisis mendalam tentang pola penyebaran pelanggan ini dapat memberikan wawasan berharga untuk merencanakan strategi pemasaran yang lebih efektif dan menyasar wilayah-wilayah potensial untuk pertumbuhan bisnis yang lebih lanjut.


**Conclution pertanyaan 3**

Rata-rata harga produk per kategori menunjukkan perbedaan yang mencolok, menandakan adanya variasi yang signifikan dalam penentuan harga di antara kategori-kategori tersebut. Misalnya, kategori komputer memiliki harga rata-rata yang cukup tinggi, yakni sekitar 1103.6891, sementara kategori home_comfort_2 menonjol sebagai yang terendah dengan harga rata-rata sebesar 24.9 saja.

Analisis rinci terhadap pola harga ini dapat memberikan pemahaman yang lebih dalam tentang dinamika pasar untuk setiap kategori produk. Informasi ini dapat digunakan untuk mengarahkan strategi harga yang tepat, serta memperkuat pemahaman terhadap preferensi dan kebutuhan pelanggan di setiap segmen pasar. Dengan demikian, perusahaan dapat mengoptimalkan penetapan harga, menghadirkan nilai tambah yang lebih besar bagi pelanggan, dan meningkatkan daya saing di pasar.
""")
