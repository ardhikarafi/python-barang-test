from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfigurasi database PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ganteng@127.0.0.1:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definisi model untuk tabel barang
class Barang(db.Model):
    __tablename__ = 'barang'
    kode = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Float, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)

# Endpoint untuk mengambil semua data barang
@app.route('/barang', methods=['GET'])
def get_barang():
    barangs = Barang.query.all()
    output = []
    for barang in barangs:
        barang_data = {'kode': barang.kode, 'name': barang.name, 'harga': barang.harga, 'jumlah': barang.jumlah}
        output.append(barang_data)

    # Membungkus data dalam struktur JSON dengan parameter tambahan
    response = {
        "statusCode": 200,
        "message": "Data barang berhasil diambil",
        "response": output
    }
    return jsonify(response)

# Endpoint untuk mengambil semua data barang
@app.route('/listbarangsimple', methods=['GET'])
def get_listbarang():
    barangs = Barang.query.all()
    output = []
    for barang in barangs:
        barang_data = {'kode': barang.kode, 'name': barang.name}
        output.append(barang_data)

    # Membungkus data dalam struktur JSON dengan parameter tambahan
    response = {
        "statusCode": 200,
        "message": "Data barang berhasil diambil",
        "response": output
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
