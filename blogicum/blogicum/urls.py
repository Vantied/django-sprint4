from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

urlpatterns = [
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    #path('profile/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),  # Для авторизации
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index')
        )
    ),  # Для регистрации
]

handler404 = 'pages.views.custom_404'
handler403 = 'pages.views.custom_403' 
handler500 = 'pages.views.custom_500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
