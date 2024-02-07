from django.urls import path
from . import views as v
urlpatterns = [
    path('', v.generate_ad_prompt),
    path('test', v.test),
]
