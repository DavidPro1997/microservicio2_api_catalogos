import mysql.connector
from app.config import Config 
import logging

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        self.cursor = self.connection.cursor(buffered=True)

    def close(self):
        self.cursor.close()
        self.connection.close()


################################### DESTINOS ###############################

class DestinosBase:
    @classmethod
    def ver_destinos(cls):
        db = Database()
        query = """
                    SELECT d.idDestino, d.destino, AVG(l.estrellas) as estrellas, MIN(l.precio) as precio_minimo, COUNT(l.precio) as numeroCatalogos 
                    FROM destinos as d
                    INNER JOIN lista_catalogos as l
                    ON d.idDestino = l.idDestino
                    GROUP BY l.idDestino
                """
        db.cursor.execute(query)
        resultados = db.cursor.fetchall()
        db.close()
        destinos = []
        for resultado in resultados:
            destino = {
                "idDestino": resultado[0],         # Ajusta el índice según la estructura de tu tabla
                "destino": resultado[1],     # Ajusta el índice según la estructura de tu tabla
                "estrellas": resultado[2],   # Ajusta el índice según la estructura de tu tabla
                "precio_minimo": resultado[3],
                "catalogos": resultado[4]
            }
            destinos.append(destino)
        return destinos if destinos else None
    


################################ CATALOGOS BASE #####################################
        
