from flask import Flask, request, jsonify
from app.services import Destinos, Catalogos

app = Flask(__name__)

@app.route('/')
def index():
    return "¡Bienvenido a la API de catalogos de MKV!"



############################ DESTINOS (PAISES) ################################

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



################################# CATALOGOS ####################################

@app.route('/verCatalogos/<int:idDestino>', methods=['GET'])
def ver_catalogos(idDestino):
    respuesta = Catalogos.ver_catalogos(idDestino)
    return jsonify(respuesta)


@app.route('/verCatalogo/<int:idCatalogo>', methods=['GET'])
def ver_catalogo(idCatalogo):
    respuesta = Catalogos.ver_catalogo(idCatalogo)
    return jsonify(respuesta)


