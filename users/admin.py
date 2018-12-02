from django.contrib import admin
from .models import MyUser, Profile, Address


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user_no', 'phone', 'country']

    class Meta:
        model = Profile


class AddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'country', 'state', 'postal_code']

    class Meta:
        model = Address


# Register to Admin
admin.site.register(MyUser)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
