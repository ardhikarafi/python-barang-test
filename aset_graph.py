import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Konfigurasi database PostgreSQL
db_config = {
    'user': 'kbd',
    'password': 'P3nG9un4GAd4n!',
    'host': '10.216.33.4',
    'port': '5435',
    'database': 'db_pool'
}

# Membuat koneksi ke database
@st.cache_data  # Meng-cache DataFrame
def load_data():
    engine = create_engine(f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    query = "SELECT * FROM aset"
    df = pd.read_sql(query, engine)
    return df

# Mengambil data dari tabel aset
df_aset = load_data()

# Menambahkan judul dan icon
st.title('Aset Graph')
st.image('https://upload.wikimedia.org/wikipedia/commons/7/73/Logo_kementerian_keuangan_republik_indonesia.png', width=100)

# Menambahkan header
st.header('Data Aset')

# Filter berdasarkan lokasi aset
locations = df_aset['lokasi_aset'].unique()
selected_location = st.selectbox('Pilih Lokasi Aset', locations)

# Filter data berdasarkan lokasi aset yang dipilih
filtered_aset = df_aset[df_aset['lokasi_aset'] == selected_location]

# Menampilkan data yang difilter
st.write('Data Aset yang Dipilih:')
st.write(filtered_aset)
# Fitur ekspor CSV

csv = filtered_aset.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_aset.csv',
    mime='text/csv',
)

# Membuat chart
st.write('Chart Nilai Aset vs Tahun')
plt.figure(figsize=(10, 6))
sns.lineplot(x='tahun', y='nilai_aset', data=filtered_aset, marker='o')
plt.title('Nilai Aset vs Tahun')
plt.xlabel('Tahun')
plt.ylabel('Nilai Aset')
st.pyplot(plt)


