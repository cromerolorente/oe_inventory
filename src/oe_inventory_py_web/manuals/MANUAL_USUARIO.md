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
8. [Monitorización (red, equipos remotos y salas)](#8-monitorización-red-equipos-remotos-y-salas)
   - [Net Overview (Zyxel Nebula)](#81-net-overview-zyxel-nebula)
   - [Remote Machines (AnyDesk)](#82-remote-machines-anydesk)
   - [Video Rooms (Logitech Sync)](#83-video-rooms-logitech-sync)
- [Anexo A: Glosario](#anexo-a-glosario)

---

## 1. Primeros pasos

<a id="login"></a>

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

<a id="password-recovery"></a>

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

<a id="home"></a>

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
- **Manual** — Acceso al manual online de la aplicacion para conocer las posibilidaes de la aplicacion o resolver alguna duda de funcionamiento.
- **Exit** — cerrar sesión (te pedirá confirmación: *"Do you want to close the current session?"*).

---

<a id="status-bar"></a>

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

<a id="staff"></a>

### 3.1 Staff (Personal)

**Para qué sirve:** gestionar a las personas y todo el equipamiento IT que tienen asignado mientras forman parte de la empresa.

![Pantalla de Staff — pestaña General](images/10-staff-general.png)
*Ficha de personal con sus datos, totales y la tabla de items asignados.*

**Cómo está organizada (tres pestañas):**
- **General** — datos de la persona, totales y la tabla de items que tiene asignados.
- **Docs** — documentos PDF de la persona (subir, listar y previsualizar).
- **List** — listado de todo el personal, con contadores *People* (total) y *Actives* (en activo).

**Campos (General), uno a uno:**
- **ID** — identificador interno; es de **solo lectura** y se rellena al buscar. No se teclea.
- **Name** — nombre de la persona. **Obligatorio**; es lo que se usa para buscar (con **Find**) y lo que aparece como "asignado a" en los activos.
- **Department** — departamento; campo con **autocompletado** sobre los valores ya existentes (puedes escribir uno nuevo). Forma parte del **ámbito** que ven los usuarios con permisos limitados.
- **Company** / **Delegation** — empresa y delegación a las que pertenece; también delimitan el ámbito.
- **eMail** — correo de la persona. Además de informativo, es la **clave de cruce** con otras pantallas (p. ej. el organizador de reuniones en *Video Rooms* se busca por este email).
- **Incorporation date** — fecha de alta.
- **Termination date** — fecha de baja; **no se edita a mano**, se rellena automáticamente al usar **Terminate**.
- **Natural Person** — marca si es una **persona física** (no un rol o recurso). **Limitación importante:** solo para personas físicas se generan los documentos de *Assign*/*Unassign*/*Terminate*.
- **Notes** — **historial automático** (altas, asignaciones, bajas…). Es de **solo lectura**: se rellena solo con cada acción, no se escribe a mano.

**Qué puedes hacer (y sus límites):**
- **Save** — guarda/crea la persona. Requiere al menos el **Name**.
- **Clear** — vacía el formulario (no borra nada de la base de datos).
- **Generate document** — genera un PDF con el inventario asignado. **Solo para personas físicas.**
- **Send Email** — envía ese informe al departamento de personas (People) vía **Resend**. **Limitación:** requiere que Resend esté configurado y que el dominio del remitente esté verificado; si no, el envío falla (queda registrado en el log).
- **Release (liberar)** — desasigna el item **seleccionado en la tabla** y lo devuelve al stock; en personas físicas genera un documento *Unassign*. Hay que seleccionar una fila primero.
- **Terminate (dar de baja)** — abre una ventana para marcar qué items **devuelve** la persona; genera un PDF *Terminate*, devuelve esos items al stock y marca el contrato como finalizado (rellena *Termination date* y pone el estado en inactivo). Acción **difícil de revertir**: úsala al cerrar el contrato.
- **Export to Excel** — exporta la tabla de items asignados de esa persona.

![Ventana de baja (Terminate)](images/11-staff-terminate-modal.png)
*Al dar de baja, marca los items devueltos; los seleccionados vuelven al stock.*

**La tabla (items asignados):** ID · Serial · Type · Brand · Model · Origin · Date · Obs · Value (€).

![Pantalla de Staff — pestaña Docs](images/12-staff-docs.png)
*Gestión de documentos PDF de la persona, con vista previa.*

**Detalles útiles:**
- Los totales (número de items y valor total) se calculan solos sumando dispositivos, licencias, teléfonos, tarjetas y llaves.
- Los documentos se guardan de forma segura y se pueden previsualizar sin descargarlos.

---

<a id="allocations"></a>

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

**Campos y filtros, uno a uno:**
- **Person** — desplegable de **personal en activo** (las personas dadas de baja no aparecen). Es obligatorio elegir persona antes de asignar.
- **Devices → Type / Brand** — filtros para acotar la búsqueda de dispositivos libres; tras **Search** se rellena el desplegable de **números de serie disponibles**.
- **Licenses → Type** — filtro análogo para licencias libres.
- **Phones → número de serie** — campo con **autocompletado** sobre los teléfonos en stock.

**Qué puedes hacer (y sus límites):**
- **Search** (en cada bloque) — busca activos **disponibles** que cumplan el filtro.
- **Assign** — asigna a la persona el item seleccionado en ese bloque. Hay que haber elegido persona **y** un número de serie.
- **Generate document** — genera un único PDF de asignación con todo lo entregado a esa persona. **Solo personas físicas.**

**Detalles y limitaciones:**
- Solo se ofrecen activos **sin asignar** (en stock); un item ya asignado no aparece hasta que se libere.
- Puedes llegar aquí con la **persona preseleccionada** desde su ficha de Staff.
- Si asignas items y sales **sin** pulsar *Generate document*, la app genera igualmente el documento de asignación automáticamente (uno por persona), para no perder la trazabilidad.

---

<a id="incorporations"></a>

### 3.3 Incorporations (Incorporaciones)

**Para qué sirve:** preparar la llegada de una persona nueva (onboarding): qué equipo necesita, gestionar el envío/recepción y, al final, convertirla en personal de la app.

![Pantalla de Incorporaciones](images/14-incorporations.png)
*Formulario de equipamiento solicitado y pestañas Pending / Discarded / Incorporated.*

**Cómo está organizada:** formulario a la izquierda y, a la derecha, tres pestañas con listados: **Pending** (pendientes), **Discarded** (descartadas) e **Incorporated** (ya incorporadas).

**Campos, uno a uno:**
- **Name** — nombre de la persona que se incorpora.
- **Company / Department / Delegation** — destino de la incorporación; **Delegation** es relevante porque el valor **REMOTE** habilita el flujo de envío por mensajería.
- **Date** — fecha prevista de incorporación.
- **Address** — dirección de envío; **solo aplica a remotos** (cuando hay que mandarle el equipo a casa).
- **Tipo de portátil** — None / **WIN** (Windows) / **MBA** (MacBook Air) / **MBP** (MacBook Pro).
- **Tipo de auriculares** — None / **Corded** (con cable) / **Cordless** (inalámbrico).
- **Casillas de equipamiento** — Phone, USB-C HUB, Screen, PDF, Mouse, ACAD, Keyboard. Marca lo que necesita la persona; estos importes alimentan las **necesidades** que se ven en *Availability*.
- **Discarded** — marca la solicitud como **descartada** (pasa a esa pestaña; no se borra).

**Qué puedes hacer (y sus límites):**
- **Save** — guarda la solicitud (queda en *Pending*).
- **Clear** — limpia el formulario.
- **Send devices** — **solo si la delegación es REMOTE**: registra el envío indicando la agencia de transporte.
- **Receive devices** — registra la recepción del material.
- **Complete incorporation** — crea la ficha de **Staff** a partir de estos datos y marca la incorporación como *Incorporated*. Es el paso final del onboarding; una vez hecho, la persona ya existe en *Staff*.

**La tabla:** Name · Company · Department · Delegation · Date y las casillas de equipamiento (WIN, MBA, MBP, Phone, Screen, Mouse, Keyboard, auriculares, USB-C, PDF, ACAD) más Send/Receive.

---

## 4. Activos

<a id="devices"></a>

### 4.1 Devices (Dispositivos)

**Para qué sirve:** el inventario de equipos informáticos (portátiles, sobremesa, tablets…), con sus datos técnicos, a quién están asignados y su paso por el servicio técnico.

![Pantalla de Dispositivos](images/05-devices.png)
*Formulario, totales a la derecha e inventario en la tabla inferior.*

**Cómo está organizada:** formulario a la izquierda, panel de **totales** y notas a la derecha, y la **tabla** de inventario abajo.

**Campos, uno a uno:**
- **Serial Number** — número de serie; es la **clave** del equipo (se busca y se guarda por él). Obligatorio.
- **Company** — empresa propietaria. **Obligatorio al guardar** (la columna no admite vacío); si no eliges empresa, el guardado se rechaza.
- **Type** — tipo de equipo (LAPTOP, IPAD…); con **autocompletado** sobre los tipos existentes.
- **Brand / Model** — marca y modelo.
- **Screen Size / HD Size / Memory** — características de hardware.
- **Have mobile SIM?** — casilla 0/1 que indica si el equipo **lleva SIM** (es un simple indicador, **no** vincula con la tabla de líneas móviles).
- **IMEI / PIN-PUK** — datos de la SIM si la tiene.
- **Origin** — procedencia (compra, traspaso…).
- **Insert Date** — fecha de alta.
- **Bill Number** — nº de factura (alimenta *Distribution Invoices*).
- **Obs** — observaciones (texto libre). **Importante:** se carga al buscar el equipo; si guardas con este campo vacío, **lo dejas vacío**.
- **Value (€)** — valor del equipo (suma a los totales y al valor de la cartera).
- **Assigned to** — persona asignada; **solo lectura** (la asignación se hace en *Allocations*/*Staff*).
- **Historial (Notes)** — registro automático de acciones; **solo lectura**. Cada **Save** añade una línea "Updated/Created by <usuario>".

**Qué puedes hacer (y sus límites):**
- **Search** — busca por número de serie y rellena la ficha.
- **Save** — guarda/actualiza. Requiere **Serial Number** y **Company**; registra la acción en el historial.
- **Support** — envía o recibe el equipo del servicio técnico (funciona como **interruptor**: si está fuera, lo recibe pidiendo el coste; si está dentro, lo envía pidiendo el destino).
- **Clear** — limpia el formulario (incluido Obs).
- **Export to Excel** — exporta el inventario completo.

**La tabla:** Serial Number · Type · Brand · Model · Screen · HD · Memory · IMEI · Mobile · PIN/PUK · Origin · Date · Bill Nº · Assigned To · Value (€).

**Detalles útiles:**
- Si el equipo está **en reparación**, verás un **aviso rojo** en la parte superior.
- Los **totales** (número de equipos y valor total) se actualizan automáticamente.
- La tabla carga los datos **por páginas** (búsqueda, orden y paginación se resuelven en el servidor), por lo que abre rápido aunque haya miles de equipos. Escribe en el buscador de la tabla para filtrar sobre **todo** el inventario.

---

<a id="licenses"></a>

### 4.2 Licenses (Licencias)

**Para qué sirve:** registrar y controlar licencias de software: compras, caducidades y a quién están asignadas.

![Pantalla de Licencias](images/06-licenses.png)
*Formulario, resumen por tipo en el centro y totales a la derecha.*

**Cómo está organizada:** formulario a la izquierda, **resumen de licencias por tipo** en el centro y **totales** + notas a la derecha. La tabla de licencias, abajo.

**Campos, uno a uno:**
- **Serial Number** — clave/identificador de la licencia (número de serie o clave de producto). Es por lo que se busca.
- **Company** — empresa propietaria.
- **Type** — tipo de licencia (con **autocompletado**); es lo que agrupa el resumen del centro.
- **Origin** — procedencia (con autocompletado).
- **Insert Date** — fecha de compra/alta.
- **Value (€)** — coste de la licencia.
- **Obs** — observaciones.
- **Bill Number** — nº de factura.
- **Assigned to** — persona/recurso al que está asignada; **solo lectura**. Una licencia asignada a la persona especial **"LICENCIAS CADUCADAS"** se considera **caducada**.

**Qué puedes hacer (y sus límites):**
- **Find** — busca por número de serie.
- **Save** — guarda/actualiza la licencia.
- **Clear** — limpia el formulario.
- **Export to Excel** — exporta el listado.

**La tabla:** Serial Number · Company · Type · Origin · Insert Date · Person · Obs · Value (€) · Bill Number.

**Detalles útiles:**
- El **resumen por tipo** muestra, para cada tipo: **compradas**, **caducadas** (asignadas a la persona "LICENCIAS CADUCADAS") y **en uso** (compradas − caducadas).
- Al hacer clic en una fila, el formulario se rellena con esa licencia.

---

<a id="phones"></a>

### 4.3 Phones (Teléfonos)

**Para qué sirve:** gestionar los teléfonos móviles corporativos y su paso por el servicio técnico.

![Pantalla de Teléfonos](images/07-phones.png)
*Ficha del teléfono, totales e inventario.*

**Campos, uno a uno:**
- **Serial Number** — clave del teléfono (se busca por él). Obligatorio.
- **Company** — empresa propietaria.
- **Brand / Model** — marca y modelo.
- **Origin** — procedencia (con autocompletado).
- **Insert Date** — fecha de alta.
- **Value (€)** — valor del teléfono.
- **IMEI** — identificador del terminal.
- **Obs** — observaciones.
- **Bill Number** — nº de factura.
- **Number** — número de la **línea** asociada; **solo lectura** (la SIM se asocia desde *Mobile Lines*).
- **Assigned to** — persona asignada; **solo lectura** (se asigna desde *Allocations*/*Staff*).

**Qué puedes hacer (y sus límites):**
- **Find** — busca por número de serie.
- **Save** — guarda/actualiza.
- **Support** — enviar/recibir del servicio técnico (interruptor, como en Devices).
- **Release** — desasigna el teléfono de la persona. En personas físicas genera un documento *Unassign*.
- **Export to Excel** — exporta el inventario.

**La tabla:** Serial Number · Company · Brand · Model · Origin · Date · Person · Number · IMEI · Obs · Value (€) · Bill Number.

**Detalles y limitaciones:** si el teléfono está en reparación, aparece un **aviso rojo** arriba. Para **asignarle una SIM** debes ir a *Mobile Lines* (allí solo se ofrecen teléfonos **sin** SIM).

---

<a id="mobile-lines"></a>

### 4.4 Mobile Lines (Líneas móviles)

**Para qué sirve:** gestionar las líneas/tarjetas SIM, incluidas eSIM y M2M, y a qué teléfono, persona o dispositivo están asociadas.

![Pantalla de Líneas móviles](images/08-mobile-lines.png)
*Datos de la línea, panel de asignación según el tipo y resumen de tarjetas.*

**Cómo está organizada:** formulario de la línea a la izquierda; a la derecha, el **panel de asignación** (cambia según sea SIM normal, **eSIM** o **M2M**), un **resumen de tarjetas** (en uso / libres / de baja / total) y las notas. La tabla, abajo.

**Campos, uno a uno:**
- **Number** — número de teléfono de la línea; es la **clave** (se busca por él).
- **Company** — empresa titular.
- **Insert Date** — fecha de alta.
- **Origin** — operador/procedencia (con autocompletado).
- **PIN / PIN2 / PUK / PUK2** — códigos de la SIM.
- **CARD (IMEI)** — identificador de la tarjeta SIM.
- **Extension** — extensión asociada, si la hay.
- **Obs** — observaciones.
- **eSIM** — casilla: la línea es una **eSIM** (se asigna a una **persona**, no a un teléfono físico).
- **M2M** — casilla: línea **máquina-a-máquina** (se asigna a un **dispositivo**).
- **Person** / **Device SN** — a quién/qué está asociada; **solo lectura**.

**Qué puedes hacer (y sus límites):**
- **Save** / **Clear** — guardar/limpiar.
- **Release** — desasigna la línea de su teléfono/persona/dispositivo (la deja libre).
- **Cancel line** — **da de baja** la línea con el proveedor (marca *Baja*). Acción a usar al cancelar el contrato.
- **Asignar según el tipo:** una **SIM normal** a un **teléfono sin SIM** (el desplegable solo ofrece teléfonos que **no** tienen ya una línea), una **eSIM** a una **persona**, o una línea **M2M** a un **dispositivo**.

**La tabla:** Number · Company · Origin · PIN · PUK · PIN2 · PUK2 · IMEI · Date · Mobile · Person · Ext · eSIM · M2M · Baja · Obs.

**Detalles y limitaciones:** al marcar **eSIM** o **M2M**, el **panel de asignación cambia** para ofrecer la opción correcta. El **resumen de tarjetas** (en uso / libres / de baja / total) se actualiza con cada cambio. Si la línea está de baja, verás un aviso.

---

<a id="fiber-lines"></a>

### 4.5 Fiber Lines (Líneas de fibra)

**Para qué sirve:** gestionar las líneas de fibra/conectividad de las sedes, su configuración técnica y las incidencias asociadas.

![Pantalla de Líneas de fibra](images/09-fiber-lines.png)
*Pestaña General con la configuración de la línea y la gestión de incidencias.*

**Cómo está organizada (dos pestañas):** **General** (formulario + incidencias) y **List** (listado de todas las líneas).

**Campos (General), uno a uno:**
- **ID** — identificador interno; solo lectura.
- **Description** — nombre/descripción de la línea (es lo que la identifica en los listados).
- **Provider** — proveedor (con autocompletado).
- **Delegation** — sede a la que da servicio.
- **Order / Service Code** — nº de pedido y código de servicio del operador.
- **Access / Router / Addressing** — datos técnicos del acceso, router y direccionamiento.
- **WIFI 1 / WIFI 2** — SSID/credenciales de las redes WiFi.
- **Start Date / Down Date** — alta y baja del servicio.
- **Fixed IP** — IP fija, si la hay.
- **Active** — casilla de estado **activo/inactivo**.
- **Registro de auditoría** — historial automático; solo lectura.

**Qué puedes hacer (y sus límites):**
- **Save** / **Clear** — guardar/limpiar la línea.
- **Add incidence** — abre el panel para registrar una **incidencia** (Working Order, fechas y descripciones de apertura/cierre).
- **Save Incidence** / **Close** — guardar o cerrar la incidencia desde su panel.
- **Export to Excel** — tanto las **líneas** como las **incidencias** de una línea.

**La tabla (List):** ID · Description · Provider · Delegation · Order · Service Code · Access · Router · Addressing · WIFI1 · WIFI2 · Active · Start Date · Down Date · Fixed IP.

---

<a id="printers"></a>

### 4.6 Printers (Impresoras)

**Para qué sirve:** registrar las impresoras: datos técnicos, ubicación, contrato y credenciales de acceso.

![Pantalla de Impresoras](images/21-printers.png)
*Pestaña General con los datos de la impresora.*

**Cómo está organizada (dos pestañas):** **General** (formulario + notas) y **List** (listado).

**Campos, uno a uno:**
- **Serial Number** — número de serie de la impresora (clave).
- **Description** — descripción/modelo.
- **Provider** — proveedor del contrato (con autocompletado).
- **Delegation** — sede donde está instalada.
- **MPS** — si está bajo contrato de servicios gestionados de impresión (Managed Print Services).
- **Fixed IP** — IP de la impresora en la red.
- **Start Date / End Date** — inicio y fin del contrato.
- **Monthly fee (€)** — cuota mensual.
- **User / Password** — credenciales de acceso al panel de la impresora.
- **Notas** — observaciones/historial.

**Qué puedes hacer:** **Save**, **Clear** y **Export to Excel** (en la pestaña List).

**La tabla (List):** Serial Number · Description · Provider · Delegation · MPS · Start Date · Down Date · Fee (€) · Fixed IP.

---

## 5. Accesos físicos

<a id="access-cards"></a>

### 5.1 Access Cards (Tarjetas de acceso)

**Para qué sirve:** gestionar las tarjetas de acceso a edificios/zonas y a qué empleado pertenecen.

![Pantalla de Tarjetas de acceso](images/17-access-cards.png)
*Ficha de la tarjeta y listado inferior.*

**Campos, uno a uno:**
- **Card** — código/identificador de la tarjeta. Es la clave.
- **Fermax MIF** — código MIFARE del sistema Fermax.
- **PIN** — código PIN; **solo lectura** (se asigna con *Generate PIN*).
- **Staff** — empleado al que pertenece; solo se ofrecen **empleados activos**.
- **State** — estado de la tarjeta (p. ej. PENDING, ACTIVATED, LOST…).
- **Obs** — observaciones.

**Qué puedes hacer (y sus límites):**
- **Save** — guardar/actualizar.
- **Clear** — limpiar.
- **Generate PIN** — asigna un **PIN aleatorio** del conjunto disponible. **Limitación:** al guardar la tarjeta ese PIN **se consume** (deja de estar disponible para otras).
- **Convert to Visitor Card** — convierte la tarjeta actual en tarjeta de visitante.

**La tabla:** ID · Card · Fermax MIF · PIN · Staff · State · Obs.

**Detalles útiles:** las tarjetas en estado **LOST** se muestran con la fila en **rosa** y no se pueden modificar.

---

<a id="visitor-cards"></a>

### 5.2 Visitors Access Cards (Tarjetas de visitantes)

**Para qué sirve:** gestionar tarjetas de acceso temporal para visitantes (sin PIN ni empleado fijo).

![Pantalla de Tarjetas de visitantes](images/18-visitor-cards.png)
*Ficha del visitante, listado e historial de la tarjeta.*

**Campos, uno a uno:**
- **Card Code** — código de la tarjeta (clave).
- **Fermax MIF** — código MIFARE del sistema Fermax.
- **User** — nombre del **visitante** (texto libre, no es un empleado del sistema).
- **State** — estado de la tarjeta.
- **Observations** — observaciones.

**Qué puedes hacer:** **Save** y **Clear**, además de exportar. (Las tarjetas de visitante **no llevan PIN ni empleado fijo**.)

**Las tablas:** un listado de tarjetas (ID · Card · Fermax MIF · User · State · Obs) y, debajo, el **historial** de la tarjeta seleccionada.

**Detalles útiles:** igual que en las de acceso, las tarjetas **LOST** aparecen en rosa.

---

<a id="access-keys"></a>

### 5.3 Access Keys (Llaves de acceso)

**Para qué sirve:** registrar las llaves físicas de oficinas/despachos y quién es responsable de cada una.

![Pantalla de Llaves de acceso](images/19-access-keys.png)
*Ficha de la llave y listado.*

**Campos, uno a uno:**
- **Key ID** — identificador de la llave (clave).
- **Company** — empresa propietaria.
- **Type** — tipo de llave (con autocompletado).
- **Staff** — empleado **responsable** de la llave.
- **Insert Date** — fecha de alta.
- **Notas** — observaciones.

**Qué puedes hacer:** **Save** y **Clear**.

**La tabla:** ID · Company · Type · Staff · Insert Date.

---

## 6. Compras y seguimiento

<a id="orders"></a>

### 6.1 Orders (Pedidos)

**Para qué sirve:** seguir el ciclo de vida de los pedidos de material: crear, procesar, recibir o cancelar.

![Pantalla de Pedidos](images/22-orders.png)
*Formulario de pedido y pestañas Pending / Canceled / Received.*

**Campos, uno a uno:**
- **ID** — identificador del pedido; se usa para buscar.
- **Article** — descripción del artículo pedido (**texto libre**).
- **Uds** — número de **unidades**.
- **Date** — fecha del pedido.
- **Historial (Notes)** — registro del pedido.

**Qué puedes hacer (y sus límites):**
- **Save** — guardar/actualizar (**Article, Uds y Date son obligatorios**).
- **Clear** — limpiar.
- **Cancel** — cancelar el pedido (solo si **no está ya tramitado**).
- **Process** — marcar como **tramitado** (enviado al proveedor).
- **Receive** — marcar como **recibido** (el pedido debe estar **tramitado** antes).

**Limitación (a tener en cuenta):** como **Article** es texto libre, su cruce con la pantalla *Availability* (columna *Orders*) se hace por coincidencia de texto y puede no acertar la categoría. Está previsto sustituir ese campo por un **desplegable controlado** para que el conteo sea exacto.

**Las pestañas:** **Pending** (pendientes), **Canceled** (cancelados) y **Received** (recibidos). Cada una con su botón de exportar.

**La tabla:** ID · Article · Date · Uds (y *Processed* en la pestaña de pendientes).

---

<a id="availability"></a>

### 6.2 Availability (Disponibilidad)

**Para qué sirve:** ver de un vistazo cuánto stock hay, cuánto se necesita y cuánto viene en camino, por tipo de artículo.

![Pantalla de Disponibilidad](images/23-availability.png)
*Tabla de disponibilidad por artículo.*

**La tabla:**
- **Article** — tipo de artículo (p. ej. LAPTOP WIN, PHONE, KEYBOARD).
- **Stock** — unidades disponibles (sin asignar).
- **Needs** — necesidades pendientes (incorporaciones aún no completadas).
- **Orders** — unidades en **pedidos pendientes** (lo que viene en camino).
- **Disp** — disponibilidad neta (**Stock − Needs + Orders**). En **verde** si es positiva, en **rojo** si es negativa.

**Qué puedes hacer:** **Export to Excel**.

**Limitación (a tener en cuenta):** la columna **Orders** se calcula cruzando el texto libre del campo *Article* de los pedidos con cada tipo de artículo, por lo que el conteo puede no ser exacto si la descripción del pedido no coincide. Está previsto controlar ese campo con un **desplegable** (ver *Orders*, §6.1).

---

<a id="under-repair"></a>

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

<a id="distribution-invoices"></a>

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

<a id="delegations"></a>

### 7.1 Delegations (Delegaciones)

**Para qué sirve:** gestionar las sedes/oficinas, con su dirección y un **mapa interactivo**.

![Pantalla de Delegaciones](images/20-delegations.png)
*Formulario y listado a la izquierda; mapa de España con los pines a la derecha.*

**Campos, uno a uno:**
- **Code** — código de la delegación (clave).
- **Delegation** — nombre de la sede. **Obligatorio.**
- **Address** — dirección postal; es la que se usa para **geolocalizar**.
- **Post Code** — código postal.
- **Town** — localidad.
- **Province** — provincia (desplegable de la tabla maestra de provincias).
- **Notas** — observaciones.

**Qué puedes hacer (y sus límites):**
- **Save** — guardar/actualizar; al guardar, la app **intenta geolocalizar** la dirección automáticamente. **Limitación:** si la dirección es imprecisa puede no situarse el pin; en ese caso usa *Geolocate*.
- **Clear** — limpiar.
- **Geolocate** — geolocalización **manual** de una delegación ya guardada.

**La tabla:** ID · Delegation · Address · Post Code · Town · Province.

**El mapa:**
- Centrado en España. Cada delegación geolocalizada aparece como un **pin**.
- **Azul** = delegación **activa**; **rojo** = **inactiva**.
- Al pulsar un pin se muestra el nombre, la dirección y el estado.

---

<a id="users"></a>

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

<a id="password-change"></a>

### 7.3 Cambiar mi contraseña

**Para qué sirve:** que cualquier usuario cambie **su propia** contraseña estando dentro de la app.

![Cambiar contraseña](images/16-password-change.png)
*Formulario de cambio de contraseña.*

**Campos:** Old Password, New Password y Confirm Password.

**Reglas de la nueva contraseña:** al menos 8 caracteres, no puede ser solo números ni una contraseña demasiado común, y las dos veces deben coincidir.

**Detalles útiles:** tras el cambio no tienes que volver a iniciar sesión; la app mantiene tu sesión abierta.

---

## 8. Monitorización (red, equipos remotos y salas)

> Todas las pantallas de esta sección son de **monitorización en tiempo casi real** y están reservadas a usuarios con el permiso **`net_overview`** (Omada usa además el permiso `omada`). Los datos se calculan en un **proceso en segundo plano cada 5 minutos** y se guardan en caché, por lo que la pantalla y la barra de estado responden al instante sin esperar a las APIs externas. La hora del último refresco se ve en el pie ("Updated").

<a id="net-overview"></a>

### 8.1 Net Overview (Zyxel Nebula)

**Para qué sirve:** ver de un vistazo el estado de la red de **todas las sedes** gestionadas en la nube de **Zyxel Nebula**: switches, puntos de acceso, firewalls, líneas WAN, clientes conectados y alarmas.

**Cómo está organizada:** al entrar aparece un **spinner "Recovering information…"** mientras se cargan los datos por AJAX; luego se muestra **una tarjeta por sede**. Cada tarjeta tiene una cabecera (nombre de la sede + estado OK/alertas + botón **Topology**) y varios paneles.

**Paneles de cada sede:**
- **WAN** — dos indicadores: **enabled** (interfaces WAN configuradas y habilitadas) y **operational** (con enlace físico activo).
- **Firewalls / Switches / Access Points** — total, **online** (verde), **offline** (rojo) y, si los hay, un contador naranja **"outdated"** (equipos con firmware desactualizado).
- **Clients** — clientes conectados **en este momento**, separados en **WiFi** y **cableado**.
- **Alerts** — número de incidencias de la sede; si hay, la tarjeta es **clicable** y abre un popup con el detalle (equipos offline y/o con firmware desactualizado).

**Qué puedes hacer:**
- **Topology** (botón por sede) — abre un **mapa** en ventana modal (Firewalls → Switches → Access Points) con, por equipo, su estado y los clientes conectados ahora; en los firewalls muestra además **CPU** y **Memoria** (verde <50 %, naranja 50–80 %, rojo >80 %).
- Hacer **clic en el panel Alerts** — ver la lista de equipos con problemas.

**Funcionalidades y alarmas:** las **alarmas** de una sede son la suma de **equipos offline** + **equipos con firmware desactualizado** (se cuentan por separado: un mismo equipo offline y desactualizado suma 2). Si un firewall supera el **80 % de CPU o memoria**, también cuenta como alarma. El total de todas las sedes se muestra en el pie como **"Net Alerts"** (fondo rojo) y se actualiza cada 5 minutos.

**Limitaciones (importante):**
- El indicador **operational** de las WAN suele mostrar **"—"**: la API de Nebula **no expone el estado de las interfaces** de los firewalls Zyxel (FLEX 700H / ATP), confirmado por el soporte de Zyxel. Para conocerlo habría que consultar el firewall por **SNMP** desde la red de la sede.
- Las conexiones del **mapa de topología** se muestran **por niveles**, no puerto a puerto (la API no da el mapa real ni el vecino LLDP).
- Requiere las credenciales `NEBULA_*` configuradas en el servidor; si faltan, la pantalla muestra un aviso de "no configurado".

> **Próximamente:** los datos del controlador **TP-Link Omada** se integrarán en esta misma pantalla. La carga será en **dos pasadas**: primero los datos de Nebula (como ahora) y, a continuación, los de Omada en el mismo formulario.

---

<a id="remote-machines"></a>

### 8.2 Remote Machines (AnyDesk)

**Para qué sirve:** saber si los **equipos remotos** (mini-PCs de las sedes) están **accesibles**, a partir de la tabla `oees_anydesk` y la **API REST de AnyDesk**.

**Cómo está organizada:** una **tarjeta por equipo** con icono de ordenador, **descripción**, su **código AnyDesk**, la **última conexión** (`last_connection`) y una **bola verde/roja** según esté accesible o no.

**Funcionalidades:** el proceso de fondo recorre los equipos cada 5 minutos; si un equipo está accesible, **sella la fecha/hora** en `last_connection`. El nº de equipos **no accesibles** se muestra en el pie como **"Remote Machines Alerts"** (fondo rojo, solo para `net_overview`); si no hay incidencias, no se muestra.

**Limitaciones:** necesita una **licencia AnyDesk** activa y registrada y sus credenciales (`ANYDESK_API_LICENSE` / `ANYDESK_API_KEY`). Mientras la API no responda (p. ej. licencia sin registrar), la pantalla usa un **modo provisional**: considera "no accesible" a los equipos que aún no tienen `last_connection`, para que el diseño y el aviso del pie sigan siendo útiles.

---

<a id="video-rooms"></a>

### 8.3 Video Rooms (Logitech Sync)

**Para qué sirve:** monitorizar el estado de las **salas de videoconferencia** equipadas con **Logitech Rally Bar / Bar Mini**, usando la **Sync Cloud API** de Logitech, y detectar reservas problemáticas.

**Cómo está organizada:** pantalla a **dos columnas**. A la **izquierda (2/3)**, una **tarjeta por sala**. A la **derecha (1/3)**, **tres tablas** de análisis.

**Tarjeta de cada sala:** nombre, **estado** (🔴 *In meeting* / 🟡 *Occupied* / 🟢 *Free*), nº de **ocupantes**, **hora de inicio–fin** de la reunión programada, **título** y **organizador**, y el **modelo/firmware/estado** del equipo, con una **bola verde/roja** (conectado/desconectado). Si la sala está **ocupada pero sin personas** o **desconectada**, la tarjeta se resalta en rojo con el motivo.

**Tablas de la derecha:**
1. **Future-booking incidences** — reservas futuras cuyo **organizador está de baja** ("User X, deactivated since dd-mm-yyyy, has N future bookings") o cuyo **email no existe** en la tabla de personal ("The email … is not found in the users table").
2. **Under-used meetings (occupancy ≤ 50 %)** — reuniones cuya ocupación efectiva fue ≤ 50 % de su duración: **Date · Start · End · Title · Organizer · % Occ.** (si no se conoce la hora de fin, se muestra la duración).
3. **Organizers ranking — meetings not held (occ. ≤ 10 min)** — ranking de organizadores con más reuniones prácticamente no celebradas: **Organizer · Total Duration · Total Occupied · Meetings**.

**Funcionalidades y alarmas:** el proceso de fondo registra cada reunión en la tabla `oees_meeting_room`: `duration` es la **duración inicial reservada** (fija) y `occupied` **suma 5 minutos** en cada revisión mientras la sala esté ocupada (por eso los minutos son múltiplos de 5). El nº de salas **ocupadas-sin-gente o desconectadas** se muestra en el pie como **"Video Rooms Alerts"** (fondo rojo, solo `net_overview`).

**Limitaciones:** requiere **licencia Logitech** y un **certificado de cliente + clave (mTLS)** en el servidor. Mientras no estén configurados, la pantalla muestra **datos de ejemplo** con un aviso **"Sample data"** para poder ajustar el diseño, y **no escribe** nada en `oees_meeting_room`. Algunos campos de la reunión (organizador, título, hora inicio/fin) dependen de que la API real los proporcione.

---

## Anexo A: Glosario

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
