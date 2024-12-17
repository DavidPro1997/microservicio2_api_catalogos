from flask import Flask, request, jsonify
import os
from app.services import Destinos, Catalogos, Servicios, Terminos, Imagenes
from flask_cors import CORS
import logging


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


@app.route('/verDestinos', methods=['GET'])
def ver_destinos():
    respuesta = Destinos.ver_destinos()
    return jsonify(respuesta)


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


@app.route('/descargarCatalogo/<int:idCatalogo>', methods=['GET'])
def descargar_catalogo(idCatalogo):
    respuesta = Catalogos.descargar_catalogo(idCatalogo)
    return jsonify(respuesta)


@app.route('/editarCatalogo/<int:idCatalogo>', methods=['POST'])
def editar_catalogo(idCatalogo):
    data = request.json
    respuesta = Catalogos.editar_catalogo(idCatalogo, data)
    return jsonify(respuesta)


@app.route('/agregarCatalogoPDF', methods=['POST'])
def editar_catalogo_pdf():
    data = request.json
    respuesta = Catalogos.editar_catalogo_pdf(data)
    return jsonify(respuesta)


@app.route('/agregarCatalogo', methods=['POST'])
def agregar_catalogo():
    data = request.json
    respuesta = Catalogos.agregar_catalogo(data)
    return jsonify(respuesta)


################################# SERVICIOS EN CATALOGOS ####################################

@app.route('/servicios/<int:idCatalogo>', methods=['GET'])
def ver_servicios(idCatalogo):
    respuesta = Servicios.ver_servicios(idCatalogo)
    return jsonify(respuesta)


@app.route('/editarServicioCatalogo', methods=['POST'])
def editar_servicios_catalogo():
    logging.info("realizando edicion de catalogo")
    data = request.json
    respuesta = Servicios.editar_servicios_catalogo_service(data)
    return jsonify(respuesta)


@app.route('/agregarServicioCatalogo', methods=['POST'])
def agregar_servicios_catalogo():
    data = request.json
    respuesta = Servicios.agregar_servicios_catalogo(data)
    return jsonify(respuesta)


@app.route('/eliminarServiciosCatalogoBloque', methods=['POST'])
def eliminar_servicios_catalogo_bloque():
    data = request.json
    respuesta = Servicios.eliminar_servicios_catalogo_bloque(data)
    return jsonify(respuesta)


################################ SERVICIO PURO ###############################


@app.route('/agregarServicio', methods=['POST'])
def agregar_servicios():
    data = request.json
    respuesta = Servicios.agregar_servicio(data)
    return jsonify(respuesta)


################################# TERMINOS CATALOGOS ####################################

@app.route('/terminos/<int:idCatalogo>', methods=['GET'])
def ver_terminos(idCatalogo):
    respuesta = Terminos.ver_terminos(idCatalogo)
    return jsonify(respuesta)


@app.route('/agregarTerminosCatalogo', methods=['POST'])
def agregar_terminos_catalogo():
    data = request.json
    respuesta = Terminos.agregar_terminos_catalogo(data)
    return jsonify(respuesta)

@app.route('/eliminarTerminosCatalogo', methods=['POST'])
def eliminar_terminos_catalogo():
    data = request.json
    respuesta = Terminos.eliminar_terminos_catalogo(data)
    return jsonify(respuesta)

################################### TERMINO PURO ################################

@app.route('/agregarTermino', methods=['POST'])
def agregar_termino():
    data = request.json
    respuesta = Terminos.agregar_termino(data)
    return jsonify(respuesta)


################################### IMAGENES ################################

@app.route('/agregarImagenes', methods=['POST'])
def agregar_imagenes():
    data = request.json
    respuesta = Imagenes.agregar_imagenes(data)
    return jsonify(respuesta)

