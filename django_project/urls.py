"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from akashicrecords import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('login/',views.login_user, name="login"),
    path("registrar/",views.registrar_user),
    path("recommend/", views.recommendation),
    path("logout/",views.logout_user, name="logout"),
    path("search/", views.search, name="search"),
    path('movies/', views.movies, name='movies'),
    path("profile/<str:username>/", views.profile_page, name="profile"),
    path("profile/<str:username>/update_profile/", views.update_profile_page, name="udpdate_profile"),

    path("import/", views.import_database),
    #Url temporária para testes v
    path("teste/", views.search, name="teste"),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)