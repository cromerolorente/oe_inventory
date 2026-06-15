# OE Inventory — Manual de Usuario

**Versión:** 1.0 (aplicación web)
**Dirigido a:** equipo de IT y personas usuarias de OE Inventory
**Qué es:** la herramienta de Octopus Energy para gestionar el inventario de activos IT — equipos, licencias, teléfonos, líneas, accesos y el personal al que se asignan.

---

## Cómo usar este manual

Lo hemos escrito para que sea fácil: lenguaje sencillo, sin tecnicismos innecesarios y con una imagen de cada pantalla para que sepas siempre dónde estás. Cada sección sigue el mismo orden:

- **Para qué sirve** — la idea en una frase.
- **Cómo está organizada** — las zonas de la pantalla.
- **Campos** — qué información se rellena.
- **Qué puedes hacer** — los botones y acciones.
- **La tabla** — qué columnas verás en el listado.
- **Detalles útiles** — trucos y comportamientos que conviene conocer.

> **Sobre las imágenes:** los huecos marcados como `![...]` se rellenan con capturas reales de tu instalación. Al final del manual tienes una **[Guía de capturas](#anexo-a-guía-de-capturas)** con la lista de imágenes a hacer y cómo nombrarlas, para que el documento quede completo.

---

## Índice

1. [Primeros pasos](#1-primeros-pasos)
   - [Iniciar sesión](#11-iniciar-sesión)
   - [He olvidado mi contraseña](#12-he-olvidado-mi-contraseña)
   - [La pantalla de inicio](#13-la-pantalla-de-inicio-menú-principal)
   - [La barra de estado](#14-la-barra-de-estado-parte-inferior)
2. [Conceptos que se repiten en toda la app](#2-conceptos-que-se-repiten-en-toda-la-app)
3. [Personal y asignaciones](#3-personal-y-asignaciones)
   - [Staff (Personal)](#31-staff-personal)
   - [Allocations (Asignaciones)](#32-allocations-asignaciones)
   - [Incorporations (Incorporaciones)](#33-incorporations-incorporaciones)
4. [Activos](#4-activos)
   - [Devices (Dispositivos)](#41-devices-dispositivos)
   - [Licenses (Licencias)](#42-licenses-licencias)
   - [Phones (Teléfonos)](#43-phones-teléfonos)
   - [Mobile Lines (Líneas móviles)](#44-mobile-lines-líneas-móviles)
   - [Fiber Lines (Líneas de fibra)](#45-fiber-lines-líneas-de-fibra)
   - [Printers (Impresoras)](#46-printers-impresoras)
5. [Accesos físicos](#5-accesos-físicos)
   - [Access Cards (Tarjetas de acceso)](#51-access-cards-tarjetas-de-acceso)
   - [Visitors Access Cards (Tarjetas de visitantes)](#52-visitors-access-cards-tarjetas-de-visitantes)
   - [Access Keys (Llaves de acceso)](#53-access-keys-llaves-de-acceso)
6. [Compras y seguimiento](#6-compras-y-seguimiento)
   - [Orders (Pedidos)](#61-orders-pedidos)
   - [Availability (Disponibilidad)](#62-availability-disponibilidad)
   - [Under Repair (En reparación)](#63-under-repair-en-reparación)
   - [Distribution Invoices (Facturas de distribución)](#64-distribution-invoices-facturas-de-distribución)
7. [Organización y usuarios](#7-organización-y-usuarios)
   - [Delegations (Delegaciones)](#71-delegations-delegaciones)
   - [Users (Usuarios de la app)](#72-users-usuarios-de-la-app)
   - [Cambiar mi contraseña](#73-cambiar-mi-contraseña)
- [Anexo A: Guía de capturas](#anexo-a-guía-de-capturas)
- [Anexo B: Glosario](#anexo-b-glosario)

---

## 1. Primeros pasos

### 1.1 Iniciar sesión

**Para qué sirve:** entrar en la aplicación con tu usuario.

![Pantalla de inicio de sesión](images/01-login.png)
*Pantalla de login de OE Inventory.*

**Campos:**
- **User** — tu nombre de usuario.
- **Password** — tu contraseña.

**Qué puedes hacer:**
- **Aceptar (✔)** — valida tus credenciales. Si son correctas, entras en la pantalla de inicio. Si no, verás el aviso *"User or password incorrect."*
- **Forgot my password?** — te lleva al proceso de recuperación (ver siguiente apartado).

> **Truco:** si ya tenías la sesión iniciada, la app te lleva directamente a la pantalla de inicio sin pedirte de nuevo las credenciales.

---

### 1.2 He olvidado mi contraseña

**Para qué sirve:** recuperar el acceso sin ayuda de nadie cuando no recuerdas tu contraseña.

![Recuperación de contraseña](images/02-recuperar-contrasena.png)
*Formulario para solicitar el correo de recuperación.*

**Cómo funciona:**
1. En la pantalla de login, pulsa **Forgot my password?**
2. Introduce el correo asociado a tu usuario.
3. Recibirás un email con un enlace seguro para crear una contraseña nueva.
4. Abres el enlace, escribes la nueva contraseña dos veces y listo.

> **Ten en cuenta:** para que llegue el correo, tu usuario debe tener un **email registrado** (se configura en la pantalla [Users](#72-users-usuarios-de-la-app)). El envío se realiza a través de Resend.

---

### 1.3 La pantalla de inicio (menú principal)

**Para qué sirve:** es tu punto de partida. Desde aquí accedes a todas las secciones para las que tengas permiso.

![Pantalla de inicio](images/03-inicio-mdi.png)
*Menú principal con el logo de Octopus y la barra de navegación superior.*

**Cómo está organizada:**
- **Barra de navegación (arriba):** botones hacia cada módulo. **Solo verás las opciones para las que tienes permiso.** Las secciones de accesos físicos se agrupan en el desplegable **Office Access** (tarjetas de staff, tarjetas de visitantes y llaves).
- **Área central:** el logo de Octopus y un mensaje de bienvenida: *"Select an option from the menu above to start working."*
- **Barra de estado (abajo):** ver el apartado siguiente.

**Qué puedes hacer:**
- Pulsar cualquier botón del menú para abrir esa sección.
- **Password Change** — cambiar tu contraseña (siempre disponible).
- **Exit** — cerrar sesión (te pedirá confirmación: *"Do you want to close the current session?"*).

---

### 1.4 La barra de estado (parte inferior)

**Para qué sirve:** darte información de un vistazo, sin tener que buscarla.

![Barra de estado](images/04-barra-estado.png)
*Barra de estado inferior con usuario, conexión, usuarios online y contadores.*

De izquierda a derecha:

- **User** — el usuario con el que has entrado.
- **Session: active / inactive** — refleja si tu navegador **tiene conexión a Internet**. Verde con nube cuando hay conexión; rojo cuando se pierde. Se actualiza solo, en el momento, sin recargar la página.
- **Online: N** — número de personas usando la aplicación ahora mismo (actividad en los últimos 5 minutos). **Pulsa sobre él** y se abre una ventana con los **nombres** de quienes están conectados.
- **Pending cards** — tarjetas de acceso (de staff y de visitantes) que están en estado *PENDING*.
- **Pending orders** — pedidos que aún no se han tramitado ni cancelado.

> **Ten en cuenta:** los contadores *Pending cards* y *Pending orders* se calculan al cargar la página; si cambian, los verás actualizados la próxima vez que navegues.

---

## 2. Conceptos que se repiten en toda la app

Para no repetirlo en cada sección, estas ideas valen para casi todas las pantallas:

- **Buscar un registro:** casi todos los formularios tienen un campo principal (Serial Number, Card, ID…) con un botón **Find (🔍)**. Escribe el dato y pulsa el botón o **Enter**: la app rellena el resto del formulario. También puedes **hacer clic en una fila** de la tabla para cargarla.
- **Guardar:** el botón **Save (💾)** crea el registro si es nuevo o actualiza el existente.
- **Limpiar:** el botón **Clear** vacía el formulario para empezar de cero.
- **Historial / Notes:** muchas pantallas tienen un cuadro **Notes** de solo lectura. Cada vez que guardas o realizas una acción, la app añade automáticamente una línea con la **fecha, hora y tu usuario**. Es la trazabilidad de quién hizo qué y cuándo.
- **Exportar a Excel:** donde hay listados, encontrarás un botón para **descargar los datos en `.xlsx`**.
- **Perfil "reader" (solo lectura):** si tu usuario tiene este perfil, **puedes consultar todo pero no modificar nada** (ni guardar, ni exportar). Si lo intentas, verás: *"You have a reader profile and can't modify data."* Es nuestra forma de dar acceso a la información sin riesgo de cambios accidentales.
- **Ámbito (scope):** en pantallas como Staff, tu usuario puede estar limitado a ciertas **empresas, delegaciones o departamentos**. Solo verás el personal y los datos dentro de tu ámbito.
- **Avisos:** los mensajes de éxito, error o aviso aparecen como ventanas emergentes con el logo de Octopus.

---

## 3. Personal y asignaciones

### 3.1 Staff (Personal)

**Para qué sirve:** gestionar a las personas y todo el equipamiento IT que tienen asignado mientras forman parte de la empresa.

![Pantalla de Staff — pestaña General](images/10-staff-general.png)
*Ficha de personal con sus datos, totales y la tabla de items asignados.*

**Cómo está organizada (tres pestañas):**
- **General** — datos de la persona, totales y la tabla de items que tiene asignados.
- **Docs** — documentos PDF de la persona (subir, listar y previsualizar).
- **List** — listado de todo el personal, con contadores *People* (total) y *Actives* (en activo).

**Campos (General):**
- **ID** (búsqueda por nombre con **Find**), **Name** (obligatorio), **Department** (con autocompletado), **Company**, **Delegation**, **eMail**, **Incorporation date**, **Termination date** (se rellena solo al dar de baja), **Natural Person** (marcar si es persona física) y **Notes** (historial, solo lectura).

**Qué puedes hacer:**
- **Save** — guardar/crear la persona.
- **Clear** — limpiar el formulario.
- **Generate document** — generar un PDF con el inventario asignado a esa persona.
- **Send Email** — enviar ese informe por correo al departamento de personas (People).
- **Release (liberar)** — desasignar un item seleccionado en la tabla y devolverlo al stock. Para personas físicas, genera automáticamente un documento *Unassign*.
- **Terminate (dar de baja)** — abre una ventana para marcar qué items devuelve la persona; genera un PDF *Terminate* y marca el contrato como finalizado (fecha de baja + estado inactivo).
- **Export to Excel** — exportar los items asignados.

![Ventana de baja (Terminate)](images/11-staff-terminate-modal.png)
*Al dar de baja, marca los items devueltos; los seleccionados vuelven al stock.*

**La tabla (items asignados):** ID · Serial · Type · Brand · Model · Origin · Date · Obs · Value (€).

![Pantalla de Staff — pestaña Docs](images/12-staff-docs.png)
*Gestión de documentos PDF de la persona, con vista previa.*

**Detalles útiles:**
- Los totales (número de items y valor total) se calculan solos sumando dispositivos, licencias, teléfonos, tarjetas y llaves.
- Los documentos se guardan de forma segura y se pueden previsualizar sin descargarlos.

---

### 3.2 Allocations (Asignaciones)

**Para qué sirve:** asignar de forma ágil dispositivos, licencias y teléfonos que están en stock a una persona en activo.

![Pantalla de Asignaciones](images/13-allocations.png)
*Selección de persona y búsqueda de activos libres para asignar.*

**Cómo está organizada:** una columna con cuatro bloques apilados — **persona**, **dispositivos**, **licencias** y **teléfonos**.

**Cómo se usa:**
1. Elige la **persona** (lista de personal activo). *Truco:* puedes llegar aquí ya con la persona preseleccionada desde su ficha.
2. En **Devices**, filtra por **Type** y **Brand** y pulsa **Search**; elige el número de serie disponible.
3. En **Licenses**, filtra por **Type** y busca el número de serie.
4. En **Phones**, escribe o elige el número de serie (campo con autocompletado) y busca.
5. Pulsa **Assign** en cada bloque para asignar ese item a la persona.

**Qué puedes hacer:**
- **Assign** — asigna el item seleccionado a la persona.
- **Generate document** — genera un único PDF de asignación con todo lo entregado a esa persona (solo personas físicas).

**Detalles útiles:**
- Solo se ofrecen activos **sin asignar** (en stock).
- Si asignas items y sales sin pulsar *Generate document*, la app genera igualmente el documento de asignación de forma automática (uno por persona), para que nunca falte la trazabilidad.

---

### 3.3 Incorporations (Incorporaciones)

**Para qué sirve:** preparar la llegada de una persona nueva (onboarding): qué equipo necesita, gestionar el envío/recepción y, al final, convertirla en personal de la app.

![Pantalla de Incorporaciones](images/14-incorporations.png)
*Formulario de equipamiento solicitado y pestañas Pending / Discarded / Incorporated.*

**Cómo está organizada:** formulario a la izquierda y, a la derecha, tres pestañas con listados: **Pending** (pendientes), **Discarded** (descartadas) e **Incorporated** (ya incorporadas).

**Campos:** Name, Company, Department, Delegation, Date, Address (para remotos), tipo de portátil (None / WIN / MBA / MBP), tipo de auriculares (None / Corded / Cordless) y casillas de equipamiento (Phone, USB-C HUB, Screen, PDF, Mouse, ACAD, Keyboard, Discarded).

**Qué puedes hacer:**
- **Save** — guardar la solicitud.
- **Clear** — limpiar.
- **Send devices** — (solo delegación REMOTE) registrar el envío indicando la agencia de transporte.
- **Receive devices** — registrar la recepción del material.
- **Complete incorporation** — crear la ficha de **Staff** a partir de estos datos y marcar la incorporación como completada.

**La tabla:** Name · Company · Department · Delegation · Date y las casillas de equipamiento (WIN, MBA, MBP, Phone, Screen, Mouse, Keyboard, auriculares, USB-C, PDF, ACAD) más Send/Receive.

---

## 4. Activos

### 4.1 Devices (Dispositivos)

**Para qué sirve:** el inventario de equipos informáticos (portátiles, sobremesa, tablets…), con sus datos técnicos, a quién están asignados y su paso por el servicio técnico.

![Pantalla de Dispositivos](images/05-devices.png)
*Formulario, totales a la derecha e inventario en la tabla inferior.*

**Cómo está organizada:** formulario a la izquierda, panel de **totales** y notas a la derecha, y la **tabla** de inventario abajo.

**Campos:** Serial Number, Company, Type (autocompletado), Brand, Model, Screen Size, HD Size, Memory, *Have mobile SIM?*, IMEI, PIN/PUK, Origin, Insert Date, Bill Number, Obs, Value (€), *Assigned to* (solo lectura) y el historial.

**Qué puedes hacer:**
- **Search** — buscar por número de serie.
- **Save** — guardar/actualizar.
- **Support** — enviar o recibir el equipo del servicio técnico (funciona como interruptor).
- **Clear** — limpiar.
- **Export to Excel** — exportar el inventario.

**La tabla:** Serial Number · Type · Brand · Model · Screen · HD · Memory · IMEI · Mobile · PIN/PUK · Origin · Date · Bill Nº · Assigned To · Value (€).

**Detalles útiles:**
- Si el equipo está **en reparación**, verás un **aviso rojo** en la parte superior.
- Los **totales** (número de equipos y valor total) se actualizan automáticamente.
- La tabla carga los datos **por páginas** (búsqueda, orden y paginación se resuelven en el servidor), por lo que abre rápido aunque haya miles de equipos. Escribe en el buscador de la tabla para filtrar sobre **todo** el inventario.

---

### 4.2 Licenses (Licencias)

**Para qué sirve:** registrar y controlar licencias de software: compras, caducidades y a quién están asignadas.

![Pantalla de Licencias](images/06-licenses.png)
*Formulario, resumen por tipo en el centro y totales a la derecha.*

**Cómo está organizada:** formulario a la izquierda, **resumen de licencias por tipo** en el centro y **totales** + notas a la derecha. La tabla de licencias, abajo.

**Campos:** Serial Number, Company, Type (autocompletado), Origin (autocompletado), Insert Date, Value (€), Obs, Bill Number y *Assigned to* (solo lectura).

**Qué puedes hacer:** **Find**, **Save**, **Clear** y **Export to Excel**.

**La tabla:** Serial Number · Company · Type · Origin · Insert Date · Person · Obs · Value (€) · Bill Number.

**Detalles útiles:**
- El **resumen por tipo** muestra, para cada tipo: **compradas**, **caducadas** (asignadas a la persona "LICENCIAS CADUCADAS") y **en uso** (compradas − caducadas).
- Al hacer clic en una fila, el formulario se rellena con esa licencia.

---

### 4.3 Phones (Teléfonos)

**Para qué sirve:** gestionar los teléfonos móviles corporativos y su paso por el servicio técnico.

![Pantalla de Teléfonos](images/07-phones.png)
*Ficha del teléfono, totales e inventario.*

**Campos:** Serial Number, Company, Brand, Model, Origin (autocompletado), Insert Date, Value (€), IMEI, Obs, Bill Number, *Number* (línea asociada, solo lectura) y *Assigned to* (solo lectura).

**Qué puedes hacer:** **Find**, **Save**, **Clear**, **Support** (enviar/recibir de servicio técnico), **Release** (desasignar de la persona) y **Export to Excel**.

**La tabla:** Serial Number · Company · Brand · Model · Origin · Date · Person · Number · IMEI · Obs · Value (€) · Bill Number.

**Detalles útiles:** si el teléfono está en reparación, aparece un aviso rojo arriba. Al liberar un teléfono de una persona física, se genera automáticamente un documento *Unassign*.

---

### 4.4 Mobile Lines (Líneas móviles)

**Para qué sirve:** gestionar las líneas/tarjetas SIM, incluidas eSIM y M2M, y a qué teléfono, persona o dispositivo están asociadas.

![Pantalla de Líneas móviles](images/08-mobile-lines.png)
*Datos de la línea, panel de asignación según el tipo y resumen de tarjetas.*

**Cómo está organizada:** formulario de la línea a la izquierda; a la derecha, el **panel de asignación** (cambia según sea SIM normal, **eSIM** o **M2M**), un **resumen de tarjetas** (en uso / libres / de baja / total) y las notas. La tabla, abajo.

**Campos:** Number, Company, Insert Date, Origin (autocompletado), PIN, PIN2, PUK, PUK2, CARD (IMEI), Extension, Obs, casillas **eSIM** y **M2M**, *Person* y *Device SN* (solo lectura).

**Qué puedes hacer:**
- **Save**, **Clear**, **Release** (desasignar) y **Cancel line** (dar de baja con el proveedor).
- Asignar según el tipo: una **SIM** a un teléfono en stock, una **eSIM** a una persona o una línea **M2M** a un dispositivo.

**La tabla:** Number · Company · Origin · PIN · PUK · PIN2 · PUK2 · IMEI · Date · Mobile · Person · Ext · eSIM · M2M · Baja · Obs.

**Detalles útiles:** al marcar **eSIM** o **M2M**, el panel de asignación cambia para ofrecerte la opción correcta. Si la línea está de baja, verás un aviso.

---

### 4.5 Fiber Lines (Líneas de fibra)

**Para qué sirve:** gestionar las líneas de fibra/conectividad de las sedes, su configuración técnica y las incidencias asociadas.

![Pantalla de Líneas de fibra](images/09-fiber-lines.png)
*Pestaña General con la configuración de la línea y la gestión de incidencias.*

**Cómo está organizada (dos pestañas):** **General** (formulario + incidencias) y **List** (listado de todas las líneas).

**Campos (General):** ID, Description, Provider (autocompletado), Delegation, Order, Service Code, Access, Router, Addressing, WIFI 1, WIFI 2, Start Date, Down Date, Fixed IP, casilla **Active** y el registro de auditoría.

**Qué puedes hacer:**
- **Save**, **Clear** y **Add incidence** (abre el panel para registrar una incidencia: Working Order, fechas y descripciones de apertura/cierre).
- **Save Incidence** / **Close** dentro del panel de incidencias.
- Exportar a Excel tanto las **líneas** como las **incidencias** de una línea.

**La tabla (List):** ID · Description · Provider · Delegation · Order · Service Code · Access · Router · Addressing · WIFI1 · WIFI2 · Active · Start Date · Down Date · Fixed IP.

---

### 4.6 Printers (Impresoras)

**Para qué sirve:** registrar las impresoras: datos técnicos, ubicación, contrato y credenciales de acceso.

![Pantalla de Impresoras](images/21-printers.png)
*Pestaña General con los datos de la impresora.*

**Cómo está organizada (dos pestañas):** **General** (formulario + notas) y **List** (listado).

**Campos:** Serial Number, Description, Provider (autocompletado), Delegation, MPS, Fixed IP, Start Date, End Date, Monthly fee (€), User, Password y notas.

**Qué puedes hacer:** **Save**, **Clear** y **Export to Excel** (en la pestaña List).

**La tabla (List):** Serial Number · Description · Provider · Delegation · MPS · Start Date · Down Date · Fee (€) · Fixed IP.

---

## 5. Accesos físicos

### 5.1 Access Cards (Tarjetas de acceso)

**Para qué sirve:** gestionar las tarjetas de acceso a edificios/zonas y a qué empleado pertenecen.

![Pantalla de Tarjetas de acceso](images/17-access-cards.png)
*Ficha de la tarjeta y listado inferior.*

**Campos:** Card, Fermax MIF, **PIN** (solo lectura), Staff (empleados activos), State (estado de la tarjeta) y Obs.

**Qué puedes hacer:**
- **Save** — guardar/actualizar.
- **Clear** — limpiar.
- **Generate PIN** — asigna un **PIN aleatorio** del conjunto disponible. Al guardar la tarjeta, ese PIN **se consume** (deja de estar disponible para otras).
- **Convert to Visitor Card** — convertir la tarjeta actual en tarjeta de visitante.

**La tabla:** ID · Card · Fermax MIF · PIN · Staff · State · Obs.

**Detalles útiles:** las tarjetas en estado **LOST** se muestran con la fila en **rosa** y no se pueden modificar.

---

### 5.2 Visitors Access Cards (Tarjetas de visitantes)

**Para qué sirve:** gestionar tarjetas de acceso temporal para visitantes (sin PIN ni empleado fijo).

![Pantalla de Tarjetas de visitantes](images/18-visitor-cards.png)
*Ficha del visitante, listado e historial de la tarjeta.*

**Campos:** Card Code, Fermax MIF, User (nombre del visitante), State y Observations.

**Qué puedes hacer:** **Save** y **Clear**, además de exportar.

**Las tablas:** un listado de tarjetas (ID · Card · Fermax MIF · User · State · Obs) y, debajo, el **historial** de la tarjeta seleccionada.

**Detalles útiles:** igual que en las de acceso, las tarjetas **LOST** aparecen en rosa.

---

### 5.3 Access Keys (Llaves de acceso)

**Para qué sirve:** registrar las llaves físicas de oficinas/despachos y quién es responsable de cada una.

![Pantalla de Llaves de acceso](images/19-access-keys.png)
*Ficha de la llave y listado.*

**Campos:** Key ID, Company, Type (autocompletado), Staff (responsable), Insert Date y notas.

**Qué puedes hacer:** **Save** y **Clear**.

**La tabla:** ID · Company · Type · Staff · Insert Date.

---

## 6. Compras y seguimiento

### 6.1 Orders (Pedidos)

**Para qué sirve:** seguir el ciclo de vida de los pedidos de material: crear, procesar, recibir o cancelar.

![Pantalla de Pedidos](images/22-orders.png)
*Formulario de pedido y pestañas Pending / Canceled / Received.*

**Campos:** ID (búsqueda), Article, Uds (unidades), Date y el historial (Notes).

**Qué puedes hacer:**
- **Save** — guardar/actualizar (Article, Uds y Date son obligatorios).
- **Clear** — limpiar.
- **Cancel** — cancelar el pedido (si no está ya tramitado).
- **Process** — marcar como tramitado.
- **Receive** — marcar como recibido (debe estar tramitado antes).

**Las pestañas:** **Pending** (pendientes), **Canceled** (cancelados) y **Received** (recibidos). Cada una con su botón de exportar.

**La tabla:** ID · Article · Date · Uds (y *Processed* en la pestaña de pendientes).

---

### 6.2 Availability (Disponibilidad)

**Para qué sirve:** ver de un vistazo cuánto stock hay, cuánto se necesita y cuánto viene en camino, por tipo de artículo.

![Pantalla de Disponibilidad](images/23-availability.png)
*Tabla de disponibilidad por artículo.*

**La tabla:**
- **Article** — tipo de artículo (p. ej. LAPTOP WIN, PHONE, KEYBOARD).
- **Stock** — unidades disponibles (sin asignar).
- **Needs** — necesidades pendientes (incorporaciones aún no completadas).
- **Orders** — unidades en pedidos pendientes.
- **Disp** — disponibilidad neta (**Stock − Needs + Orders**). En **verde** si es positiva, en **rojo** si es negativa.

**Qué puedes hacer:** **Export to Excel**.

---

### 6.3 Under Repair (En reparación)

**Para qué sirve:** seguir los equipos y teléfonos que están en el taller: cuándo salieron, cuándo volvieron y qué costó.

![Pantalla En reparación](images/24-under-repair.png)
*Pestañas Pending y Repaired, con el valor total reparado.*

**Cómo está organizada (dos pestañas):** **Pending** (en taller) y **Repaired** (ya recuperados).

**Qué puedes hacer:**
- En **Pending**, seleccionar un equipo y pulsar **Support / Receive** para registrar su vuelta indicando el **valor** de la reparación.
- Exportar a Excel en ambas pestañas.

**Las tablas:**
- **Pending:** ID · Serial Number · Model · Date Out · Destiny.
- **Repaired:** ID · Serial Number · Model · Date Out · Date In · Destiny · Value.

**Detalles útiles:** en la pestaña **Repaired** verás el **Total Value** (suma del coste de todas las reparaciones recuperadas).

---

### 6.4 Distribution Invoices (Facturas de distribución)

**Para qué sirve:** desglosar una factura para ver **dónde se asignó cada activo** (empresa, delegación, departamento, persona y valor).

![Pantalla de Facturas de distribución](images/25-distribution-invoices.png)
*Búsqueda por número de factura con opción de subtotales.*

**Cómo se usa:**
1. Escribe el **Bill Number** y pulsa **Search (🔍)**.
2. Marca **Show subtotals** para ver subtotales por departamento, delegación y empresa. *Al marcar/desmarcar, la búsqueda se relanza sola.*

**La tabla:** Company · Delegation · Department · User · Serial Number · Model · Value.

**Qué puedes hacer:** **Export to Excel** (aparece cuando hay resultados).

**Detalles útiles:** con los subtotales activados se intercalan filas resaltadas en **amarillo** con los totales en cascada (departamento → delegación → empresa).

---

## 7. Organización y usuarios

### 7.1 Delegations (Delegaciones)

**Para qué sirve:** gestionar las sedes/oficinas, con su dirección y un **mapa interactivo**.

![Pantalla de Delegaciones](images/20-delegations.png)
*Formulario y listado a la izquierda; mapa de España con los pines a la derecha.*

**Campos:** Code, Delegation (nombre, obligatorio), Address, Post Code, Town, Province y notas.

**Qué puedes hacer:** **Save** (al guardar, la app intenta **geolocalizar** la dirección), **Clear** y **Geolocate** (geolocalización manual de una delegación ya guardada).

**La tabla:** ID · Delegation · Address · Post Code · Town · Province.

**El mapa:**
- Centrado en España. Cada delegación geolocalizada aparece como un **pin**.
- **Azul** = delegación **activa**; **rojo** = **inactiva**.
- Al pulsar un pin se muestra el nombre, la dirección y el estado.

---

### 7.2 Users (Usuarios de la app)

**Para qué sirve:** crear y administrar las personas que usan OE Inventory, sus **permisos** y su **ámbito** de datos.

![Pantalla de Usuarios](images/15-users.png)
*Datos del usuario, permisos por módulo y ámbito por empresa/delegación/departamento.*

**Cómo está organizada:** datos del usuario (login, nombre, email, contraseña, permisos) y, debajo, el **ámbito** en tres bloques: **Companies**, **Delegations** y **Departments**.

**Campos:**
- **Login**, **Name**, **Email**.
- **Password** — normalmente aparece enmascarada. Solo se puede fijar una contraseña inicial cuando el usuario es nuevo y no tiene contraseña, y siempre que **tú tengas el permiso "users"**.
- **Application Permits** — casillas para habilitar cada módulo (activo, reader, users, staff, devices, licenses, phones, mobile_lines, fiber_lines, allocations, incorporations, orders, delegation, access_cards, visitors_cards, access_keys, under_repair, facturas, printers…).

**Qué puedes hacer:**
- **Save** — crear el usuario (si el login no existe) o actualizar el existente.
- **Clear** — limpiar el formulario.
- Marcar las **empresas, delegaciones y departamentos** que definen su ámbito (puede tener uno, varios o ninguno de cada).

**Detalles útiles:**
- Solo los usuarios con el permiso **"users"** pueden fijar contraseñas iniciales y editar permisos.
- El ámbito funciona de forma **acumulativa y opcional**: si no asignas ninguna empresa, el usuario las ve todas; lo mismo con delegaciones y departamentos.

---

### 7.3 Cambiar mi contraseña

**Para qué sirve:** que cualquier usuario cambie **su propia** contraseña estando dentro de la app.

![Cambiar contraseña](images/16-password-change.png)
*Formulario de cambio de contraseña.*

**Campos:** Old Password, New Password y Confirm Password.

**Reglas de la nueva contraseña:** al menos 8 caracteres, no puede ser solo números ni una contraseña demasiado común, y las dos veces deben coincidir.

**Detalles útiles:** tras el cambio no tienes que volver a iniciar sesión; la app mantiene tu sesión abierta.

---

## Anexo A: Guía de capturas

Para completar el manual, haz estas capturas y guárdalas en `docs/images/` con **exactamente** estos nombres. Recomendación: usa datos de ejemplo (no reales) y un ancho de ~1400 px.

| Nº | Archivo | Qué capturar |
|----|---------|--------------|
| 01 | `01-login.png` | Pantalla de login completa. |
| 02 | `02-recuperar-contrasena.png` | Formulario "Forgot my password". |
| 03 | `03-inicio-mdi.png` | Pantalla de inicio con el menú superior. |
| 04 | `04-barra-estado.png` | Detalle de la barra de estado inferior (recorte horizontal). |
| 05 | `05-devices.png` | Devices con datos en formulario y tabla. |
| 06 | `06-licenses.png` | Licenses con el resumen por tipo visible. |
| 07 | `07-phones.png` | Phones con una ficha cargada. |
| 08 | `08-mobile-lines.png` | Mobile Lines mostrando un panel de asignación. |
| 09 | `09-fiber-lines.png` | Fiber Lines, pestaña General con el panel de incidencias abierto. |
| 10 | `10-staff-general.png` | Staff, pestaña General con items asignados. |
| 11 | `11-staff-terminate-modal.png` | Ventana de baja (Terminate) con casillas de items. |
| 12 | `12-staff-docs.png` | Staff, pestaña Docs con un PDF en vista previa. |
| 13 | `13-allocations.png` | Allocations con persona seleccionada y un activo buscado. |
| 14 | `14-incorporations.png` | Incorporations con el formulario y las tres pestañas. |
| 15 | `15-users.png` | Users con permisos y ámbito visibles. |
| 16 | `16-password-change.png` | Formulario de cambio de contraseña. |
| 17 | `17-access-cards.png` | Access Cards (incluye, si puedes, una fila LOST en rosa). |
| 18 | `18-visitor-cards.png` | Visitors Access Cards con el historial inferior. |
| 19 | `19-access-keys.png` | Access Keys con el listado. |
| 20 | `20-delegations.png` | Delegations con el mapa y varios pines (azul y rojo). |
| 21 | `21-printers.png` | Printers, pestaña General. |
| 22 | `22-orders.png` | Orders con las pestañas Pending/Canceled/Received. |
| 23 | `23-availability.png` | Availability con la tabla y algún valor en rojo. |
| 24 | `24-under-repair.png` | Under Repair, pestaña Repaired con el Total Value. |
| 25 | `25-distribution-invoices.png` | Distribution Invoices con subtotales activados. |

> **Cómo hacer una captura en Mac:** `Cmd + Shift + 4` y arrastra para seleccionar la zona (la imagen se guarda en el Escritorio). En Windows, usa la **Herramienta Recortes** (`Win + Shift + S`).

---

## Anexo B: Glosario

- **Activo (asset):** cualquier elemento del inventario (dispositivo, licencia, teléfono, línea, tarjeta, llave, impresora).
- **Stock:** activos que no están asignados a ninguna persona.
- **Asignar / Liberar (Assign / Release):** entregar un activo a una persona / devolverlo al stock.
- **Baja (Terminate):** finalizar el contrato de una persona y recuperar su equipamiento.
- **Perfil reader:** usuario de solo lectura.
- **Ámbito (scope):** conjunto de empresas/delegaciones/departamentos que un usuario puede ver.
- **eSIM / M2M:** tipos especiales de línea móvil (SIM integrada / comunicación entre máquinas).
- **PENDING / LOST:** estados de las tarjetas de acceso (pendiente / perdida).

---

*OE Inventory — hecho para que gestionar el inventario sea simple, transparente y rápido. ¿Echas algo en falta en este manual? Cuéntanoslo y lo mejoramos.*