class CatalogosBase:
    @classmethod
    def ver_catalogos(cls, idDestino=None):
        db = Database()
        try:
            query = """
                        SELECT * from lista_catalogos as l 
                        INNER JOIN destinos as d
                        on l.idDestino = d.idDestino
                    """
            if idDestino:
                query += " WHERE l.idDestino = %s"
                db.cursor.execute(query, (idDestino,))
            else:
                db.cursor.execute(query)
            resultados = db.cursor.fetchall()
            db.close()
            catalogos = []
            for resultado in resultados:
                cat = {
                    "idCatalogo": resultado[0], 
                    "idDestino": resultado[1],         # Ajusta el índice según la estructura de tu tabla
                    "nombre": resultado[2],     # Ajusta el índice según la estructura de tu tabla
                    "precio": resultado[3], 
                    "adultos": resultado[4],
                    "ninos": resultado[5],
                    "dias": resultado[6],  # Ajusta el índice según la estructura de tu tabla
                    "noches": resultado[7],
                    "descripcion": resultado[8],
                    "estrellas": resultado[9], 
                    "visible": resultado[10],  # Ajusta el índice según la estructura de tu tabla
                    "destino": resultado[12]
                }
                catalogos.append(cat)
            return catalogos if catalogos else None
        except Exception as e:
            db.close()
            logging.error(f"Hubo un error "+e)
            print(f"Hubo un error "+e)
            return None
        
    @classmethod
    def ver_catalogo(cls, idCatalogo):
        db = Database()
        query = """
                    SELECT * from lista_catalogos as l 
                    INNER JOIN destinos as d
                    on l.idDestino = d.idDestino
                    where l.id = %s
                """
        db.cursor.execute(query, (idCatalogo,))
        resultados = db.cursor.fetchall()
        db.close()
        catalogos = []
        for resultado in resultados:
            cat = {
                "idCatalogo": resultado[0], 
                "idDestino": resultado[1],         # Ajusta el índice según la estructura de tu tabla
                "nombre": resultado[2],     # Ajusta el índice según la estructura de tu tabla
                "precio": resultado[3], 
                "adultos": resultado[4],
                "ninos": resultado[5],
                "dias": resultado[6],  # Ajusta el índice según la estructura de tu tabla
                "noches": resultado[7],
                "descripcion": resultado[8],
                "estrellas": resultado[9],
                "visible": resultado[10],  # Ajusta el índice según la estructura de tu tabla
                "destino": resultado[12]
            }
            catalogos.append(cat)
        return catalogos

    @classmethod
    def ver_incluye_catalogos(cls, idCatalogo):
        db = Database()
        query = """
                    SELECT sc.idCatalogo as idCatalogo, lc.nombre as nombreCatalogo,s.id as idServicio ,s.nombre as tipoServicio ,sc.detalle as observaciones, sc.id as idCatalogoServicio
                    from catalogos_servicios as sc
                    INNER JOIN servicios as s on sc.idServicio = s.id
                    INNER JOIN lista_catalogos as lc on lc.id = sc.idCatalogo
                    WHERE sc.idCatalogo = %s
                """
        db.cursor.execute(query, (idCatalogo,))
        resultados = db.cursor.fetchall()
        db.close()
        incluye = []
        for resultado in resultados:
            cat = {
                "idServicio": resultado[2],         # Ajusta el índice según la estructura de tu tabla
                "nombreServicio": resultado[3],     # Ajusta el índice según la estructura de tu tabla
                "observaciones": resultado[4],
                "idCatalogoServicio": resultado[5]
            }
            incluye.append(cat)
        return incluye

    @classmethod
    def ver_terminos_catalogos(cls, idCatalogo):
        db = Database()
        query = """
                    SELECT st.idCatalogo, st.idTermino, t.termino
                    from catalogos_terminos as st
                    INNER JOIN terminos as t on st.idTermino = t.idTermino
                    WHERE st.idCatalogo = %s
                """
        db.cursor.execute(query, (idCatalogo,))
        resultados = db.cursor.fetchall()
        db.close()
        terminos = []
        for resultado in resultados:
            term = {
                "idCatalogo": resultado[0],         # Ajusta el índice según la estructura de tu tabla
                "idTermino": resultado[1],     # Ajusta el índice según la estructura de tu tabla
                "termino": resultado[2]
            }
            terminos.append(term)
        return terminos
    
    @classmethod
    def editar_catalogo(cls, idCatalogo, data):
        db = Database()
        query = """
                    UPDATE lista_catalogos SET 
                    idDestino = %s, nombre = %s, precio = %s, adultos = %s, ninos = %s, dias = %s, noches = %s,
                    descripcion = %s, estrellas = %s, visible = %s
                    WHERE id = %s
                """
        try:
            db.cursor.execute(query, (data["idDestino"],data["nombre"],data["precio"],data["adultos"],data["ninos"],data["dias"],data["noches"],data["descripcion"],data["estrellas"],int(data["visible"]),idCatalogo))
            db.connection.commit()  # Confirma la transacción
            resultado = {"estado":True, "mensaje": "Datos actualizados correctamente"}
        except Exception as e:
            db.connection.rollback()  # Revertir si hay un error
            resultado = {"estado":False, "mensaje": "Hubo un error al modificar los datos"}
        finally:
            db.close()
            return resultado

    @classmethod
    def agregar_catalogo(cls,data):
        db = Database()
        query = """INSERT INTO lista_catalogos (idDestino, nombre, precio,adultos, ninos, dias, noches, descripcion, estrellas, visible) 
                    VALUES(%s, %s,%s,%s, %s,%s,%s, %s,%s,%s)
                """
        try:
            db.cursor.execute(query, (data["idDestino"],data["nombre"],data["precio"],data["adultos"],data["ninos"],data["dias"],data["noches"],data["descripcion"],data["estrellas"],int(data["visible"])))
            db.connection.commit()  # Confirma la transacción
            last_inserted_id = db.cursor.lastrowid
            resultado = {"estado":True, "mensaje": "Catalogo insertado correctamente", "idCatalogo": last_inserted_id}
        except Exception as e:
            db.connection.rollback()  # Revertir si hay un error
            resultado = {"estado":False, "mensaje": "Hubo un error al insertar"}
        finally:
            db.close()
            return resultado
################################ SERVICIOS BASE #####################################

