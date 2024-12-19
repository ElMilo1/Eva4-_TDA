import mysql.connector
from mysql.connector import Error

class DAO:
    def __init__(self, host="localhost", user="root", password="", database="mi_libreria"):
        """Inicializa la conexión a la base de datos."""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada correctamente.")

    def obtener_usuario(self, username):
        """Obtiene un usuario por su nombre de usuario."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            consulta = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(consulta, (username,))
            resultado = cursor.fetchone()
            return resultado
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            cursor.close()

    def agregar_usuario(self, username, password, role):
        """Agrega un nuevo usuario (administrador o usuario regular)."""
        try:
            cursor = self.connection.cursor()
            consulta = "INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)"
            cursor.execute(consulta, (username, password, role))
            self.connection.commit()
            print("Usuario agregado correctamente.")
        except Error as e:
            print(f"Error al agregar usuario: {e}")
        finally:
            cursor.close()

    def validar_credenciales(self, username, password):
        """Valida las credenciales de un usuario."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            consulta = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
            cursor.execute(consulta, (username, password))
            resultado = cursor.fetchone()
            return resultado
        except Error as e:
            print(f"Error al validar credenciales: {e}")
            return None
        finally:
            cursor.close()

    def eliminar_usuario(self, username):
        """Elimina un usuario por su nombre de usuario."""
        try:
            cursor = self.connection.cursor()
            consulta = "DELETE FROM usuarios WHERE username = %s"
            cursor.execute(consulta, (username,))
            self.connection.commit()
            print("Usuario eliminado correctamente.")
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
        finally:
            cursor.close()


    #  Gestión de Editoriales

    def agregar_editorial(self, nombre, direccion=None, telefono=None, email=None):
        """Agrega una nueva editorial."""
        try:
            cursor = self.connection.cursor()
            consulta = "INSERT INTO editoriales (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(consulta, (nombre, direccion, telefono, email))
            self.connection.commit()
            print("Editorial agregada correctamente.")
        except Error as e:
            print(f"Error al agregar editorial: {e}")
        finally:
            cursor.close()

    def obtener_editoriales(self):
        """Obtiene todas las editoriales."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            consulta = "SELECT * FROM editoriales"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            print(f"Error al obtener editoriales: {e}")
            return []
        finally:
            cursor.close()

    def eliminar_editorial(self, editorial_id):
        """Elimina una editorial si no tiene productos asociados."""
        try:
            cursor = self.connection.cursor()
            consulta = "DELETE FROM editoriales WHERE id = %s"
            cursor.execute(consulta, (editorial_id,))
            self.connection.commit()
            print("Editorial eliminada correctamente.")
        except Error as e:
            print(f"Error al eliminar editorial: {e}")
        finally:
            cursor.close()

    def selec_editar_edit(self,id):
        try:
            cursor = self.connection.cursor()
            sql = 'SELECT * FROM editoriales WHERE id = %s'
            cursor.execute(sql,(id,))
            respuesta = cursor.fetchone()
            return respuesta
        except Error as e:
            print(f'Error al recuperar editorial')
            return []
        finally:
            cursor.close()

    def upd_editorial(self,id,nombre,direccion,telefono,email):
        try:
            cursor =self.connection.cursor()
            sql = 'UPDATE `editoriales` SET `nombre`="%s",`direccion`="%s",`telefono`="%s",`email`= "%s" WHERE id = "%s"'
            values = (nombre,direccion,telefono,email,id)
            cursor.execute(sql,values)
            print("Actualizado correctamente.")
        except Error as e:
            print(f"Error al actualizar: {e}")
        finally:
            cursor.close()

    #  Gestión de Autores 

    def agregar_autor(self, nombre, nacionalidad=None, fecha_nacimiento=None):
        """Agrega un nuevo autor."""
        try:
            cursor = self.connection.cursor()
            consulta = "INSERT INTO autores (nombre, nacionalidad, fecha_nacimiento) VALUES (%s, %s, %s)"
            cursor.execute(consulta, (nombre, nacionalidad, fecha_nacimiento))
            self.connection.commit()
            print("Autor agregado correctamente.")
        except Error as e:
            print(f"Error al agregar autor: {e}")
        finally:
            cursor.close()

    def obtener_autores(self):
        """Obtiene todos los autores."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            consulta = "SELECT * FROM autores"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            print(f"Error al obtener autores: {e}")
            return []
        finally:
            cursor.close()

    def eliminar_autor(self, autor_id):
        """Elimina un autor si no tiene productos asociados."""
        try:
            cursor = self.connection.cursor()
            consulta = "DELETE FROM autores WHERE id = %s"
            cursor.execute(consulta, (autor_id,))
            self.connection.commit()
            print("Autor eliminado correctamente.")
        except Error as e:
            print(f"Error al eliminar autor: {e}")
        finally:
            cursor.close()

    #  Gestión de Productos

    def agregar_producto(self, nombre, tipo, editorial_id, descripcion):
        """Agrega un nuevo producto."""
        try:
            cursor = self.connection.cursor()
            consulta = """
            INSERT INTO productos (nombre, tipo, editorial_id, descripcion)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(consulta, (nombre, tipo, editorial_id, descripcion))
            self.connection.commit()
            print("Producto agregado correctamente.")
        except Error as e:
            print(f"Error al agregar producto: {e}")
        finally:
            cursor.close()

    def asociar_autor_producto(self, producto_id, autor_id):
        """Asocia un autor a un producto."""
        try:
            cursor = self.connection.cursor()
            consulta = "INSERT INTO producto_autor (producto_id, autor_id) VALUES (%s, %s)"
            cursor.execute(consulta, (producto_id, autor_id))
            self.connection.commit()
            print("Autor asociado al producto correctamente.")
        except Error as e:
            print(f"Error al asociar autor al producto: {e}")
        finally:
            cursor.close()

    def obtener_productos(self):
        """Obtiene todos los productos."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            consulta = "SELECT * FROM productos"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            cursor.close()
    
    def eliminar_producto(self,id):
        """Elimina un producto."""
        try:
            cursor = self.connection.cursor()
            sql = 'DELETE FROM productos WHERE id = %s'
            cursor.execute(sql,(id,))
            self.connection.commit()
            print("Producto eliminada con exito.")
        except Error as x:
            print(f'Error al eliminar producto: {x}')
        finally:
            cursor.close()


    # Gestión de Bodegas

    def agregar_bodega(self, nombre, direccion, capacidad):
        """Agrega una nueva bodega."""
        try:
            cursor = self.connection.cursor()
            consulta = "INSERT INTO bodegas (nombre, direccion, capacidad) VALUES (%s, %s, %s)"
            cursor.execute(consulta, (nombre, direccion, capacidad))
            self.connection.commit()
            print("Bodega agregada correctamente.")
        except Error as e:
            print(f"Error al agregar bodega: {e}")
        finally:
            cursor.close()

    def obtener_bodegas(self):
        """Obtiene todas las bodegas."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            consulta = "SELECT * FROM bodegas"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            print(f"Error al obtener bodegas: {e}")
            return []
        finally:
            cursor.close()

    def eliminar_bodegas(self,id):
        """Elimina una bodega."""
        try:
            cursor = self.connection.cursor()
            sql = 'DELETE FROM bodegas WHERE id = %s'
            cursor.execute(sql,(id,))
            self.connection.commit()
            print("Bodega eliminada con exito.")
        except Error as x:
            print(f'Error al eliminar bodega: {x}')
        finally:
            cursor.close()

    # Gestión de Inventario

    def agregar_inventario(self, bodega_id, producto_id, cantidad):
        """Agrega o actualiza el inventario de un producto en una bodega."""
        try:
            cursor = self.connection.cursor()
            consulta = """
            INSERT INTO inventario (bodega_id, producto_id, cantidad)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE cantidad = cantidad + VALUES(cantidad)
            """
            cursor.execute(consulta, (bodega_id, producto_id, cantidad))
            self.connection.commit()
            print("Inventario actualizado correctamente.")
        except Error as e:
            print(f"Error al actualizar inventario: {e}")
        finally:
            cursor.close()

    def obtener_inventario(self):
        """Obtiene el inventario agrupado por bodega, producto y tipo."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            consulta = """
            SELECT 
                b.nombre AS bodega,
                p.nombre AS producto,
                p.tipo AS tipo,
                i.cantidad AS cantidad
            FROM inventario i
            JOIN productos p ON i.producto_id = p.id
            JOIN bodegas b ON i.bodega_id = b.id
            ORDER BY b.nombre, p.nombre;
            """
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            print(f"Error al obtener el inventario: {e}")
            return []
        finally:
            cursor.close()

    

    # Gestión de Movimientos

    def registrar_movimiento(self, bodega_origen_id, bodega_destino_id, usuario_id, productos):
        """Registra un movimiento de productos entre bodegas."""
        try:
            cursor = self.connection.cursor()

            # Insertar movimiento
            consulta_movimiento = """
            INSERT INTO movimientos (bodega_origen_id, bodega_destino_id, usuario_id)
            VALUES (%s, %s, %s)
            """
            cursor.execute(consulta_movimiento, (bodega_origen_id, bodega_destino_id, usuario_id))
            movimiento_id = cursor.lastrowid

            # Insertar detalles del movimiento
            consulta_detalle = """
            INSERT INTO detalle_movimientos (movimiento_id, producto_id, cantidad)
            VALUES (%s, %s, %s)
            """
            for producto_id, cantidad in productos.items():
                cursor.execute(consulta_detalle, (movimiento_id, producto_id, cantidad))

            self.connection.commit()
            print("Movimiento registrado correctamente.")
        except Error as e:
            print(f"Error al registrar movimiento: {e}")
        finally:
            cursor.close()

    def obtener_movimientos(self):
        """Obtiene todos los movimientos registrados."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            consulta = "SELECT * FROM movimientos"
            cursor.execute(consulta)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            print(f"Error al obtener movimientos: {e}")
            return []
        finally:
            cursor.close()
