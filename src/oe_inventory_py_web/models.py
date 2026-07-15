#   This is an auto-generated Django model module.
#   You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
#   Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    # Django YA CREA automáticamente: id, username, password, email, etc.
    
    # Aquí pones los campos EXTRA que tenías en oees_users (ejemplos):
    reader = models.IntegerField(default = 1, verbose_name="reader")
    activo = models.IntegerField(default = 1, verbose_name="activo")
    users = models.IntegerField(default = 0, verbose_name="users")
    staff = models.IntegerField(default = 0, verbose_name="staff")
    devices = models.IntegerField(default = 0, verbose_name="devices")
    licenses = models.IntegerField(default = 0, verbose_name="licenses")
    phones = models.IntegerField(default=0, verbose_name="phones")
    mobile_lines = models.IntegerField(default=0, verbose_name="mobile_lines")
    fiber_lines = models.IntegerField(default=0, verbose_name="fiber_lines")
    allocations = models.IntegerField(default=0, verbose_name="allocations")
    incorporations = models.IntegerField(default=0, verbose_name="incorporations")
    incorporator = models.IntegerField(default=0, verbose_name="incorporator")
    orders = models.IntegerField(default=0, verbose_name="orders")
    delegation = models.IntegerField(default=0, verbose_name="delegation")
    delegations = models.CharField(max_length=100, null=True, blank=True, verbose_name="delegations")
    disponibility = models.IntegerField(default=0, verbose_name="disponobility")
    notes = models.TextField(verbose_name="notes")
    access_cards = models.IntegerField(default=0, verbose_name="access_cards")
    visitors_cards = models.IntegerField(default=0, verbose_name="visitors_cards")
    access_keys = models.IntegerField(default=0, verbose_name="access_keys")
    departments = models.CharField(max_length=100, null=True, blank=True, verbose_name="departments")
    under_repair = models.IntegerField(default=0, verbose_name="under_repair")
    companies = models.CharField(max_length=100, null=True, blank=True, verbose_name="companies")
    facturas = models.IntegerField(default=0, verbose_name="facturas")
    printers = models.IntegerField(default=0, verbose_name="printers")
    not_returned = models.IntegerField(default=0, verbose_name="not_returned")
    omada = models.IntegerField(default=0, verbose_name="omada")
    net_overview = models.IntegerField(default=0, verbose_name="net_overview")

