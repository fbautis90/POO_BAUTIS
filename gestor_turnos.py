
import csv
import os
import datetime

class Cliente:
    #Clase para representar un cliente
    
    def __init__(self, id_cliente, nombre, apellido, email):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} (ID: {self.id_cliente})"


class Turno:
    #Clase para representar un turno
    
    def __init__(self, id_turno, cliente, servicio, fecha_hora, estado="Pendiente"):
        self.id_turno = id_turno
        self.cliente = cliente
        self.servicio = servicio
        self.fecha_hora = fecha_hora
        self.estado = estado
    
    def __str__(self):
        fecha_str = self.fecha_hora.strftime('%Y-%m-%d %H:%M')
        return f"Turno {self.id_turno}: {self.cliente} - {self.servicio} ({fecha_str}) [{self.estado}]"


class GestorTurnos:
    #Clase principal para gestionar turnos y clientes
    
    def __init__(self):
        self.archivo_csv = "turnos.csv"
        self.clientes = []
        self.turnos = []
        self.proximo_id_cliente = 1
        self.proximo_id_turno = 1
        
        # Campos para el CSV
        self.campos_csv = [
            "id_turno", "id_cliente", "nombre_cliente", "apellido_cliente", 
            "email_cliente", "servicio", "fecha", "hora", "estado"
        ]
        
        # Cargar datos si existen
        self.cargar_datos()
    
    def crear_archivo_si_no_existe(self):
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=self.campos_csv)
                escritor.writeheader()
    
    def encontrar_cliente_por_email(self, email):
        indice = 0
        while indice < len(self.clientes):
            if self.clientes[indice].email == email:
                return self.clientes[indice]
            indice = indice + 1
        return None

    def cargar_datos(self):
        self.crear_archivo_si_no_existe()
        
        # Intentar cargar datos
        with open(self.archivo_csv, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            datos = list(lector)
            
            if len(datos) == 0:
                print("Sistema iniciado - No hay datos previos")
                return
            
            # Cargar clientes y turnos
            clientes_dict = {}
            
            indice = 0
            while indice < len(datos):
                row = datos[indice]
                
                # Crear cliente si no existe
                id_cliente = int(row['id_cliente'])
                if id_cliente not in clientes_dict:
                    cliente = Cliente(
                        id_cliente=id_cliente,
                        nombre=row['nombre_cliente'],
                        apellido=row['apellido_cliente'],
                        email=row['email_cliente']
                    )
                    clientes_dict[id_cliente] = cliente
                    self.clientes.append(cliente)
                
                # Crear turno
                cliente = clientes_dict[id_cliente]
                fecha_str = f"{row['fecha']} {row['hora']}"
                fecha_hora = datetime.datetime.strptime(fecha_str, '%Y-%m-%d %H:%M')
                
                turno = Turno(
                    id_turno=int(row['id_turno']),
                    cliente=cliente,
                    servicio=row['servicio'],
                    fecha_hora=fecha_hora,
                    estado=row['estado']
                )
                self.turnos.append(turno)
                
                indice = indice + 1
            
            # Actualizar contadores
            if len(self.clientes) > 0:
                max_id = 0
                i = 0
                while i < len(self.clientes):
                    if self.clientes[i].id_cliente > max_id:
                        max_id = self.clientes[i].id_cliente
                    i = i + 1
                self.proximo_id_cliente = max_id + 1
            
            if len(self.turnos) > 0:
                max_id = 0
                i = 0
                while i < len(self.turnos):
                    if self.turnos[i].id_turno > max_id:
                        max_id = self.turnos[i].id_turno
                    i = i + 1
                self.proximo_id_turno = max_id + 1
            
            print("Datos cargados exitosamente")
    
    def guardar_datos(self):
        with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=self.campos_csv)
            escritor.writeheader()
            
            indice = 0
            while indice < len(self.turnos):
                turno = self.turnos[indice]
                turno_dict = {
                    'id_turno': turno.id_turno,
                    'id_cliente': turno.cliente.id_cliente,
                    'nombre_cliente': turno.cliente.nombre,
                    'apellido_cliente': turno.cliente.apellido,
                    'email_cliente': turno.cliente.email,
                    'servicio': turno.servicio,
                    'fecha': turno.fecha_hora.strftime('%Y-%m-%d'),
                    'hora': turno.fecha_hora.strftime('%H:%M'),
                    'estado': turno.estado
                }
                escritor.writerow(turno_dict)
                indice = indice + 1

    def alta_cliente(self):
        print("\n" + "="*40)
        print("ALTA NUEVO CLIENTE")
        print("="*40)
        
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        email = input("Email: ").strip()
        
        # Verificar si ya existe
        cliente_existente = self.encontrar_cliente_por_email(email)
        if cliente_existente:
            print(f"Cliente ya existe: {cliente_existente}")
            return cliente_existente
        
        # Crear nuevo cliente
        cliente = Cliente(
            id_cliente=self.proximo_id_cliente,
            nombre=nombre,
            apellido=apellido,
            email=email
        )
        
        self.clientes.append(cliente)
        self.proximo_id_cliente = self.proximo_id_cliente + 1
        
        self.guardar_datos()
        print(f"Cliente creado: {cliente}")
        return cliente
    
    def solicitar_turno(self):
        print("\n" + "="*40)
        print("SOLICITAR TURNO")
        print("="*40)
        
        # Seleccionar cliente
        if len(self.clientes) == 0:
            print("No hay clientes. Creando nuevo cliente...")
            cliente = self.alta_cliente()
        else:
            print("1. Cliente existente")
            print("2. Nuevo cliente")
            
            opcion = input("Seleccione (1-2): ").strip()
            
            if opcion == "1":
                cliente = self.seleccionar_cliente()
            else:
                cliente = self.alta_cliente()
        
        if not cliente:
            print("No se pudo seleccionar cliente")
            return
        
        print(f"\nTurno para: {cliente}")
        
        # Pedir fecha
        fecha_str = input("Fecha (YYYY-MM-DD): ").strip()
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Pedir hora
        hora_str = input("Hora (HH:MM): ").strip()
        hora = datetime.datetime.strptime(hora_str, '%H:%M').time()
        
        # Combinar fecha y hora
        fecha_hora = datetime.datetime.combine(fecha, hora)
        
        # Pedir servicio
        servicio = input("Servicio: ").strip()
        
        # Crear turno
        turno = Turno(
            id_turno=self.proximo_id_turno,
            cliente=cliente,
            servicio=servicio,
            fecha_hora=fecha_hora,
            estado="Pendiente"
        )
        
        self.turnos.append(turno)
        self.proximo_id_turno = self.proximo_id_turno + 1
        
        self.guardar_datos()
        print(f"Turno creado: {turno}")
    
    def seleccionar_cliente(self):
        if len(self.clientes) == 0:
            return None
        
        print("\nClientes:")
        indice = 0
        while indice < len(self.clientes):
            numero = indice + 1
            cliente = self.clientes[indice]
            print(f"{numero}. {cliente}")
            indice = indice + 1
        
        seleccion = input(f"Seleccione (1-{len(self.clientes)}): ").strip()
        numero = int(seleccion)
        indice = numero - 1
        
        if 0 <= indice < len(self.clientes):
            return self.clientes[indice]
        return None

    def listar_turnos(self):
        print("\n" + "="*50)
        print("LISTA DE TURNOS")
        print("="*50)
        
        if len(self.turnos) == 0:
            print("No hay turnos")
            return
        
        indice = 0
        while indice < len(self.turnos):
            turno = self.turnos[indice]
            print(f"{turno}")
            indice = indice + 1
        
        print(f"\nTotal: {len(self.turnos)} turnos")
    
    def encontrar_turno_por_id(self, id_turno):
        indice = 0
        while indice < len(self.turnos):
            if self.turnos[indice].id_turno == id_turno:
                return self.turnos[indice]
            indice = indice + 1
        return None
    
    def modificar_turno(self):
        print("\n" + "="*40)
        print("MODIFICAR TURNO")
        print("="*40)
        
        if len(self.turnos) == 0:
            print("No hay turnos")
            return
        
        turno_id = int(input("ID del turno: ").strip())
        turno = self.encontrar_turno_por_id(turno_id)
        
        if not turno:
            print("Turno no encontrado")
            return
        
        print(f"Turno actual: {turno}")
        
        print("\n1. Cambiar servicio")
        print("2. Cambiar estado")
        
        opcion = input("Seleccione (1-2): ").strip()
        
        if opcion == "1":
            nuevo_servicio = input("Nuevo servicio: ").strip()
            turno.servicio = nuevo_servicio
            self.guardar_datos()
            print("Servicio actualizado")
            
        elif opcion == "2":
            print("Estados: Pendiente, Confirmado, Completado, Cancelado")
            nuevo_estado = input("Nuevo estado: ").strip()
            turno.estado = nuevo_estado
            self.guardar_datos()
            print("Estado actualizado")
    
    def cancelar_turno(self):
        print("\n" + "="*40)
        print("CANCELAR TURNO")
        print("="*40)
        
        if len(self.turnos) == 0:
            print("No hay turnos")
            return
        
        turno_id = int(input("ID del turno: ").strip())
        turno = self.encontrar_turno_por_id(turno_id)
        
        if not turno:
            print("Turno no encontrado")
            return
        
        print(f"Turno: {turno}")
        
        confirmacion = input("¿Cancelar? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            # Eliminar turno
            nueva_lista = []
            indice = 0
            while indice < len(self.turnos):
                if self.turnos[indice].id_turno != turno_id:
                    nueva_lista.append(self.turnos[indice])
                indice = indice + 1
            
            self.turnos = nueva_lista
            self.guardar_datos()
            print("Turno cancelado")
        else:
            print("No se canceló")

    def buscar_turnos(self):
        print("\n" + "="*40)
        print("BUSCAR TURNOS")
        print("="*40)
        
        if len(self.turnos) == 0:
            print("No hay turnos")
            return
        
        print("1. Por cliente")
        print("2. Por fecha")
        
        opcion = input("Seleccione (1-2): ").strip()
        
        if opcion == "1":
            cliente = self.seleccionar_cliente()
            if not cliente:
                return
            
            print(f"\nTurnos de {cliente}:")
            encontrados = 0
            indice = 0
            while indice < len(self.turnos):
                if self.turnos[indice].cliente.id_cliente == cliente.id_cliente:
                    print(self.turnos[indice])
                    encontrados = encontrados + 1
                indice = indice + 1
            
            if encontrados == 0:
                print("No hay turnos para este cliente")
        
        elif opcion == "2":
            fecha_str = input("Fecha (YYYY-MM-DD): ").strip()
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            print(f"\nTurnos del {fecha}:")
            encontrados = 0
            indice = 0
            while indice < len(self.turnos):
                if self.turnos[indice].fecha_hora.date() == fecha:
                    print(self.turnos[indice])
                    encontrados = encontrados + 1
                indice = indice + 1
            
            if encontrados == 0:
                print("No hay turnos para esta fecha")
    
    def menu_principal(self):
        while True:
            print("\n" + "="*40)
            print("GESTOR DE TURNOS")
            print("="*40)
            print("1. Alta cliente")
            print("2. Solicitar turno")
            print("3. Lista turnos")
            print("4. Modificar turno")
            print("5. Cancelar turno")
            print("6. Buscar turnos")
            print("7. Guardar")
            print("0. Salir")
            
            seleccion = input("\nOpción: ").strip()
            
            if seleccion == "1":
                self.alta_cliente()
            elif seleccion == "2":
                self.solicitar_turno()
            elif seleccion == "3":
                self.listar_turnos()
            elif seleccion == "4":
                self.modificar_turno()
            elif seleccion == "5":
                self.cancelar_turno()
            elif seleccion == "6":
                self.buscar_turnos()
            elif seleccion == "7":
                self.guardar_datos()
                print("Datos guardados")
            elif seleccion == "0":
                self.guardar_datos()
                print("Sistema cerrado")
                break
            else:
                print("Opción inválida")
            
            input("\nPresione Enter para continuar...")


def main():
    print("Gestión de Turnos")
    print("-" * 30)
    
    gestor = GestorTurnos()
    gestor.menu_principal()


if __name__ == "__main__":
    main()