class ServicioBase:
    @classmethod
    def ver_servicios(cls):
        db = Database()
        query = """
                    select * from servicios
                """
        db.cursor.execute(query)
        resultados = db.cursor.fetchall()
        db.close()
        servicios = []
        for resultado in resultados:
            servicio = {
                "idServicio": resultado[0],   
                "nombreServicio": resultado[1]
            }
            servicios.append(servicio)
        return servicios
            

    @classmethod
    def agregar_servicio_catalogo(cls, idCatalogo, idServicio, detalles):
        db = Database()
        query = "INSERT INTO catalogos_servicios (idCatalogo, idServicio, detalle) VALUES(%s, %s,%s)"
        try:
            for detalle in detalles:
                db.cursor.execute(query, (idCatalogo,idServicio,detalle))
            db.connection.commit()  # Confirma la transacción
            resultado = {"estado":True, "mensaje": "Servicio insertado correctamente"}
        except Exception as e:
            db.connection.rollback()  # Revertir si hay un error
            resultado = {"estado":False, "mensaje": "Hubo un error al insertar"}
        finally:
            db.close()
            return resultado
        
    
    @classmethod
    def agregar_servicio(cls, nombre):
        db = Database()
        query = "INSERT INTO servicios (nombre) VALUES(%s)"
        try:
            db.cursor.execute(query, (nombre,))
            db.connection.commit()  # Confirma la transacción
            resultado = {"estado":True, "mensaje": "Servicio insertado correctamente"}
        except Exception as e:
            db.connection.rollback()  # Revertir si hay un error
            resultado = {"estado":False, "mensaje": "Hubo un error al insertar"}
        finally:
            db.close()
            return resultado
                
        
    @classmethod
    def eliminar_servicio_catalogo_bloque(cls, idCatalogo, idServicio):
        db = Database()
        query = "DELETE FROM catalogos_servicios WHERE idCatalogo = %s AND idServicio = %s"
        try:
            db.cursor.execute(query, (idCatalogo, idServicio))
            db.connection.commit()  # Confirma la transacción
            resultado = {"estado":True, "mensaje": "Servicio eliminado correctamente"}
        except Exception as e:
            db.connection.rollback()  # Revertir si hay un error
            resultado = {"estado":False, "mensaje": f"Hubo un error al eliminar los datos: {str(e)}"}
        finally:
            db.close()
            return resultado
    

################################ TERMINOS BASE #####################################

class TerminosBase:
    @classmethod
    def ver_terminos(cls):
        db = Database()
        query = """
                    select * from terminos
                """
        db.cursor.execute(query)
        resultados = db.cursor.fetchall()
        db.close()
        terminos = []
        for resultado in resultados:
            servicio = {
                "idTermino": resultado[0],   
                "termino": resultado[1]
            }
            terminos.append(servicio)
        return terminos if terminos else None
    

    @classmethod
    def agregar_termino(cls, nombre):
        db = Database()
        query = "INSERT INTO terminos (termino) VALUES(%s)"
        try:
            db.cursor.execute(query, (nombre,))
            db.connection.commit()  # Confirma la transacción
            resultado = {"estado":True, "mensaje": "Termino insertado correctamente"}
        except Exception as e:
            db.connection.rollback()  # Revertir si hay un error
            resultado = {"estado":False, "mensaje": "Hubo un error al insertar"}
        finally:
            db.close()
            return resultado
    
    
    @classmethod
    def agregar_terminos_catalogo(cls, idCatalogo, terminos):
        db = Database()
        query = "INSERT INTO catalogos_terminos (idCatalogo, idTermino) VALUES(%s,%s)"
        try:
            for termino in terminos:
                db.cursor.execute(query, (idCatalogo,int(termino)))
            db.connection.commit()  # Confirma la transacción
            resultado = {"estado":True, "mensaje": "Terminos insertados correctamente"}
        except Exception as e:
            db.connection.rollback()  # Revertir si hay un error
            resultado = {"estado":False, "mensaje": "Hubo un error al insertar"}
        finally:
            db.close()
            return resultado
        

    @classmethod
    def eliminar_terminos_catalogo(cls, idCatalogo, idTermino):
        db = Database()
        query = "DELETE FROM catalogos_terminos WHERE idCatalogo = %s AND idTermino = %s"
        try:
            db.cursor.execute(query, (idCatalogo, idTermino))
            db.connection.commit()  # Confirma la transacción
            resultado = {"estado":True, "mensaje": "Servicio eliminado correctamente"}
        except Exception as e:
            db.connection.rollback()  # Revertir si hay un error
            resultado = {"estado":False, "mensaje": f"Hubo un error al eliminar los datos: {str(e)}"}
        finally:
            db.close()
            return resultado














