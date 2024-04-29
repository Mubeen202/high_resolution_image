from django.urls import path
from .views import *

urlpatterns = [
    path('high_reso_img', ImageView.as_view(
        {
        'post': 'post',
    }
    )
    ),
    path('rephase',
         ImageView.as_view(
        {
        'post': 'rephrase',
    }
    )),
]