import os
import logging
from app.models import DestinosBase, CatalogosBase, ServicioBase, TerminosBase
from collections import defaultdict
import base64
import requests


logging.basicConfig(
    filename = os.path.abspath("logs/output.log"), 
    level=logging.DEBUG,  # Define el nivel de los logs (INFO, DEBUG, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'
)


############################## DESTINOS LOGICA ############################

class Destinos:
    @staticmethod
    def ver_destinos():
        destinos = DestinosBase.ver_destinos()
        if destinos is not None:
            return {"estado":True, "mensaje": "Consulta completada", "datos": destinos}
        else:
            return {"estado":False, "mensaje": "No tiene destinos"}           
     
         
        
############################## CATALOGOS LOGICA ############################

class Catalogos:
    @staticmethod
    def ver_catalogos(idDestino = None):
        catalogos = CatalogosBase.ver_catalogos(idDestino)
        if catalogos is not None:
            for element in catalogos:
                incluye = CatalogosBase.ver_incluye_catalogos(int(element['idCatalogo']))
                element['incluye'] = Catalogos.unificar_servicios(incluye)
            if idDestino is None:
                resultado = Catalogos.agrupar_por_idDestino(catalogos)
                return {"estado":True, "mensaje": "Consulta completada", "datos": resultado}
            else:
                return {"estado":True, "mensaje": "Consulta completada", "datos": catalogos}
        else:
            return {"estado":False, "mensaje": "No tiene catalogos"}  
        
        
    @staticmethod
    def ver_catalogo(idCatalogo):
        detalleCatalogo = CatalogosBase.ver_catalogo(idCatalogo)
        if detalleCatalogo is not None:
            for element in detalleCatalogo:
                incluye = CatalogosBase.ver_incluye_catalogos(element['idCatalogo'])
                terminos = CatalogosBase.ver_terminos_catalogos(element['idCatalogo'])
                element['terminos'] = terminos
                element['incluye'] = Catalogos.unificar_servicios(incluye)
            return {"estado":True, "mensaje": "Consulta completada", "datos": detalleCatalogo}
        else:
            return {"estado":False, "mensaje": "No tiene catalogos"}
        

    @staticmethod
    def editar_catalogo(idCatalogo, data):
        respuesta = CatalogosBase.editar_catalogo(idCatalogo, data)
        return respuesta

        

    @staticmethod
    def descargar_catalogo(idCatalogo):
        catalogoArray = CatalogosBase.ver_catalogo(idCatalogo)
        catalogo = catalogoArray[0]
        if catalogoArray is not None and catalogo is not None:
            ruta = f"https://website.mvevip.com/{catalogo['pdfURL']}"
            base64 = Catalogos.pdf_to_base64(ruta)
            return {"estado":True, "mensaje": "Consulta completada", "datos": base64}
        else:
            return {"estado":False, "mensaje": "No tiene catalogos"}
    

    @staticmethod
    def pdf_to_base64(url):
        response = requests.get(url)
        if response.status_code == 200:
            encoded_pdf = base64.b64encode(response.content).decode('utf-8')
            return encoded_pdf
        else:
            raise Exception(f"Error al descargar el archivo PDF: {response.status_code}")

    
    @staticmethod
    def unificar_servicios(incluye):
        if incluye:
            resultado = {}
            for item in incluye:
                id_servicio = item["idServicio"]
                id_catalogo_servicio = item["idCatalogoServicio"]
                detalle = item["observaciones"]

                # Si el servicio aún no está en resultado, agregarlo
                if id_servicio not in resultado:
                    resultado[id_servicio] = {
                        "idServicio": id_servicio,
                        "nombreServicio": item["nombreServicio"],
                        "observaciones": [
                            {"idCatalogoServicio": id_catalogo_servicio, "detalle": detalle}
                        ],
                    }
                else:
                    # Si el servicio ya existe, agregar la observación al array
                    resultado[id_servicio]["observaciones"].append(
                        {"idCatalogoServicio": id_catalogo_servicio, "detalle": detalle}
                    )
            # Convertir el resultado a una lista
            output = list(resultado.values())
            return output
        else:
            return None
        
    @staticmethod
    def agrupar_por_idDestino(lista_catalogos):
        agrupados = defaultdict(list)  # Creamos un defaultdict para agrupar por idDestino
        
        # Iteramos sobre cada catálogo
        for catalogo in lista_catalogos:
            id_destino = catalogo.get('idDestino')  # Obtenemos el idDestino
            agrupados[id_destino].append(catalogo)  # Agrupamos el catálogo según su idDestino
        
        # Convertimos el defaultdict a una lista de diccionarios
        resultado = [{"idDestino": id_destino, "catalogos": catalogos} for id_destino, catalogos in agrupados.items()]
        return resultado
    

