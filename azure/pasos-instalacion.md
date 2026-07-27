# Laboratorio – Técnicas de Prueba
## Requisitos
Tener una suscripción Azure for Students activa.
### Paso 1

Entrar al Portal de Azure.

https://portal.azure.com

### Paso 2

Crear un Resource Group

Nombre sugerido
`TDP-LAB`

### Paso 3

Abrir el enlace

(Deploy to Azure)

### Paso 4

Completar únicamente

VM Name

`tdp-server`

Usuario

`tdp`

Contraseña

(la que deseen)

### Paso 5

Presionar

Review + Create

### Paso 6

Esperar aproximadamente

10 minutos.

Durante este tiempo Azure:

- crea la VM
- instala Python
- instala MySQL
- configura el entorno
ejecuta automáticamente vm-setup.sh

### Paso 7

Obtener la IP pública de la VM

Ir a

```
Virtual Machine
       ↓
   Networking
       ↓
   Public IP
```
Paso 8

Conectarse por SSH

Windows

`ssh tdp@IP_PUBLICA`

Mac

`ssh tdp@IP_PUBLICA`

Linux

`ssh tdp@IP_PUBLICA`
