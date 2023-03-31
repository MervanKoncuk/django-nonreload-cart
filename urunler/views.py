from django.shortcuts import render, redirect
import iyzipay
import json
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
import pprint
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
# import jsonresponse
from django.http import JsonResponse
# Create your views here.

api_key = 'sandbox-P0pc0m5C6J5ZP28gkQpBVtRXrFRHm8mr'
secret_key = 'sandbox-5UKiwkqmhFYRq2gzn9iTPvKRFUfctyud'
base_url = 'sandbox-api.iyzipay.com'

options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}


sozlukToken = list()

def payment(request):
    context = dict()
    sepetim = Odeme.objects.get(user = request.user)
    buyer={
        'id': 'BY789',
        'name': 'John',
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address={
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]

    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': sepetim.toplamFiyat,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://localhost:8000/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(json_content["checkoutFormContent"])

@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(result)
def index(request):
    urunler = Urun.objects.all()
    kategoriler = Kategori.objects.all()
    sepet = Sepet.objects.filter(user = request.user)
    # uzunluk = len(sepet)
    # Arama
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
        urunler = Urun.objects.filter(
            Q(isim__icontains = search) |
            Q(kategori__isim__icontains = search)
        )
    if request.method == 'POST':
        urun = request.POST['urunId']
        adet = request.POST['adet']
        urunum = Urun.objects.get(id = urun)
        if Sepet.objects.filter(user = request.user, urun = urun).exists():
            sepet = Sepet.objects.get(user = request.user, urun = urunum)
            sepet.adet += int(adet)
            sepet.fiyat += int(adet) * urunum.fiyat
            sepet.save()
            
        else:
            sepet = Sepet(user = request.user, urun = urunum, adet = adet, fiyat = int(adet) * urunum.fiyat)
            sepet.save()
    uzunluk = Sepet.objects.filter(user = request.user)
    post = request.POST #Ajax'dan dönen post verilerini alıyoruz.

    # site_adi = post.get('site_adi') #Post değerinden site_adi verisini alıyoruz.

    # #Aynı şekilde diğer verileri de alıyoruz.
    # gonderen_kisi = post.get('urunId')
    # gonderilme_nedeni = post.get('adet')

    # result = True
    # message = ""
    # if site_adi=="http://127.0.0.1:8000":
    #     message = "http://127.0.0.1:8000 işlem başarılı"
    # else:
    #     message = "Yazıklar olsun! :("
    #     result = False


    
    context = {
        'urunler':urunler,
        'search':search,
        'kategoriler':kategoriler,
        'uzunluk':uzunluk,
        # 'result':result,
        # 'message':message
    }
   
    return render(request, 'index.html', context)

def detail(request, urunId):
    urun = Urun.objects.get(id = urunId)
    context = {
        'urun':urun
    }
    return render(request, 'urun.html', context)

def olustur(request):
    form = UrunForm()
    if request.method == 'POST':
        form = UrunForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürün oluşturuldu')
            return redirect('index')
    context = {
        'form':form
    }
    return render(request, 'olustur.html', context)


# ckeditor

# Ödeme
def success(request):
    messages.success(request, 'Ödeme başarılı')
    return redirect('index')
def failure(request):
    messages.error(request, 'Ödeme başarısız')
    return redirect('payment')

def sepet(request):
    urun = Sepet.objects.filter(user = request.user)
    toplam = 0
    
    for i in urun:
        toplam += i.fiyat
        
    if request.method == "POST":
        odeme = request.POST['odeme']
        
        odenen = Sepet.objects.filter(user = request.user)
        print(odenen[0].urun)
        odemeYap = Odeme.objects.create(
            toplamFiyat = odeme,
            user = request.user,
        )
        odemeYap.sepet.add(*odenen)
        

        odemeYap.save()
        
        return redirect('payment')
    context = {
        'urun':urun,
        'toplam':toplam
    }
    return render(request, 'sepet.html', context)