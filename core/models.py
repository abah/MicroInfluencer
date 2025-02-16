from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class User(AbstractUser):
    class Role(models.TextChoices):
        INFLUENCER = 'INFLUENCER', _('Influencer')
        ADVERTISER = 'ADVERTISER', _('Advertiser')
        ADMIN = 'ADMIN', _('Admin')
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.INFLUENCER)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

class InfluencerProfile(models.Model):
    NICHE_CHOICES = [
        ('Fashion', 'Fashion'),
        ('Beauty', 'Beauty'),
        ('Technology', 'Technology'),
        ('Gaming', 'Gaming'),
        ('Lifestyle', 'Lifestyle'),
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Fitness', 'Fitness'),
        ('Education', 'Education'),
        ('Business', 'Business'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text=_('Tell us about yourself and your content creation experience')
    )
    niche = models.CharField(
        max_length=100,
        choices=NICHE_CHOICES,
        help_text=_('Your primary content category')
    )
    platform = models.CharField(
        max_length=50,
        choices=[
            ('Instagram', 'Instagram'),
            ('TikTok', 'TikTok'),
            ('YouTube', 'YouTube'),
            ('Multiple', 'Multiple Platforms')
        ],
        help_text=_('Your main social media platform'),
        default='Multiple'
    )
    follower_count = models.PositiveIntegerField(
        help_text=_('Total number of followers on your main platform')
    )
    engagement_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('Average engagement rate (likes + comments) / followers * 100'),
        default=0.00
    )
    instagram_handle = models.CharField(
        max_length=30,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^@[a-zA-Z0-9._]{1,30}$',
                message='Instagram handle must start with @ and contain only letters, numbers, dots and underscores'
            )
        ],
        help_text=_('Your Instagram username (start with @)')
    )
    tiktok_handle = models.CharField(
        max_length=30,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^@[a-zA-Z0-9._]{1,30}$',
                message='TikTok handle must start with @ and contain only letters, numbers, dots and underscores'
            )
        ],
        help_text=_('Your TikTok username (start with @)')
    )
    youtube_channel = models.URLField(
        max_length=100,
        blank=True,
        help_text=_('Your YouTube channel URL')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-follower_count', '-created_at']
        verbose_name = _('Influencer Profile')
        verbose_name_plural = _('Influencer Profiles')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.niche}"

    def clean(self):
        super().clean()
        if self.platform == 'Instagram' and not self.instagram_handle:
            raise models.ValidationError({
                'instagram_handle': _('Instagram handle is required when Instagram is selected as platform')
            })
        elif self.platform == 'TikTok' and not self.tiktok_handle:
            raise models.ValidationError({
                'tiktok_handle': _('TikTok handle is required when TikTok is selected as platform')
            })
        elif self.platform == 'YouTube' and not self.youtube_channel:
            raise models.ValidationError({
                'youtube_channel': _('YouTube channel URL is required when YouTube is selected as platform')
            })

