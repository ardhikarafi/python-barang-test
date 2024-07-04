import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import psycopg2

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

# Display the dataset information
df.info()

# Display top 10 rows
print(df.head(10))

# Impute missing values in the column with mean (or median, mode, etc.)
# Ensure column names are correctly matched with DataFrame
column_to_impute = 'total_objek_dioptimalisasi'
if column_to_impute in df.columns:
    df[column_to_impute] = df[column_to_impute].fillna(df[column_to_impute].mean())
else:
    print(f"Column {column_to_impute} not found in DataFrame")

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
    print(f'Mean Squared Error: {mse}')
    print(f'R-squared: {r2}')

# 1.1 NILAI TANAH SENGKETA (NOT INCLUDING JMLH TANAH SENGKETA)
evaluate_model(Y1_test1, Y1_pred1)

# 1.2 JUMLAH_TANAH_BERSENGKETA (NOT INCLUDING NILAI TANAH SENGKETA)
evaluate_model(Y1_test2, Y1_pred2)

# 2.1 NILAI TANAH SENGKETA (NOT INCLUDING JMLH TANAH SENGKETA)
evaluate_model(Y2_test1, Y2_pred1)

# 2.2 JUMLAH_TANAH BERSENGKETA (NOT INCLUDING NILAI TANAH SENGKETA)
evaluate_model(Y2_test2, Y2_pred2)
