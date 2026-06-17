from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import (
    OeesAccessCards, OeesAccessCardsStates, OeesAccessCardsVisitors, OeesAccessKeys,
    OeesCompanies, OeesDelegations, OeesDevices, OeesFiberLines, OeesFiberLinesIncidences,
    OeesIncorporations, OeesLicenses, OeesMobileLines, OeesMobilePhones, OeesOrders,
    OeesPrinters, OeesStaff, OeesUnderRepair,
)


class PublicPagesTests(TestCase):
    """Smoke tests that don't depend on pre-existing data."""

    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/login.html')

    def test_home_requires_login(self):
        response = self.client.get(reverse('mdi_home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_devices_requires_login(self):
        response = self.client.get(reverse('frm_devices'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)


class AuthenticatedFlowTests(TestCase):
    """Tests covering an authenticated session."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='tester', password='pass12345', devices=1
        )

    def test_home_renders_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('mdi_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/base_mdi.html')

    def test_api_get_user_never_returns_password_hash(self):
        """Security regression: the password hash must never reach the client."""
        response = self.client.get(reverse('api_get_user'), {'login': 'tester'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['password'], '********')
        self.assertNotIn(self.user.password, response.content.decode())


class StaffScreenTests(TestCase):
    """Smoke tests for the Staff screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='ituser', password='pass12345', staff=1)
        self.staff = OeesStaff.objects.create(
            name='Jane Tester', persona_fisica=1, notes='', state=1, department='IT'
        )

    def test_staff_requires_login(self):
        response = self.client.get(reverse('frm_staff'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_staff_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_staff'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmStaff.html')

    def test_api_get_staff_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_staff'), {'id': self.staff.id_staff})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['name'], 'Jane Tester')

    def test_api_get_staff_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_staff'), {'id': 999999})
        self.assertFalse(response.json()['exists'])

    def test_staff_report_returns_pdf(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('staff_report'), {'staff': self.staff.id_staff})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_release_generates_unassign_doc(self):
        import tempfile
        from datetime import date
        from django.test import override_settings
        from oe_inventory_py_web.models import OeesDevices, OeesDocs
        User = get_user_model()
        admin = User.objects.create_user(username='rel_u', password='pass12345', staff=1, reader=0)
        dev = OeesDevices.objects.create(
            serial_number='DEV-R1', type='LAPTOP', brand='Dell', model='X',
            origin='New', insert_date=date(2026, 1, 1), value=0.0, persone=self.staff)
        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp):
            self.client.force_login(admin)
            resp = self.client.post(reverse('frm_staff'), {
                'action': 'release', 'code': str(self.staff.id_staff),
                'item_id': f'D{dev.id_device}', 'serial': 'DEV-R1', 'name': self.staff.name,
            })
            self.assertEqual(resp.status_code, 302)
            dev.refresh_from_db()
            self.assertIsNone(dev.persone_id)              # item unassigned
            self.assertTrue(OeesDocs.objects.filter(       # Unassign document generated
                id_staff_id=self.staff.id_staff, doc_name__startswith='Unassign-').exists())

    def test_terminate_returns_items_and_generates_document(self):
        import tempfile
        from datetime import date
        from django.test import override_settings
        from oe_inventory_py_web.models import OeesDevices, OeesDocs
        User = get_user_model()
        admin = User.objects.create_user(username='term_u', password='pass12345', staff=1, reader=0)
        dev = OeesDevices.objects.create(
            serial_number='DEV-T1', type='LAPTOP', brand='Dell', model='X',
            origin='New', insert_date=date(2026, 1, 1), value=0.0, persone=self.staff)

        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp):
            self.client.force_login(admin)
            resp = self.client.post(reverse('frm_staff'), {
                'action': 'terminate', 'code': str(self.staff.id_staff),
                'returned_items': f'D{dev.id_device}',
            })
            self.assertEqual(resp.status_code, 302)

            dev.refresh_from_db()
            self.assertIsNone(dev.persone_id)              # item freed back to stock
            self.staff.refresh_from_db()
            self.assertEqual(self.staff.state, 0)          # contract terminated
            self.assertTrue(self.staff.fecha_baja)
            self.assertTrue(OeesDocs.objects.filter(       # Terminate document saved
                id_staff_id=self.staff.id_staff, doc_name='Terminate').exists())

    def test_scope_staff_applies_optional_and_filters(self):
        # The three scopes are optional and combined with AND (each one narrows
        # further only when set). A user with no scope sees everyone; with a
        # company AND a department set, only staff matching BOTH are shown.
        from .views import scope_staff_queryset
        from .models import OeesCompanies

        comp = OeesCompanies.objects.create(name='ACME')
        # self.staff = Jane, department='IT', no company.
        OeesStaff.objects.create(name='MatchBoth', persona_fisica=1, notes='', state=1,
                                 department='IT', company_id=comp.id_company)
        OeesStaff.objects.create(name='OnlyCompany', persona_fisica=1, notes='', state=1,
                                 department='SALES', company_id=comp.id_company)
        User = get_user_model()

        # No scope -> sees everyone.
        no_scope = User.objects.create_user(username='no_scope', password='pass12345')
        self.assertEqual(scope_staff_queryset(no_scope, OeesStaff.objects.all()).count(), 3)

        # Company AND department set -> only staff matching both.
        scoped = User.objects.create_user(
            username='scoped_user', password='pass12345',
            departments='IT', companies=str(comp.id_company),
        )
        names = set(
            scope_staff_queryset(scoped, OeesStaff.objects.all()).values_list('name', flat=True)
        )
        self.assertEqual(names, {'MatchBoth'})  # Jane (no company) and OnlyCompany (SALES) excluded

    def test_scope_staff_without_company_uses_other_dimensions(self):
        # A user may have NO company assigned but still have delegations and/or
        # departments: the missing dimension simply doesn't filter, the others do.
        from .views import scope_staff_queryset
        from .models import OeesDelegations

        deleg = OeesDelegations.objects.create(delegation='MADRID', notes='')
        OeesStaff.objects.create(name='DelegDept', persona_fisica=1, notes='', state=1,
                                 department='IT', delegation_id=deleg.id_delegation)
        OeesStaff.objects.create(name='SameDelegOtherDept', persona_fisica=1, notes='', state=1,
                                 department='HR', delegation_id=deleg.id_delegation)
        User = get_user_model()
        u = User.objects.create_user(
            username='no_company_user', password='pass12345',
            delegations=str(deleg.id_delegation), departments='IT',  # no companies
        )
        names = set(
            scope_staff_queryset(u, OeesStaff.objects.all()).values_list('name', flat=True)
        )
        self.assertEqual(names, {'DelegDept'})  # delegation AND department; company not required


class LicensesScreenTests(TestCase):
    """Smoke tests for the Licenses screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='lic_user', password='pass12345', licenses=1, reader=0)
        self.lic = OeesLicenses.objects.create(serial_number='LIC-1', type='Office', value=99.0, obs='')

    def test_licenses_requires_login(self):
        response = self.client.get(reverse('frm_licenses'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_licenses_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_licenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmLicenses.html')

    def test_license_summary_by_type(self):
        from oe_inventory_py_web.models import OeesStaff
        expired = OeesStaff.objects.create(name='LICENCIAS CADUCADAS', persona_fisica=1, notes='', state=1)
        # self.lic = LIC-1 type 'Office' (unassigned). Add one Office assigned to
        # the expired person, and one of another type.
        OeesLicenses.objects.create(serial_number='LIC-2', type='Office', value=0, obs='', persone=expired)
        OeesLicenses.objects.create(serial_number='LIC-3', type='Visio', value=0, obs='')

        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_licenses'))
        summary = {s['type']: s for s in response.context['license_summary']}

        self.assertEqual(summary['Office']['purchased'], 2)
        self.assertEqual(summary['Office']['expired'], 1)
        self.assertEqual(summary['Office']['in_use'], 1)
        self.assertEqual(summary['Visio']['purchased'], 1)
        self.assertEqual(summary['Visio']['expired'], 0)
        self.assertEqual(summary['Visio']['in_use'], 1)

    def test_api_get_license_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_license'), {'serial_number': 'LIC-1'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['type'], 'Office')

    def test_api_get_license_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_license'), {'serial_number': 'NOPE'})
        self.assertFalse(response.json()['exists'])

    def test_save_creates_license(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_licenses'), {
            'action': 'save', 'serial_number': 'LIC-NEW', 'type': 'CAD',
            'origin': 'Vendor', 'value': '150.00', 'obs': 'test', 'insert_date': '2026-01-10',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesLicenses.objects.filter(serial_number='LIC-NEW').exists())


class PhonesScreenTests(TestCase):
    """Smoke tests for the Mobile Phones screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='ph_user', password='pass12345', phones=1, reader=0)
        self.phone = OeesMobilePhones.objects.create(serial_number='PH-1', type='', value=50.0, brand='Apple')

    def test_phones_requires_login(self):
        response = self.client.get(reverse('frm_phones'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_phones_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_phones'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmPhones.html')

    def test_phone_release_generates_unassign_doc(self):
        import tempfile
        from django.test import override_settings
        from oe_inventory_py_web.models import OeesStaff, OeesDocs
        owner = OeesStaff.objects.create(name='Phone Owner', persona_fisica=1, notes='', state=1)
        self.phone.persone = owner
        self.phone.save(update_fields=['persone'])
        self.client.force_login(self.user)
        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp):
            resp = self.client.post(reverse('frm_phones'), {
                'action': 'release', 'serial_number': 'PH-1', 'person': 'Phone Owner',
            })
            self.assertEqual(resp.status_code, 302)
            self.phone.refresh_from_db()
            self.assertIsNone(self.phone.persone_id)        # phone unassigned
            self.assertTrue(OeesDocs.objects.filter(        # Unassign document generated
                id_staff_id=owner.id_staff, doc_name__startswith='Unassign-').exists())

    def test_api_get_phone_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_phone'), {'serial_number': 'PH-1'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['brand'], 'Apple')

    def test_api_get_phone_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_phone'), {'serial_number': 'NOPE'})
        self.assertFalse(response.json()['exists'])

    def test_save_creates_phone(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_phones'), {
            'action': 'save', 'serial_number': 'PH-NEW', 'brand': 'Samsung',
            'model': 'S24', 'origin': 'Vendor', 'value': '300.00', 'imei': '123', 'insert_date': '2026-02-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesMobilePhones.objects.filter(serial_number='PH-NEW').exists())

    def test_support_creates_under_repair(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_phones'), {'action': 'support', 'serial_number': 'PH-1'})
        self.assertEqual(response.status_code, 302)
        from .models import OeesUnderRepair
        self.assertTrue(OeesUnderRepair.objects.filter(serial_number='PH-1', type='M', date_in__isnull=True).exists())


class FiberScreenTests(TestCase):
    """Smoke tests for the Fiber Lines screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='fb_user', password='pass12345', fiber_lines=1, reader=0)
        self.fiber = OeesFiberLines.objects.create(
            description='Fiber A', proveedor='ISP', orden='O1', codigo_servicio='SC1',
            acceso='acc', router='rt', direccionamiento='addr', wifi1='w1', wifi2='w2',
            estado=1, fecha_inicio=date(2026, 1, 1), notes='',
        )

    def test_fiber_requires_login(self):
        response = self.client.get(reverse('frm_fiber'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_fiber_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_fiber'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmFiberLines.html')

    def test_api_get_fiber_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_fiber'), {'id': self.fiber.id_fiber_line})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['description'], 'Fiber A')

    def test_api_get_fiber_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_fiber'), {'id': 999999})
        self.assertFalse(response.json()['exists'])

    def test_save_creates_fiber(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_fiber'), {
            'action': 'save', 'description': 'New Fiber', 'provider': 'ISP2', 'order': 'O2',
            'service_code': 'SC2', 'access': 'a', 'router': 'r', 'addressing': 'd',
            'wifi1': '', 'wifi2': '', 'estado': '1', 'start_date': '2026-03-01', 'ip_fixed': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesFiberLines.objects.filter(description='New Fiber').exists())

    def test_save_incidence(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_fiber'), {
            'action': 'save_incidence', 'code': str(self.fiber.id_fiber_line), 'working_code': 'WC1',
            'open_date': '2026-02-01', 'open_description': 'opened',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesFiberLinesIncidences.objects.filter(
            id_fiber_line_id=self.fiber.id_fiber_line, working_code='WC1').exists())


class PrintersScreenTests(TestCase):
    """Smoke tests for the Printers screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='pr_user', password='pass12345', printers=1, reader=0)
        self.printer = OeesPrinters.objects.create(serial_number='PR-1', description='HP LaserJet', ip='10.0.0.5')

    def test_printers_requires_login(self):
        response = self.client.get(reverse('frm_printers'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_printers_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_printers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmPrinters.html')

    def test_api_get_printer_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_printer'), {'serial_number': 'PR-1'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['description'], 'HP LaserJet')

    def test_api_get_printer_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_printer'), {'serial_number': 'NOPE'})
        self.assertFalse(response.json()['exists'])

    def test_save_creates_printer(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_printers'), {
            'action': 'save', 'serial_number': 'PR-NEW', 'description': 'Canon',
            'provider': 'Vendor', 'ip': '10.0.0.9', 'start_date': '2026-04-01', 'fee': '12.50',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesPrinters.objects.filter(serial_number='PR-NEW').exists())

    def test_save_persists_contract_and_page_costs(self):
        self.client.force_login(self.user)
        self.client.post(reverse('frm_printers'), {
            'action': 'save', 'serial_number': 'PR-CTR', 'description': 'Xerox',
            'ip': '10.0.0.10', 'start_date': '2026-04-01',
            'contract_number': 'RENT-2026-77', 'bw_page_cost': '0.012', 'color_page_cost': '0.085',
        })
        pr = OeesPrinters.objects.get(serial_number='PR-CTR')
        self.assertEqual(pr.contract_number, 'RENT-2026-77')
        self.assertEqual(pr.bw_page_cost, 0.012)
        self.assertEqual(pr.color_page_cost, 0.085)

    def test_page_costs_default_to_zero_and_contract_null_when_blank(self):
        self.client.force_login(self.user)
        self.client.post(reverse('frm_printers'), {
            'action': 'save', 'serial_number': 'PR-BLANK', 'description': 'Brother',
            'ip': '10.0.0.11', 'start_date': '2026-04-01',
        })
        pr = OeesPrinters.objects.get(serial_number='PR-BLANK')
        self.assertIsNone(pr.contract_number)
        self.assertEqual(pr.bw_page_cost, 0)
        self.assertEqual(pr.color_page_cost, 0)

    def test_api_get_printer_returns_new_fields(self):
        self.printer.contract_number = 'C-1'
        self.printer.bw_page_cost = 0.02
        self.printer.color_page_cost = 0.1
        self.printer.save()
        self.client.force_login(self.user)
        data = self.client.get(reverse('api_get_printer'), {'serial_number': 'PR-1'}).json()['data']
        self.assertEqual(data['contract_number'], 'C-1')
        self.assertEqual(data['bw_page_cost'], '0.02')
        self.assertEqual(data['color_page_cost'], '0.1')

    def test_list_shows_total_monthly_fee(self):
        OeesPrinters.objects.create(serial_number='PR-F1', description='A', ip='1', fee=10.0)
        OeesPrinters.objects.create(serial_number='PR-F2', description='B', ip='2', fee=12.5)
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_printers'))
        self.assertEqual(response.context['fee_total'], 22.5)


class AllocationsScreenTests(TestCase):
    """Smoke tests for the Allocations screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='al_user', password='pass12345', allocations=1, reader=0)
        self.staff = OeesStaff.objects.create(name='Joe Worker', persona_fisica=1, notes='', state=1)
        self.device = OeesDevices.objects.create(
            serial_number='DV-1', type='Laptop', brand='Dell', model='X',
            origin='New', insert_date=date(2026, 1, 1), value=0.0,
        )
        self.phone = OeesMobilePhones.objects.create(serial_number='PH-A', type='', value=0.0)

    def test_allocations_requires_login(self):
        response = self.client.get(reverse('frm_allocations'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_allocations_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_allocations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmAllocations.html')

    def test_search_available_phones(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_allocations_search'), {'kind': 'phones'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('PH-A', response.json()['serials'])

    def test_assign_device_to_staff(self):
        from oe_inventory_py_web.models import OeesDocs
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_allocations'), {
            'action': 'assign_device', 'staff': str(self.staff.id_staff), 'device_serial': 'DV-1',
        })
        self.assertEqual(response.status_code, 302)
        self.device.refresh_from_db()
        self.assertEqual(self.device.persone_id, self.staff.id_staff)
        # Assignment alone no longer generates a document (grouped via the button).
        self.assertFalse(OeesDocs.objects.filter(id_staff_id=self.staff.id_staff).exists())

    def test_generate_allocation_doc_for_physical(self):
        import tempfile
        from django.test import override_settings
        from oe_inventory_py_web.models import OeesDocs
        self.client.force_login(self.user)
        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp):
            # Assign a couple of items first (no doc yet), then generate one document.
            self.client.post(reverse('frm_allocations'), {
                'action': 'assign_device', 'staff': str(self.staff.id_staff), 'device_serial': 'DV-1',
            })
            self.client.post(reverse('frm_allocations'), {
                'action': 'assign_phone', 'staff': str(self.staff.id_staff), 'phone_serial': 'PH-A',
            })
            self.assertFalse(OeesDocs.objects.filter(id_staff_id=self.staff.id_staff).exists())

            resp = self.client.post(reverse('frm_allocations'), {
                'action': 'generate_doc', 'staff': str(self.staff.id_staff),
            })
            self.assertEqual(resp.status_code, 302)
            docs = OeesDocs.objects.filter(id_staff_id=self.staff.id_staff, doc_name__startswith='Allocation-')
            self.assertEqual(docs.count(), 1)   # a single grouped document

    def test_generate_doc_skipped_for_non_physical(self):
        from oe_inventory_py_web.models import OeesDocs
        company = OeesStaff.objects.create(name='ACME SL', persona_fisica=0, notes='', state=1)
        self.client.force_login(self.user)
        resp = self.client.post(reverse('frm_allocations'), {
            'action': 'generate_doc', 'staff': str(company.id_staff),
        })
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(OeesDocs.objects.filter(id_staff_id=company.id_staff).exists())

    def test_auto_doc_on_leave_generates_pending(self):
        import tempfile
        from django.test import override_settings
        from oe_inventory_py_web.models import OeesDocs
        self.client.force_login(self.user)
        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp):
            # Assign (marks pending in session), then leave without generating.
            self.client.post(reverse('frm_allocations'), {
                'action': 'assign_device', 'staff': str(self.staff.id_staff), 'device_serial': 'DV-1',
            })
            self.assertFalse(OeesDocs.objects.filter(id_staff_id=self.staff.id_staff).exists())

            resp = self.client.post(reverse('frm_allocations'), {'action': 'auto_doc'})
            self.assertEqual(resp.status_code, 204)
            self.assertEqual(OeesDocs.objects.filter(
                id_staff_id=self.staff.id_staff, doc_name__startswith='Allocation-').count(), 1)

            # A second auto_doc (no pending left) does nothing.
            self.client.post(reverse('frm_allocations'), {'action': 'auto_doc'})
            self.assertEqual(OeesDocs.objects.filter(id_staff_id=self.staff.id_staff).count(), 1)

    def test_auto_doc_generates_one_document_per_pending_person(self):
        import tempfile
        from django.test import override_settings
        from oe_inventory_py_web.models import OeesDocs
        other = OeesStaff.objects.create(name='Ann Other', persona_fisica=1, notes='', state=1)
        self.client.force_login(self.user)
        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp):
            # Assign to person A, then switch and assign to person B (no doc yet).
            self.client.post(reverse('frm_allocations'), {
                'action': 'assign_device', 'staff': str(self.staff.id_staff), 'device_serial': 'DV-1',
            })
            self.client.post(reverse('frm_allocations'), {
                'action': 'assign_phone', 'staff': str(other.id_staff), 'phone_serial': 'PH-A',
            })
            # On leave, ONE document is generated per pending person.
            resp = self.client.post(reverse('frm_allocations'), {'action': 'auto_doc'})
            self.assertEqual(resp.status_code, 204)
            self.assertEqual(OeesDocs.objects.filter(
                id_staff_id=self.staff.id_staff, doc_name__startswith='Allocation-').count(), 1)
            self.assertEqual(OeesDocs.objects.filter(
                id_staff_id=other.id_staff, doc_name__startswith='Allocation-').count(), 1)


class IncorporationsScreenTests(TestCase):
    """Smoke tests for the Incorporations screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='inc_user', password='pass12345', incorporations=1, reader=0)
        self.company = OeesCompanies.objects.create(name='Acme')
        self.deleg = OeesDelegations.objects.create(delegation='HQ', notes='')
        self.inc = OeesIncorporations.objects.create(
            name='New Hire', department='IT', insert_date=date(2026, 1, 1),
            company_id=self.company.id_company, delegation_id=self.deleg.id_delegation,
            cordedh=0, cordlessh=0, usbchub=0, pdf=0, acad=0,
            incorporated=0, send=0, receive=0, descartado=0,
        )

    def test_incorporations_requires_login(self):
        response = self.client.get(reverse('frm_incorporations'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_incorporations_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_incorporations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmIncorporations.html')

    def test_api_get_incorporation_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_incorporation'), {'id': self.inc.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['name'], 'New Hire')

    def test_api_get_incorporation_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_incorporation'), {'id': 999999})
        self.assertFalse(response.json()['exists'])

    def test_pending_ordered_by_date_descending(self):
        # self.inc is dated 2026-01-01; add an older and a newer one.
        common = dict(
            department='IT', company_id=self.company.id_company,
            delegation_id=self.deleg.id_delegation, cordedh=0, cordlessh=0,
            usbchub=0, pdf=0, acad=0, incorporated=0, send=0, receive=0, descartado=0)
        OeesIncorporations.objects.create(name='Older', insert_date=date(2025, 6, 1), **common)
        OeesIncorporations.objects.create(name='Newer', insert_date=date(2026, 12, 1), **common)
        self.client.force_login(self.user)
        rows = self.client.get(reverse('frm_incorporations')).context['pending_rows']
        dates = [r['date'] for r in rows]
        self.assertEqual(dates, sorted(dates, reverse=True))   # newest date first
        self.assertEqual(rows[0]['name'], 'Newer')

    def test_save_creates_incorporation(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_incorporations'), {
            'action': 'save', 'name': 'Bob New', 'company': str(self.company.id_company),
            'department': 'IT', 'delegation': str(self.deleg.id_delegation),
            'insert_date': '2026-05-01', 'laptop': 'win', 'phone': '1',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesIncorporations.objects.filter(name='Bob New', win=1, phone=1).exists())

    def test_complete_migrates_to_staff(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_incorporations'), {
            'action': 'complete', 'code': str(self.inc.id),
        })
        self.assertEqual(response.status_code, 302)
        self.inc.refresh_from_db()
        self.assertEqual(self.inc.incorporated, 1)
        self.assertTrue(OeesStaff.objects.filter(name='New Hire').exists())


class OrdersScreenTests(TestCase):
    """Smoke tests for the Orders screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='or_user', password='pass12345', orders=1, reader=0)
        self.order = OeesOrders.objects.create(
            article='Cables', uds=10, insert_date=date(2026, 1, 1), notes='',
            tramitado=0, cancelado=0, recibido=0,
        )

    def test_orders_requires_login(self):
        response = self.client.get(reverse('frm_orders'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_orders_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmOrders.html')

    def test_api_get_order_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_order'), {'id': self.order.id_order})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['article'], 'Cables')

    def test_api_get_order_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_order'), {'id': 999999})
        self.assertFalse(response.json()['exists'])

    def test_save_creates_order(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_orders'), {
            'action': 'save', 'article': 'Mice', 'uds': '5', 'insert_date': '2026-06-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesOrders.objects.filter(article='Mice', uds=5).exists())

    def test_process_order(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_orders'), {'action': 'process', 'code': str(self.order.id_order)})
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.tramitado, 1)


class MobileLinesScreenTests(TestCase):
    """Smoke tests for the Mobile Lines screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='ml_user', password='pass12345', mobile_lines=1, reader=0)
        self.line = OeesMobileLines.objects.create(
            number='600100200', imei='', pin='', puk='', pin2='', puk2='',
            extension='', esim=0, m2m=0, obs='', origin='Vodafone',
        )

    def test_mobile_lines_requires_login(self):
        response = self.client.get(reverse('frm_mobile_lines'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_mobile_lines_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_mobile_lines'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmMobileLines.html')

    def test_api_get_line_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_line'), {'number': '600100200'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['origin'], 'Vodafone')

    def test_api_get_line_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_line'), {'number': '000'})
        self.assertFalse(response.json()['exists'])

    def test_save_creates_line(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_mobile_lines'), {
            'action': 'save', 'number': '600999888', 'origin': 'Orange', 'pin': '1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesMobileLines.objects.filter(number='600999888').exists())

    def test_cancel_sets_baja(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_mobile_lines'), {'action': 'cancel', 'number': '600100200'})
        self.assertEqual(response.status_code, 302)
        self.line.refresh_from_db()
        self.assertIsNotNone(self.line.fecha_baja)


class AvailabilityScreenTests(TestCase):
    """Smoke tests for the Availability screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='av_user', password='pass12345', disponibility=1)
        OeesDevices.objects.create(
            serial_number='AV-1', type='LAPTOP WIN', brand='Dell', model='X',
            origin='New', insert_date=date(2026, 1, 1), value=0.0,
        )

    def test_availability_requires_login(self):
        response = self.client.get(reverse('frm_availability'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_availability_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_availability'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmAvailability.html')

    def test_availability_excel_export(self):
        # Only non-reader profiles can download the Excel export.
        self.user.reader = 0
        self.user.save(update_fields=['reader'])
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_availability'), {'export': 'excel'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    def test_availability_excel_export_blocked_for_reader(self):
        # Reader profiles (reader=1) cannot download Excel exports; the
        # middleware redirects them back to the screen instead.
        self.user.reader = 1
        self.user.save(update_fields=['reader'])
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_availability'), {'export': 'excel'})
        self.assertEqual(response.status_code, 302)


class UnderRepairScreenTests(TestCase):
    """Smoke tests for the Under Repair screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='ur_user', password='pass12345', under_repair=1, reader=0)
        OeesDevices.objects.create(
            serial_number='UR-1', type='Laptop', brand='Dell', model='X',
            origin='New', insert_date=date(2026, 1, 1), value=0.0,
        )
        self.repair = OeesUnderRepair.objects.create(
            type='D', serial_number='UR-1', date_out=date(2026, 1, 2),
            destiny='Tech Service', notes='', value=0.0,
        )

    def test_under_repair_requires_login(self):
        response = self.client.get(reverse('frm_under_repair'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_under_repair_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_under_repair'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmUnderRepair.html')

    def test_receive_sets_date_in(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_under_repair'), {
            'action': 'receive', 'id': str(self.repair.id_under_repair), 'value': '12,50',
        })
        self.assertEqual(response.status_code, 302)
        self.repair.refresh_from_db()
        self.assertIsNotNone(self.repair.date_in)
        self.assertEqual(self.repair.value, 12.5)


class DistInvoicesScreenTests(TestCase):
    """Smoke tests for the Distribution Invoices screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='di_user', password='pass12345', facturas=1, reader=0)
        company = OeesCompanies.objects.create(name='Acme')
        deleg = OeesDelegations.objects.create(delegation='HQ', notes='')
        self.staff = OeesStaff.objects.create(
            name='Owner', persona_fisica=1, notes='', state=1,
            company_id=company.id_company, delegation_id=deleg.id_delegation, department='IT',
        )
        OeesDevices.objects.create(
            serial_number='DI-1', type='Laptop', brand='Dell', model='XPS', origin='New',
            insert_date=date(2026, 1, 1), value=1000.0, bill_number='BILL-1', persone=self.staff,
        )

    def test_dist_invoices_requires_login(self):
        response = self.client.get(reverse('frm_dist_invoices'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_dist_invoices_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_dist_invoices'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmDistributionInvoices.html')

    def test_dist_invoices_search(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_dist_invoices'), {'bill': 'BILL-1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DI-1')

    def test_dist_invoices_excel(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_dist_invoices'), {'bill': 'BILL-1', 'export': 'excel'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )


class PasswordChangeScreenTests(TestCase):
    """Smoke tests for the Password Change screen (Django-managed auth)."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='pwd_user', password='oldpass12345')

    def test_password_change_requires_login(self):
        response = self.client.get(reverse('frm_password_change'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_password_change_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmPasswordChange.html')

    def test_password_change_success(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_password_change'), {
            'old_password': 'oldpass12345',
            'new_password1': 'BrandNew9988',
            'new_password2': 'BrandNew9988',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('BrandNew9988'))

    def test_password_change_wrong_old(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_password_change'), {
            'old_password': 'WRONG',
            'new_password1': 'BrandNew9988',
            'new_password2': 'BrandNew9988',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpass12345'))


class DelegationsScreenTests(TestCase):
    """Smoke tests for the Delegations screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='dl_user', password='pass12345', delegations=1, reader=0)
        self.deleg = OeesDelegations.objects.create(delegation='Headquarters', notes='', poblacion='Madrid')

    def test_delegations_requires_login(self):
        response = self.client.get(reverse('frm_delegations'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_delegations_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_delegations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmDelegations.html')

    def test_api_get_delegation_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_delegation'), {'id': self.deleg.id_delegation})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['delegation'], 'Headquarters')
        self.assertEqual(data['data']['poblacion'], 'Madrid')

    def test_save_creates_delegation(self):
        from unittest.mock import patch
        self.client.force_login(self.user)
        # Mock geocoding so the test never hits the network.
        with patch('oe_inventory_py_web.views._geocode_delegation', return_value=(40.4168, -3.7038)):
            response = self.client.post(reverse('frm_delegations'), {
                'action': 'save', 'delegation': 'Branch Office', 'direccion': 'Main St 1',
                'cpostal': '28001', 'poblacion': 'Madrid', 'provincia': 'Madrid',
            })
        self.assertEqual(response.status_code, 302)
        d = OeesDelegations.objects.get(delegation='Branch Office', poblacion='Madrid')
        self.assertEqual(d.latitude, 40.4168)   # geocoded coordinates stored
        self.assertEqual(d.longitude, -3.7038)

    def test_map_includes_geocoded_delegation(self):
        # A delegation with coordinates must appear in the map data on the page.
        self.deleg.latitude = 40.4168
        self.deleg.longitude = -3.7038
        self.deleg.save(update_fields=['latitude', 'longitude'])
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_delegations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'delegations-map')      # map container
        self.assertContains(response, 'delegations-map-data')  # JSON data block
        self.assertContains(response, '40.4168')               # the point itself

    def test_geocode_action_updates_coordinates(self):
        from unittest.mock import patch
        self.client.force_login(self.user)
        with patch('oe_inventory_py_web.views._geocode_delegation', return_value=(41.3874, 2.1686)):
            response = self.client.post(reverse('frm_delegations'), {
                'action': 'geocode', 'code': str(self.deleg.id_delegation),
                'direccion': 'Av Diagonal 1', 'poblacion': 'Barcelona',
            })
        self.assertEqual(response.status_code, 302)
        self.deleg.refresh_from_db()
        self.assertEqual(self.deleg.latitude, 41.3874)
        self.assertEqual(self.deleg.longitude, 2.1686)


class AccessCardsScreenTests(TestCase):
    """Smoke tests for the Access Cards screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='ac_user', password='pass12345', access_cards=1, reader=0)
        self.state = OeesAccessCardsStates.objects.create(id_state=1, description='ACTIVE')
        self.card = OeesAccessCards.objects.create(
            ac_max='C1', fermax_mif='F1', pin_card='', state_card=1, obs='', notes='',
        )

    def test_access_cards_requires_login(self):
        response = self.client.get(reverse('frm_access_cards'))
        self.assertEqual(response.status_code, 302)

    def test_access_cards_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_access_cards'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmAccessCards.html')

    def test_api_get_card_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_card'), {'card': 'C1'})
        self.assertTrue(response.json()['exists'])

    def test_save_creates_card(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_access_cards'), {
            'action': 'save', 'card': 'C2', 'fermax': 'F2', 'state': '1', 'obs': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesAccessCards.objects.filter(ac_max='C2').exists())

    def test_save_card_consumes_pin_from_pool(self):
        from oe_inventory_py_web.models import OeesAccessCardsPins
        OeesAccessCardsPins.objects.create(pin='1234')
        OeesAccessCardsPins.objects.create(pin='5678')
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_access_cards'), {
            'action': 'save', 'card': 'C3', 'fermax': 'F3', 'state': '1', 'obs': '', 'pin': '1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(OeesAccessCards.objects.get(ac_max='C3').pin_card, '1234')
        self.assertFalse(OeesAccessCardsPins.objects.filter(pin='1234').exists())  # consumed
        self.assertTrue(OeesAccessCardsPins.objects.filter(pin='5678').exists())   # untouched

    def test_card_pin_api_returns_available_pin(self):
        from oe_inventory_py_web.models import OeesAccessCardsPins
        OeesAccessCardsPins.objects.create(pin='4321')
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_card_pin'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['pin'], '4321')

    def test_release_converts_to_visitor(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_access_cards'), {'action': 'release', 'card': 'C1'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesAccessCardsVisitors.objects.filter(ac_max='C1').exists())
        self.assertFalse(OeesAccessCards.objects.filter(ac_max='C1').exists())


class AccessKeysScreenTests(TestCase):
    """Smoke tests for the Access Keys screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='ak_user', password='pass12345', access_keys=1, reader=0)
        self.key = OeesAccessKeys.objects.create(type='Master', insert_date=date(2026, 1, 1), notes='')

    def test_access_keys_requires_login(self):
        response = self.client.get(reverse('frm_access_keys'))
        self.assertEqual(response.status_code, 302)

    def test_access_keys_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_access_keys'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmAccessKeys.html')

    def test_api_get_key_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_key'), {'id': self.key.id_key})
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['type'], 'Master')

    def test_save_creates_key(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_access_keys'), {
            'action': 'save', 'type': 'Backup', 'insert_date': '2026-02-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesAccessKeys.objects.filter(type='Backup').exists())


class VisitorCardsScreenTests(TestCase):
    """Smoke tests for the Visitors Access Cards screen."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='vc_user', password='pass12345', visitors_cards=1, reader=0)
        self.state = OeesAccessCardsStates.objects.create(id_state=1, description='ACTIVE')
        self.card = OeesAccessCardsVisitors.objects.create(
            ac_max='V1', fermax_mif='F1', name='Visitor', state_card_id=1, obs='', pin_card='', notes='',
        )

    def test_visitor_cards_requires_login(self):
        response = self.client.get(reverse('frm_visitor_cards'))
        self.assertEqual(response.status_code, 302)

    def test_visitor_cards_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_visitor_cards'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oe_inventory_py_web/frmVisitorsAccessCards.html')

    def test_api_get_visitor_card_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_get_visitor_card'), {'card': 'V1'})
        data = response.json()
        self.assertTrue(data['exists'])
        self.assertEqual(data['data']['user'], 'Visitor')

    def test_save_creates_visitor_card(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_visitor_cards'), {
            'action': 'save', 'card': 'V2', 'fermax': 'F2', 'user': 'Jane', 'state': '1', 'obs': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OeesAccessCardsVisitors.objects.filter(ac_max='V2').exists())


class PasswordFlowTests(TestCase):
    """Initial-password by admin (frmUser) and the 'Forgot my password' reset flow."""

    def test_login_page_has_forgot_password_link(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, reverse('password_reset'))

    def test_password_reset_form_renders(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')

    def test_admin_with_users_permit_sets_initial_password_for_new_user(self):
        User = get_user_model()
        admin = User.objects.create_user(username='admin_u', password='pass12345', users=1)
        self.client.force_login(admin)
        response = self.client.post(reverse('frm_users'), {
            'login': 'newbie', 'nombre': 'New Bie', 'is_new': '1',
            'email': 'newbie@example.com', 'password': 'initpass123',
        })
        self.assertEqual(response.status_code, 302)
        newbie = User.objects.get(username='newbie')
        self.assertTrue(newbie.has_usable_password())
        self.assertTrue(newbie.check_password('initpass123'))
        self.assertEqual(newbie.email, 'newbie@example.com')  # email stored for recovery

    def test_password_ignored_without_users_permit(self):
        User = get_user_model()
        plain = User.objects.create_user(username='plain_u', password='pass12345', users=0)
        self.client.force_login(plain)
        self.client.post(reverse('frm_users'), {
            'login': 'newbie2', 'nombre': 'New Bie2', 'is_new': '1', 'password': 'initpass123',
        })
        newbie2 = User.objects.get(username='newbie2')
        self.assertFalse(newbie2.has_usable_password())  # no Users permit -> password not set

    def test_initial_password_not_overwritten_for_existing_user(self):
        # An existing user that already has a password keeps it (the field is
        # only for setting an INITIAL password).
        User = get_user_model()
        admin = User.objects.create_user(username='admin_u2', password='pass12345', users=1)
        target = User.objects.create_user(username='haspw', password='original123', staff=1)
        self.client.force_login(admin)
        self.client.post(reverse('frm_users'), {
            'login': 'haspw', 'nombre': 'Has Pw', 'is_new': '0', 'password': 'hacked999',
        })
        target.refresh_from_db()
        self.assertTrue(target.check_password('original123'))   # unchanged
        self.assertFalse(target.check_password('hacked999'))


class FooterCountersTests(TestCase):
    """The base_mdi footer counters (pending access cards / pending orders)."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='footer_u', password='pass12345')

    def test_pending_counters(self):
        from datetime import date
        from oe_inventory_py_web.models import (
            OeesAccessCardsStates, OeesAccessCards, OeesOrders,
        )
        pending = OeesAccessCardsStates.objects.create(description='PENDING')
        delivered = OeesAccessCardsStates.objects.create(description='DELIVERED')

        # Access cards: only the one in PENDING should count.
        OeesAccessCards.objects.create(ac_max='C1', fermax_mif='F1', pin_card='1234',
                                       state_card=pending.id_state, obs='', notes='')
        OeesAccessCards.objects.create(ac_max='C2', fermax_mif='F2', pin_card='1234',
                                       state_card=delivered.id_state, obs='', notes='')

        # Orders: only tramitado=0 AND cancelado=0 should count as pending.
        OeesOrders.objects.create(article='A', uds=1, insert_date=date(2026, 1, 1), notes='',
                                  tramitado=0, cancelado=0, recibido=0)   # pending
        OeesOrders.objects.create(article='B', uds=1, insert_date=date(2026, 1, 1), notes='',
                                  tramitado=1, cancelado=0, recibido=0)   # processed -> excluded
        OeesOrders.objects.create(article='C', uds=1, insert_date=date(2026, 1, 1), notes='',
                                  tramitado=0, cancelado=1, recibido=0)   # cancelled -> excluded

        self.client.force_login(self.user)
        response = self.client.get(reverse('mdi_home'))
        self.assertEqual(response.context['total_cards'], 1)
        self.assertEqual(response.context['total_orders'], 1)


class StaffDocStorageTests(TestCase):
    """Staff documents are saved/served via Django's storage API (S3-ready)."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='doc_u', password='pass12345', staff=1, reader=0)
        self.staff = OeesStaff.objects.create(name='Doc Person', persona_fisica=1, notes='',
                                              state=1, department='IT')

    def test_upload_and_serve_via_storage(self):
        import tempfile
        from django.test import override_settings
        from django.core.files.uploadedfile import SimpleUploadedFile
        from oe_inventory_py_web.models import OeesDocs

        with tempfile.TemporaryDirectory() as tmp, override_settings(MEDIA_ROOT=tmp):
            self.client.force_login(self.user)
            pdf = SimpleUploadedFile('contract.pdf', b'%PDF-1.4 test', content_type='application/pdf')
            up = self.client.post(reverse('frm_staff'), {
                'action': 'upload_doc', 'code': str(self.staff.id_staff),
                'doc_name': 'Contract', 'doc_file': pdf,
            })
            self.assertEqual(up.status_code, 302)
            self.assertTrue(OeesDocs.objects.filter(
                id_staff_id=self.staff.id_staff, doc_name='Contract').exists())

            served = self.client.get(reverse('staff_doc', kwargs={
                'staff_id': self.staff.id_staff, 'doc_name': 'Contract'}))
            self.assertEqual(served.status_code, 200)
            self.assertEqual(served['Content-Type'], 'application/pdf')


class OnlineUsersTests(TestCase):
    """Counting users currently connected to the app (option 2: last activity)."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='online_a', password='pass12345', devices=1
        )
        self.other = User.objects.create_user(
            username='online_b', password='pass12345', devices=1
        )

    def _make_session(self, user, last_activity):
        """Create a DB session for `user` stamped with `last_activity` (epoch)."""
        from django.contrib.sessions.backends.db import SessionStore
        store = SessionStore()
        store['_auth_user_id'] = str(user.pk)
        store['last_activity'] = last_activity
        store.create()
        return store

    def test_counts_recently_active_user(self):
        import time
        from .context_processors import count_online_users
        self._make_session(self.user, time.time())
        self.assertEqual(count_online_users(), 1)

    def test_ignores_stale_session(self):
        import time
        from .context_processors import count_online_users
        # Active 10 minutes ago: outside the 5-minute window.
        self._make_session(self.user, time.time() - 600)
        self.assertEqual(count_online_users(), 0)

    def test_counts_distinct_users_not_sessions(self):
        import time
        from .context_processors import count_online_users
        now = time.time()
        # Same user on two devices must count once; a second user adds one.
        self._make_session(self.user, now)
        self._make_session(self.user, now)
        self._make_session(self.other, now)
        self.assertEqual(count_online_users(), 2)

    def test_middleware_stamps_last_activity(self):
        self.client.force_login(self.user)
        self.client.get(reverse('mdi_home'))
        session = self.client.session
        self.assertIn('last_activity', session)

    def test_online_count_in_footer_context(self):
        import time
        # Another user already has a persisted active session.
        self._make_session(self.other, time.time())
        self.client.force_login(self.user)
        response = self.client.get(reverse('mdi_home'))
        self.assertIn('online_users', response.context)
        self.assertGreaterEqual(response.context['online_users'], 1)

    def test_current_user_always_counted_on_own_footer(self):
        # The requester is online by definition even before their session
        # stamp is flushed to the DB, so the footer must never show 0 for them.
        self.client.force_login(self.user)
        response = self.client.get(reverse('mdi_home'))
        self.assertGreaterEqual(response.context['online_users'], 1)

    def test_current_user_always_listed_in_popup(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_online_users'))
        self.assertIn('online_a', response.json()['users'])

    def test_api_online_users_returns_names(self):
        import time
        self._make_session(self.other, time.time())
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_online_users'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('online_b', data['users'])
        self.assertEqual(data['count'], len(data['users']))

    def test_api_online_users_uses_full_name_when_available(self):
        import time
        self.other.first_name = 'Ada'
        self.other.last_name = 'Lovelace'
        self.other.save()
        self._make_session(self.other, time.time())
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_online_users'))
        self.assertIn('Ada Lovelace', response.json()['users'])

    def test_api_online_users_requires_login(self):
        response = self.client.get(reverse('api_online_users'))
        self.assertEqual(response.status_code, 302)


class DevicesGridServerSideTests(TestCase):
    """The Devices grid loads server-side (DataTables) instead of all at once."""

    def setUp(self):
        from oe_inventory_py_web.models import OeesDevices
        User = get_user_model()
        self.user = User.objects.create_user(
            username='dev_admin', password='pass12345', devices=1, reader=0)
        self.company = OeesCompanies.objects.create(name='Acme')
        for i in range(3):
            OeesDevices.objects.create(
                serial_number=f'SN-{i}', type='LAPTOP', brand='Dell',
                model=f'M{i}', origin='New', insert_date=date(2026, 1, 1), value=100.0)
        OeesDevices.objects.create(
            serial_number='PHONE-9', type='PHONE', brand='Apple',
            model='15', origin='New', insert_date=date(2026, 1, 1), value=900.0,
            bill_number='FAC-2026-001')

    def test_frm_devices_does_not_render_rows_inline(self):
        # The page ships an empty tbody; rows arrive via AJAX afterwards.
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_devices'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'class="device-row"')
        # Totals are computed by aggregation, not by looping a grid in Python.
        self.assertEqual(response.context['total_devices'], 4)
        self.assertEqual(response.context['total_value'], 1200.0)

    def test_datatable_returns_paginated_json(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_devices_datatable'), {
            'draw': '2', 'start': '0', 'length': '2',
            'order[0][column]': '0', 'order[0][dir]': 'asc',
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['draw'], 2)
        self.assertEqual(data['recordsTotal'], 4)
        self.assertEqual(data['recordsFiltered'], 4)
        self.assertEqual(len(data['data']), 2)  # only the requested page

    def test_datatable_global_search_filters(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('api_devices_datatable'), {
            'draw': '1', 'start': '0', 'length': '50',
            'search[value]': 'PHONE',
        })
        data = response.json()
        self.assertEqual(data['recordsFiltered'], 1)
        self.assertEqual(data['data'][0]['serial'], 'PHONE-9')
        # The Bill Number column must carry its value through to the grid.
        self.assertEqual(data['data'][0]['bill'], 'FAC-2026-001')

    def test_datatable_requires_login(self):
        response = self.client.get(reverse('api_devices_datatable'))
        self.assertEqual(response.status_code, 302)

    def test_save_creates_a_brand_new_device(self):
        # Typing a new serial and pressing Save must create the device, like
        # frmPhones/frmLicenses do.
        from oe_inventory_py_web.models import OeesDevices
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_devices'), {
            'action': 'save', 'serial_number': 'BRAND-NEW-1', 'id_company': str(self.company.id_company),
            'type': 'LAPTOP', 'brand': 'HP', 'model': 'X1', 'value': '0',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(OeesDevices.objects.filter(serial_number='BRAND-NEW-1').exists())

    def test_save_requires_a_company(self):
        from oe_inventory_py_web.models import OeesDevices
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_devices'), {
            'action': 'save', 'serial_number': 'NO-COMPANY-1',
            'type': 'LAPTOP', 'brand': 'HP', 'model': 'X1', 'value': '0',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please select a company')
        self.assertFalse(OeesDevices.objects.filter(serial_number='NO-COMPANY-1').exists())

    def test_api_get_device_reports_under_repair_flag(self):
        # The AJAX lookup must say whether the device is in maintenance, so the
        # banner can be toggled when switching devices without a page reload.
        from datetime import date as _date
        OeesUnderRepair.objects.create(
            serial_number='SN-0', type='1', date_out=_date(2026, 1, 2),
            destiny='Technical Service', notes='', value=0.0)  # date_in NULL = in repair
        self.client.force_login(self.user)
        in_repair = self.client.get(reverse('api_get_device'), {'serial_number': 'SN-0'}).json()
        self.assertTrue(in_repair['under_repair'])
        not_repair = self.client.get(reverse('api_get_device'), {'serial_number': 'SN-1'}).json()
        self.assertFalse(not_repair['under_repair'])

    def test_unassigned_device_renders_without_fk_error(self):
        # SN-0 has no assigned person; loading it must not raise on the
        # persone FK and must show "Unassigned".
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_devices'), {
            'action': 'find', 'serial_number': 'SN-0',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['device_staff'], 'Unassigned')

    def test_support_send_stores_destiny_type_and_note(self):
        self.client.force_login(self.user)
        self.client.post(reverse('frm_devices'), {
            'action': 'support', 'serial_number': 'SN-0', 'repair_destiny': 'Madrid SAT',
        })
        rep = OeesUnderRepair.objects.filter(serial_number='SN-0', date_in__isnull=True).first()
        self.assertIsNotNone(rep)
        self.assertEqual(rep.destiny, 'Madrid SAT')
        self.assertEqual(rep.type, 'D')          # marked as a device
        dev = OeesDevices.objects.get(serial_number='SN-0')
        self.assertIn('Sent to maintenance (Madrid SAT)', dev.notes)

    def test_support_message_rendered_on_same_page(self):
        # The success message must appear on this render (consumed here), not
        # leak to the next screen the user visits.
        self.client.force_login(self.user)
        response = self.client.post(reverse('frm_devices'), {
            'action': 'support', 'serial_number': 'SN-0', 'repair_destiny': 'SAT',
        })
        self.assertContains(response, 'sent to technical support')

    def test_sent_device_appears_in_under_repair_pending(self):
        from oe_inventory_py_web.views import _under_repair_rows
        self.client.force_login(self.user)
        self.client.post(reverse('frm_devices'), {
            'action': 'support', 'serial_number': 'SN-0', 'repair_destiny': 'SAT',
        })
        serials = [r['serial'] for r in _under_repair_rows(repaired=False)]
        self.assertIn('SN-0', serials)

    def test_support_receive_records_cost_and_note(self):
        from datetime import date as _date
        OeesUnderRepair.objects.create(
            serial_number='SN-1', type='D', date_out=_date(2026, 1, 2),
            destiny='SAT', notes='', value=0.0)
        self.client.force_login(self.user)
        self.client.post(reverse('frm_devices'), {
            'action': 'support', 'serial_number': 'SN-1', 'repair_value': '45.50',
        })
        rep = OeesUnderRepair.objects.get(serial_number='SN-1')
        self.assertIsNotNone(rep.date_in)       # received
        self.assertEqual(rep.value, 45.50)       # cost recorded
        dev = OeesDevices.objects.get(serial_number='SN-1')
        self.assertIn('Received from maintenance', dev.notes)


class UserManualTests(TestCase):
    """In-app user manual: rendering, language switch and contextual help."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='manual_u', password='pass12345', devices=1)

    def test_manual_requires_login(self):
        response = self.client.get(reverse('manual'))
        self.assertEqual(response.status_code, 302)

    def test_manual_renders_spanish_by_default(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manual'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Manual de Usuario')
        # A stable per-screen anchor must be present for deep links.
        self.assertContains(response, 'id="devices"')

    def test_manual_renders_english(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manual'), {'lang': 'en'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Manual')

    def test_manual_shows_both_language_buttons(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manual'))
        self.assertContains(response, '?lang=es')
        self.assertContains(response, '?lang=en')

    def test_manual_rewrites_image_paths_to_static(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manual'))
        body = response.content.decode()
        self.assertIn('/static/manual_images/', body)
        self.assertNotIn('src="images/', body)

    def test_help_anchor_in_context_for_a_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_devices'))
        self.assertEqual(response.context['manual_anchor'], 'devices')

    def test_navbar_has_manual_link(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('mdi_home'))
        self.assertContains(response, reverse('manual'))


class ResendEmailBackendTests(TestCase):
    """Email goes through the Resend API backend (replaces the SMTP backend)."""

    def test_payload_plain_text_message(self):
        from django.core.mail import EmailMessage
        from oe_inventory_py_web.email_backend import build_resend_payload
        msg = EmailMessage(subject='Reset', body='Click here', to=['u@example.com'])
        payload = build_resend_payload(msg)
        self.assertEqual(payload['to'], ['u@example.com'])
        self.assertEqual(payload['subject'], 'Reset')
        self.assertEqual(payload['text'], 'Click here')
        self.assertNotIn('html', payload)

    def test_payload_html_alternative_becomes_html(self):
        from django.core.mail import EmailMultiAlternatives
        from oe_inventory_py_web.email_backend import build_resend_payload
        msg = EmailMultiAlternatives(subject='Hi', body='plain', to=['u@example.com'])
        msg.attach_alternative('<b>rich</b>', 'text/html')
        payload = build_resend_payload(msg)
        self.assertEqual(payload['html'], '<b>rich</b>')

    def test_payload_includes_pdf_attachment(self):
        from django.core.mail import EmailMessage
        from oe_inventory_py_web.email_backend import build_resend_payload
        msg = EmailMessage(subject='Inv', body='see attached', to=['u@example.com'])
        msg.attach('Inventory.pdf', b'%PDF-1.4 xyz', 'application/pdf')
        payload = build_resend_payload(msg)
        self.assertEqual(len(payload['attachments']), 1)
        att = payload['attachments'][0]
        self.assertEqual(att['filename'], 'Inventory.pdf')
        # Bytes are serialised as a list of integers (Resend SDK format).
        self.assertEqual(bytes(att['content']), b'%PDF-1.4 xyz')

    def test_payload_uses_default_from_when_unset(self):
        from django.core.mail import EmailMessage
        from django.test import override_settings
        from oe_inventory_py_web.email_backend import build_resend_payload
        with override_settings(DEFAULT_FROM_EMAIL='noreply@octoenergy.com'):
            msg = EmailMessage(subject='x', body='y', to=['u@example.com'])
            payload = build_resend_payload(msg)
            self.assertEqual(payload['from'], 'noreply@octoenergy.com')

    def test_backend_errors_without_api_key(self):
        from django.core.mail import EmailMessage
        from django.test import override_settings
        from oe_inventory_py_web.email_backend import ResendEmailBackend
        msg = EmailMessage(subject='x', body='y', to=['u@example.com'])
        with override_settings(RESEND_API_KEY=''):
            backend = ResendEmailBackend(fail_silently=False)
            with self.assertRaises(ValueError):
                backend.send_messages([msg])
            # With fail_silently the call is a no-op (0 sent), never the network.
            backend_silent = ResendEmailBackend(fail_silently=True)
            self.assertEqual(backend_silent.send_messages([msg]), 0)


class SessionSecurityTests(TestCase):
    """Sessions expire after inactivity and when the browser closes."""

    def test_session_settings_are_configured(self):
        from django.conf import settings
        self.assertEqual(settings.SESSION_COOKIE_AGE, 30 * 60)
        self.assertTrue(settings.SESSION_SAVE_EVERY_REQUEST)
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)

    def test_session_is_browser_close_with_30min_idle(self):
        User = get_user_model()
        user = User.objects.create_user(username='sess_u', password='pass12345')
        self.client.force_login(user)
        self.client.get(reverse('mdi_home'))
        session = self.client.session
        # Cookie dies on browser close, and the idle window is 30 minutes.
        self.assertTrue(session.get_expire_at_browser_close())
        self.assertEqual(session.get_expiry_age(), 30 * 60)


class NotReturnedScreenTests(TestCase):
    """Material still assigned to staff who already left (fecha_baja set)."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='nr_user', password='pass12345', not_returned=1, reader=0)
        self.gone = OeesStaff.objects.create(
            name='Zoe Gone', notes='', persona_fisica=1, state=0, fecha_baja='2026-01-01')
        self.active = OeesStaff.objects.create(
            name='Andy Active', notes='', persona_fisica=1, state=1)
        OeesDevices.objects.create(
            serial_number='DEV-GONE', type='LAPTOP', brand='Dell', model='X',
            origin='New', insert_date=date(2026, 1, 1), value=500.0,
            persone=self.gone, mobile_line=0)
        OeesDevices.objects.create(
            serial_number='DEV-ACTIVE', type='LAPTOP', brand='HP', model='Y',
            origin='New', insert_date=date(2026, 1, 1), value=300.0,
            persone=self.active, mobile_line=0)

    def test_requires_login(self):
        self.assertEqual(self.client.get(reverse('frm_not_returned')).status_code, 302)

    def test_lists_only_terminated_staff_items(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_not_returned'))
        self.assertEqual(response.status_code, 200)
        serials = [r['serial'] for r in response.context['rows']]
        self.assertIn('DEV-GONE', serials)         # left -> shown
        self.assertNotIn('DEV-ACTIVE', serials)    # active -> not shown

    def test_row_has_person_date_aging_and_value(self):
        self.client.force_login(self.user)
        rows = self.client.get(reverse('frm_not_returned')).context['rows']
        row = next(r for r in rows if r['serial'] == 'DEV-GONE')
        self.assertEqual(row['person'], 'Zoe Gone')
        self.assertEqual(row['termination_date'], '2026-01-01')
        self.assertEqual(row['category'], 'Device')
        self.assertEqual(row['value'], 500.0)
        self.assertIsNotNone(row['aging_days'])

    def test_total_value_only_counts_terminated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('frm_not_returned'))
        self.assertEqual(response.context['total_value'], 500.0)

    def test_includes_access_keys(self):
        from oe_inventory_py_web.models import OeesAccessKeys
        OeesAccessKeys.objects.create(type='Main door', id_staff=self.gone, insert_date=date(2026, 1, 1))
        self.client.force_login(self.user)
        rows = self.client.get(reverse('frm_not_returned')).context['rows']
        self.assertTrue(any(r['category'] == 'Access Key' and r['person'] == 'Zoe Gone' for r in rows))

    def test_spanish_date_normalized_to_english_and_aged(self):
        spanish = OeesStaff.objects.create(
            name='Bob Spanish', notes='', persona_fisica=1, state=0, fecha_baja='15-03-2026')
        OeesDevices.objects.create(
            serial_number='DEV-ES', type='LAPTOP', brand='Dell', model='Z',
            origin='New', insert_date=date(2026, 1, 1), value=100.0,
            persone=spanish, mobile_line=0)
        self.client.force_login(self.user)
        rows = self.client.get(reverse('frm_not_returned')).context['rows']
        row = next(r for r in rows if r['serial'] == 'DEV-ES')
        self.assertEqual(row['termination_date'], '2026-03-15')   # dd-mm-yyyy -> yyyy-mm-dd
        self.assertIsNotNone(row['aging_days'])                   # parsed -> aging computed

    def test_subtotals_row_inserted_per_person(self):
        self.client.force_login(self.user)
        rows = self.client.get(reverse('frm_not_returned'), {'subtotals': 'on'}).context['rows']
        subs = [r for r in rows if r.get('sub')]
        self.assertTrue(any(r['person'] == 'Total Zoe Gone' and r['value'] == 500.0 for r in subs))
