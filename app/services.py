import os
import shutil
import logging
from app.models import DestinosBase, CatalogosBase, ServicioBase, TerminosBase, BancosBase
from collections import defaultdict
import base64
import requests
from pathlib import Path


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
        if detalleCatalogo:
            for element in detalleCatalogo:
                incluye = CatalogosBase.ver_incluye_catalogos(element['idCatalogo'])
                terminos = CatalogosBase.ver_terminos_catalogos(element['idCatalogo'])
                element['terminos'] = terminos
                element['incluye'] = Catalogos.unificar_servicios(incluye)
            return {"estado":True, "mensaje": "Consulta completada", "datos": detalleCatalogo}
        else:
            return {"estado":False, "mensaje": "No tiene catalogos"}
        

    @staticmethod
    def agregar_catalogo(data):
        respuesta = CatalogosBase.agregar_catalogo(data)
        return respuesta
    

    @staticmethod
    def editar_catalogo(idCatalogo, data):
        respuesta = CatalogosBase.editar_catalogo(idCatalogo, data)
        return respuesta
    

    @staticmethod
    def editar_catalogo_pdf(data):
        ruta = "/img/destinos/destino_"+data["idDestino"]+"/catalogo_"+data["idCatalogo"]+"/catalogo_"+data["idCatalogo"]+".pdf"
        respuesta = Comun.update_file_from_base64(data["pdf"],ruta)
        if respuesta:
            return {"estado":True, "mensaje": "PDF actualizado correctamente"}
        return {"estado":False, "mensaje": "Error al actualizar pdf"}


        

    @staticmethod
    def descargar_catalogo(idCatalogo):
        catalogoArray = CatalogosBase.ver_catalogo(idCatalogo)
        catalogo = catalogoArray[0]
        if catalogoArray is not None and catalogo is not None:
            ruta = f"https://mvevip.com/img/destinos/destino_{catalogo['idDestino']}/catalogo_{catalogo['idCatalogo']}/catalogo_{catalogo['idCatalogo']}.pdf"
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
            return []
        
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
    def editar_servicios_catalogo_service(data):
        logging.info("aqui ya no vino")
        resutadoEliminar = ServicioBase.eliminar_servicio_catalogo_bloque(data["idCatalogo"], data["idServicio"])
        if resutadoEliminar["estado"]:
            resultado = ServicioBase.agregar_servicio_catalogo(data["idCatalogo"], data["idServicio"], data["detalle"])
            if resultado["estado"]:
                resultado["mensaje"] = "Servicio editado correctamente"
            return resultado
        else:
            return resutadoEliminar
    

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
    

############################## IMAGENES LOGICA ############################
class Imagenes:
    @staticmethod
    def agregar_imagenes(data):
        if "imagenes" in data and data["imagenes"]:
            for imagen in data["imagenes"]:
                url = "/img/destinos/destino_"+data["idDestino"]+"/catalogo_"+data["idCatalogo"]+"/"+imagen["posicion"]+".jpg"
                resultado = Comun.update_file_from_base64(imagen["imagen"], url)
                if resultado is False:
                    return {"estado":False, "mensaje": "Hubo un error al insertar las imagenes"}
            return {"estado":True, "mensaje": "Imagenes insertadas correctamente"}
        else:
            url = "/img/destinos/destino_"+data["idDestino"]+"/header_destino_"+data["idDestino"]+".jpg"
            if "imagen" in data and data["imagen"]:
                resultado = Comun.update_file_from_base64(data["imagen"], url)
                if resultado is True:
                    return {"estado":True, "mensaje": "Se ha guardado la imagen correctamente"}
            return {"estado":False, "mensaje": "Hubo un error al insertar las imagenes"}



############################## DESTINOS LOGICA ############################

