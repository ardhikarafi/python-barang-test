from flask import Blueprint, jsonify
from .models import Barang
from . import db

bp = Blueprint('main', __name__)

# Endpoint untuk mengambil semua data barang
@bp.route('/barang', methods=['GET'])
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

# Endpoint untuk mengambil data barang sederhana
@bp.route('/listbarangsimple', methods=['GET'])
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
