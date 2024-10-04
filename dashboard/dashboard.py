import pandas as pd

# Membaca file all_data.csv untuk pertanyaan 1 dan 2
all_data = pd.read_csv('https://raw.githubusercontent.com/Bennykw404/Submmission-Data-Analis/refs/heads/main/data/all_data.csv')

# Membaca file geolocation.csv untuk pertanyaan 3
geolocation = pd.read_csv('https://raw.githubusercontent.com/Bennykw404/Submmission-Data-Analis/refs/heads/main/data/geolocation.csv')

# Menghitung jumlah pembelian per kota dan provinsi
purchase_frequency_city = all_data.groupby(['customer_city', 'customer_state'])['customer_unique_id'].count().reset_index()
purchase_frequency_city = purchase_frequency_city.rename(columns={'customer_unique_id': 'purchase_count'}).sort_values(by='purchase_count', ascending=False)

# Visualisasi Frekuensi Pembelian per Kota
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.header("Frekuensi Pembelian Pelanggan per Kota dan Provinsi")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=purchase_frequency_city.head(10), x='purchase_count', y='customer_city', palette='viridis', ax=ax)
ax.set_title('10 Kota dengan Frekuensi Pembelian Tertinggi', fontsize=16)
ax.set_xlabel('Jumlah Pembelian', fontsize=12)
ax.set_ylabel('Kota', fontsize=12)
st.pyplot(fig)


# Menghitung durasi pengiriman (hari) dari tanggal pembelian ke pengiriman
all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])
all_data['order_delivered_customer_date'] = pd.to_datetime(all_data['order_delivered_customer_date'])
all_data['delivery_duration'] = (all_data['order_delivered_customer_date'] - all_data['order_purchase_timestamp']).dt.days

# Filter data yang memiliki nilai valid di 'delivery_duration'
data_filtered = all_data[all_data['delivery_duration'].notnull()]

# Mengelompokkan data berdasarkan bulan untuk menghitung rata-rata durasi pengiriman
data_filtered['order_purchase_month'] = data_filtered['order_purchase_timestamp'].dt.to_period('M')
monthly_avg_delivery_duration = data_filtered.groupby('order_purchase_month')['delivery_duration'].mean()

# Visualisasi Rata-rata Waktu Pengiriman
st.header("Tren Rata-rata Waktu Pengiriman dari Waktu ke Waktu")
fig, ax = plt.subplots(figsize=(12, 6))
monthly_avg_delivery_duration.plot(kind='line', marker='o', ax=ax)
ax.set_title('Tren Rata-rata Waktu Pengiriman per Bulan', fontsize=16)
ax.set_xlabel('Bulan Pembelian', fontsize=12)
ax.set_ylabel('Rata-rata Waktu Pengiriman (Hari)', fontsize=12)
ax.grid(True)
st.pyplot(fig)


# Menghitung jumlah pembeli per kota
customer_city_count = all_data.groupby('customer_city')['customer_unique_id'].count().reset_index()
customer_city_count = customer_city_count.rename(columns={'customer_unique_id': 'purchase_count'}).sort_values(by='purchase_count', ascending=False)

# Visualisasi Jumlah Pembeli per Kota
st.header("Kota dengan Jumlah Pembeli Terbanyak")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=customer_city_count.head(10), x='purchase_count', y='customer_city', palette='coolwarm', ax=ax)
ax.set_title('10 Kota dengan Jumlah Pembeli Terbanyak', fontsize=16)
ax.set_xlabel('Jumlah Pembeli', fontsize=12)
ax.set_ylabel('Kota', fontsize=12)
st.pyplot(fig)