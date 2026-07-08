from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from oe_inventory_py_web import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Ruta para tu pantalla de Login (Asegúrate de que tenga el name='login')
    path('login/', views.login_view, name='login'),

    # Al loguearse, el usuario irá aquí (MDI limpio)
    path('', views.mdi_home_view, name='mdi_home'),
    
    # Solo se cargará el formulario al entrar en esta URL
    path('devices/', views.frm_devices_view, name='frm_devices'),

    # Ruta para hacer el logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # ---- "Forgot my password" (email reset flow) ----
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html',
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html',
    ), name='password_reset_complete'),

    # Ruta para sacar datos de un solo dispositivo mediante serial (AJAX)
    path('api/get-device/', views.api_get_device, name='api_get_device'),
    path('api/devices-datatable/', views.api_devices_datatable, name='api_devices_datatable'),

    # NUEVA RUTA PARA EL FINDER:
    path('api/finder/', views.api_finder, name='api_finder'),

    # Rutas para el manejo de los Usuarios
    path('users/', views.frm_users, name='frm_users'),
    path('api/get-user/', views.api_get_user, name='api_get_user'),
    path('api/online-users/', views.api_online_users, name='api_online_users'),
    path('manual/', views.manual_view, name='manual'),
    path('not-returned/', views.frm_not_returned_view, name='frm_not_returned'),
    path('omada/', views.frm_omada_view, name='frm_omada'),
    path('net-overview/', views.frm_net_overview_view, name='frm_net_overview'),
    path('remote-machines/', views.frm_remote_machines_view, name='frm_remote_machines'),
    path('video-rooms/', views.frm_video_rooms_view, name='frm_video_rooms'),
    path('api/net-alerts/', views.api_net_alerts, name='api_net_alerts'),
    path('api/footer-counts/', views.api_footer_counts, name='api_footer_counts'),

    # Licenses screen
    path('licenses/', views.frm_licenses_view, name='frm_licenses'),
    path('api/get-license/', views.api_get_license, name='api_get_license'),

    # Mobile Phones screen
    path('phones/', views.frm_phones_view, name='frm_phones'),
    path('api/get-phone/', views.api_get_phone, name='api_get_phone'),

    # Fiber Lines screen
    path('fiber/', views.frm_fiber_view, name='frm_fiber'),
    path('api/get-fiber/', views.api_get_fiber, name='api_get_fiber'),

    # Printers screen
    path('printers/', views.frm_printers_view, name='frm_printers'),
    path('api/get-printer/', views.api_get_printer, name='api_get_printer'),

    # Allocations screen
    path('allocations/', views.frm_allocations_view, name='frm_allocations'),
    path('api/allocations-search/', views.api_allocations_search, name='api_allocations_search'),

    # Incorporations screen
    path('incorporations/', views.frm_incorporations_view, name='frm_incorporations'),
    path('api/get-incorporation/', views.api_get_incorporation, name='api_get_incorporation'),

    # Orders screen
    path('orders/', views.frm_orders_view, name='frm_orders'),
    path('api/get-order/', views.api_get_order, name='api_get_order'),

    # Mobile Lines (SIM cards) screen
    path('mobile-lines/', views.frm_mobile_lines_view, name='frm_mobile_lines'),
    path('api/get-line/', views.api_get_line, name='api_get_line'),

    # Availability screen
    path('availability/', views.frm_availability_view, name='frm_availability'),

    # Under Repair screen
    path('under-repair/', views.frm_under_repair_view, name='frm_under_repair'),

    # Distribution Invoices screen
    path('dist-invoices/', views.frm_dist_invoices_view, name='frm_dist_invoices'),

    # Password change screen
    path('password-change/', views.frm_password_change_view, name='frm_password_change'),

    # Delegations screen
    path('delegations/', views.frm_delegations_view, name='frm_delegations'),
    path('api/get-delegation/', views.api_get_delegation, name='api_get_delegation'),

    # Office Access — Access Cards
    path('access-cards/', views.frm_access_cards_view, name='frm_access_cards'),
    path('api/get-card/', views.api_get_card, name='api_get_card'),
    path('api/card-pin/', views.api_card_pin, name='api_card_pin'),

    # Office Access — Access Keys
    path('access-keys/', views.frm_access_keys_view, name='frm_access_keys'),
    path('api/get-key/', views.api_get_key, name='api_get_key'),

    # Office Access — Visitors Access Cards
    path('visitor-cards/', views.frm_visitor_cards_view, name='frm_visitor_cards'),
    path('api/get-visitor-card/', views.api_get_visitor_card, name='api_get_visitor_card'),

    # Staff screen
    path('staff/', views.frm_staff_view, name='frm_staff'),
    path('api/get-staff/', views.api_get_staff, name='api_get_staff'),
    path('staff/report/', views.staff_report, name='staff_report'),
    path('staff/report/email/', views.staff_email_report, name='staff_email_report'),
    path('staff/doc/<int:staff_id>/<str:doc_name>/', views.staff_doc, name='staff_doc'),

    # TEMPORARY: AnyDesk Cloudflare 403 diagnostic (remove after support review)
    path('anydesk-diag/', views.anydesk_diag, name='anydesk_diag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
