import streamlit as st
import psycopg2
import pandas as pd
import altair as alt

# Pengaturan koneksi ke database PostgreSQL
conn = psycopg2.connect(
    host="10.216.33.4",
    port="5435",
    database="db_pool",
    user="kbd",
    password="P3nG9un4GAd4ng#!"
)

# Fungsi untuk mengambil data dari tabel dan menghitung persentase no_psp tidak null
def get_no_psp_data():
    query = """
    SELECT nama_kl,
           SUM(CASE WHEN no_psp IS NOT NULL THEN 1 ELSE 0 END) AS count_null,
           COUNT(*) AS total
    FROM pool_siman_eksternal.v_ma_aset_tanah
    GROUP BY nama_kl
    """
    data = pd.read_sql_query(query, conn)
    data['percentage'] = data.apply(lambda row: (row['count_null'] / row['total']) * 100 if row['total'] > 0 else 0, axis=1)
    # Mengurutkan data berdasarkan percentage dan mengambil 10 nilai terendah
    data = data.sort_values(by='percentage').head(10)
    return data[['nama_kl', 'percentage']]

# Fungsi untuk mengambil data dari tabel dan menghitung total status_sengketa per nama_kl
def get_status_sengketa_data():
    query = """
    SELECT nama_kl,
           status_sengketa,
           COUNT(*) AS total
    FROM pool_siman_eksternal.v_ma_aset_tanah
    GROUP BY nama_kl, status_sengketa
    """
    data = pd.read_sql_query(query, conn)
    return data

# Streamlit UI
st.title('Dashboard Monitoring Pengelolaan Aset BMN')

# Tombol untuk memuat data dan menampilkan chart persentase no_psp tidak null
if st.button('Tampilkan Chart Persentase PSP'):
    no_psp_data = get_no_psp_data()
    
    # Membuat chart dengan Altair
    no_psp_chart = alt.Chart(no_psp_data).mark_bar().encode(
        x=alt.X('nama_kl', sort=alt.EncodingSortField(field='percentage', order='ascending'), axis=alt.Axis(title='Instansi')),
        y=alt.Y('percentage', axis=alt.Axis(title='Persen'))
    ).properties(
        title='Top 10 Persentase PSP Terendah Tanah Instansi ',
        width=800,
        height=400
    )
    
    st.altair_chart(no_psp_chart, use_container_width=True)

# Tombol untuk memuat data dan menampilkan chart status_sengketa
if st.button('Tampilkan Chart Status Sengketa'):
    status_sengketa_data = get_status_sengketa_data()
    
    # Membuat chart dengan Altair
    status_sengketa_chart = alt.Chart(status_sengketa_data).mark_bar().encode(
        x=alt.X('nama_kl', sort=alt.EncodingSortField(field='total', order='descending'), axis=alt.Axis(title='Instansi')),
        y=alt.Y('total', axis=alt.Axis(title='Total')),
        color=alt.Color('status_sengketa', legend=alt.Legend(title='Status Sengketa'))
    ).properties(
        title='Total Status Sengketa Aset Tanah di Instansi',
        width=800,
        height=400
    )
    
    st.altair_chart(status_sengketa_chart, use_container_width=True)

# Menutup koneksi
conn.close()
