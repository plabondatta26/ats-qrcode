from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('qr/text/', qr_to_text_view, name='qr_to_text_view'),
    path('result/<data>/<str:form>/', result, name='result_url'),

]
