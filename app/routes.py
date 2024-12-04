from flask import Flask, request, jsonify
from app.services import Destinos

app = Flask(__name__)

@app.route('/')
def index():
    return "¡Bienvenido a la API de catalogos de MKV!"



######################### DESTINOS #############################

# @app.route('/crearDestino', methods=['POST'])
# def crear_destino():
#     data = request.json
#     respuesta = Switch.verificar_tipo_doc(data)
#     return jsonify(respuesta)


@app.route('/verDestinos', methods=['GET'])
def ver_destinos():
    respuesta = Destinos.ver_destinos()
    return jsonify(respuesta)


# @app.route('/destino/<int:id>', methods=['GET'])
# def descargar_plantilla(id):
#     respuesta = Switch.verificar_tipo_doc_descarga(id)
#     return jsonify(respuesta)



######################### MOSTRAR #############################







# @app.route('/detalleDestino/<int:id>', methods=['GET'])
# def descargar_plantilla(id):
#     respuesta = Switch.verificar_tipo_doc_descarga(id)
#     return jsonify(respuesta)


