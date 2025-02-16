from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.utils import timezone

from .models import User, InfluencerProfile, AdvertiserProfile, Project, Collaboration
from .forms import (
    SignUpForm,
    InfluencerProfileForm,
    AdvertiserProfileForm,
    ProjectForm,
    CollaborationForm,
    ProjectSearchForm,
    InfluencerSearchForm
)

def home(request):
    context = {
        'latest_projects': Project.objects.select_related(
            'advertiser',
            'advertiser__advertiserprofile'
        ).filter(
            status__in=['PENDING', 'IN_PROGRESS']
        ).order_by('-created_at')[:3],
        
        'featured_influencers': User.objects.select_related(
            'influencer_profile'
        ).filter(
            role='INFLUENCER'
        ).order_by('-influencer_profile__follower_count')[:3],
        
        'influencer_count': User.objects.filter(role='INFLUENCER').count(),
        'project_count': Project.objects.filter(status__in=['PENDING', 'IN_PROGRESS']).count(),
        'niche_count': InfluencerProfile.objects.values('niche').distinct().count(),
        'advertiser_count': User.objects.filter(role='ADVERTISER').count(),
    }
    return render(request, 'core/home.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please complete your profile.')
            if user.role == 'INFLUENCER':
                return redirect('influencer_profile_create')
            else:
                return redirect('advertiser_profile_create')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def create_influencer_profile(request):
    if hasattr(request.user, 'influencer_profile'):
        messages.warning(request, 'You already have an influencer profile.')
        return redirect('influencer_detail', pk=request.user.influencer_profile.pk)
    
    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your influencer profile has been created!')
            return redirect('influencer_detail', pk=profile.pk)
    else:
        form = InfluencerProfileForm()
    return render(request, 'core/profile_form.html', {'form': form, 'title': 'Create Influencer Profile'})

@login_required
def create_advertiser_profile(request):
    if hasattr(request.user, 'advertiser_profile'):
        messages.warning(request, 'You already have an advertiser profile.')
        return redirect('advertiser_detail', pk=request.user.advertiser_profile.pk)
    
    if request.method == 'POST':
        form = AdvertiserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your advertiser profile has been created!')
            return redirect('advertiser_detail', pk=profile.pk)
    else:
        form = AdvertiserProfileForm()
    return render(request, 'core/profile_form.html', {'form': form, 'title': 'Create Advertiser Profile'})

class InfluencerListView(ListView):
    model = InfluencerProfile
    template_name = 'core/influencer_list.html'
    context_object_name = 'influencers'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        min_followers = self.request.GET.get('min_followers')
        max_followers = self.request.GET.get('max_followers')
        niche = self.request.GET.get('niche')

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(bio__icontains=search)
            )
        if min_followers:
            queryset = queryset.filter(follower_count__gte=min_followers)
        if max_followers:
            queryset = queryset.filter(follower_count__lte=max_followers)
        if niche:
            queryset = queryset.filter(niche__iexact=niche)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = InfluencerSearchForm(self.request.GET)
        return context

class InfluencerDetailView(DetailView):
    model = InfluencerProfile
    template_name = 'core/influencer_detail.html'
    context_object_name = 'influencer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all collaborations for this influencer with related project data
        collaborations = Collaboration.objects.filter(
            influencer=self.object.user
        ).select_related('project').order_by('-updated_at')
        
        # Group collaborations by status
        context['active_projects'] = [
            collab for collab in collaborations 
            if collab.status in ['APPROVED', 'IN_PROGRESS']
        ]
        context['pending_projects'] = [
            collab for collab in collaborations 
            if collab.status == 'PENDING'
        ]
        context['completed_projects'] = [
            collab for collab in collaborations 
            if collab.status == 'COMPLETED'
        ]
        context['cancelled_projects'] = [
            collab for collab in collaborations 
            if collab.status in ['REJECTED', 'CANCELLED']
        ]
        
        return context

class AdvertiserDetailView(DetailView):
    model = AdvertiserProfile
    template_name = 'core/advertiser_detail.html'
    context_object_name = 'advertiser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all projects with related collaborations
        projects = Project.objects.filter(
            advertiser=self.object.user
        ).select_related('advertiser').prefetch_related('collaborations').order_by('-updated_at')
        
        # Group projects by status
        context['active_projects'] = [
            p for p in projects 
            if p.status in ['APPROVED', 'IN_PROGRESS']
        ]
        context['pending_projects'] = [
            p for p in projects 
            if p.status == 'PENDING'
        ]
        context['completed_projects'] = [
            p for p in projects 
            if p.status == 'COMPLETED'
        ]
        context['cancelled_projects'] = [
            p for p in projects 
            if p.status in ['REJECTED', 'CANCELLED']
        ]
        
        return context