class AdvertiserProfile(models.Model):
    INDUSTRY_CHOICES = [
        ('Fashion', 'Fashion & Apparel'),
        ('Beauty', 'Beauty & Cosmetics'),
        ('Technology', 'Technology & Software'),
        ('Food', 'Food & Beverage'),
        ('Health', 'Health & Wellness'),
        ('Travel', 'Travel & Tourism'),
        ('Education', 'Education & E-learning'),
        ('Finance', 'Finance & Fintech'),
        ('Entertainment', 'Entertainment & Media'),
        ('Retail', 'Retail & E-commerce'),
        ('Other', 'Other')
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='advertiser_profile'
    )
    company_name = models.CharField(
        max_length=100,
        help_text=_('Name of your company or brand')
    )
    industry = models.CharField(
        max_length=100,
        choices=INDUSTRY_CHOICES,
        help_text=_('Primary industry of your business'),
        default='Other'
    )
    website = models.URLField(
        blank=True,
        help_text=_('Your company website URL')
    )
    description = models.TextField(
        help_text=_('Tell us about your company and what kind of influencers you\'re looking for'),
        default='',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Advertiser Profile')
        verbose_name_plural = _('Advertiser Profiles')

    def __str__(self):
        return f"{self.company_name} ({self.industry})"

    def clean(self):
        super().clean()
        if not self.website and not self.description:
            raise models.ValidationError(
                _('Either website or company description must be provided')
            )
        
        if self.description and len(self.description.split()) < 20:
            raise models.ValidationError({
                'description': _('Company description should be more detailed (at least 20 words)')
            })

class Project(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')
    
    title = models.CharField(max_length=200)
    description = models.TextField(help_text=_('Detailed description of the project and its goals'))
    advertiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    influencer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_projects')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('Project budget in USD')
    )
    requirements = models.TextField(help_text=_('Specific requirements and expectations for the influencer'))
    deadline = models.DateField(help_text=_('Project completion deadline'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_review_project', 'Can review project'),
            ('can_manage_project', 'Can manage project'),
        ]

    def __str__(self):
        return f"{self.title} by {self.advertiser.get_full_name()}"

    def clean(self):
        if self.deadline and self.deadline < timezone.now().date():
            raise models.ValidationError({'deadline': _('Deadline cannot be in the past')})
        
        if self.status == self.Status.COMPLETED and not self.influencer:
            raise models.ValidationError({'status': _('Cannot mark project as completed without an assigned influencer')})
        
        if self.influencer and self.influencer.role != User.Role.INFLUENCER:
            raise models.ValidationError({'influencer': _('Assigned user must be an influencer')})
        
        if self.advertiser.role != User.Role.ADVERTISER:
            raise models.ValidationError({'advertiser': _('Project creator must be an advertiser')})

class Collaboration(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collaborations')
    influencer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborations')
    proposal = models.TextField(
        help_text=_('Your proposal for this project'),
        default='',
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    submission_link = models.URLField(blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ['project', 'influencer']

    def __str__(self):
        return f"{self.project.title} - {self.influencer.get_full_name()}"

    def save(self, *args, **kwargs):
        # Track if this is a new instance
        is_new = self.pk is None
        
        if not is_new:
            # Get old status before update
            old_instance = Collaboration.objects.get(pk=self.pk)
            old_status = old_instance.status
            
            # If status changes from PENDING to APPROVED
            if old_status == 'PENDING' and self.status == 'APPROVED':
                # Reject all other pending applications
                Collaboration.objects.filter(
                    project=self.project,
                    status='PENDING'
                ).exclude(pk=self.pk).update(
                    status='REJECTED',
                    feedback='Project telah diberikan kepada influencer lain'
                )
                
                # Update project status and influencer
                self.project.status = 'IN_PROGRESS'
                self.project.influencer = self.influencer
                self.project.save(update_fields=['status', 'influencer', 'updated_at'])
            
            # If status changes to COMPLETED
            elif self.status == 'COMPLETED' and old_status != 'COMPLETED':
                self.completed_at = timezone.now()
                # Only update project status if all active collaborations are completed
                if not self.project.collaborations.exclude(pk=self.pk).filter(
                    status__in=['APPROVED', 'IN_PROGRESS']
                ).exists():
                    self.project.status = 'COMPLETED'
                    self.project.save(update_fields=['status', 'updated_at'])
            
            # If status changes to CANCELLED
            elif self.status == 'CANCELLED':
                # Reset project status only if this was the active collaboration
                if old_status in ['APPROVED', 'IN_PROGRESS']:
                    # Check if there are other active collaborations
                    if not self.project.collaborations.exclude(pk=self.pk).filter(
                        status__in=['APPROVED', 'IN_PROGRESS']
                    ).exists():
                        self.project.status = 'PENDING'
                        self.project.influencer = None
                        self.project.save(update_fields=['status', 'influencer', 'updated_at'])
            
            # If status changes to REJECTED
            elif self.status == 'REJECTED':
                # Reset project status only if this was the active collaboration
                if old_status in ['APPROVED', 'IN_PROGRESS']:
                    # Check if there are other active collaborations
                    if not self.project.collaborations.exclude(pk=self.pk).filter(
                        status__in=['APPROVED', 'IN_PROGRESS']
                    ).exists():
                        self.project.status = 'PENDING'
                        self.project.influencer = None
                        self.project.save(update_fields=['status', 'influencer', 'updated_at'])
            
            # If status changes to IN_PROGRESS
            elif self.status == 'IN_PROGRESS' and old_status != 'IN_PROGRESS':
                self.project.status = 'IN_PROGRESS'
                self.project.save(update_fields=['status', 'updated_at'])
        
        super().save(*args, **kwargs)

class ProjectUpdate(models.Model):
    UPDATE_TYPE_CHOICES = [
        ('BRIEF', 'Brief'),
        ('PROGRESS', 'Progress Update'),
        ('REVISION', 'Revision Request'),
        ('FEEDBACK', 'Feedback'),
    ]
    
    collaboration = models.ForeignKey(
        Collaboration, 
        on_delete=models.CASCADE, 
        related_name='updates'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_updates'
    )
    update_type = models.CharField(
        max_length=20, 
        choices=UPDATE_TYPE_CHOICES
    )
    content = models.TextField()
    attachment_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['collaboration', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
        ]

    def __str__(self):
        return f"{self.get_update_type_display()} by {self.sender.get_full_name()}"

    def clean(self):
        if not self.sender_id:
            raise ValidationError({
                'sender': 'Sender is required.'
            })
            
        if not self.collaboration_id:
            raise ValidationError({
                'collaboration': 'Collaboration is required.'
            })

        # Validate sender's role and permissions
        if self.sender.role == User.Role.ADVERTISER:
            if self.sender != self.collaboration.project.advertiser:
                raise ValidationError({
                    'sender': 'Only the project advertiser can send this update.'
                })
            if self.update_type not in ['BRIEF', 'REVISION', 'FEEDBACK']:
                raise ValidationError({
                    'update_type': 'Advertisers can only send briefs, revision requests, and feedback.'
                })
        elif self.sender.role == User.Role.INFLUENCER:
            if self.sender != self.collaboration.influencer:
                raise ValidationError({
                    'sender': 'Only the assigned influencer can send this update.'
                })
            if self.update_type != 'PROGRESS':
                raise ValidationError({
                    'update_type': 'Influencers can only send progress updates.'
                })
        else:
            raise ValidationError({
                'sender': 'Invalid sender role for project updates.'
            })

    def get_update_type_color(self):
        colors = {
            'BRIEF': 'brief',
            'PROGRESS': 'progress',
            'REVISION': 'revision',
            'FEEDBACK': 'feedback'
        }
        return colors.get(self.update_type, '')
