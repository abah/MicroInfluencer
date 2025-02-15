from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

from .models import User, InfluencerProfile, AdvertiserProfile, Project, Collaboration

class CustomAdminSite(admin.AdminSite):
    site_header = 'MicroInfluencer Administration'
    site_title = 'MicroInfluencer Admin'
    index_title = 'Dashboard'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Statistik Pengguna
        total_users = User.objects.count()
        total_influencers = User.objects.filter(role='INFLUENCER').count()
        total_advertisers = User.objects.filter(role='ADVERTISER').count()
        
        # Statistik Project
        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(status='IN_PROGRESS').count()
        completed_projects = Project.objects.filter(status='COMPLETED').count()
        
        # Statistik Kolaborasi
        total_collaborations = Collaboration.objects.count()
        successful_collaborations = Collaboration.objects.filter(status='COMPLETED').count()
        
        # Tren Project (30 hari terakhir)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        projects_trend = Project.objects.filter(
            created_at__gte=thirty_days_ago
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Top Influencers
        top_influencers = InfluencerProfile.objects.order_by('-follower_count')[:5]
        
        # Project berdasarkan Status
        projects_by_status = Project.objects.values('status').annotate(
            count=Count('id')
        )
        
        context = {
            'total_users': total_users,
            'total_influencers': total_influencers,
            'total_advertisers': total_advertisers,
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'total_collaborations': total_collaborations,
            'successful_collaborations': successful_collaborations,
            'projects_trend': projects_trend,
            'top_influencers': top_influencers,
            'projects_by_status': projects_by_status,
        }
        
        return render(request, 'admin/dashboard.html', context)

admin_site = CustomAdminSite(name='admin')

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )

@admin.register(InfluencerProfile, site=admin_site)
class InfluencerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'niche', 'follower_count', 'created_at')
    list_filter = ('niche', 'created_at')
    search_fields = ('user__email', 'niche', 'bio')
    ordering = ('-follower_count',)

@admin.register(AdvertiserProfile, site=admin_site)
class AdvertiserProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'website', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('company_name', 'user__email', 'bio')
    ordering = ('-created_at',)

@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'advertiser', 'influencer', 'status', 'budget', 'deadline', 'created_at')
    list_filter = ('status', 'created_at', 'deadline')
    search_fields = ('title', 'description', 'advertiser__email', 'influencer__email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

@admin.register(Collaboration, site=admin_site)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('project', 'influencer', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'influencer__email', 'feedback')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

admin_site.register(User, CustomUserAdmin)