class ProjectListView(ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        min_budget = self.request.GET.get('min_budget')
        max_budget = self.request.GET.get('max_budget')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        if min_budget:
            queryset = queryset.filter(budget__gte=min_budget)
        if max_budget:
            queryset = queryset.filter(budget__lte=max_budget)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProjectSearchForm(self.request.GET)
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Ambil kolaborasi user saat ini dengan select_related untuk optimasi
            context['user_collaboration'] = Collaboration.objects.filter(
                project=self.object,
                influencer=self.request.user
            ).select_related('influencer').first()
            
            # Jika user adalah advertiser
            if self.request.user == self.object.advertiser:
                collaborations = self.object.collaborations.select_related('influencer').order_by('-updated_at')
                context['collaborations'] = collaborations
                context['pending_collaborations'] = [c for c in collaborations if c.status == 'PENDING']
                context['active_collaborations'] = [c for c in collaborations if c.status in ['APPROVED', 'IN_PROGRESS']]
                context['completed_collaborations'] = [c for c in collaborations if c.status == 'COMPLETED']
                context['rejected_collaborations'] = [c for c in collaborations if c.status in ['REJECTED', 'CANCELLED']]
            # Jika user adalah influencer yang sudah diterima
            elif context['user_collaboration'] and context['user_collaboration'].status in ['APPROVED', 'IN_PROGRESS', 'COMPLETED']:
                context['collaborations'] = [context['user_collaboration']]
            # Jika user adalah influencer lain atau belum diterima
            else:
                context['collaborations'] = []
        
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'advertiser_profile'):
            messages.error(request, 'Only advertisers can create projects.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.advertiser = self.request.user
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.advertiser != self.request.user:
            return HttpResponseForbidden("You don't have permission to edit this project.")
        return super().dispatch(request, *args, **kwargs)

@login_required
def apply_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if project.status != 'PENDING':
        messages.error(request, 'This project is no longer accepting applications.')
        return redirect('project_detail', pk=pk)
    
    if not hasattr(request.user, 'influencer_profile'):
        messages.error(request, 'Only influencers can apply to projects.')
        return redirect('project_detail', pk=pk)
    
    existing_collab = Collaboration.objects.filter(
        project=project,
        influencer=request.user
    ).exists()
    
    if existing_collab:
        messages.warning(request, 'You have already applied to this project.')
        return redirect('project_detail', pk=pk)
    
    if request.method == 'POST':
        form = CollaborationForm(request.POST)
        if form.is_valid():
            collaboration = form.save(commit=False)
            collaboration.project = project
            collaboration.influencer = request.user
            collaboration.save()
            messages.success(request, 'Your application has been submitted!')
            return redirect('project_detail', pk=pk)
    else:
        form = CollaborationForm()
    
    return render(request, 'core/collaboration_form.html', {
        'form': form,
        'project': project
    })

@login_required
def update_collaboration_status(request, pk, status):
    collaboration = get_object_or_404(Collaboration, pk=pk)
    project = collaboration.project
    
    if request.user != project.advertiser:
        messages.error(request, 'Only the project owner can update collaboration status.')
        return redirect('project_detail', pk=project.pk)
    
    valid_transitions = {
        'PENDING': ['APPROVED', 'REJECTED'],
        'APPROVED': ['IN_PROGRESS'],
        'IN_PROGRESS': ['COMPLETED', 'CANCELLED'],
    }
    
    current_status = collaboration.status
    if status not in valid_transitions.get(current_status, []):
        messages.error(request, f'Invalid status transition from {current_status} to {status}.')
        return redirect('project_detail', pk=project.pk)
    
    collaboration.status = status
    if status == 'COMPLETED':
        collaboration.completed_at = timezone.now()
    collaboration.save()
    
    status_messages = {
        'APPROVED': 'Application approved! The influencer has been notified.',
        'REJECTED': 'Application rejected.',
        'IN_PROGRESS': 'Collaboration marked as in progress.',
        'COMPLETED': 'Collaboration marked as completed.',
        'CANCELLED': 'Collaboration has been cancelled.',
    }
    messages.success(request, status_messages[status])
    
    if status == 'APPROVED':
        project.status = 'IN_PROGRESS'
        project.save()
    elif status == 'COMPLETED':
        if not project.collaborations.exclude(status='COMPLETED').exists():
            project.status = 'COMPLETED'
            project.save()
    
    return redirect('project_detail', pk=project.pk)

class CollaborationListView(LoginRequiredMixin, ListView):
    model = Collaboration
    template_name = 'core/collaboration_list.html'
    context_object_name = 'collaborations'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.role == User.Role.INFLUENCER:
            return Collaboration.objects.filter(influencer=self.request.user)
        else:
            return Collaboration.objects.filter(project__advertiser=self.request.user)

class CollaborationDetailView(LoginRequiredMixin, DetailView):
    model = Collaboration
    template_name = 'core/collaboration_detail.html'
    context_object_name = 'collaboration'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == User.Role.INFLUENCER:
            return queryset.filter(influencer=self.request.user)
        else:
            return queryset.filter(project__advertiser=self.request.user)
