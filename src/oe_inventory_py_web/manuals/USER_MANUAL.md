# OE Inventory — User Manual

**Version:** 1.0 (web application)
**Audience:** the IT team and OE Inventory users
**What it is:** Octopus Energy's tool to manage the IT asset inventory — devices, licences, phones, lines, access and the people they are assigned to.

---

## How to use this manual

We've written it to be easy: plain language, no unnecessary jargon, and a picture of every screen so you always know where you are. Each section follows the same order:

- **What it's for** — the idea in one sentence.
- **How it's laid out** — the areas of the screen.
- **Fields** — the information you fill in.
- **What you can do** — the buttons and actions.
- **The table** — the columns you'll see in the list.
- **Handy details** — tips and behaviours worth knowing.

> **About the images:** the placeholders marked as `![...]` are filled with real screenshots from your installation. At the end of the manual there's a **[Screenshot guide](#appendix-a-screenshot-guide)** listing the images to take and how to name them, so the document ends up complete.

---

## Contents

1. [Getting started](#1-getting-started)
   - [Sign in](#11-sign-in)
   - [I forgot my password](#12-i-forgot-my-password)
   - [The home screen](#13-the-home-screen-main-menu)
   - [The status bar](#14-the-status-bar-bottom)
2. [Concepts repeated across the app](#2-concepts-repeated-across-the-app)
3. [People and assignments](#3-people-and-assignments)
   - [Staff](#31-staff)
   - [Allocations](#32-allocations)
   - [Incorporations](#33-incorporations)
4. [Assets](#4-assets)
   - [Devices](#41-devices)
   - [Licenses](#42-licenses)
   - [Phones](#43-phones)
   - [Mobile Lines](#44-mobile-lines)
   - [Fiber Lines](#45-fiber-lines)
   - [Printers](#46-printers)
5. [Physical access](#5-physical-access)
   - [Access Cards](#51-access-cards)
   - [Visitors Access Cards](#52-visitors-access-cards)
   - [Access Keys](#53-access-keys)
6. [Purchasing and tracking](#6-purchasing-and-tracking)
   - [Orders](#61-orders)
   - [Availability](#62-availability)
   - [Under Repair](#63-under-repair)
   - [Distribution Invoices](#64-distribution-invoices)
7. [Organisation and users](#7-organisation-and-users)
   - [Delegations](#71-delegations)
   - [Users](#72-users)
   - [Change my password](#73-change-my-password)
8. [Monitoring (network, remote machines and rooms)](#8-monitoring-network-remote-machines-and-rooms)
   - [Net Overview (Zyxel Nebula)](#81-net-overview-zyxel-nebula)
   - [Remote Machines (AnyDesk)](#82-remote-machines-anydesk)
   - [Video Rooms (Logitech Sync)](#83-video-rooms-logitech-sync)
- [Appendix A: Glossary](#appendix-a-glossary)

---

## 1. Getting started

<a id="login"></a>

### 1.1 Sign in

**What it's for:** logging into the application with your user.

![Login screen](images/01-login.png)
*OE Inventory login screen.*

**Fields:**
- **User** — your username.
- **Password** — your password.

**What you can do:**
- **OK (✔)** — checks your credentials. If they're correct, you land on the home screen. If not, you'll see *"User or password incorrect."*
- **Forgot my password?** — takes you to the recovery process (see next section).

> **Tip:** if you were already signed in, the app takes you straight to the home screen without asking for credentials again.

---

<a id="password-recovery"></a>

### 1.2 I forgot my password

**What it's for:** regaining access on your own when you can't remember your password.

![Password recovery](images/02-recuperar-contrasena.png)
*Form to request the recovery email.*

**How it works:**
1. On the login screen, click **Forgot my password?**
2. Enter the email linked to your user.
3. You'll receive an email with a secure link to set a new password.
4. Open the link, type the new password twice, and you're done.

> **Note:** for the email to arrive, your user must have a **registered email** (set on the [Users](#72-users) screen). Email is sent through Resend.

---

<a id="home"></a>

### 1.3 The home screen (main menu)

**What it's for:** your starting point. From here you reach every section you have permission for.

![Home screen](images/03-inicio-mdi.png)
*Main menu with the Octopus logo and the top navigation bar.*

**How it's laid out:**
- **Navigation bar (top):** buttons to each module. **You'll only see the options you have permission for.** Physical-access sections are grouped under the **Office Access** dropdown (staff cards, visitor cards and keys).
- **Central area:** the Octopus logo and a welcome message: *"Select an option from the menu above to start working."*
- **Status bar (bottom):** see the next section.

**What you can do:**
- Click any menu button to open that section.
- **Password Change** — change your password (always available).
- **Exit** — sign out (you'll be asked to confirm: *"Do you want to close the current session?"*).

---

<a id="status-bar"></a>

### 1.4 The status bar (bottom)

**What it's for:** giving you information at a glance, without having to look for it.

![Status bar](images/04-barra-estado.png)
*Bottom status bar with user, connection, online users and counters.*

From left to right:

- **User** — the user you signed in with.
- **Session: active / inactive** — reflects whether your browser **has an internet connection**. Green with a cloud when connected; red when it drops. It updates on its own, instantly, with no page reload.
- **Online: N** — how many people are using the app right now (activity in the last 5 minutes). **Click on it** and a window opens with the **names** of those connected.
- **Pending cards** — access cards (staff and visitors) that are in *PENDING* state.
- **Pending orders** — orders not yet processed or cancelled.

> **Note:** the *Pending cards* and *Pending orders* counters are computed when the page loads; if they change, you'll see them updated the next time you navigate.

---

## 2. Concepts repeated across the app

So we don't repeat it in every section, these ideas apply to almost every screen:

- **Find a record:** almost every form has a main field (Serial Number, Card, ID…) with a **Find (🔍)** button. Type the value and press the button or **Enter**: the app fills in the rest of the form. You can also **click a row** in the table to load it.
- **Save:** the **Save (💾)** button creates the record if it's new or updates the existing one.
- **Clear:** the **Clear** button empties the form to start over.
- **History / Notes:** many screens have a read-only **Notes** box. Each time you save or perform an action, the app automatically adds a line with the **date, time and your user**. It's the audit trail of who did what and when.
- **Export to Excel:** wherever there are lists, you'll find a button to **download the data as `.xlsx`**.
- **"reader" profile (read-only):** if your user has this profile, you **can view everything but change nothing** (no saving, no exporting). If you try, you'll see: *"You have a reader profile and can't modify data."* It's our way of giving access to information without the risk of accidental changes.
- **Scope:** on screens like Staff, your user can be limited to certain **companies, delegations or departments**. You'll only see the people and data within your scope.
- **Alerts:** success, error and warning messages appear as pop-ups with the Octopus logo.

---

## 3. People and assignments

<a id="staff"></a>

### 3.1 Staff

**What it's for:** managing people and all the IT equipment assigned to them while they're part of the company.

![Staff screen — General tab](images/10-staff-general.png)
*Staff record with their details, totals and the table of assigned items.*

**How it's laid out (three tabs):**
- **General** — the person's details, totals and the table of items assigned to them.
- **Docs** — the person's PDF documents (upload, list and preview).
- **List** — a list of all staff, with *People* (total) and *Actives* (active) counters.

**Fields (General), one by one:**
- **ID** — internal identifier; **read-only**, filled in when you search. You don't type it.
- **Name** — the person's name. **Required**; it's what you search by (with **Find**) and what shows as "assigned to" on assets.
- **Department** — department; field with **autocomplete** over existing values (you can type a new one). Part of the **scope** seen by users with limited permissions.
- **Company** / **Delegation** — the company and site the person belongs to; also limit the scope.
- **eMail** — the person's email. As well as informative, it is the **join key** with other screens (e.g. the meeting organizer in *Video Rooms* is matched by this email).
- **Incorporation date** — start date.
- **Termination date** — offboarding date; **not edited by hand**, it's filled automatically by **Terminate**.
- **Natural Person** — ticks whether this is a **physical person** (not a role or resource). **Important limitation:** the *Assign*/*Unassign*/*Terminate* documents are generated **only for physical persons**.
- **Notes** — **automatic history** (creation, assignments, offboarding…). **Read-only**: it fills itself with each action, you don't write it.

**What you can do (and its limits):**
- **Save** — saves/creates the person. Requires at least the **Name**.
- **Clear** — empties the form (deletes nothing from the database).
- **Generate document** — generates a PDF with the assigned inventory. **Physical persons only.**
- **Send Email** — sends that report to the People department via **Resend**. **Limitation:** it needs Resend configured and the sender's domain verified; otherwise the send fails (logged).
- **Release** — unassigns the item **selected in the table** and returns it to stock; for physical persons it generates an *Unassign* document. You must select a row first.
- **Terminate** — opens a window to tick which items the person **returns**; generates a *Terminate* PDF, returns those items to stock and marks the contract as ended (fills *Termination date* and sets the state to inactive). A **hard-to-undo** action: use it when closing the contract.
- **Export to Excel** — exports that person's assigned-items table.

![Terminate window](images/11-staff-terminate-modal.png)
*On offboarding, tick the returned items; the selected ones go back to stock.*

**The table (assigned items):** ID · Serial · Type · Brand · Model · Origin · Date · Obs · Value (€).

![Staff screen — Docs tab](images/12-staff-docs.png)
*Managing the person's PDF documents, with preview.*

**Handy details:**
- The totals (number of items and total value) are computed automatically by summing devices, licences, phones, cards and keys.
- Documents are stored securely and can be previewed without downloading.

---

<a id="allocations"></a>

### 3.2 Allocations

**What it's for:** quickly assigning devices, licences and phones that are in stock to an active person.

![Allocations screen](images/13-allocations.png)
*Selecting a person and searching for free assets to assign.*

**How it's laid out:** a single column with four stacked blocks — **person**, **devices**, **licences** and **phones**.

**How to use it:**
1. Choose the **person** (list of active staff). *Tip:* you can arrive here with the person preselected from their record.
2. In **Devices**, filter by **Type** and **Brand** and press **Search**; pick the available serial number.
3. In **Licenses**, filter by **Type** and search for the serial number.
4. In **Phones**, type or pick the serial number (field with autocomplete) and search.
5. Press **Assign** in each block to assign that item to the person.

**Fields and filters, one by one:**
- **Person** — dropdown of **active staff** (offboarded people don't appear). You must pick a person before assigning.
- **Devices → Type / Brand** — filters to narrow the search for free devices; after **Search** the dropdown of **available serial numbers** is filled.
- **Licenses → Type** — analogous filter for free licences.
- **Phones → serial number** — field with **autocomplete** over phones in stock.

**What you can do (and its limits):**
- **Search** (in each block) — finds **available** assets matching the filter.
- **Assign** — assigns the item selected in that block to the person. You must have chosen a person **and** a serial number.
- **Generate document** — generates a single assignment PDF with everything given to that person. **Physical persons only.**

**Details and limitations:**
- Only **unassigned** assets (in stock) are offered; an already-assigned item won't appear until it's released.
- You can arrive here with the **person preselected** from their Staff record.
- If you assign items and leave **without** pressing *Generate document*, the app generates the assignment document automatically anyway (one per person), so the audit trail is never missing.

---

<a id="incorporations"></a>

### 3.3 Incorporations

**What it's for:** preparing a new joiner's arrival (onboarding): what equipment they need, managing shipping/receipt and, finally, turning them into app staff.

![Incorporations screen](images/14-incorporations.png)
*Requested-equipment form and the Pending / Discarded / Incorporated tabs.*

**How it's laid out:** a form on the left and, on the right, three lists: **Pending**, **Discarded** and **Incorporated**.

**Fields, one by one:**
- **Name** — name of the joiner.
- **Company / Department / Delegation** — destination of the incorporation; **Delegation** matters because the **REMOTE** value enables the courier-shipping flow.
- **Date** — expected start date.
- **Address** — shipping address; **applies to remote joiners only** (when the kit must be sent to their home).
- **Laptop type** — None / **WIN** (Windows) / **MBA** (MacBook Air) / **MBP** (MacBook Pro).
- **Headset type** — None / **Corded** / **Cordless**.
- **Equipment checkboxes** — Phone, USB-C HUB, Screen, PDF, Mouse, ACAD, Keyboard. Tick what the person needs; these feed the **needs** shown in *Availability*.
- **Discarded** — marks the request as **discarded** (moves to that tab; nothing is deleted).

**What you can do (and its limits):**
- **Save** — saves the request (stays in *Pending*).
- **Clear** — clears the form.
- **Send devices** — **only if the delegation is REMOTE**: records the shipment, indicating the courier agency.
- **Receive devices** — records receipt of the material.
- **Complete incorporation** — creates the **Staff** record from this data and marks the incorporation as *Incorporated*. It's the final onboarding step; once done, the person exists in *Staff*.

**The table:** Name · Company · Department · Delegation · Date and the equipment checkboxes (WIN, MBA, MBP, Phone, Screen, Mouse, Keyboard, headsets, USB-C, PDF, ACAD) plus Send/Receive.

---

## 4. Assets

<a id="devices"></a>

### 4.1 Devices

**What it's for:** the inventory of computer equipment (laptops, desktops, tablets…), with their technical data, who they're assigned to and their time at the technical service.

![Devices screen](images/05-devices.png)
*Form, totals on the right and inventory in the table below.*

**How it's laid out:** form on the left, **totals** and notes panel on the right, and the inventory **table** below.

**Fields, one by one:**
- **Serial Number** — serial number; the device's **key** (you search and save by it). Required.
- **Company** — owning company. **Required to save** (the column can't be empty); if you don't pick a company, the save is rejected.
- **Type** — device type (LAPTOP, IPAD…); with **autocomplete** over existing types.
- **Brand / Model** — make and model.
- **Screen Size / HD Size / Memory** — hardware specs.
- **Have mobile SIM?** — a 0/1 checkbox marking whether the device **carries a SIM** (just a flag, it does **not** link to the mobile-lines table).
- **IMEI / PIN-PUK** — SIM data if it has one.
- **Origin** — provenance (purchase, transfer…).
- **Insert Date** — registration date.
- **Bill Number** — invoice number (feeds *Distribution Invoices*).
- **Obs** — free-text notes. **Important:** it's loaded when you search the device; if you save with this field empty, **you leave it empty**.
- **Value (€)** — device value (adds to the totals and the portfolio value).
- **Assigned to** — assigned person; **read-only** (assignment is done in *Allocations*/*Staff*).
- **History (Notes)** — automatic action log; **read-only**. Each **Save** adds an "Updated/Created by <user>" line.

**What you can do (and its limits):**
- **Search** — searches by serial number and fills the record.
- **Save** — saves/updates. Requires **Serial Number** and **Company**; logs the action in the history.
- **Support** — sends the device to / receives it from the technical service (works as a **toggle**: if it's out, it receives it asking for the cost; if it's in, it sends it asking for the destination).
- **Clear** — clears the form (including Obs).
- **Export to Excel** — exports the full inventory.

**The table:** Serial Number · Type · Brand · Model · Screen · HD · Memory · IMEI · Mobile · PIN/PUK · Origin · Date · Bill Nº · Assigned To · Value (€).

**Handy details:**
- If the device is **under repair**, you'll see a **red warning** at the top.
- The **totals** (number of devices and total value) update automatically.
- The table loads data **by pages** (search, sort and pagination are handled on the server), so it opens fast even with thousands of devices. Type in the table's search box to filter across the **whole** inventory.

---

<a id="licenses"></a>

### 4.2 Licenses

**What it's for:** registering and tracking software licences: purchases, expiries and who they're assigned to.

![Licenses screen](images/06-licenses.png)
*Form, by-type summary in the middle and totals on the right.*

**How it's laid out:** form on the left, **by-type licence summary** in the middle and **totals** + notes on the right. The licence table is below.

**Fields, one by one:**
- **Serial Number** — the licence's key/identifier (serial number or product key). You search by it.
- **Company** — owning company.
- **Type** — licence type (with **autocomplete**); this is what the central summary groups by.
- **Origin** — provenance (with autocomplete).
- **Insert Date** — purchase/registration date.
- **Value (€)** — licence cost.
- **Obs** — notes.
- **Bill Number** — invoice number.
- **Assigned to** — person/resource it's assigned to; **read-only**. A licence assigned to the special person **"LICENCIAS CADUCADAS"** counts as **expired**.

**What you can do (and its limits):**
- **Find** — searches by serial number.
- **Save** — saves/updates the licence.
- **Clear** — clears the form.
- **Export to Excel** — exports the list.

**The table:** Serial Number · Company · Type · Origin · Insert Date · Person · Obs · Value (€) · Bill Number.

**Handy details:**
- The **by-type summary** shows, for each type: **purchased**, **expired** (assigned to the person "LICENCIAS CADUCADAS") and **in use** (purchased − expired).
- Clicking a row fills the form with that licence.

---

<a id="phones"></a>

### 4.3 Phones

**What it's for:** managing corporate mobile phones and their time at the technical service.

![Phones screen](images/07-phones.png)
*Phone record, totals and inventory.*

**Fields, one by one:**
- **Serial Number** — the phone's key (you search by it). Required.
- **Company** — owning company.
- **Brand / Model** — make and model.
- **Origin** — provenance (with autocomplete).
- **Insert Date** — registration date.
- **Value (€)** — phone value.
- **IMEI** — handset identifier.
- **Obs** — notes.
- **Bill Number** — invoice number.
- **Number** — the associated **line** number; **read-only** (the SIM is linked from *Mobile Lines*).
- **Assigned to** — assigned person; **read-only** (assigned from *Allocations*/*Staff*).

**What you can do (and its limits):**
- **Find** — searches by serial number.
- **Save** — saves/updates.
- **Support** — send/receive from the technical service (toggle, as in Devices).
- **Release** — unassigns the phone from the person. For physical persons it generates an *Unassign* document.
- **Export to Excel** — exports the inventory.

**The table:** Serial Number · Company · Brand · Model · Origin · Date · Person · Number · IMEI · Obs · Value (€) · Bill Number.

**Details and limitations:** if the phone is under repair, a **red warning** appears at the top. To **assign it a SIM** go to *Mobile Lines* (which only offers phones **without** a SIM).

---

<a id="mobile-lines"></a>

### 4.4 Mobile Lines

**What it's for:** managing lines/SIM cards, including eSIM and M2M, and which phone, person or device they're linked to.

![Mobile Lines screen](images/08-mobile-lines.png)
*Line details, the assignment panel by type and the card summary.*

**How it's laid out:** the line form on the left; on the right, the **assignment panel** (changes for a normal SIM, **eSIM** or **M2M**), a **card summary** (in use / free / cancelled / total) and the notes. The table is below.

**Fields, one by one:**
- **Number** — the line's phone number; the **key** (you search by it).
- **Company** — holder company.
- **Insert Date** — registration date.
- **Origin** — carrier/provenance (with autocomplete).
- **PIN / PIN2 / PUK / PUK2** — SIM codes.
- **CARD (IMEI)** — SIM card identifier.
- **Extension** — associated extension, if any.
- **Obs** — notes.
- **eSIM** — checkbox: the line is an **eSIM** (assigned to a **person**, not a physical phone).
- **M2M** — checkbox: **machine-to-machine** line (assigned to a **device**).
- **Person** / **Device SN** — what it's linked to; **read-only**.

**What you can do (and its limits):**
- **Save** / **Clear** — save/clear.
- **Release** — unassigns the line from its phone/person/device (frees it).
- **Cancel line** — **cancels** the line with the provider (marks it *Cancelled*). Use it when closing the contract.
- **Assign by type:** a **normal SIM** to a **phone without a SIM** (the dropdown only offers phones that don't already have a line), an **eSIM** to a **person**, or an **M2M** line to a **device**.

**The table:** Number · Company · Origin · PIN · PUK · PIN2 · PUK2 · IMEI · Date · Mobile · Person · Ext · eSIM · M2M · Cancelled · Obs.

**Details and limitations:** ticking **eSIM** or **M2M** **changes the assignment panel** to offer the right option. The **card summary** (in use / free / cancelled / total) updates with each change. If the line is cancelled, you'll see a warning.

---

<a id="fiber-lines"></a>

### 4.5 Fiber Lines

**What it's for:** managing the sites' fibre/connectivity lines, their technical configuration and the associated incidents.

![Fiber Lines screen](images/09-fiber-lines.png)
*General tab with the line configuration and incident management.*

**How it's laid out (two tabs):** **General** (form + incidents) and **List** (list of all lines).

**Fields (General), one by one:**
- **ID** — internal identifier; read-only.
- **Description** — the line's name/description (identifies it in the listings).
- **Provider** — provider (with autocomplete).
- **Delegation** — site it serves.
- **Order / Service Code** — the carrier's order number and service code.
- **Access / Router / Addressing** — technical data for the access, router and addressing.
- **WIFI 1 / WIFI 2** — SSID/credentials of the WiFi networks.
- **Start Date / Down Date** — service start and end.
- **Fixed IP** — fixed IP, if any.
- **Active** — active/inactive state checkbox.
- **Audit log** — automatic history; read-only.

**What you can do (and its limits):**
- **Save** / **Clear** — save/clear the line.
- **Add incidence** — opens the panel to log an **incident** (Working Order, dates and open/close descriptions).
- **Save Incidence** / **Close** — save or close the incident from its panel.
- **Export to Excel** — both the **lines** and the **incidents** of a line.

**The table (List):** ID · Description · Provider · Delegation · Order · Service Code · Access · Router · Addressing · WIFI1 · WIFI2 · Active · Start Date · Down Date · Fixed IP.

---

<a id="printers"></a>

### 4.6 Printers

**What it's for:** registering printers: technical data, location, contract and access credentials.

![Printers screen](images/21-printers.png)
*General tab with the printer details.*

**How it's laid out (two tabs):** **General** (form + notes) and **List** (listing).

**Fields, one by one:**
- **Serial Number** — the printer's serial number (key).
- **Description** — description/model.
- **Provider** — contract provider (with autocomplete).
- **Delegation** — site where it's installed.
- **MPS** — whether it's under a Managed Print Services contract.
- **Fixed IP** — the printer's IP on the network.
- **Start Date / End Date** — contract start and end.
- **Monthly fee (€)** — monthly fee.
- **User / Password** — credentials to access the printer's panel.
- **Notes** — observations/history.

**What you can do:** **Save**, **Clear** and **Export to Excel** (on the List tab).

**The table (List):** Serial Number · Description · Provider · Delegation · MPS · Start Date · Down Date · Fee (€) · Fixed IP.

---

## 5. Physical access

<a id="access-cards"></a>

### 5.1 Access Cards

**What it's for:** managing building/zone access cards and which employee they belong to.

![Access Cards screen](images/17-access-cards.png)
*Card record and the list below.*

**Fields, one by one:**
- **Card** — the card's code/identifier (key).
- **Fermax MIF** — the MIFARE code from the Fermax system.
- **PIN** — PIN code; **read-only** (assigned via *Generate PIN*).
- **Staff** — the employee it belongs to; only **active employees** are offered.
- **State** — card state (e.g. PENDING, ACTIVATED, LOST…).
- **Obs** — notes.

**What you can do (and its limits):**
- **Save** — save/update.
- **Clear** — clear.
- **Generate PIN** — assigns a **random PIN** from the available pool. **Limitation:** when you save the card that PIN **is consumed** (it stops being available for others).
- **Convert to Visitor Card** — convert the current card into a visitor card.

**The table:** ID · Card · Fermax MIF · PIN · Staff · State · Obs.

**Handy details:** cards in **LOST** state are shown with the row in **pink** and can't be modified.

---

<a id="visitor-cards"></a>

### 5.2 Visitors Access Cards

**What it's for:** managing temporary access cards for visitors (no PIN, no fixed employee).

![Visitors Access Cards screen](images/18-visitor-cards.png)
*Visitor record, list and the card history.*

**Fields, one by one:**
- **Card Code** — the card's code (key).
- **Fermax MIF** — the MIFARE code from the Fermax system.
- **User** — the **visitor's** name (free text — not a system employee).
- **State** — card state.
- **Observations** — notes.

**What you can do:** **Save** and **Clear**, plus export. (Visitor cards have **no PIN and no fixed employee**.)

**The tables:** a card list (ID · Card · Fermax MIF · User · State · Obs) and, below it, the **history** of the selected card.

**Handy details:** as with access cards, **LOST** cards appear in pink.

---

<a id="access-keys"></a>

### 5.3 Access Keys

**What it's for:** registering physical office/room keys and who is responsible for each one.

![Access Keys screen](images/19-access-keys.png)
*Key record and listing.*

**Fields, one by one:**
- **Key ID** — the key's identifier (key).
- **Company** — owning company.
- **Type** — key type (with autocomplete).
- **Staff** — the employee **responsible** for the key.
- **Insert Date** — date added.
- **Notes** — observations.

**What you can do:** **Save** and **Clear**.

**The table:** ID · Company · Type · Staff · Insert Date.

---

## 6. Purchasing and tracking

<a id="orders"></a>

### 6.1 Orders

**What it's for:** tracking the lifecycle of material orders: create, process, receive or cancel.

![Orders screen](images/22-orders.png)
*Order form and the Pending / Canceled / Received tabs.*

**Fields, one by one:**
- **ID** — the order identifier; used to search.
- **Article** — description of the ordered item (**free text**).
- **Uds** — number of **units**.
- **Date** — order date.
- **History (Notes)** — order log.

**What you can do (and its limits):**
- **Save** — save/update (**Article, Uds and Date are required**).
- **Clear** — clear.
- **Cancel** — cancel the order (only if **not already processed**).
- **Process** — mark as **processed** (sent to the supplier).
- **Receive** — mark as **received** (the order must be **processed** first).

**Limitation (worth noting):** because **Article** is free text, its match against the *Availability* screen (the *Orders* column) is done by text and may miss the category. The plan is to replace this field with a **controlled dropdown** so the count is exact.

**The tabs:** **Pending**, **Canceled** and **Received**. Each one has its export button.

**The table:** ID · Article · Date · Uds (and *Processed* on the pending tab).

---

<a id="availability"></a>

### 6.2 Availability

**What it's for:** seeing at a glance how much stock there is, how much is needed and how much is on the way, by article type.

![Availability screen](images/23-availability.png)
*Availability table by article.*

**The table:**
- **Article** — article type (e.g. LAPTOP WIN, PHONE, KEYBOARD).
- **Stock** — available units (unassigned).
- **Needs** — pending needs (incorporations not yet completed).
- **Orders** — units in **pending orders** (what's on the way).
- **Disp** — net availability (**Stock − Needs + Orders**). **Green** if positive, **red** if negative.

**What you can do:** **Export to Excel**.

**Limitation (worth noting):** the **Orders** column is computed by matching the free-text *Article* field of orders against each article type, so the count may be inexact if the order's description doesn't match. The plan is to control that field with a **dropdown** (see *Orders*, §6.1).

---

<a id="under-repair"></a>

### 6.3 Under Repair

**What it's for:** tracking devices and phones at the repair shop: when they left, when they came back and what it cost.

![Under Repair screen](images/24-under-repair.png)
*Pending and Repaired tabs, with the total repaired value.*

**How it's laid out (two tabs):** **Pending** (at the shop) and **Repaired** (already recovered).

**What you can do:**
- On **Pending**, select a device and press **Support / Receive** to record its return, entering the repair **value**.
- Export to Excel on both tabs.

**The tables:**
- **Pending:** ID · Serial Number · Model · Date Out · Destiny.
- **Repaired:** ID · Serial Number · Model · Date Out · Date In · Destiny · Value.

**Handy details:** on the **Repaired** tab you'll see the **Total Value** (sum of the cost of all recovered repairs).

---

<a id="distribution-invoices"></a>

### 6.4 Distribution Invoices

**What it's for:** breaking down an invoice to see **where each asset was assigned** (company, delegation, department, person and value).

![Distribution Invoices screen](images/25-distribution-invoices.png)
*Search by invoice number with a subtotals option.*

**How to use it:**
1. Type the **Bill Number** and press **Search (🔍)**.
2. Tick **Show subtotals** to see subtotals by department, delegation and company. *Ticking/unticking re-runs the search on its own.*

**The table:** Company · Delegation · Department · User · Serial Number · Model · Value.

**What you can do:** **Export to Excel** (appears when there are results).

**Handy details:** with subtotals on, **yellow** highlighted rows are interleaved with the cascading totals (department → delegation → company).

---

## 7. Organisation and users

<a id="delegations"></a>

### 7.1 Delegations

**What it's for:** managing the sites/offices, with their address and an **interactive map**.

![Delegations screen](images/20-delegations.png)
*Form and listing on the left; map of Spain with the pins on the right.*

**Fields, one by one:**
- **Code** — the delegation's code (key).
- **Delegation** — the site's name. **Required.**
- **Address** — postal address; this is what's used to **geolocate**.
- **Post Code** — postcode.
- **Town** — town/city.
- **Province** — province (dropdown from the master provinces table).
- **Notes** — observations.

**What you can do (and its limits):**
- **Save** — save/update; on saving, the app **tries to geolocate** the address automatically. **Limitation:** if the address is imprecise the pin may not be placed; use *Geolocate* in that case.
- **Clear** — clear.
- **Geolocate** — **manual** geolocation of an already-saved delegation.

**The table:** ID · Delegation · Address · Post Code · Town · Province.

**The map:**
- Centred on Spain. Each geolocated delegation appears as a **pin**.
- **Blue** = **active** delegation; **red** = **inactive**.
- Clicking a pin shows the name, address and state.

---

<a id="users"></a>

### 7.2 Users

**What it's for:** creating and administering the people who use OE Inventory, their **permissions** and their data **scope**.

![Users screen](images/15-users.png)
*User details, per-module permissions and scope by company/delegation/department.*

**How it's laid out:** the user's details (login, name, email, password, permissions) and, below, the **scope** in three blocks: **Companies**, **Delegations** and **Departments**.

**Fields:**
- **Login**, **Name**, **Email**.
- **Password** — normally shown masked. An initial password can only be set when the user is new and has no password, and provided **you have the "users" permission**.
- **Application Permits** — checkboxes to enable each module (active, reader, users, staff, devices, licenses, phones, mobile_lines, fiber_lines, allocations, incorporations, orders, delegation, access_cards, visitors_cards, access_keys, under_repair, facturas, printers…).

**What you can do:**
- **Save** — create the user (if the login doesn't exist) or update the existing one.
- **Clear** — clear the form.
- Tick the **companies, delegations and departments** that define their scope (they can have one, several or none of each).

**Handy details:**
- Only users with the **"users"** permission can set initial passwords and edit permissions.
- Scope works **cumulatively and optionally**: if you assign no company, the user sees them all; same with delegations and departments.

---

<a id="password-change"></a>

### 7.3 Change my password

**What it's for:** letting any user change **their own** password while inside the app.

![Change password](images/16-password-change.png)
*Change-password form.*

**Fields:** Old Password, New Password and Confirm Password.

**New-password rules:** at least 8 characters, can't be all numbers or too common, and both entries must match.

**Handy details:** after the change you don't have to sign in again; the app keeps your session open.

---

## 8. Monitoring (network, remote machines and rooms)

> Every screen in this section is **near-real-time monitoring** and is restricted to users with the **`net_overview`** permission (Omada also uses the `omada` permission). The data is computed by a **background process every 5 minutes** and cached, so the screen and the status bar respond instantly without waiting on the external APIs. The time of the last refresh is shown in the footer ("Updated").

<a id="net-overview"></a>

### 8.1 Net Overview (Zyxel Nebula)

**What it is for:** see at a glance the network status of **all managed sites** in the **Zyxel Nebula** cloud: switches, access points, firewalls, WAN links, connected clients and alarms.

**Layout:** on entry a **"Recovering information…" spinner** shows while the data loads over AJAX; then **one card per site** appears. Each card has a header (site name + OK/alerts state + **Topology** button) and several panels.

**Per-site panels:**
- **WAN** — two figures: **enabled** (configured/enabled WAN interfaces) and **operational** (with a live physical link).
- **Firewalls / Switches / Access Points** — total, **online** (green), **offline** (red) and, when present, an orange **"outdated"** counter (devices with out-of-date firmware).
- **Clients** — clients connected **right now**, split into **WiFi** and **wired**.
- **Alerts** — the site's incident count; when there are any, the card is **clickable** and opens a popup with the detail (offline and/or outdated-firmware devices).

**What you can do:**
- **Topology** (per-site button) — opens a **map** in a modal (Firewalls → Switches → Access Points) showing each device's status and the clients connected now; firewalls also show **CPU** and **Memory** (green <50 %, orange 50–80 %, red >80 %).
- **Click the Alerts panel** — see the list of devices with problems.

**Features and alarms:** a site's **alarms** are the sum of **offline devices** + **devices with outdated firmware** (counted separately: a device that is both offline and outdated counts as 2). A firewall over **80 % CPU or memory** also counts as an alarm. The total across all sites appears in the footer as **"Net Alerts"** (red) and refreshes every 5 minutes.

**Limitations (important):**
- The WAN **operational** figure usually shows **"—"**: the Nebula API **does not expose interface status** for the Zyxel firewalls (FLEX 700H / ATP), as confirmed by Zyxel support. Obtaining it would require querying the firewall over **SNMP** from the site network.
- The **topology map** links are shown **by tier**, not port-to-port (the API exposes neither the real map nor LLDP neighbour data).
- It requires the `NEBULA_*` credentials configured on the server; if missing, the screen shows a "not configured" notice.

> **Coming soon:** the **TP-Link Omada** controller data will be integrated into this same screen. Loading will happen in **two passes**: first the Nebula data (as now) and then the Omada data into the same form.

---

<a id="remote-machines"></a>

### 8.2 Remote Machines (AnyDesk)

**What it is for:** tell whether the **remote machines** (site mini-PCs) are **reachable**, based on the `oees_anydesk` table and the **AnyDesk REST API**.

**Layout:** **one card per machine** with a computer icon, **description**, its **AnyDesk code**, the **last connection** (`last_connection`) and a **green/red dot** depending on reachability.

**Features:** the background process scans the machines every 5 minutes; when a machine is reachable it **stamps the date/time** in `last_connection`. The number of **unreachable** machines is shown in the footer as **"Remote Machines Alerts"** (red, `net_overview` only); when there are none, it is hidden.

**Limitations:** it needs an active, **registered AnyDesk licence** and its credentials (`ANYDESK_API_LICENSE` / `ANYDESK_API_KEY`). While the API does not respond (e.g. an unregistered licence), the screen uses a **provisional mode**: it treats machines without a `last_connection` as "unreachable", so the design and the footer badge stay useful.

---

<a id="video-rooms"></a>

### 8.3 Video Rooms (Logitech Sync)

**What it is for:** monitor the state of the **videoconference rooms** fitted with **Logitech Rally Bar / Bar Mini** using Logitech's **Sync Cloud API**, and surface problematic bookings.

**Layout:** a **two-column** screen. On the **left (2/3)**, **one card per room**. On the **right (1/3)**, **three analysis tables**.

**Each room card:** name, **state** (🔴 *In meeting* / 🟡 *Occupied* / 🟢 *Free*), number of **occupants**, the scheduled meeting's **start–end time**, **title** and **organizer**, and the device's **model/firmware/status**, with a **green/red dot** (connected/disconnected). If the room is **occupied with no people** or **disconnected**, the card is highlighted in red with the reason.

**Right-hand tables:**
1. **Future-booking incidences** — future bookings whose **organizer is deactivated** ("User X, deactivated since dd-mm-yyyy, has N future bookings") or whose **email is not found** in the staff table ("The email … is not found in the users table").
2. **Under-used meetings (occupancy ≤ 50 %)** — meetings whose effective occupancy was ≤ 50 % of their duration: **Date · Start · End · Title · Organizer · % Occ.** (when the end time is unknown, the duration is shown instead).
3. **Organizers ranking — meetings not held (occ. ≤ 10 min)** — organizers with the most barely-held meetings: **Organizer · Total Duration · Total Occupied · Meetings**.

**Features and alarms:** the background process records each meeting in the `oees_meeting_room` table: `duration` is the **initial reserved length** (fixed) and `occupied` **adds 5 minutes** on each cycle while the room is occupied (hence values are multiples of 5). The number of rooms **occupied-but-empty or disconnected** appears in the footer as **"Video Rooms Alerts"** (red, `net_overview` only).

**Limitations:** it requires a **Logitech licence** and a **client certificate + key (mTLS)** on the server. Until they are configured the screen shows **sample data** with a **"Sample data"** notice (so the design can be worked on) and **writes nothing** to `oees_meeting_room`. Some meeting fields (organizer, title, start/end time) depend on the live API providing them.

---

## Appendix A: Glossary

- **Asset:** any item in the inventory (device, licence, phone, line, card, key, printer).
- **Stock:** assets not assigned to anyone.
- **Assign / Release:** hand an asset to a person / return it to stock.
- **Terminate:** end a person's contract and recover their equipment.
- **reader profile:** a read-only user.
- **Scope:** the set of companies/delegations/departments a user can see.
- **eSIM / M2M:** special mobile-line types (embedded SIM / machine-to-machine).
- **PENDING / LOST:** access-card states (pending / lost).

---

*OE Inventory — built to make managing the inventory simple, transparent and fast. Is something missing from this manual? Tell us and we'll improve it.*
