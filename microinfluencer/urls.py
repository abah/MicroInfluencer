"""
URL configuration for microinfluencer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from core.models import Project, InfluencerProfile, AdvertiserProfile
from django.views.generic.base import RedirectView

# Sitemap configuration
sitemaps = {
    'projects': GenericSitemap({
        'queryset': Project.objects.filter(status='PENDING'),
        'date_field': 'updated_at',
    }, priority=0.9),
    'influencers': GenericSitemap({
        'queryset': InfluencerProfile.objects.all(),
        'date_field': 'updated_at',
    }, priority=0.8),
    'advertisers': GenericSitemap({
        'queryset': AdvertiserProfile.objects.all(),
        'date_field': 'updated_at',
    }, priority=0.8),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    
    # SEO and Favicon URLs
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon/favicon.ico')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
