"""pm_weights URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# views
from animals.views import AnimalViewSet

from rest_framework import routers

# register default animal views with router
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'animal', AnimalViewSet)

# bind the non-default views 
animal_weight = AnimalViewSet.as_view({'post': 'add_weight'})
estimated_weight = AnimalViewSet.as_view({'get': 'estimated_weight'})

urlpatterns = [
     # animal urls
    url(r'animal/(?P<id>[0-9]+)/weight$', animal_weight),
    url(r'animal/estimated_weight', estimated_weight),
    # base router & admin urls
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
