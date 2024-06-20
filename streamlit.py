import streamlit as st
import psycopg2
import matplotlib.pyplot as plt

# Koneksi ke database PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="ganteng",
    host="127.0.0.1",
    port="5432"
)

# Fungsi untuk mengambil data barang dari database
def get_barang_from_db():
    cursor = conn.cursor()
    query = "SELECT harga, jumlah, name FROM barang"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

# Tampilkan data menggunakan Streamlit
def main():
    st.title('Grafik Harga dan Jumlah Produk dari Database')

    # Ambil data dari database
    data_barang = get_barang_from_db()

    # Ekstraksi data untuk grafik
    names = [barang[2] for barang in data_barang]
    harga = [barang[0] for barang in data_barang]
    jumlah = [barang[1] for barang in data_barang]

    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    opacity = 0.8

    index = range(len(data_barang))
    rects1 = ax.bar(index, harga, bar_width, alpha=opacity, color='b', label='Harga')
    rects2 = ax.bar([i + bar_width for i in index], jumlah, bar_width, alpha=opacity, color='g', label='Jumlah')

    ax.set_xlabel('Produk')
    ax.set_ylabel('Nilai')
    ax.set_title('Harga dan Jumlah Produk')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(names)
    ax.legend()

    # Tampilkan grafik menggunakan Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()
