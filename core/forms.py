from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from .models import User, InfluencerProfile, AdvertiserProfile, Project, Collaboration
from django.utils import timezone

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ('INFLUENCER', 'Influencer'),
        ('ADVERTISER', 'Advertiser'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'password1', 'password2')

class InfluencerProfileForm(forms.ModelForm):
    def clean_follower_count(self):
        follower_count = self.cleaned_data.get('follower_count')
        if follower_count and follower_count < 0:
            raise forms.ValidationError("Follower count cannot be negative.")
        return follower_count

    def clean_engagement_rate(self):
        engagement_rate = self.cleaned_data.get('engagement_rate')
        if engagement_rate and (engagement_rate < 0 or engagement_rate > 100):
            raise forms.ValidationError("Engagement rate must be between 0 and 100.")
        return engagement_rate

    class Meta:
        model = InfluencerProfile
        fields = ['bio', 'niche', 'platform', 'follower_count', 'engagement_rate', 'instagram_handle', 'tiktok_handle', 'youtube_channel']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'follower_count': forms.NumberInput(attrs={'min': 0}),
            'engagement_rate': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': '0.01'}),
            'instagram_handle': forms.TextInput(attrs={'placeholder': '@username'}),
            'tiktok_handle': forms.TextInput(attrs={'placeholder': '@username'}),
            'youtube_channel': forms.URLInput(attrs={'placeholder': 'https://youtube.com/c/channel'}),
        }

class AdvertiserProfileForm(forms.ModelForm):
    class Meta:
        model = AdvertiserProfile
        fields = ['company_name', 'industry', 'website', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'website': forms.URLInput(attrs={'placeholder': 'https://'}),
        }

class ProjectForm(forms.ModelForm):
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline

    class Meta:
        model = Project
        fields = ['title', 'description', 'requirements', 'budget', 'deadline']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
            'budget': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

class CollaborationForm(forms.ModelForm):
    class Meta:
        model = Collaboration
        fields = ['proposal', 'submission_link']
        widgets = {
            'proposal': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe how you plan to promote this project and why you would be a good fit...'
            }),
            'submission_link': forms.URLInput(attrs={
                'placeholder': 'https://',
                'pattern': 'https?://.+'
            }),
        }
        help_texts = {
            'proposal': 'Explain your approach, previous experience, and why you\'re the best fit for this project.',
            'submission_link': 'Link to your content or deliverables (required when completing the project)'
        }

    def clean_submission_link(self):
        status = self.instance.status if self.instance else None
        submission_link = self.cleaned_data.get('submission_link')
        
        if status == 'COMPLETED' and not submission_link:
            raise forms.ValidationError("Submission link is required when marking collaboration as completed")
        return submission_link

    def clean(self):
        cleaned_data = super().clean()
        proposal = cleaned_data.get('proposal')
        
        if proposal and len(proposal.split()) < 20:
            raise forms.ValidationError({
                'proposal': "Your proposal should be more detailed (at least 20 words)"
            })
        
        return cleaned_data

class ProjectSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by title or description'})
    )
    min_budget = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min budget', 'step': '0.01'})
    )
    max_budget = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Max budget', 'step': '0.01'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All')] + list(Project.Status.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_budget = cleaned_data.get('min_budget')
        max_budget = cleaned_data.get('max_budget')
        
        if min_budget and max_budget and min_budget > max_budget:
            raise forms.ValidationError("Minimum budget cannot be greater than maximum budget")
        return cleaned_data

class InfluencerSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name or bio'})
    )
    niche = forms.ChoiceField(
        choices=[('', 'All Niches')] + [
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
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    platform = forms.ChoiceField(
        choices=[('', 'All Platforms')] + [
            ('Instagram', 'Instagram'),
            ('TikTok', 'TikTok'),
            ('YouTube', 'YouTube'),
            ('Multiple', 'Multiple Platforms')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_followers = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min followers'})
    )
    max_followers = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Max followers'})
    )
    min_engagement = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'placeholder': 'Min engagement rate', 'step': '0.01'})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_followers = cleaned_data.get('min_followers')
        max_followers = cleaned_data.get('max_followers')
        
        if min_followers and max_followers and min_followers > max_followers:
            raise forms.ValidationError("Minimum followers cannot be greater than maximum followers")
        return cleaned_data 