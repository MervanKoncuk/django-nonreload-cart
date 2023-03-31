from django.contrib import admin
from .models import *
class SepetAdmin(admin.ModelAdmin):
    list_display = ['user', 'urun', 'adet', 'fiyat']
    list_filter = ['user', 'urun']
    search_fields = ['user', 'urun']
    list_per_page = 10
# Register your models here.
admin.site.register(Urun)
admin.site.register(Kategori)
admin.site.register(AltKategori)
admin.site.register(TekKategori)
admin.site.register(Sepet, SepetAdmin)
admin.site.register(Odeme)