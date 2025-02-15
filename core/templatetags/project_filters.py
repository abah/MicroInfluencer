from django import template
from core.models import Project, Collaboration
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='filter_by_project')
def filter_by_project(collaborations, project):
    """Filter collaborations by project"""
    return collaborations.filter(project=project).exists()

@register.filter(name='count_completed')
def count_completed(collaborations):
    """Count completed collaborations"""
    return collaborations.filter(status='COMPLETED').count()

@register.filter(name='format_currency')
def format_currency(value):
    """Format number as currency"""
    try:
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return value

@register.filter(name='get_status_display')
def get_status_display(project):
    """Get human-readable status with proper context"""
    if project.status == 'PENDING':
        pending_count = project.collaborations.filter(status='PENDING').count()
        if pending_count > 0:
            return mark_safe(f'Sedang Memilih Influencer <span class="badge bg-warning">{pending_count} aplikasi menunggu</span>')
        return 'Menunggu Influencer'
    elif project.status == 'IN_PROGRESS':
        return 'Sedang Dikerjakan'
    elif project.status == 'COMPLETED':
        return 'Selesai'
    elif project.status == 'CANCELLED':
        return 'Dibatalkan'
    return project.get_status_display()

@register.filter(name='get_status_class')
def get_status_class(status):
    """Get CSS class for status badge"""
    status_classes = {
        'PENDING': 'badge-warning',
        'IN_PROGRESS': 'badge-primary',
        'COMPLETED': 'badge-success',
        'CANCELLED': 'badge-danger'
    }
    return status_classes.get(status, 'badge-secondary')

@register.filter(name='get_collaboration')
def get_collaboration(project, user):
    """Get collaboration for a project and user"""
    return project.collaborations.filter(influencer=user).first()

@register.filter(name='can_apply')
def can_apply(project, user):
    """Check if user can apply to project"""
    if not user.is_authenticated or user.role != 'INFLUENCER':
        return False
        
    # Project harus dalam status PENDING
    if project.status != Project.Status.PENDING:
        return False
        
    # Cek kelengkapan profil
    try:
        profile = user.influencer_profile
        if not all([profile.bio, profile.niche, profile.follower_count]):
            return False
    except:
        return False
        
    # Cek apakah sudah ada kolaborasi yang aktif
    if project.collaborations.filter(status='IN_PROGRESS').exists():
        return False
        
    # Cek apakah sudah pernah apply
    return not project.collaborations.filter(influencer=user).exists()

@register.filter(name='get_collaboration_status')
def get_collaboration_status(project, user):
    """Get collaboration status message for influencer"""
    if not user or not user.is_authenticated or user.role != 'INFLUENCER':
        return None
        
    collab = project.collaborations.filter(influencer=user).first()
    if not collab:
        if project.status != Project.Status.PENDING:
            return "Project tidak menerima aplikasi"
        return None
    
    status_messages = {
        'PENDING': 'Menunggu persetujuan dari advertiser',
        'IN_PROGRESS': 'Anda sedang mengerjakan project ini',
        'COMPLETED': 'Anda telah menyelesaikan project ini',
        'CANCELLED': 'Aplikasi Anda tidak dipilih'
    }
    return status_messages.get(collab.status)

@register.filter(name='can_manage_collaboration')
def can_manage_collaboration(project, user):
    """Check if user can manage collaboration"""
    return user == project.advertiser or project.collaborations.filter(influencer=user).exists()

@register.filter(name='get_pending_applications_count')
def get_pending_applications_count(project):
    """Get count of pending applications for a project"""
    return project.collaborations.filter(status='PENDING').count()

@register.filter(name='has_active_collaboration')
def has_active_collaboration(project):
    """Check if project has active collaboration"""
    return project.status == Project.Status.IN_PROGRESS and project.collaborations.filter(status='IN_PROGRESS').exists()

@register.filter(name='get_advertiser_collab_status')
def get_advertiser_collab_status(project):
    """Get collaboration status message for advertiser"""
    if project.status == Project.Status.PENDING:
        pending_count = project.collaborations.filter(status='PENDING').count()
        if pending_count > 0:
            return f"Ada {pending_count} influencer menunggu persetujuan Anda"
        return "Belum ada influencer yang mengajukan diri"
        
    elif project.status == Project.Status.IN_PROGRESS:
        if project.influencer:
            return f"Project sedang dikerjakan oleh {project.influencer.get_full_name()}"
        return "Project sedang dikerjakan"
        
    elif project.status == Project.Status.COMPLETED:
        if project.influencer:
            return f"Project telah diselesaikan oleh {project.influencer.get_full_name()}"
        return "Project telah selesai"
        
    return "Project dibatalkan"