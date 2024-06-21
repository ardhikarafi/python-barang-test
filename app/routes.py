from flask import Blueprint, jsonify, request
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

# Endpoint untuk menambahkan data barang
@bp.route('/barang', methods=['POST'])
def add_barang():
    data = request.get_json()

    if not data or not 'kode' in data or not 'name' in data or not 'harga' in data or not 'jumlah' in data:
        return jsonify({
            "statusCode": 400,
            "message": "Data tidak lengkap",
            "response": None
        }), 400

    new_barang = Barang(
        kode=data['kode'],
        name=data['name'],
        harga=data['harga'],
        jumlah=data['jumlah']
    )

    try:
        db.session.add(new_barang)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "statusCode": 500,
            "message": f"Kesalahan dalam menambahkan data: {str(e)}",
            "response": None
        }), 500

    response = {
        "statusCode": 201,
        "message": "Data barang berhasil ditambahkan",
        "response": {
            "kode": new_barang.kode,
            "name": new_barang.name,
            "harga": new_barang.harga,
            "jumlah": new_barang.jumlah
        }
    }
    return jsonify(response), 201
