#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import datetime


class Cliente:
    def __init__(self, id_cliente, nombre, apellido, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} (ID: {self.id_cliente})"


class Turno:
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
    def __init__(self):
        self.archivo_csv = "turnos.csv"
        
        # Campos para el CSV
        self.campos_csv = [
            "id_turno", "id_cliente", "nombre_cliente", "apellido_cliente", 
            "telefono_cliente", "servicio", "fecha", "hora", "estado"
        ]
        
        # Crear archivo si no existe
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.DictWriter(f, fieldnames=self.campos_csv)
                escritor.writeheader()
            print("Archivo creado")
    
    def leer_todos_los_turnos(self):
        # Lee todos los turnos del CSV y devuelve lista
        turnos = []
        clientes_dict = {}
        
        with open(self.archivo_csv, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            datos = list(lector)
            
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
                        telefono=row['telefono_cliente']
                    )
                    clientes_dict[id_cliente] = cliente
                else:
                    cliente = clientes_dict[id_cliente]
                
                # Crear turno
                fecha_str = f"{row['fecha']} {row['hora']}"
                fecha_hora = datetime.datetime.strptime(fecha_str, '%Y-%m-%d %H:%M')
                
                turno = Turno(
                    id_turno=int(row['id_turno']),
                    cliente=cliente,
                    servicio=row['servicio'],
                    fecha_hora=fecha_hora,
                    estado=row['estado']
                )
                turnos.append(turno)
                indice = indice + 1
        
        return turnos
    
    def guardar_todos_los_turnos(self, turnos):
        # Guarda todos los turnos al CSV (sobrescribe todo)
        with open(self.archivo_csv, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=self.campos_csv)
            escritor.writeheader()
            
            indice = 0
            while indice < len(turnos):
                turno = turnos[indice]
                turno_dict = {
                    'id_turno': turno.id_turno,
                    'id_cliente': turno.cliente.id_cliente,
                    'nombre_cliente': turno.cliente.nombre,
                    'apellido_cliente': turno.cliente.apellido,
                    'telefono_cliente': turno.cliente.telefono,
                    'servicio': turno.servicio,
                    'fecha': turno.fecha_hora.strftime('%Y-%m-%d'),
                    'hora': turno.fecha_hora.strftime('%H:%M'),
                    'estado': turno.estado
                }
                escritor.writerow(turno_dict)
                indice = indice + 1
    
    def obtener_proximo_id_turno(self):
        # Lee el CSV y calcula el próximo ID
        turnos = self.leer_todos_los_turnos()
        if len(turnos) == 0:
            return 1
        
        max_id = 0
        indice = 0
        while indice < len(turnos):
            if turnos[indice].id_turno > max_id:
                max_id = turnos[indice].id_turno
            indice = indice + 1
        
        return max_id + 1
    
    def obtener_proximo_id_cliente(self):
        # Lee el CSV y calcula el próximo ID de cliente
        turnos = self.leer_todos_los_turnos()
        if len(turnos) == 0:
            return 1
        
        max_id = 0
        indice = 0
        while indice < len(turnos):
            if turnos[indice].cliente.id_cliente > max_id:
                max_id = turnos[indice].cliente.id_cliente
            indice = indice + 1
        
        return max_id + 1
    
    def buscar_cliente_por_telefono(self, telefono):
        # Busca cliente en el CSV
        turnos = self.leer_todos_los_turnos()
        
        indice = 0
        while indice < len(turnos):
            if turnos[indice].cliente.telefono == telefono:
                return turnos[indice].cliente
            indice = indice + 1
        
        return None

    def alta_cliente(self):
        print("\n" + "="*30)
        print("ALTA CLIENTE")
        print("="*30)
        
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        telefono = input("Teléfono: ").strip()
        
        # Verificar si ya existe
        cliente_existente = self.buscar_cliente_por_telefono(telefono)
        if cliente_existente:
            print(f"Cliente ya existe: {cliente_existente}")
            return cliente_existente
        
        # Crear nuevo cliente
        nuevo_id = self.obtener_proximo_id_cliente()
        cliente = Cliente(
            id_cliente=nuevo_id,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono
        )
        
        print(f"Cliente creado: {cliente}")
        return cliente
    
    def solicitar_turno(self):
        print("\n" + "="*30)
        print("SOLICITAR TURNO")
        print("="*30)
        
        # Obtener cliente
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
        
        # Obtener datos del turno
        print(f"\nTurno para: {cliente}")
        
        fecha_str = input("Fecha (YYYY-MM-DD): ").strip()
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        hora_str = input("Hora (HH:MM): ").strip()
        hora = datetime.datetime.strptime(hora_str, '%H:%M').time()
        
        fecha_hora = datetime.datetime.combine(fecha, hora)
        servicio = input("Servicio: ").strip()
        
        # Crear turno
        nuevo_id = self.obtener_proximo_id_turno()
        turno = Turno(
            id_turno=nuevo_id,
            cliente=cliente,
            servicio=servicio,
            fecha_hora=fecha_hora,
            estado="Pendiente"
        )
        
        # Leer todos los turnos actuales + agregar el nuevo + guardar todo
        turnos = self.leer_todos_los_turnos()
        turnos.append(turno)
        self.guardar_todos_los_turnos(turnos)
        
        print(f"Turno creado: {turno}")
    
    def seleccionar_cliente(self):
        turnos = self.leer_todos_los_turnos()
        
        if len(turnos) == 0:
            print("No hay clientes")
            return None
        
        # Obtener clientes únicos
        clientes_unicos = []
        indice = 0
        while indice < len(turnos):
            cliente = turnos[indice].cliente
            
            # Verificar si ya está en la lista
            ya_existe = False
            j = 0
            while j < len(clientes_unicos):
                if clientes_unicos[j].id_cliente == cliente.id_cliente:
                    ya_existe = True
                    break
                j = j + 1
            
            if not ya_existe:
                clientes_unicos.append(cliente)
            
            indice = indice + 1
        
        print("\nClientes:")
        indice = 0
        while indice < len(clientes_unicos):
            numero = indice + 1
            print(f"{numero}. {clientes_unicos[indice]}")
            indice = indice + 1
        
        seleccion = input(f"Seleccione (1-{len(clientes_unicos)}): ").strip()
        numero = int(seleccion)
        indice = numero - 1
        
        if 0 <= indice < len(clientes_unicos):
            return clientes_unicos[indice]
        return None

    def listar_turnos(self):
        print("\n" + "="*40)
        print("LISTA DE TURNOS")
        print("="*40)
        
        turnos = self.leer_todos_los_turnos()
        
        if len(turnos) == 0:
            print("No hay turnos")
            return
        
        indice = 0
        while indice < len(turnos):
            print(turnos[indice])
            indice = indice + 1
        
        print(f"\nTotal: {len(turnos)} turnos")
    
    def modificar_turno(self):
        print("\n" + "="*30)
        print("MODIFICAR TURNO")
        print("="*30)
        
        turnos = self.leer_todos_los_turnos()
        
        if len(turnos) == 0:
            print("No hay turnos")
            return
        
        turno_id = int(input("ID del turno: ").strip())
        
        # Buscar turno
        turno_encontrado = None
        indice_turno = -1
        indice = 0
        while indice < len(turnos):
            if turnos[indice].id_turno == turno_id:
                turno_encontrado = turnos[indice]
                indice_turno = indice
                break
            indice = indice + 1
        
        if not turno_encontrado:
            print("Turno no encontrado")
            return
        
        print(f"Turno: {turno_encontrado}")
        
        print("\n1. Cambiar servicio")
        print("2. Cambiar estado")
        
        opcion = input("Seleccione (1-2): ").strip()
        
        if opcion == "1":
            nuevo_servicio = input("Nuevo servicio: ").strip()
            turnos[indice_turno].servicio = nuevo_servicio
            
        elif opcion == "2":
            print("Estados: Pendiente, Confirmado, Completado, Cancelado")
            nuevo_estado = input("Nuevo estado: ").strip()
            turnos[indice_turno].estado = nuevo_estado
        
        # Guardar todos los turnos actualizados
        self.guardar_todos_los_turnos(turnos)
        print("Turno actualizado")
    
    def cancelar_turno(self):
        print("\n" + "="*30)
        print("CANCELAR TURNO")
        print("="*30)
        
        turnos = self.leer_todos_los_turnos()
        
        if len(turnos) == 0:
            print("No hay turnos")
            return
        
        turno_id = int(input("ID del turno: ").strip())
        
        # Buscar turno
        turno_encontrado = None
        indice = 0
        while indice < len(turnos):
            if turnos[indice].id_turno == turno_id:
                turno_encontrado = turnos[indice]
                break
            indice = indice + 1
        
        if not turno_encontrado:
            print("Turno no encontrado")
            return
        
        print(f"Turno: {turno_encontrado}")
        confirmacion = input("¿Cancelar? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            # Crear nueva lista sin este turno
            turnos_nuevos = []
            indice = 0
            while indice < len(turnos):
                if turnos[indice].id_turno != turno_id:
                    turnos_nuevos.append(turnos[indice])
                indice = indice + 1
            
            # Guardar la nueva lista
            self.guardar_todos_los_turnos(turnos_nuevos)
            print("Turno cancelado")
        else:
            print("No se canceló")

    def buscar_turnos(self):
        print("\n" + "="*30)
        print("BUSCAR TURNOS")
        print("="*30)
        
        turnos = self.leer_todos_los_turnos()
        
        if len(turnos) == 0:
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
            while indice < len(turnos):
                if turnos[indice].cliente.id_cliente == cliente.id_cliente:
                    print(turnos[indice])
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
            while indice < len(turnos):
                if turnos[indice].fecha_hora.date() == fecha:
                    print(turnos[indice])
                    encontrados = encontrados + 1
                indice = indice + 1
            
            if encontrados == 0:
                print("No hay turnos para esta fecha")
    
    def menu_principal(self):
        while True:
            print("\n" + "="*30)
            print("SISTEMA DE TURNOS")
            print("="*30)
            print("1. Alta cliente")
            print("2. Solicitar turno")
            print("3. Lista turnos")
            print("4. Modificar turno")
            print("5. Cancelar turno")
            print("6. Buscar turnos")
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
            elif seleccion == "0":
                print("Sistema cerrado")
                break
            else:
                print("Opción inválida")
            
            input("\nPresione Enter...")


def main():
    print("Sistema de Turnos")
    print("-" * 20)
    
    gestor = GestorTurnos()
    gestor.menu_principal()


if __name__ == "__main__":
    main()
