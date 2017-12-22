from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api/v1/', include('{{cookiecutter.project_name}}.{{cookiecutter.django_app}}.urls')),
]
