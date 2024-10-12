from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register),
    path('login/',views.user_login),
    path('logout/',views.user_logout),
    path('products/',views.products),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('filterbyprice/',views.filterbyprice),
    path('product_details/<pid>',views.product_details),
    path('addcart/<pid>',views.cart),
    path('viewcart/',views.viewcart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('removecart/<cid>',views.removecart),
    path('placeorder/',views.placeorder),
    path('fetchorder/',views.fetchorder),
    path('removeorder/<pid>',views.removeorder),
    path('makepayment/',views.makepayment),
    path('about/',views.about),
    path('contact/',views.contact),
    path('paymentsuccess/',views.paymentsuccess),
    path('search/',views.search),
]
urlpatterns+=static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)