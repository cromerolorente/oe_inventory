from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (OeesAccessCards, OeesAccessCardsPins, OeesAccessCardsStates,
OeesAccessCardsVisitors, OeesAccessCardsVisitorsNotes, OeesAccessKeys,
OeesCompanies, OeesDelegations, OeesDevices, OeesDocs, OeesFiberLines,
OeesFiberLinesIncidences, OeesIncorporations, OeesLicenses, OeesLogs,
OeesMobileLines, OeesMobilePhones, OeesOrders, OeesParameters, OeesPrinters,
OeesReturns, OeesStaff, OeesUnderRepair,)

admin.site.register(OeesAccessCards)
admin.site.register(OeesAccessCardsPins)
admin.site.register(OeesAccessCardsStates)
admin.site.register(OeesAccessCardsVisitors)
admin.site.register(OeesAccessCardsVisitorsNotes)
admin.site.register(OeesAccessKeys)
admin.site.register(OeesCompanies)
admin.site.register(OeesDelegations)
admin.site.register(OeesDevices)
admin.site.register(OeesDocs)
admin.site.register(OeesFiberLines)
admin.site.register(OeesFiberLinesIncidences)
admin.site.register(OeesIncorporations)
admin.site.register(OeesLicenses)
admin.site.register(OeesLogs)
admin.site.register(OeesMobileLines)
admin.site.register(OeesMobilePhones)
admin.site.register(OeesOrders)
admin.site.register(OeesParameters)
admin.site.register(OeesPrinters)
admin.site.register(OeesReturns)
admin.site.register(OeesStaff)
admin.site.register(OeesUnderRepair)
