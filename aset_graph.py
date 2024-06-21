import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Konfigurasi database PostgreSQL
db_config = {
    'user': 'postgres',
    'password': 'ganteng',
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'postgres'
}

# Membuat engine SQLAlchemy
engine = create_engine(f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

# Fungsi untuk mengambil data dari tabel barang
def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

# Memuat data barang dan aset
df_barang = load_data('barang')
df_aset = load_data('aset')

# Membuat aplikasi Streamlit
st.title('Data Barang dan Aset')

# Tab untuk data barang dan aset
tab1, tab2 = st.tabs(['Barang', 'Aset'])

with tab1:
    st.header('Data Barang')
    
    # Filter berdasarkan nama barang
    product_names = df_barang['name'].unique()
    selected_product = st.selectbox('Pilih Nama Produk', product_names)

    # Filter data berdasarkan pilihan
    filtered_barang = df_barang[df_barang['name'] == selected_product]

    # Menampilkan data yang difilter
    st.write('Data Barang yang Dipilih:')
    st.write(filtered_barang)

    # Membuat chart
    st.write('Chart Harga vs Jumlah')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='harga', y='jumlah', data=filtered_barang)
    plt.title('Harga vs Jumlah')
    plt.xlabel('Harga')
    plt.ylabel('Jumlah')
    st.pyplot(plt)

with tab2:
    st.header('Data Aset')
    
    # Filter berdasarkan nama aset
    asset_names = df_aset['nama_aset'].unique()
    selected_asset = st.selectbox('Pilih Nama Aset', asset_names)

    # Filter data berdasarkan pilihan
    filtered_aset = df_aset[df_aset['nama_aset'] == selected_asset]

    # Menampilkan data yang difilter
    st.write('Data Aset yang Dipilih:')
    st.write(filtered_aset)

    # Membuat chart
    st.write('Chart Nilai Aset vs Tahun')
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='tahun', y='nilai_aset', data=filtered_aset, marker='o')
    plt.title('Nilai Aset vs Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Nilai Aset')
    st.pyplot(plt)
