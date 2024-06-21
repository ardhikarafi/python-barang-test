from flask import Blueprint, jsonify, request
from .models import Aset, Barang
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

# Endpoint untuk mengambil semua data aset
@bp.route('/getAset', methods=['GET'])
def get_aset():
    asets = Aset.query.all()
    output = []
    for aset in asets:
        aset_data = {
            'id': aset.id,
            'nama_aset': aset.nama_aset,
            'tahun': aset.tahun,
            'nilai_aset': aset.nilai_aset,
            'lokasi_aset': aset.lokasi_aset,
            'pemilik_aset': aset.pemilik_aset
        }
        output.append(aset_data)

    response = {
        "statusCode": 200,
        "message": "Data aset berhasil diambil",
        "response": output
    }
    return jsonify(response)

# Endpoint untuk menambahkan data aset
@bp.route('/addAset', methods=['POST'])
def add_aset():
    data = request.get_json()

    if not data or not 'nama_aset' in data or not 'tahun' in data or not 'nilai_aset' in data or not 'lokasi_aset' in data or not 'pemilik_aset' in data:
        return jsonify({
            "statusCode": 400,
            "message": "Data tidak lengkap",
            "response": None
        }), 400

    new_aset = Aset(
        nama_aset=data['nama_aset'],
        tahun=data['tahun'],
        nilai_aset=data['nilai_aset'],
        lokasi_aset=data['lokasi_aset'],
        pemilik_aset=data['pemilik_aset']
    )

    try:
        db.session.add(new_aset)
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
        "message": "Data aset berhasil ditambahkan",
        "response": {
            "id": new_aset.id,
            "nama_aset": new_aset.nama_aset,
            "tahun": new_aset.tahun,
            "nilai_aset": new_aset.nilai_aset,
            "lokasi_aset": new_aset.lokasi_aset,
            "pemilik_aset": new_aset.pemilik_aset
        }
    }
    return jsonify(response), 201