############################## SERVICIOS LOGICA ############################

class Servicios:
    @staticmethod
    def ver_servicios(idCatalogo):
        servicios = ServicioBase.ver_servicios()
        consulta = Catalogos.ver_catalogo(idCatalogo)
        if servicios and consulta:
            catalogo = consulta["datos"][0]
            serviciosCompletos = Servicios.agregar_check(servicios,catalogo["incluye"]) 
            return {"estado":True, "mensaje": "Consulta completada", "datos": serviciosCompletos}
        else:
            return {"estado":False, "mensaje": "Consulta completada"}
        
    
    @staticmethod
    def editar_servicios_catalogo(data):
        resultado = ServicioBase.editar_servicio_catalogo(data["idCatalogoServicio"], data["detalle"])
        return resultado
    

    @staticmethod
    def agregar_servicios_catalogo(data):
        resultado = ServicioBase.agregar_servicio_catalogo(data["idCatalogo"], data["idServicio"], data["detalle"])
        return resultado
    
        

    @staticmethod
    def eliminar_servicios_catalogo_bloque(data):
        resultado = ServicioBase.eliminar_servicio_catalogo_bloque(data["idCatalogo"], data["idServicio"])
        return resultado


    @staticmethod
    def agregar_servicio(data):
        resultado = ServicioBase.agregar_servicio(data["nombre"])
        return resultado


    
    @staticmethod
    def agregar_check(completo, subconjunto):
        subconjunto_ids = {item['idServicio'] for item in subconjunto}
        for item in completo:
            item['check'] = item['idServicio'] in subconjunto_ids
            for sub_item in subconjunto:
                if sub_item['idServicio'] == item['idServicio']:
                    item['observaciones'] = sub_item.get('observaciones', None)  # Agregar las observaciones si existen
                    break
        return completo
          
        

############################## TERMINOS LOGICA ############################

class Terminos:
    @staticmethod
    def ver_terminos(idCatalogo):
        terminos = TerminosBase.ver_terminos()
        consulta = Catalogos.ver_catalogo(idCatalogo)
        if terminos and consulta:
            catalogo = consulta["datos"][0]
            terminosCompletos = Terminos.agregar_check(terminos,catalogo["terminos"]) 
            return {"estado":True, "mensaje": "Consulta completada", "datos": terminosCompletos}
        else:
            return {"estado":False, "mensaje": "Consulta completada"} 
        
    
    @staticmethod
    def agregar_terminos_catalogo(data):
        resultado = TerminosBase.agregar_terminos_catalogo(data["idCatalogo"], data["terminos"])
        return resultado
    

    @staticmethod
    def agregar_termino(data):
        resultado = TerminosBase.agregar_termino(data["nombreTermino"])
        return resultado
    

    @staticmethod
    def eliminar_terminos_catalogo(data):
        resultado = TerminosBase.eliminar_terminos_catalogo(data["idCatalogo"], data["idTermino"])
        return resultado
        
        
    @staticmethod
    def agregar_check(completo, subconjunto):
        subconjunto_ids = {item['idTermino'] for item in subconjunto}
        for item in completo:
            item['check'] = item['idTermino'] in subconjunto_ids
        return completo