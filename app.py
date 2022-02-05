from flask import Flask, jsonify, request
import base64
from dateutil import parser
from cfdiclient import (Autenticacion, DescargaMasiva, Fiel, SolicitaDescarga,
                        VerificaSolicitudDescarga)

app = Flask(__name__)


def get_python_cfdi_token(cer_b64, key_b64, password):
    cer_der = base64.b64decode(cer_b64)
    key_der = base64.b64decode(key_b64)
    fiel = Fiel(cer_der, key_der, password)
    auth = Autenticacion(fiel)
    token = auth.obtener_token()
    return fiel, token


@app.route("/api/v1/SolicitaDescarga", methods=['POST'])
def solicita_descarga():
    try:
        data = request.get_json()
        fiel, token = get_python_cfdi_token(
            data['cer_b64'],
            data['key_b64'],
            data['password'],
        )
        descarga = SolicitaDescarga(fiel)
        solicitud = descarga.solicitar_descarga(
            token,
            data['rfc'],
            parser.parse(data['fecha_inicial']),
            parser.parse(data['fecha_final']),
            rfc_receptor=data['rfc_receptor'] if 'rfc_receptor' in data else None,
            rfc_emisor=data['rfc_emisor'] if 'rfc_emisor' in data else None,
            tipo_solicitud=data['tipo_solicitud']
        )
        return jsonify(solicitud), 200
    except KeyError as e:
        return jsonify(f'Falta atributo: {e}'), 400


@app.route("/api/v1/VerificaSolicitudDescarga", methods=['POST'])
def verifica_solicitud_descarga():
    try:
        data = request.get_json()
        fiel, token = get_python_cfdi_token(
            data['cer_b64'],
            data['key_b64'],
            data['password'],
        )
        verificacion = VerificaSolicitudDescarga(fiel)

        verificacion = verificacion.verificar_descarga(
            token,
            data['rfc'],
            data['id_solicitud']
        )
        return jsonify(verificacion), 200
    except KeyError as e:
        return jsonify(f'Falta atributo: {e}'), 400


@app.route("/api/v1/DescargaMasiva", methods=['POST'])
def descarga_masiva():
    try:
        data = request.get_json()
        fiel, token = get_python_cfdi_token(
            data['cer_b64'],
            data['key_b64'],
            data['password'],
        )
        descarga = DescargaMasiva(fiel)

        descarga = descarga.descargar_paquete(
            token,
            data['rfc'],
            data['paquete']
        )
        return jsonify(descarga), 200
    except KeyError as e:
        return jsonify(f'Falta atributo: {e}'), 400


@app.route("/health", methods=['POST'])
def health():
    return "ok"


@app.route("/", methods=['GET'])
def index():
    return "POST /api/v1/SolicitaDescarga<br/>POST /api/v1/VerificaSolicitudDescarga<br/>POST /api/v1/DescargaMasiva<br/>"
