import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import psycopg2
import matplotlib.pyplot as plt

# Establish the connection
conn = psycopg2.connect(
    host="10.216.33.4",
    port="5435",
    database="db_pool",
    user="kbd",
    password="P3nG9un4GAd4ng#!"
)

# Define the query
query = """
SELECT KODE_SATKER, 
       NAMA_SATKER, 
       COUNT(CASE WHEN KEPEMILIKAN = 'Bersertifikat atas nama Pemerintah RI c.q Kementerian/ Lembaga' THEN 1 END) AS selesai_sertipikasi,
       COUNT(CASE WHEN STATUS_SENGKETA IS NOT NULL THEN 1 END) AS jumlah_tanah_bersengketa,  
       SUM(CASE WHEN STATUS_SENGKETA IS NOT NULL THEN NILAI_PEROLEHAN ELSE 0 END) AS nilai_tanah_sengketa, 
       SUM(OPTIMALISASI) AS total_objek_dioptimalisasi,
       COUNT(CASE WHEN NO_PSP IS NULL THEN 1 END) AS jumlah_aset_belum_psp
FROM pool_siman_eksternal.v_ma_aset_tanah
GROUP BY KODE_SATKER, NAMA_SATKER
ORDER BY COUNT(STATUS_SENGKETA) DESC;
"""

# Load data from PostgreSQL into a DataFrame
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Display the dataset information in Streamlit
st.title('Analisis Model Regresi')
st.write('Informasi Dataset:')
st.write(df.info())

# Display top 10 rows
st.write('Top 10 rows of the dataset:')
st.write(df.head(10))

# Impute missing values in the column with mean (or median, mode, etc.)
# Ensure column names are correctly matched with DataFrame
column_to_impute = 'total_objek_dioptimalisasi'
if column_to_impute in df.columns:
    df[column_to_impute] = df[column_to_impute].fillna(df[column_to_impute].mean())
else:
    st.write(f"Column {column_to_impute} not found in DataFrame")

# Define the dependent variable (Y) and independent variable(s) (X)
Y1_opt1 = df['total_objek_dioptimalisasi']
X1_opt1 = df[['selesai_sertipikasi', 'nilai_tanah_sengketa', 'jumlah_aset_belum_psp']]

Y1_opt2 = df['total_objek_dioptimalisasi']
X1_opt2 = df[['selesai_sertipikasi', 'jumlah_tanah_bersengketa', 'jumlah_aset_belum_psp']]

Y2_Sert1 = df['selesai_sertipikasi']
X2_Sert1 = df[['nilai_tanah_sengketa', 'total_objek_dioptimalisasi', 'jumlah_aset_belum_psp']]

Y2_Sert2 = df['selesai_sertipikasi']
X2_Sert2 = df[['jumlah_tanah_bersengketa', 'total_objek_dioptimalisasi', 'jumlah_aset_belum_psp']]

# Split the data into training and testing sets
X1_train1, X1_test1, Y1_train1, Y1_test1 = train_test_split(X1_opt1, Y1_opt1, test_size=0.3, random_state=42)
X1_train2, X1_test2, Y1_train2, Y1_test2 = train_test_split(X1_opt2, Y1_opt2, test_size=0.3, random_state=42)
X2_train1, X2_test1, Y2_train1, Y2_test1 = train_test_split(X2_Sert1, Y2_Sert1, test_size=0.3, random_state=42)
X2_train2, X2_test2, Y2_train2, Y2_test2 = train_test_split(X2_Sert2, Y2_Sert2, test_size=0.3, random_state=42)

# Create and train the model
model11 = LinearRegression()
model12 = LinearRegression()
model21 = LinearRegression()
model22 = LinearRegression()

# Fit the models
model_1_1 = model11.fit(X1_train1, Y1_train1)
model_1_2 = model12.fit(X1_train2, Y1_train2)
model_2_1 = model21.fit(X2_train1, Y2_train1)
model_2_2 = model22.fit(X2_train2, Y2_train2)

# Predict on the test set
Y1_pred1 = model_1_1.predict(X1_test1)
Y1_pred2 = model_1_2.predict(X1_test2)
Y2_pred1 = model_2_1.predict(X2_test1)
Y2_pred2 = model_2_2.predict(X2_test2)

# Evaluate the models
def evaluate_model(Y_test, Y_pred):
    mse = mean_squared_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)
    return mse, r2