class OeesAccessCards(models.Model):
    id_card = models.AutoField(primary_key=True)
    ac_max = models.CharField(max_length=8)
    fermax_mif = models.CharField(max_length=10)
    pin_card = models.CharField(max_length=4)
    id_staff = models.ForeignKey('OeesStaff', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_staff')
    state_card = models.IntegerField(db_column='state_card')
    obs = models.CharField(max_length=200)
    notes = models.TextField()

    def __str__(self):
        return f"Ac_Max: {self.ac_max} - Fermax_mif: {self.fermax_mif}"
 
    class Meta:
        managed = True
        db_table = 'oees_access_cards'


class OeesAccessCardsPins(models.Model):
    id_pin = models.AutoField(primary_key=True)
    pin = models.CharField(max_length=4)

    def __str__(self):
        return f"Id: {self.id_pin} - pin: {self.pin}"

    class Meta:
        managed = True
        db_table = 'oees_access_cards_pins'


class OeesAccessCardsStates(models.Model):
    id_state = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f"Id: {self.id_state} - Description: {self.description}"

    class Meta:
        managed = True
        db_table = 'oees_access_cards_states'


class OeesAccessCardsVisitors(models.Model):
    id_card = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ac_max = models.CharField(max_length=8)
    fermax_mif = models.CharField(max_length=10)
    pin_card = models.CharField(max_length=4)
    state_card = models.ForeignKey('OeesAccessCardsStates', on_delete=models.SET_NULL, blank=True, null=True, db_column='state_card')
    obs = models.CharField(max_length=200)
    notes = models.TextField()

    def __str__(self):
        return f"Id_Card: {self.id_card} - Ac_max: {self.ac_max}"        

    class Meta:
        managed = True
        db_table = 'oees_access_cards_visitors'


class OeesAccessCardsVisitorsNotes(models.Model):
    id_line = models.AutoField(primary_key=True)
    id_visitors_card = models.ForeignKey('OeesAccessCardsVisitors', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_visitors_card')
    notes = models.TextField()

    class Meta:
        managed = True
        db_table = 'oees_access_cards_visitors_notes'


class OeesAccessKeys(models.Model):
    id_key = models.AutoField(primary_key=True)
    id_company = models.ForeignKey('OeesCompanies', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_company')
    type = models.CharField(max_length=100)
    notes = models.TextField()
    id_staff = models.ForeignKey('OeesStaff', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_staff')
    insert_date = models.DateField()

    def __str__(self):
        return f"Id: {self.id_key} - Type: {self.type}"

    class Meta:
        managed = True
        db_table = 'oees_access_keys'


class OeesCompanies(models.Model):
    id_company = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Id: {self.id_company} - Company: {self.name}"

    class Meta:
        managed = True
        db_table = 'oees_companies'


class OeesProvinces(models.Model):
    id_province = models.AutoField(primary_key=True)
    province = models.CharField(max_length=50)

    def __str__(self):
        return f"Id: {self.id_province} - Province: {self.province}"

    class Meta:
        managed = True
        db_table = 'oees_provinces'


class OeesDelegations(models.Model):
    id_delegation = models.AutoField(primary_key=True)
    delegation = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    cpostal = models.CharField(max_length=10, blank=True, null=True)
    poblacion = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.ForeignKey('OeesProvinces', on_delete=models.SET_NULL, blank=True, null=True, db_column='provincia')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    activo = models.IntegerField(default=1)
    notes = models.TextField()

    def __str__(self):
        return f"Id: {self.id_delegation} - Delegation: {self.delegation}"


    class Meta:
        managed = True
        db_table = 'oees_delegations'


class OeesDevices(models.Model):
    id_device = models.BigAutoField(primary_key=True)
    serial_number = models.CharField(max_length=30)
    company = models.ForeignKey('OeesCompanies', on_delete=models.SET_NULL, blank=True, null=True, db_column='company')
    type = models.CharField(max_length=25)
    brand = models.CharField(max_length=25)
    model = models.CharField(max_length=50)
    screen_size = models.CharField(max_length=15, blank=True, null=True)
    hd = models.CharField(max_length=15, blank=True, null=True)
    memory = models.CharField(max_length=15, blank=True, null=True)
    imei = models.CharField(max_length=25, blank=True, null=True)
    pin_puk = models.CharField(max_length=50, blank=True, null=True)
    origin = models.CharField(max_length=25)
    insert_date = models.DateField()
    bill_number = models.CharField(max_length=25, blank=True, null=True)
    persone = models.ForeignKey('OeesStaff', on_delete=models.SET_NULL, blank=True, null=True, db_column='persone')
    obs = models.CharField(max_length=200, blank=True, null=True)
    value = models.FloatField()
    # Plain 0/1 flag ("has mobile SIM?"), NOT a reference to oees_mobile_lines.
    mobile_line = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Serial_number: {self.serial_number} - Type: {self.type}"


    class Meta:
        managed = True
        db_table = 'oees_devices'


class OeesDocs(models.Model):
    id_doc = models.AutoField(primary_key=True)
    id_staff = models.ForeignKey('OeesStaff', on_delete=models.SET_NULL, blank=True, null=True, db_column = 'id_staff')
    doc_name = models.TextField()
    notes = models.TextField()

    class Meta:
        managed = True
        db_table = 'oees_docs'


class OeesFiberLines(models.Model):
    id_fiber_line = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    id_delegation = models.ForeignKey('OeesDelegations', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_delegation')
    proveedor = models.CharField(max_length=100)
    orden = models.CharField(max_length=15)
    codigo_servicio = models.CharField(max_length=50)
    acceso = models.CharField(max_length=100)
    router = models.CharField(max_length=100)
    direccionamiento = models.CharField(max_length=100)
    wifi1 = models.CharField(max_length=100)
    wifi2 = models.CharField(max_length=100)
    estado = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_baja = models.DateField(blank=True, null=True)
    ip_fija = models.CharField(max_length=14, blank=True, null=True)
    fee = models.FloatField(default=0)
    notes = models.TextField()

    def __str__(self):
        return f"Id: {self.id_fiber_line} - Description: {self.description}"

    class Meta:
        managed = True
        db_table = 'oees_fiber_lines'


class OeesFiberLinesIncidences(models.Model):
    id_incidence = models.AutoField(primary_key=True)
    id_fiber_line = models.ForeignKey('OeesFiberLines', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_fiber_line')
    working_code = models.CharField(max_length=25)
    open_date = models.CharField(max_length=10, blank=True, null=True)
    open_description = models.TextField(blank=True, null=True)
    close_date = models.CharField(max_length=10, blank=True, null=True)
    close_description = models.TextField(blank=True, null=True)
    notes = models.TextField()

    def __str__(self):
        return f"Id: {self.id_incidence} - Code: {self.working_code}"

    class Meta:
        managed = True
        db_table = 'oees_fiber_lines_incidences'


class OeesIncorporations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=254, blank=True, null=True, db_column='personal_email')
    company = models.ForeignKey('OeesCompanies', on_delete=models.SET_NULL, blank=True, null=True, db_column='company')
    department = models.CharField(max_length=50)
    insert_date = models.DateField()
    direccion = models.TextField(blank=True, null=True)
    win = models.IntegerField(blank=True, null=True)
    mba = models.IntegerField(blank=True, null=True)
    mbp = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    screen = models.IntegerField(blank=True, null=True)
    mouse = models.IntegerField(blank=True, null=True)          # right-handed mouse
    left_mouse = models.IntegerField(blank=True, null=True)     # left-handed mouse
    keyboard = models.IntegerField(blank=True, null=True)
    sweatshirt_size = models.CharField(max_length=4, blank=True, null=True)
    cordedh = models.IntegerField(db_column='cordedH')  # Field name made lowercase.
    cordlessh = models.IntegerField(db_column='cordlessH')  # Field name made lowercase.
    usbchub = models.IntegerField(db_column='usbcHub')  # Field name made lowercase.
    pdf = models.IntegerField()
    acad = models.IntegerField()
    descartado = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    delegation = models.ForeignKey('OeesDelegations', on_delete=models.SET_NULL, blank=True, null=True, db_column='delegation')
    incorporated = models.IntegerField()
    send = models.IntegerField()
    receive = models.IntegerField()
    # 0 = not sent, 1 = preferences PDF emailed, 2 = returned PDF processed.
    email_processed = models.IntegerField(default=0)

    def __str__(self):
        return f"Name: {self.name} - Department: {self.department}" 

    class Meta:
        managed = True
        db_table = 'oees_incorporations'


class OeesLicenses(models.Model):
    id_license = models.AutoField(primary_key=True)
    serial_number = models.CharField(max_length=50)
    origin = models.CharField(max_length=50, blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    company = models.ForeignKey('OeesCompanies', on_delete=models.SET_NULL, blank=True, null=True, db_column='company')
    type = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    value = models.FloatField()
    persone = models.ForeignKey('OeesStaff', on_delete=models.SET_NULL, blank=True, null=True, db_column='persone')
    obs = models.TextField()
    bill_number = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return f"Serial_Number: {self.serial_number} - Type: {self.type}"

    class Meta:
        managed = True
        db_table = 'oees_licenses'


class OeesLogs(models.Model):
    id_log = models.AutoField(primary_key=True)
    user = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    date = models.DateField()
    log = models.TextField()

    class Meta:
        managed = True
        db_table = 'oees_logs'


class OeesMobileLines(models.Model):
    id_mobile_line = models.AutoField(primary_key=True)
    number = models.CharField(max_length=50)
    origin = models.CharField(max_length=50, blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    company = models.ForeignKey('OeesCompanies', on_delete=models.SET_NULL, blank=True, null=True, db_column='company')
    notes = models.TextField(blank=True, null=True)
    mobile = models.ForeignKey('OeesMobilePhones', on_delete=models.SET_NULL, blank=True, null=True, db_column='mobile')
    imei = models.CharField(max_length=30)
    pin = models.CharField(max_length=4)
    puk = models.CharField(max_length=10)
    pin2 = models.CharField(max_length=4)
    puk2 = models.CharField(max_length=10)
    extension = models.CharField(max_length=10)
    esim = models.IntegerField()
    m2m = models.IntegerField(db_column='M2M')  # Field name made lowercase.
    fecha_baja = models.DateField(blank=True, null=True)
    obs = models.TextField()
    fee = models.FloatField(default=0)
    desc_tarif = models.CharField(max_length=255, blank=True, null=True, db_column='DescTarif')

    def __str__(self):
        return f"Number: {self.number} - Origin: {self.origin}"

    class Meta:
        managed = True
        db_table = 'oees_mobile_lines'


class OeesMobilePhones(models.Model):
    id_mobile_phone = models.AutoField(primary_key=True)
    serial_number = models.CharField(max_length=50)
    origin = models.CharField(max_length=50, blank=True, null=True)
    insert_date = models.DateField(blank=True, null=True)
    company = models.ForeignKey('OeesCompanies', on_delete=models.SET_NULL, blank=True, null=True, db_column='company')
    type = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    value = models.FloatField()
    persone = models.ForeignKey('OeesStaff', on_delete=models.SET_NULL, blank=True, null=True, db_column='persone')
    id_line = models.ForeignKey('OeesMobileLines', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_line')
    imei = models.CharField(max_length=50, blank=True, null=True)
    pin_puk = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=25, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    bill_number = models.CharField(max_length=25, blank=True, null=True)
    obs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Serial_Number: {self.serial_number} - Model: {self.model}"

    class Meta:
        managed = True
        db_table = 'oees_mobile_phones'


class OeesOrders(models.Model):
    id_order = models.AutoField(primary_key=True)
    article = models.TextField()
    uds = models.IntegerField()
    insert_date = models.DateField()
    notes = models.TextField()
    tramitado = models.IntegerField()
    cancelado = models.IntegerField()
    recibido = models.IntegerField()

    def __str__(self):
        return f"Id: {self.id_order} - Article: {self.article}"

    class Meta:
        managed = True
        db_table = 'oees_orders'


class OeesParameters(models.Model):
    id_param = models.AutoField(primary_key=True)
    parameter = models.TextField()
    value = models.TextField()

    def __str__(self):
        return f"Parameter: {self.parameter} - Value: {self.value}"

    class Meta:
        managed = True
        db_table = 'oees_parameters'


class OeesPrinters(models.Model):
    id_printer = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    proveedor = models.CharField(max_length=50, blank=True, null=True)
    id_delegation = models.ForeignKey('OeesDelegations', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_delegation')
    mps = models.CharField(max_length=15, blank=True, null=True)
    ip = models.CharField(max_length=15)
    serial_number = models.CharField(max_length=50)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_baja = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.CharField(max_length=25, blank=True, null=True)
    password = models.CharField(max_length=25, blank=True, null=True)
    fee = models.FloatField(blank=True, null=True)
    # Contract number for renting / pay-per-use printers (NULL when not applicable).
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    # Per-page printing costs (default 0).
    bw_page_cost = models.FloatField(default=0)
    color_page_cost = models.FloatField(default=0)

    def __str__(self):
        return f"Serial_Number: {self.serial_number} - Description: {self.description}"

    class Meta:
        managed = True
        db_table = 'oees_printers'


class OeesReturns(models.Model):
    id_return = models.AutoField(primary_key=True)
    id_line = models.ForeignKey('OeesMobileLines', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_line')
    id_staff = models.ForeignKey('OeesStaff', on_delete=models.SET_NULL, blank=True, null=True, db_column='id_staff')
    serial_number = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    value = models.FloatField()
    state = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'oees_returns'


class OeesStaff(models.Model):
    id_staff = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=25, blank=True, null=True)
    company = models.ForeignKey('OeesCompanies', on_delete=models.SET_NULL, blank=True, null=True, db_column='company')
    state = models.IntegerField(blank=True, null=True)
    delegation = models.ForeignKey('OeesDelegations', on_delete=models.SET_NULL, blank=True, null=True, db_column='delegation')
    obs = models.TextField(blank=True, null=True)
    notes = models.TextField()
    persona_fisica = models.IntegerField()
    email = models.CharField(max_length=100, blank=True, null=True)
    fecha_incorporacion = models.CharField(max_length=10, blank=True, null=True)
    fecha_baja = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Id: {self.id_staff} - Name: {self.name}"

    class Meta:
        managed = True
        db_table = 'oees_staff'


class OeesUnderRepair(models.Model):
    id_under_repair = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=1)
    serial_number = models.CharField(max_length=40)
    date_out = models.DateField()
    date_in = models.DateField(blank=True, null=True)
    destiny = models.CharField(max_length=200)
    notes = models.TextField()
    value = models.FloatField()

    def __str__(self):
        return f"Id: {self.id_under_repair} - Serial Number: {self.serial_number}"

    class Meta:
        managed = True
        db_table = 'oees_under_repair'


class OeesMeetingRoom(models.Model):
    # Meeting-usage tracking, fed every 5 minutes by the background status check.
    id = models.AutoField(primary_key=True)
    meet_id = models.CharField(max_length=100, unique=True)   # Logitech meeting id
    description = models.CharField(max_length=255, blank=True, null=True)  # meeting title
    org_email = models.CharField(max_length=100, blank=True, null=True)    # organizer email
    duration = models.IntegerField(default=0)   # minutes, +5 each cycle while occupied
    occupied = models.IntegerField(default=0)   # effective occupied minutes (reserved)
    start_time = models.DateTimeField(blank=True, null=True)  # room reservation start
    end_time = models.DateTimeField(blank=True, null=True)    # room reservation end

    def __str__(self):
        return f"Meeting {self.meet_id} - {self.duration} min"

    class Meta:
        managed = True
        db_table = 'oees_meeting_room'

