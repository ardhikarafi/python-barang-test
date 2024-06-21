from . import db

# Definisi model untuk tabel barang
class Barang(db.Model):
    __tablename__ = 'barang'
    kode = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Float, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