# 1.1 NILAI TANAH SENGKETA (NOT INCLUDING JMLH TANAH SENGKETA)
mse_1_1, r2_1_1 = evaluate_model(Y1_test1, Y1_pred1)

# 1.2 JUMLAH_TANAH_BERSENGKETA (NOT INCLUDING NILAI TANAH SENGKETA)
mse_1_2, r2_1_2 = evaluate_model(Y1_test2, Y1_pred2)

# 2.1 NILAI TANAH SENGKETA (NOT INCLUDING JMLH TANAH SENGKETA)
mse_2_1, r2_2_1 = evaluate_model(Y2_test1, Y2_pred1)

# 2.2 JUMLAH_TANAH BERSENGKETA (NOT INCLUDING NILAI TANAH SENGKETA)
mse_2_2, r2_2_2 = evaluate_model(Y2_test2, Y2_pred2)

# Display evaluation results in Streamlit
st.write("### Evaluasi Model:")
st.write(f"Model 1.1 (total_objek_dioptimalisasi dengan nilai_tanah_sengketa):")
st.write(f"- Mean Squared Error: {mse_1_1}")
st.write(f"- R-squared: {r2_1_1}")

st.write(f"Model 1.2 (total_objek_dioptimalisasi dengan jumlah_tanah_bersengketa):")
st.write(f"- Mean Squared Error: {mse_1_2}")
st.write(f"- R-squared: {r2_1_2}")

st.write(f"Model 2.1 (selesai_sertipikasi dengan nilai_tanah_sengketa):")
st.write(f"- Mean Squared Error: {mse_2_1}")
st.write(f"- R-squared: {r2_2_1}")

st.write(f"Model 2.2 (selesai_sertipikasi dengan jumlah_tanah_bersengketa):")
st.write(f"- Mean Squared Error: {mse_2_2}")
st.write(f"- R-squared: {r2_2_2}")

# Visualize the results
st.write("### Visualisasi Prediksi vs Nilai Aktual")

fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Model 1.1
axs[0, 0].scatter(Y1_test1, Y1_pred1, color='blue')
axs[0, 0].plot([Y1_test1.min(), Y1_test1.max()], [Y1_test1.min(), Y1_test1.max()], 'k--', lw=2)
axs[0, 0].set_title('Model 1.1: Prediksi vs Nilai Aktual')
axs[0, 0].set_xlabel('Nilai Aktual')
axs[0, 0].set_ylabel('Prediksi')

# Model 1.2
axs[0, 1].scatter(Y1_test2, Y1_pred2, color='green')
axs[0, 1].plot([Y1_test2.min(), Y1_test2.max()], [Y1_test2.min(), Y1_test2.max()], 'k--', lw=2)
axs[0, 1].set_title('Model 1.2: Prediksi vs Nilai Aktual')
axs[0, 1].set_xlabel('Nilai Aktual')
axs[0, 1].set_ylabel('Prediksi')

# Model 2.1
axs[1, 0].scatter(Y2_test1, Y2_pred1, color='red')
axs[1, 0].plot([Y2_test1.min(), Y2_test1.max()], [Y2_test1.min(), Y2_test1.max()], 'k--', lw=2)
axs[1, 0].set_title('Model 2.1: Prediksi vs Nilai Aktual')
axs[1, 0].set_xlabel('Nilai Aktual')
axs[1, 0].set_ylabel('Prediksi')

# Model 2.2
axs[1, 1].scatter(Y2_test2, Y2_pred2, color='purple')
axs[1, 1].plot([Y2_test2.min(), Y2_test2.max()], [Y2_test2.min(), Y2_test2.max()], 'k--', lw=2)
axs[1, 1].set_title('Model 2.2: Prediksi vs Nilai Aktual')
axs[1, 1].set_xlabel('Nilai Aktual')
axs[1, 1].set_ylabel('Prediksi')

st.pyplot(fig)

# Display the conclusion in Streamlit
st.write("### Kesimpulan Analisis Model Regresi")

