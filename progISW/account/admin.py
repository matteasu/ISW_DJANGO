from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
#from account.models import Statistiche
from account.models import Equipaggiamento



class AccountAdmin(UserAdmin):
	list_display = ('playerID', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('playerID','last_login')
	ordering = ('playerID','last_login')
	readonly_fields = ('date_joined', 'last_login')
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)
#admin.site.register(Statistiche)
admin.site.register(Equipaggiamento)
