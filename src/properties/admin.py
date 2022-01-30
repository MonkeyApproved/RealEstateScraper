from django.contrib import admin
from properties.models import XeResult


class XeResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(XeResult, XeResultAdmin)
