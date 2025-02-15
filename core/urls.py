from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('influencer-profile/create/', views.create_influencer_profile, name='influencer_profile_create'),
    path('advertiser-profile/create/', views.create_advertiser_profile, name='advertiser_profile_create'),
    
    # Influencer URLs
    path('influencers/', views.InfluencerListView.as_view(), name='influencer_list'),
    path('influencers/<int:pk>/', views.InfluencerDetailView.as_view(), name='influencer_detail'),
    
    # Advertiser URLs
    path('advertisers/<int:pk>/', views.AdvertiserDetailView.as_view(), name='advertiser_detail'),
    
    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/new/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/apply/', views.apply_project, name='apply_project'),
    
    # Collaboration URLs
    path('collaborations/<int:pk>/<str:status>/', views.update_collaboration_status, name='update_collaboration_status'),
] 