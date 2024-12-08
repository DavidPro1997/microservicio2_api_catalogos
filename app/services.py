import os
import logging
from app.models import DestinosBase, CatalogosBase
from collections import defaultdict


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
    def unificar_servicios(incluye):
        if incluye:
            resultado = {}
            for item in incluye:
                id_servicio = item["idServicio"]
                observaciones = item["observaciones"]
                if id_servicio not in resultado:
                    resultado[id_servicio] = {
                        "idServicio": id_servicio,
                        "nombreServicio": item["nombreServicio"],
                        "observaciones": [observaciones],
                    }
                else:
                    # Si ya está, agrega la observación
                    resultado[id_servicio]["observaciones"].append(observaciones)
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