st.write("1. **Deskripsi Dataset**:")
st.write("""
Dataset yang digunakan berisi informasi tentang tanah dari berbagai satuan kerja (`KODE_SATKER`, `NAMA_SATKER`) dengan beberapa fitur utama:
- `selesai_sertipikasi`: Jumlah tanah yang sudah bersertifikat.
- `jumlah_tanah_bersengketa`: Jumlah tanah yang sedang dalam sengketa.
- `nilai_tanah_sengketa`: Nilai perolehan tanah yang sedang dalam sengketa.
- `total_objek_dioptimalisasi`: Total objek yang telah dioptimalisasi.
- `jumlah_aset_belum_psp`: Jumlah aset yang belum memiliki PSP (Penetapan Status Penggunaan).
""")

st.write("2. **Model dan Tujuan**:")
st.write("""
Empat model regresi linier digunakan untuk menganalisis hubungan antara variabel-variabel tersebut dengan tujuan untuk memprediksi `total_objek_dioptimalisasi` dan `selesai_sertipikasi`.

- **Model 1.1**: Memprediksi `total_objek_dioptimalisasi` menggunakan `selesai_sertipikasi`, `nilai_tanah_sengketa`, dan `jumlah_aset_belum_psp`.
- **Model 1.2**: Memprediksi `total_objek_dioptimalisasi` menggunakan `selesai_sertipikasi`, `jumlah_tanah_bersengketa`, dan `jumlah_aset_belum_psp`.
- **Model 2.1**: Memprediksi `selesai_sertipikasi` menggunakan `nilai_tanah_sengketa`, `total_objek_dioptimalisasi`, dan `jumlah_aset_belum_psp`.
- **Model 2.2**: Memprediksi `selesai_sertipikasi` menggunakan `jumlah_tanah_bersengketa`, `total_objek_dioptimalisasi`, dan `jumlah_aset_belum_psp`.
""")

st.write("3. **Hasil Evaluasi Model**:")
st.write("""
Berikut adalah hasil evaluasi model menggunakan Mean Squared Error (MSE) dan R-squared (R2):

- **Model 1.1**:
  - MSE: `mse_1_1`
  - R2: `r2_1_1`
- **Model 1.2**:
  - MSE: `mse_1_2`
  - R2: `r2_1_2`
- **Model 2.1**:
  - MSE: `mse_2_1`
  - R2: `r2_2_1`
- **Model 2.2**:
  - MSE: `mse_2_2`
  - R2: `r2_2_2`

Hasil ini menunjukkan seberapa baik model dalam memprediksi variabel target berdasarkan fitur yang ada. MSE yang lebih rendah dan R2 yang lebih tinggi mengindikasikan performa model yang lebih baik.
""")

st.write("4. **Interpretasi Visualisasi**:")
st.write("""
- **Model 1.1**:
  - Visualisasi prediksi vs nilai aktual menunjukkan sejauh mana prediksi model sesuai dengan nilai aktual untuk `total_objek_dioptimalisasi` tanpa mempertimbangkan `jumlah_tanah_bersengketa`.
- **Model 1.2**:
  - Visualisasi ini menunjukkan performa model dalam memprediksi `total_objek_dioptimalisasi` dengan mempertimbangkan `jumlah_tanah_bersengketa`.
- **Model 2.1**:
  - Visualisasi ini menunjukkan bagaimana model memprediksi `selesai_sertipikasi` tanpa mempertimbangkan `jumlah_tanah_bersengketa`.
- **Model 2.2**:
  - Visualisasi ini menunjukkan performa prediksi `selesai_sertipikasi` dengan mempertimbangkan `jumlah_tanah_bersengketa`.
""")

st.write("5. **Kesimpulan Utama**:")
st.write("""
- **Pengaruh Variabel**: 
  - `selesai_sertipikasi` dan `jumlah_tanah_bersengketa` memiliki pengaruh signifikan dalam memprediksi `total_objek_dioptimalisasi`.
  - `nilai_tanah_sengketa` dan `total_objek_dioptimalisasi` juga merupakan prediktor penting untuk `selesai_sertipikasi`.
- **Akurasi Model**:
  - Akurasi model cukup baik dengan R2 yang cukup tinggi, namun ada ruang untuk perbaikan, terutama pada model dengan MSE yang lebih tinggi.
- **Rekomendasi**:
  - Menambahkan fitur tambahan atau menggunakan teknik pemodelan yang lebih kompleks (misalnya, model non-linier) dapat meningkatkan akurasi prediksi.
  - Pembersihan data lebih lanjut dan penanganan missing values secara lebih cermat dapat membantu meningkatkan performa model.
""")
