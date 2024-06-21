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
def load_data():
    query = "SELECT * FROM barang"
    df = pd.read_sql(query, engine)
    return df

# Memuat data
df = load_data()

# Membuat aplikasi Streamlit
st.title('Data Barang')

# Filter berdasarkan nama barang
product_names = df['name'].unique()
selected_product = st.selectbox('Pilih Nama Produk', product_names)

# Filter data berdasarkan pilihan
filtered_data = df[df['name'] == selected_product]

# Menampilkan data yang difilter
st.write('Data Barang yang Dipilih:')
st.write(filtered_data)

# Membuat chart
st.write('Chart Harga vs Jumlah')
plt.figure(figsize=(10, 6))
sns.barplot(x='harga', y='jumlah', data=filtered_data)
plt.title('Harga vs Jumlah')
plt.xlabel('Harga')
plt.ylabel('Jumlah')
st.pyplot(plt)
