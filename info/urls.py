from django.urls import path
from info.apis import *

app_name = 'info'

urlpatterns = [
    path('info', ApiInfo.as_view(), name='api_info'),
]
