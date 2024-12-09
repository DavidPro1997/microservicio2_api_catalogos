import os
import logging
from app.models import DestinosBase, CatalogosBase


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
    def ver_catalogos(idDestino):
        catalogos = CatalogosBase.ver_catalogos(idDestino)
        if catalogos is not None:
            for element in catalogos:
                incluye = CatalogosBase.ver_incluye_catalogos(element['idCatalogo'])
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
                element['incluye'] = output
            return {"estado":True, "mensaje": "Consulta completada", "datos": catalogos}
        else:
            return {"estado":False, "mensaje": "No tiene catalogos"}  
        
        
    @staticmethod
    def ver_catalogo(idCatalogo):
        detalleCatalogo = CatalogosBase.ver_catalogo(idCatalogo)
        if detalleCatalogo is not None:
            for element in detalleCatalogo:
                incluye = CatalogosBase.ver_incluye_catalogos(element['idCatalogo'])
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
                element['incluye'] = output
            return {"estado":True, "mensaje": "Consulta completada", "datos": detalleCatalogo}
        else:
            return {"estado":False, "mensaje": "No tiene catalogos"} 