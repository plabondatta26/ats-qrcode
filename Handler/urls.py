from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('qr/text/', qr_to_text_view, name='qr_to_text_view'),
    path('result/<slug:data>/<str:form>/', result, name='result'),
    path('camera/open/', video_qr_code, name='video_qr_code')
]
