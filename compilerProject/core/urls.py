"""compilerProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from api.views import index, problems, leaderboard, auth, base, profile, textEditor
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('', index, name='index'),
    path('auth', auth, name='auth'),
    path('problems', problems, name='problems'),
    path('leaderboard', leaderboard, name='leaderboard'),
    path('base', base, name='base'),
    path('profile', profile, name='profile'),
    path('textEditor/<slug:slug>', textEditor, name='textEditor'),

]
