from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('<username>', views.profile, name='profile'),
]
