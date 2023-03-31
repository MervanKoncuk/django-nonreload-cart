from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.
class Kategori(models.Model):
    isim = models.CharField(max_length=100)
    
    def __str__(self):
        return self.isim

class AltKategori(models.Model):
    isim = models.CharField(max_length=100)
    
    def __str__(self):
        return self.isim

class TekKategori(models.Model):
    isim = models.CharField(max_length=100)
    
    def __str__(self):
        return self.isim

class Urun(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, null=True) # CASCADE = kategori silindiğinde ona bağlı olan ürünleri de siler. SET_NULL = .. boşa çıkarır
    sub_category = models.ManyToManyField(AltKategori)
    tek = models.OneToOneField(TekKategori, on_delete=models.CASCADE, null=True, blank=True)
    isim = models.CharField(max_length=50)
    aciklama = RichTextField(max_length=500, null=True)
    fiyat = models.IntegerField()
    resim = models.FileField(upload_to = 'urunler/', null=True, blank=True)
    def __str__(self):
        return self.isim
# ForeignKey = ManytoOne
# ManyToMany 
# OneToOne

class Sepet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    adet = models.IntegerField()
    fiyat = models.IntegerField()

    def __str__(self):
        return self.user.username
        
class Odeme(models.Model):
    toplamFiyat = models.IntegerField()
    sepet = models.ManyToManyField(Sepet)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.user.username