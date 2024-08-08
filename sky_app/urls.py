from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import AddCustomerAPI, GetCustomerAPI

sky_app_router = SimpleRouter()
sky_app_router.register('add-customer', AddCustomerAPI, basename="AddCustomerAPI")
sky_app_router.register('get-customers', GetCustomerAPI, basename=GetCustomerAPI)
urlpatterns = [
    path('', include(sky_app_router.urls)),
]