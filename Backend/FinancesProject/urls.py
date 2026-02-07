from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('', health_check, name='health'),
    path('admin/', admin.site.urls),
    path("api/", include("FinancesApp.urls"))
]
