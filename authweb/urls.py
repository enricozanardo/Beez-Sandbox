from django.urls import path
from authweb.apis import *

app_name = 'authweb'

urlpatterns = [
    path('login', APILogin.as_view(), name='list_blocks'),
]