class Bancos:
    @staticmethod
    def ver_bancos():
        bancos = BancosBase.ver_bancos()
        if bancos:
            return {"estado":True, "mensaje": "Consulta completada", "datos": bancos}
        else:
            return {"estado":False, "mensaje": "No tiene destinos"} 

    @staticmethod
    def ver_banco(idBanco):
        resultado = BancosBase.ver_banco(idBanco)
        banco = resultado[0]
        if banco:
            ruta = f"/img/bancos/banco_{banco['idBanco']}/campanas"
            imagenes = Bancos.contar_archivos(ruta)
            if imagenes is not None:
                banco["numImagenes"] = imagenes
                return {"estado":True, "mensaje": "Consulta completada", "datos": banco}
        else:
            return {"estado":False, "mensaje": "No tiene bancos"}   
        

    @staticmethod
    def contar_archivos(url):
        system_name = os.name
        if system_name == 'posix':
            ruta_carpeta = "/var/www/html/mvevip_website"+url
        elif system_name == 'nt':
            ruta_carpeta = "C:/xampp/htdocs/MarketingVip/mvevip_website"+url
        else:
            print(f"El sistema operativo es: {system_name}")
            logging.error(f"El sistema operativo es: {system_name}")
            return 0
        try:
            # Verificar si la ruta es válida
            if not os.path.exists(ruta_carpeta):
                print("La ruta no existe.")
                logging.error("La ruta no existe.")
                return 0
            
            # Obtener todos los archivos en la carpeta
            archivos = [f for f in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, f))]
            
            # Retornar la cantidad de archivos
            return len(archivos)
        
        except Exception as e:
            logging.error(f"Ocurrió un error: {e}")
            print(f"Ocurrió un error: {e}")
            return 0

    @staticmethod
    def verificar_banco(data):
        aux = True
        if data["imagenes"]:
            for imagenes in data["imagenes"]:
                if imagenes["posicion"] == '1':
                    ruta = "/img/bancos/banco_"+data["idBanco"]+"/main.jpg"
                    log_imagen = Comun.update_file_from_base64(imagenes["imagen"], ruta)
                    if log_imagen == False:
                        aux = False
                elif imagenes["posicion"] == '2':
                    ruta = "/img/bancos/banco_"+data["idBanco"]+"/header_"+data["idBanco"]+".jpg"
                    log_imagen = Comun.update_file_from_base64(imagenes["imagen"], ruta)
                    if log_imagen == False:
                        aux = False
                else:
                    posicion = int(imagenes["posicion"])-2
                    posicion = str(posicion)
                    ruta = "/img/bancos/banco_"+data["idBanco"]+"/campanas/"+posicion+".jpg"
                    log_imagen = Comun.update_file_from_base64(imagenes["imagen"], ruta)
                    if log_imagen == False:
                        aux = False
        data["imagenes"] = ""
        if data["idBanco"]:
            if aux:
                return BancosBase.editar_banco(data)
        else:
            if aux:
                return BancosBase.agregar_banco(data)
        return {"estado":False, "mensaje": "Ocurrio un error con las imagenes"} 
    

    @staticmethod
    def eliminar_campana(data):
        if data["idBanco"] and data["posicion"]:
            ruta = "/img/bancos/banco_"+data["idBanco"]+"/campanas/"+data["posicion"]+".jpg"
            log_imagen = Comun.eliminar_recurso(ruta)
            if log_imagen == True:
                return {"estado":True, "mensaje": "Se ha eliminado correctamente la imagem"}
            return {"estado":False, "mensaje": "Ocurrio un error al eliminar las imagenes"}
        
        
    @staticmethod
    def descargar_banco(idBanco):
        ruta = f"https://mvevip.com/img/bancos/banco_{idBanco}/banco_{idBanco}.pdf"
        base64 = Catalogos.pdf_to_base64(ruta)
        return {"estado":True, "mensaje": "Consulta completada", "datos": base64}
    
    
    @staticmethod
    def agregar_catalogo_banco_pdf(data):
        ruta = "/img/bancos/banco_"+data["idBanco"]+"/banco_"+data["idBanco"]+".pdf"
        respuesta = Comun.update_file_from_base64(data["pdf"],ruta)
        if respuesta:
            return {"estado":True, "mensaje": "PDF actualizado correctamente"}
        return {"estado":False, "mensaje": "Error al actualizar pdf"}


############################# GOOGLE API #####################################

class Google:
    @staticmethod
    def ver_comentarios():
        API_KEY = "AIzaSyCFbtiQ1Qi8UhexHE5OtkU9XOsayi9ozYo"
        PLACE_ID = "ChIJP-rRHHua1ZERJ9tpyH6hMtg"

        # URL de la API de Google Places
        URL = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=reviews&key={API_KEY}"
        response = requests.get(URL)
        
        if response.status_code == 200:
            data = response.json()
            return {"estado": True, "datos": data, "mensaje":"Se han econtrado comentarios"}
        else:
            print("Error en la solicitud:", response.status_code)
            return {"estado": False, "datos": "Hubo un error al extraer los comentarios",}


############################## FUNCIONES COMUNES ############################
class Comun:
    @staticmethod
    def update_file_from_base64(base64_string, url):
        system_name = os.name
        if system_name == 'posix':
            ruta_guardado = "/var/www/html/mvevip_website"+url
        elif system_name == 'nt':
            ruta_guardado = "C:/xampp/htdocs/MarketingVip/mvevip_website"+url
        else:
            print(f"El sistema operativo es: {system_name}")
            logging.error(f"El sistema operativo es: {system_name}")
            return False
        try:
            Path(ruta_guardado).parent.mkdir(parents=True, exist_ok=True)
            if "," in base64_string:
                base64_string = base64_string.split(",")[1]
            imagen_bytes = base64.b64decode(base64_string)
            with open(ruta_guardado, "wb") as archivo_imagen:
                archivo_imagen.write(imagen_bytes)
            logging.info(f"Imagen Guardada")
            return True
        except Exception as e:
            print(f"Error al guardar la imagen: {e}")
            logging.error(f"Error al guardar la imagen: {e}")
            return False
        
    
    @staticmethod
    def eliminar_recurso(url):
        system_name = os.name
        if system_name == 'posix':
            ruta = "/var/www/html/mvevip_website"+url
        elif system_name == 'nt':
            ruta = "C:/xampp/htdocs/MarketingVip/mvevip_website"+url
        else:
            print(f"El sistema operativo es: {system_name}")
            logging.error(f"El sistema operativo es: {system_name}")
            return False
        try:
            if os.path.isfile(ruta):
                os.remove(ruta)
                return True
            else:
                return True
        except Exception as e:
            return False


