import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from dao import DAO  # Asegúrate de que el archivo dao.py esté correctamente configurado
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes")

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Librería Virtual")
        self.geometry("800x600")
        self.resizable(False, False)

        # DAO para la conexión con la base de datos
        self.dao = DAO()

        # Estilo general
        self.configure(bg="#f5f5f5")

        # Frame principal
        self.frame_actual = None
        self.cambiar_frame(LoginFrame)

    def cambiar_frame(self, frame_class):
        if self.frame_actual is not None:
            self.frame_actual.destroy()
        self.frame_actual = frame_class(self)
        self.frame_actual.pack(fill="both", expand=True)

    def cargar_imagen(self, nombre, size):
        """Carga una imagen desde la carpeta 'imagenes'."""
        ruta = os.path.join(IMAGES_DIR, nombre)
        try:
            image = Image.open(ruta)
            image = image.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except FileNotFoundError:
            print(f"Archivo no encontrado: {ruta}")
            return None

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Imagen de fondo
        self.bg_image = master.cargar_imagen("libros.jpg", (800, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Título
        self.title = tk.Label(self, text="Inicio de Sesión", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Campos de entrada
        self.username_label = tk.Label(self, text="Usuario:", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Contraseña:", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        # Botón de inicio de sesión
        self.login_button = tk.Button(self, text="Iniciar Sesión", font=("Arial", 14, "bold"), bg="#007BFF", fg="white",
                                       command=self.iniciar_sesion)
        self.login_button.pack(pady=20)

        # Botón de registrar usuario
        self.register_button = tk.Button(self, text="Registrar Usuario", font=("Arial", 12, "bold"), bg="#28A745", fg="white",
                                         command=self.abrir_registro)
        self.register_button.pack(pady=5)

    def abrir_registro(self):
        self.master.cambiar_frame(RegistroFrame)

    def iniciar_sesion(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Por favor, ingrese todos los campos")
            return

        # Verificar las credenciales con el DAO
        usuario = self.master.dao.validar_credenciales(username, password)
        if usuario:
            if usuario["role"] == "admin":
                self.master.cambiar_frame(AdminFrame)
            else:
                self.master.cambiar_frame(UserFrame)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

class RegistroFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Imagen de fondo
        self.bg_image = master.cargar_imagen("registro.png", (800, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Título
        self.title = tk.Label(self, text="Registrar Usuario", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Campos de entrada
        self.username_label = tk.Label(self, text="Usuario:", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Contraseña:", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        self.role_label = tk.Label(self, text="Rol (admin/user):", font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.role_label.pack(pady=5)
        self.role_entry = tk.Entry(self, font=("Arial", 14))
        self.role_entry.pack(pady=5)

        # Botón para registrar
        self.register_button = tk.Button(self, text="Registrar", font=("Arial", 14, "bold"), bg="#007BFF", fg="white",
                                        command=self.registrar_usuario)
        self.register_button.pack(pady=20)

        # Botón para volver
        self.back_button = tk.Button(self, text="Volver", font=("Arial", 12, "bold"), bg="#DC3545", fg="white",
                                     command=lambda: master.cambiar_frame(LoginFrame))
        self.back_button.pack(pady=10)

    def registrar_usuario(self):
        """Registra un nuevo usuario en la base de datos."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if role not in ["admin", "user"]:
            messagebox.showerror("Error", "El rol debe ser 'admin' o 'user'.")
            return

        try:
            self.master.dao.agregar_usuario(username, password, role)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.master.cambiar_frame(LoginFrame)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

class AdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Imagen de fondo
        self.bg_image = master.cargar_imagen("gestion.jpg", (800, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(self, text="Panel de Administración", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.label.pack(pady=20)

        # Botones de funcionalidades
        self.boton_gestionar_productos = tk.Button(self, text="Gestionar Productos", font=("Arial", 14), bg="#007BFF", fg="white",
                                                command=lambda: master.cambiar_frame(GestionProductosFrame))
        self.boton_gestionar_productos.pack(pady=10)

        self.boton_gestionar_autores = tk.Button(self, text="Gestionar Autores", font=("Arial", 14), bg="#007BFF", fg="white",
                                                command=lambda: master.cambiar_frame(GestionAutoresFrame))
        self.boton_gestionar_autores.pack(pady=10)

        self.boton_gestionar_autores = tk.Button(self, text="Gestionar Editoriales", font=("Arial", 14), bg="#007BFF", fg="white",
                                                command=lambda: master.cambiar_frame(GestionEditorialesFrame))
        self.boton_gestionar_autores.pack(pady=10)

        self.boton_gestionar_bodegas = tk.Button(self, text="Gestionar Bodegas", font=("Arial", 14), bg="#007BFF", fg="white",
                                                command=lambda: master.cambiar_frame(GestionBodegasFrame))
        self.boton_gestionar_bodegas.pack(pady=10)

        self.boton_generar_informes = tk.Button(self, text="Generar Informes", font=("Arial", 14), bg="#007BFF", fg="white",
                                                command=lambda: master.cambiar_frame(GenerarInformesFrame))
        self.boton_generar_informes.pack(pady=10)

        self.logout_button = tk.Button(self, text="Cerrar Sesión", font=("Arial", 14, "bold"), bg="#DC3545", fg="white",
                                        command=lambda: master.cambiar_frame(LoginFrame))
        self.logout_button.pack(pady=20)

class GestionProductosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.title = tk.Label(self, text="Gestión de Productos", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Botones de funcionalidad
        self.boton_agregar = tk.Button(self, text="Agregar Producto", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.abrir_formulario_agregar)
        self.boton_agregar.pack(pady=10)

        self.boton_agregar = tk.Button(self, text="Eliminar Producto", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.form_eliminar_producto)
        self.boton_agregar.pack(pady=10)

        self.boton_listar = tk.Button(self, text="Listar Productos", font=("Arial", 14), bg="#007BFF", fg="white",
                                      command=self.listar_productos)
        self.boton_listar.pack(pady=10)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(AdminFrame))
        self.boton_volver.pack(pady=20)

    def abrir_formulario_agregar(self):
        # Crear una ventana secundaria para agregar un producto
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Producto")
        ventana.geometry("400x400")
        ventana.resizable(False, False)

        # Campos de entrada
        tk.Label(ventana, text="Nombre del Producto:", font=("Arial", 12)).pack(pady=5)
        nombre_entry = tk.Entry(ventana, font=("Arial", 12))
        nombre_entry.pack(pady=5)

        tk.Label(ventana, text="Tipo (libro/revista/enciclopedia):", font=("Arial", 12)).pack(pady=5)
        tipo_entry = tk.Entry(ventana, font=("Arial", 12))
        tipo_entry.pack(pady=5)

        tk.Label(ventana, text="ID de la Editorial:", font=("Arial", 12)).pack(pady=5)
        editorial_entry = tk.Entry(ventana, font=("Arial", 12))
        editorial_entry.pack(pady=5)

        tk.Label(ventana, text="Descripción:", font=("Arial", 12)).pack(pady=5)
        descripcion_entry = tk.Text(ventana, font=("Arial", 12), height=5, width=40)
        descripcion_entry.pack(pady=5)

        # Botón para guardar
        tk.Button(ventana, text="Guardar", font=("Arial", 12), bg="#007BFF", fg="white",
                  command=lambda: self.guardar_producto(nombre_entry.get(), tipo_entry.get(), editorial_entry.get(),
                                                        descripcion_entry.get("1.0", tk.END), ventana)).pack(pady=10)

    def guardar_producto(self, nombre, tipo, editorial_id, descripcion, ventana):
        """Guarda el producto en la base de datos."""
        if not nombre or not tipo or not editorial_id or not descripcion.strip():
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if tipo not in ["libro", "revista", "enciclopedia"]:
            messagebox.showerror("Error", "El tipo debe ser 'libro', 'revista' o 'enciclopedia'.")
            return

        try:
            # Llamar al DAO para agregar el producto
            editorial_id = int(editorial_id)  # Asegurarse de que el ID sea un entero
            self.master.dao.agregar_producto(nombre, tipo, editorial_id, descripcion.strip())
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            ventana.destroy()  # Cerrar la ventana secundaria
        except ValueError:
            messagebox.showerror("Error", "El ID de la editorial debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

    def form_eliminar_producto(self):
        """Ventana de ingreso de id"""
        ventana = tk.Toplevel(self)
        ventana.title("Eliminar producto.")
        ventana.geometry("400x300")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Id del producto a eliminar:", font=("Arial", 12)).pack(pady=5)
        id_entry = tk.Entry(ventana, font=("Arial", 12))
        id_entry.pack(pady=5)

        # Aquí hacemos el ajuste para pasar el id correctamente al método eliminar_bodega
        tk.Button(ventana, text="Seleccionar", font=("Arial", 12), bg="#007BFF", fg="White",
                command=lambda: self.eliminar_producto(id_entry.get(), ventana)).pack(pady=10)

    def eliminar_producto(self, x, ventana):
        """eliminar producto por id"""
        if not x:
            messagebox.showerror("Error", "Ingresa el id de un producto a borrar.")
            return

        try:
            x = int(x)  # Convierte a entero    
            if x <= 0:
                raise ValueError("Ingresa un id valido.")

            # Llama al método eliminar_producto de la clase DAO, pasando el id como argumento
            self.master.dao.eliminar_producto(x)
            messagebox.showinfo("Exito", "Producto eliminado con exito.")
            ventana.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def listar_productos(self):
        productos = self.master.dao.obtener_productos()
        mensaje = "\n".join([f"{p["id"]} - {p["nombre"]} ({p["tipo"]})" for p in productos])
        messagebox.showinfo("Lista de Productos", mensaje if mensaje else "No hay productos disponibles.")

class GestionAutoresFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master)

        # Titulo
        self.title = tk.Label(self, text="Gestion de Autores" , font=("Arial" , 24 , "bold") , bg = "#ffffff", fg="#333333")
        self.title.pack(pady=20)

        #botones
        self.boton_agregar = tk.Button(self, text="Agregar Autor", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.abrir_formulario_agregar_autor)
        self.boton_agregar.pack(pady=10)

        self.boton_agregar = tk.Button(self, text="Eliminar Autor", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.form_eliminar_autor)
        self.boton_agregar.pack(pady=10)

        self.boton_agregar = tk.Button(self, text="Listar autores", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.listar_autor)
        self.boton_agregar.pack(pady=10)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(AdminFrame))
        self.boton_volver.pack(pady=20)

    def abrir_formulario_agregar_autor(self):
            # Crear una ventana secundaria para agregar un producto
            ventana = tk.Toplevel(self)
            ventana.title("Agregar Autor.")
            ventana.geometry("400x400")
            ventana.resizable(False, False)

            # Campos de entrada
            tk.Label(ventana, text="Nombre del autor:", font=("Arial", 12)).pack(pady=5)
            nombre_entry = tk.Entry(ventana, font=("Arial", 12))
            nombre_entry.pack(pady=5)

            tk.Label(ventana, text="Nacionalidad", font=("Arial", 12)).pack(pady=5)
            nacionalidad_entry = tk.Entry(ventana, font=("Arial", 12))
            nacionalidad_entry.pack(pady=5)

            tk.Label(ventana, text="Fecha de nacimiento: (Anio/Mes/Dia)", font=("Arial", 12)).pack(pady=5)
            fecha_entry = tk.Entry(ventana, font=("Arial", 12))
            fecha_entry.pack(pady=5)

            # Botón para guardar
            tk.Button(ventana, text="Guardar", font=("Arial", 12), bg="#007BFF", fg="white",
                    command=lambda: self.guardar_autor(nombre_entry.get(), nacionalidad_entry.get(), fecha_entry.get(),
                                                            ventana)).pack(pady=10)
            
    def guardar_autor(self,nombre,nacionalidad,fecha,ventana):
        """Guarda la bodega en la base de datos."""
        if not nombre or not nacionalidad or not fecha:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            self.master.dao.agregar_autor(nombre, nacionalidad, fecha)
            messagebox.showinfo("Éxito", "Autor agregado correctamente.")
            ventana.destroy()  # Cerrar la ventana secundaria
        except ValueError as e:
            messagebox.showerror("Error", f"Fecha inválida: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar al autor: {e}") 

    def form_eliminar_autor(self):
        """Ventana de ingreso de id"""
        ventana = tk.Toplevel(self)
        ventana.title("Eliminar autor.")
        ventana.geometry("400x300")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Id del autor a eliminar:", font=("Arial", 12)).pack(pady=5)
        id_entry = tk.Entry(ventana, font=("Arial", 12))
        id_entry.pack(pady=5)

        # Aquí hacemos el ajuste para pasar el id correctamente al método eliminar_bodega
        tk.Button(ventana, text="Seleccionar", font=("Arial", 12), bg="#007BFF", fg="White",
                command=lambda: self.eliminar_autor(id_entry.get(), ventana)).pack(pady=10)

    def eliminar_autor(self, x, ventana):
        """eliminar autor por id"""
        if not x:
            messagebox.showerror("Error", "Ingresa el id de un autor a borrar.")
            return

        try:
            x = int(x)  # Convierte a entero    
            if x <= 0:
                raise ValueError("Ingresa un id valido.")

            # Llama al método eliminar_autor de la clase DAO, pasando el id como argumento
            self.master.dao.eliminar_autor(x)
            messagebox.showinfo("Exito", "Autor eliminado con exito.")
            ventana.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def listar_autor(self):
        autores = self.master.dao.obtener_autores()
        respuesta = "\n".join([f"{p["id"]} - {p["nombre"]}({p["nacionalidad"]})" for p in autores])
        messagebox.showinfo("Lista de autores" , respuesta if respuesta else "No hay autores para mostrar")

class GestionEditorialesFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master)

    # Título
        self.title = tk.Label(self, text="Gestión de Editoriales", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Botones de funcionalidad
        self.boton_agregar = tk.Button(self, text="Agregar Editorial", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.abrir_formulario_agregar_editorial)
        self.boton_agregar.pack(pady=10)

        self.boton_eliminar = tk.Button(self, text="Eliminar Editorial", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.form_eliminar_editorial)
        self.boton_eliminar.pack(pady=10)

        self.boton_editar = tk.Button(self, text="Editar Editorial", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.form_select_editorial)
        self.boton_editar.pack(pady=10)

        self.boton_listar = tk.Button(self, text="Listar Editorial", font=("Arial", 14), bg="#007BFF", fg="white",
                                      command=self.listar_Editorial)
        self.boton_listar.pack(pady=10)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(AdminFrame))
        self.boton_volver.pack(pady=20)

    def abrir_formulario_agregar_editorial(self):
        # Crear una ventana secundaria para agregar un Editorial
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Editorial")
        ventana.geometry("400x400")
        ventana.resizable(False, False)

        # Campos de entrada
        tk.Label(ventana, text="Nombre de la Editorial:", font=("Arial", 12)).pack(pady=5)
        nombre_entry = tk.Entry(ventana, font=("Arial", 12))
        nombre_entry.pack(pady=5)

        tk.Label(ventana, text="Direccion:", font=("Arial", 12)).pack(pady=5)
        direccion_entry = tk.Entry(ventana, font=("Arial", 12))
        direccion_entry.pack(pady=5)

        tk.Label(ventana, text="Telefono:", font=("Arial", 12)).pack(pady=5)
        telefono_entry = tk.Entry(ventana, font=("Arial", 12))
        telefono_entry.pack(pady=5)

        tk.Label(ventana, text="email:", font=("Arial", 12)).pack(pady=5)
        email_entry = tk.Entry(ventana, font=("Arial", 12))
        email_entry.pack(pady=5)

        # Botón para guardar
        tk.Button(ventana, text="Guardar", font=("Arial", 12), bg="#007BFF", fg="white",
                  command=lambda: self.agregar_editorial(nombre_entry.get(), direccion_entry.get(),telefono_entry.get(),email_entry.get(), ventana)).pack(pady=10)

    def agregar_editorial(self, nombre, direccion, telefono, email, ventana):
        """Guarda el producto en la base de datos."""
        if not nombre or not direccion or not telefono or not email.strip():
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            self.master.dao.agregar_editorial(nombre, direccion, telefono, email)
            messagebox.showinfo("Éxito", "Editorial agregada correctamente.")
            ventana.destroy()  # Cerrar la ventana secundaria
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la editorial: {e}")

    def form_eliminar_editorial(self):
        """Ventana de ingreso de id"""
        ventana = tk.Toplevel(self)
        ventana.title("Eliminar editorial.")
        ventana.geometry("400x300")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Id de la editorial a eliminar:", font=("Arial", 12)).pack(pady=5)
        id_entry = tk.Entry(ventana, font=("Arial", 12))
        id_entry.pack(pady=5)

        # Aquí hacemos el ajuste para pasar el id correctamente al método eliminar_bodega
        tk.Button(ventana, text="Seleccionar", font=("Arial", 12), bg="#007BFF", fg="White",
                command=lambda: self.eliminar_editorial(id_entry.get(), ventana)).pack(pady=10)

    def eliminar_editorial(self, x, ventana):
        """eliminar editorial por id"""
        if not x:
            messagebox.showerror("Error", "Ingresa el id de una editorial a borrar.")
            return

        try:
            x = int(x)  # Convierte a entero    
            if x <= 0:
                raise ValueError("Ingresa un id valido.")

            # Llama al método eliminar_bodegas de la clase DAO, pasando el id como argumento
            self.master.dao.eliminar_editorial(x)
            messagebox.showinfo("Exito", "Editorial eliminada con exito.")
            ventana.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def form_select_editorial(self):
        """Ventana sleeccion por id"""
        ventana = tk.Toplevel(self)
        ventana.title("Seleccion de editorial por id.")
        ventana.geometry("400x300")
        ventana.resizable(False,False)

        tk.Label(ventana, text="Id de editorial a editar:",font=('Arial',12)).pack(pady=5)
        id_entry = tk.Entry(ventana,font=("Arial",12))
        id_entry.pack(pady=5)

        tk.Button(ventana,text="Seleccionar",font=("Arial",12),bg="#007BFF" , fg="white",
                  command=lambda:self.selec_editorial_edit(id_entry.get(),ventana)).pack(pady=5)

    def selec_editorial_edit(self,x,ventana):
        editorial = self.master.dao.selec_editar_edit(x)
        self.upd_editorial(editorial[0])

    def upd_editorial(self,x1):
        """ventana de edicion"""
        ventana = tk.Toplevel(self)
        ventana.title("Actualizar editorial.")
        ventana.geometry("400x300")
        ventana.resizable(False,False)
        
        tk.Label(ventana,text=f"Id de la editorial a editar:{x1}")
        id_entry = x1
        tk.Label(ventana,text="Nuevo nombre de la editorial.",font=("Arial",12)).pack(pady=5)
        name_entry = tk.Entry(ventana, font=("Arial",12))
        name_entry.pack(pady=5)

        tk.Label(ventana,text="Nueva direccion de la editorial.",font=("Arial",12)).pack(pady=5)
        direccion_entry = tk.Entry(ventana,font=("Arial",12))
        direccion_entry.pack(pady=5)

        tk.Label(ventana,text="Nuevo telefono de la editorial.",font=("Arial",12)).pack(pady=5)
        telefono_entry = tk.Entry(ventana,font=("Arial",12))
        telefono_entry.pack(pady=5)

        tk.Label(ventana,text="Nuevo email de la editorial.",font=("Arial",12)).pack(pady=5)
        email_entry = tk.Entry(ventana,font=("Arial",12))
        email_entry.pack(pady=5)

        tk.Button(ventana,text="Actualizar",font=("Arial",12) , bg="#007BFF" , fg="white",
                  command=lambda: self.guardar_edit(id_entry,name_entry.get(),direccion_entry.get(),telefono_entry.get(),email_entry.get(),ventana)).pack(pady=10)

    
    def guardar_edit(self,x1,x2,x3,x4,x5,ventana):
        if not x1 or not x2 or not x3 or not x4 or not x5:
            messagebox.showerror("Error","Todos los campos son obligatorios.")
            return
        try:
            self.master.dao.upd_editorial(x1,x2,x3,x4,x5)
            messagebox.showinfo("Exito","Editorial actualizada con exito.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo actualizar la editorial: {e}")



    def listar_Editorial(self):
        editoriales = self.master.dao.obtener_editoriales()
        mensaje = "\n".join([f" Id: {p["id"]} - Nombre: {p["nombre"]}" for p in editoriales])
        messagebox.showinfo("Lista de editoriales", mensaje if mensaje else "No hay editoriales disponibles.")

class GestionBodegasFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.title = tk.Label(self, text="Gestión de Bodegas", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Botones de funcionalidad
        self.boton_agregar = tk.Button(self, text="Agregar Bodega", font=("Arial", 14), bg="#007BFF", fg="white",
                                       command=self.abrir_formulario_agregar)
        self.boton_agregar.pack(pady=10)

        self.boton_eliminar = tk.Button(self, text="Eliminar Bodega", font=("Arial", 14) , bg="#007BFF",fg="white",
                                        command=self.form_eliminar)
        self.boton_eliminar.pack(pady=10)

        self.boton_listar = tk.Button(self, text="Listar Bodegas", font=("Arial", 14), bg="#007BFF", fg="white",
                                      command=self.listar_bodegas)
        self.boton_listar.pack(pady=10)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(AdminFrame))
        self.boton_volver.pack(pady=20)

    def abrir_formulario_agregar(self):
        """Abre una ventana secundaria para agregar una nueva bodega."""
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Bodega")
        ventana.geometry("400x300")
        ventana.resizable(False, False)

        # Campos del formulario
        tk.Label(ventana, text="Nombre de la Bodega:", font=("Arial", 12)).pack(pady=5)
        nombre_entry = tk.Entry(ventana, font=("Arial", 12))
        nombre_entry.pack(pady=5)

        tk.Label(ventana, text="Dirección de la Bodega:", font=("Arial", 12)).pack(pady=5)
        direccion_entry = tk.Entry(ventana, font=("Arial", 12))
        direccion_entry.pack(pady=5)

        tk.Label(ventana, text="Capacidad (en unidades):", font=("Arial", 12)).pack(pady=5)
        capacidad_entry = tk.Entry(ventana, font=("Arial", 12))
        capacidad_entry.pack(pady=5)

        # Botón para guardar
        tk.Button(ventana, text="Guardar", font=("Arial", 12), bg="#007BFF", fg="white",
                  command=lambda: self.guardar_bodega(nombre_entry.get(), direccion_entry.get(), capacidad_entry.get(),
                                                     ventana)).pack(pady=10)

    def guardar_bodega(self, nombre, direccion, capacidad, ventana):
        """Guarda la bodega en la base de datos."""
        if not nombre or not direccion or not capacidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            capacidad = int(capacidad)  # Validar que la capacidad sea un número entero
            if capacidad <= 0:
                raise ValueError("La capacidad debe ser mayor a 0.")

            # Llamar al DAO para agregar la bodega
            self.master.dao.agregar_bodega(nombre, direccion, capacidad)
            messagebox.showinfo("Éxito", "Bodega agregada correctamente.")
            ventana.destroy()  # Cerrar la ventana secundaria
        except ValueError as e:
            messagebox.showerror("Error", f"Capacidad inválida: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la bodega: {e}")  

    def form_eliminar(self):
        """Ventana de ingreso de id"""
        ventana = tk.Toplevel(self)
        ventana.title("Eliminar bodega.")
        ventana.geometry("400x300")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Id de la bodega a eliminar:", font=("Arial", 12)).pack(pady=5)
        id_entry = tk.Entry(ventana, font=("Arial", 12))
        id_entry.pack(pady=5)

        # Aquí hacemos el ajuste para pasar el id correctamente al método eliminar_bodega
        tk.Button(ventana, text="Seleccionar", font=("Arial", 12), bg="#007BFF", fg="White",
                command=lambda: self.eliminar_bodega(id_entry.get(), ventana)).pack(pady=10)

    def eliminar_bodega(self, x, ventana):
        """eliminar bodega por id"""
        if not x:
            messagebox.showerror("Error", "Ingresa el id de una bodega a borrar.")
            return

        try:
            x = int(x)  # Convierte a entero    
            if x <= 0:
                raise ValueError("Ingresa un id valido.")

            # Llama al método eliminar_bodegas de la clase DAO, pasando el id como argumento
            self.master.dao.eliminar_bodegas(x)
            messagebox.showinfo("Exito", "Bodega eliminada con exito.")
            ventana.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")

    def listar_bodegas(self):
        bodegas = self.master.dao.obtener_bodegas()
        mensaje = "\n".join([f"{b["id"]} - {b["nombre"]}" for b in bodegas])
        messagebox.showinfo("Lista de Bodegas", mensaje if mensaje else "No hay bodegas disponibles.")

class GenerarInformesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.title = tk.Label(self, text="Generar Informes", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Botones de funcionalidad
        self.boton_inventario = tk.Button(self, text="Informe de Inventario", font=("Arial", 14), bg="#007BFF", fg="white",
                                          command=self.generar_informe_inventario)
        self.boton_inventario.pack(pady=10)

        self.boton_movimientos = tk.Button(self, text="Informe de Movimientos", font=("Arial", 14), bg="#007BFF", fg="white",
                                           command=self.generar_informe_movimientos)
        self.boton_movimientos.pack(pady=10)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(AdminFrame))
        self.boton_volver.pack(pady=20)

    def generar_informe_inventario(self):
        """Genera un informe del inventario por bodega."""
        try:
            # Obtener el inventario desde el DAO
            inventario = self.master.dao.obtener_inventario()

            if not inventario:
                messagebox.showinfo("Informe de Inventario", "No hay productos en el inventario.")
                return

            # Formatear el informe
            informe = []
            for item in inventario:
                informe.append(
                    f"Bodega: {item["bodega"]} - Producto: {item["producto"]} - Tipo: {item["tipo"]} - Cantidad: {item["cantidad"]}"
                )

            mensaje = "\n".join(informe)
            messagebox.showinfo("Informe de Inventario", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el informe de inventario: {e}")

    def generar_informe_movimientos(self):
        movimientos = self.master.dao.obtener_movimientos()
        mensaje = "\n".join([f"ID: {m["id"]} - Origen: {m["bodega_origen_id"]} - Destino: {m["bodega_destino_id"]}" for m in movimientos])
        messagebox.showinfo("Informe de Movimientos", mensaje if mensaje else "No hay movimientos registrados.")

class UserFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Imagen de fondo
        self.bg_image = master.cargar_imagen("user.jpg", (800, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(self, text="Bienvenido Bodeguero", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.label.pack(pady=20)

        self.boton_mover_productos = tk.Button(self, text="Mover Productos", font=("Arial", 14), bg="#007BFF", fg="white",
                                               command=lambda: master.cambiar_frame(MoverProductosFrame))
        self.boton_mover_productos.pack(pady=10)

        self.logout_button = tk.Button(self, text="Cerrar Sesión", font=("Arial", 14, "bold"), bg="#DC3545", fg="white",
                                        command=lambda: master.cambiar_frame(LoginFrame))
        self.logout_button.pack(pady=20)

class MoverProductosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Título
        self.title = tk.Label(self, text="Mover Productos", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333")
        self.title.pack(pady=20)

        # Campos de entrada
        self.origen_label = tk.Label(self, text="Bodega Origen:", font=("Arial", 14))
        self.origen_label.pack(pady=5)
        self.origen_entry = tk.Entry(self, font=("Arial", 14))
        self.origen_entry.pack(pady=5)

        self.destino_label = tk.Label(self, text="Bodega Destino:", font=("Arial", 14))
        self.destino_label.pack(pady=5)
        self.destino_entry = tk.Entry(self, font=("Arial", 14))
        self.destino_entry.pack(pady=5)

        self.productos_label = tk.Label(self, text="Productos y Cantidades (ID:Cantidad):", font=("Arial", 14))
        self.productos_label.pack(pady=5)
        self.productos_entry = tk.Entry(self, font=("Arial", 14))
        self.productos_entry.pack(pady=5)

        # Botones
        self.boton_confirmar = tk.Button(self, text="Confirmar Movimiento", font=("Arial", 14), bg="#007BFF", fg="white",
                                         command=self.confirmar_movimiento)
        self.boton_confirmar.pack(pady=20)

        self.boton_volver = tk.Button(self, text="Volver", font=("Arial", 14), bg="#DC3545", fg="white",
                                      command=lambda: master.cambiar_frame(UserFrame))
        self.boton_volver.pack(pady=10)

    def confirmar_movimiento(self):
        bodega_origen = self.origen_entry.get()
        bodega_destino = self.destino_entry.get()
        productos_texto = self.productos_entry.get()

        if not bodega_origen or not bodega_destino or not productos_texto:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Procesar productos y cantidades
            productos = {}
            for item in productos_texto.split(","):
                producto_id, cantidad = map(str.strip, item.split(":"))
                productos[int(producto_id)] = int(cantidad)

            # Registrar el movimiento
            usuario_id = 1  # Asume que el usuario logueado tiene ID 1; adapta según tu lógica
            self.master.dao.registrar_movimiento(bodega_origen, bodega_destino, usuario_id, productos)
            messagebox.showinfo("Éxito", "Movimiento registrado correctamente.")
            self.master.cambiar_frame(UserFrame)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el movimiento: {e}")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
