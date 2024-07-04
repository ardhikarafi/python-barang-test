import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

st.title("Data Analytics - Persentase PSP per Kementerian/Lembaga")

# Koneksi ke database PostgreSQL
conn = psycopg2.connect(
    host="10.216.33.4",
    port="5435",
    database="db_pool",
    user="kbd",
    password="P3nG9un4GAd4ng#!"
)

# Fungsi hash untuk psycopg2 connection
def conn_hash_func(_):
    return None

@st.cache_data(hash_funcs={psycopg2.extensions.connection: conn_hash_func})
def load_data(conn):
    query = """
    SELECT nama_kl, no_psp, kepemilikan
    FROM pool_siman_eksternal.v_ma_aset_tanah
    """
    data = pd.read_sql_query(query, conn)
    return data

data = load_data(conn)
data.rename(columns={'no_psp': 'PSP'}, inplace=True)

# Menghitung persentase PSP per nama_kl
percentage_data = data.groupby('nama_kl')['PSP'].apply(lambda x: (~x.isnull()).mean() * 100).reset_index()
percentage_data.columns = ['nama_kl', 'persentase_PSP']

# Menghitung persentase PSP total
total_PSP = data['PSP'].notnull().sum()
total_rows = data.shape[0]
total_percentage_PSP = (total_PSP / total_rows) * 100

# Menemukan Kementerian/Lembaga yang sudah mencapai 100% PSP
fully_compliant_kl = percentage_data[percentage_data['persentase_PSP'] == 100]['nama_kl'].tolist()

# Menemukan 10 Kementerian/Lembaga dengan persentase PSP terendah
top_10_lowest_kl = percentage_data.sort_values(by='persentase_PSP').head(10)

# Menampilkan total persentase PSP dari seluruh data di atas dengan gaya yang menarik
st.markdown(f"""
    <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; border: 2px solid #007acc; text-align: center;">
        <h2 style="color: #007acc;">Total Persentase PSP dari seluruh data:</h2>
        <h1 style="color: #007acc;">{total_percentage_PSP:.2f}%</h1>
    </div>
    """, unsafe_allow_html=True)

# Visualisasi data
st.header("Persentase PSP per Kementerian/Lembaga")
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='persentase_PSP', y='nama_kl', data=percentage_data.sort_values(by='persentase_PSP'), palette="Blues_d")
ax.set_xlabel('Persentase PSP (%)')
ax.set_ylabel('Kementerian/Lembaga')
ax.set_title('Persentase PSP per Kementerian/Lembaga', fontsize=16, color="#007acc")
st.pyplot(fig)

# Analisis tambahan
st.header("Kementerian/Lembaga yang sudah mencapai 100%")
if fully_compliant_kl:
    st.markdown("<p style='color: #007acc;'>Kementerian/Lembaga:</p>", unsafe_allow_html=True)
    for kl in fully_compliant_kl:
        st.write(f"- {kl}")
else:
    st.markdown("<p style='color: #ff0000;'>Tidak ada Kementerian/Lembaga yang mencapai 100% PSP.</p>", unsafe_allow_html=True)

st.header("Top 10 Kementerian/Lembaga dengan Persentase PSP Terendah")
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='persentase_PSP', y='nama_kl', data=top_10_lowest_kl, palette="Reds_d")
ax.set_xlabel('Persentase PSP (%)')
ax.set_ylabel('Kementerian/Lembaga')
ax.set_title('Top 10 Kementerian/Lembaga dengan Persentase PSP Terendah', fontsize=16, color="#ff0000")
st.pyplot(fig)

# Analisis tambahan berdasarkan kepemilikan
st.header("Analisis Distribusi PSP untuk Kepemilikan Tertentu")
specific_kepemilikan = "Bersertifikat atas nama Pemerintah RI c.q Kementerian/ Lembaga"
filtered_data = data[data['kepemilikan'] == specific_kepemilikan]

plt.figure(figsize=(12, 8))
sns.histplot(filtered_data['PSP'], bins=30, kde=True, color='skyblue')
plt.xlabel('PSP')
plt.ylabel('Frekuensi')
plt.title(f'Distribusi PSP untuk Kepemilikan: "{specific_kepemilikan}"', fontsize=16, color="#007acc")
st.pyplot()

# Close connection
conn.close()
