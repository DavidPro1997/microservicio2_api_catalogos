from flask import Flask, request, jsonify
from app.services import Destinos, Catalogos
from flask_cors import CORS


app = Flask(__name__)


# Configuración de CORS específica con encabezados y métodos permitidos
CORS(app, resources={r"/*": {"origins": ["http://dev.mvevip_website.com","https://website.mvevip.com","https://mvevip.com"]}}, 
     supports_credentials=True, 
     allow_headers=["Content-Type", "Authorization"],
     methods=["POST", "OPTIONS", "GET", "DELETE"])



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

@app.route('/verCatalogos', methods=['GET'])
def ver_catalogos_todos():
    respuesta = Catalogos.ver_catalogos()
    return jsonify(respuesta)


@app.route('/verCatalogos/<int:idDestino>', methods=['GET'])
def ver_catalogos(idDestino):
    respuesta = Catalogos.ver_catalogos(idDestino)
    return jsonify(respuesta)


@app.route('/verCatalogo/<int:idCatalogo>', methods=['GET'])
def ver_catalogo(idCatalogo):
    respuesta = Catalogos.ver_catalogo(idCatalogo)
    return jsonify(respuesta)


