from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import InfluencerProfile, AdvertiserProfile, Project, Collaboration
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')

        # Create influencers
        influencers_data = [
            {
                'email': 'sarah@example.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Fashion and lifestyle content creator',
                    'niche': 'Fashion',
                    'platform': 'Instagram',
                    'follower_count': 50000,
                    'engagement_rate': 3.5,
                    'instagram_handle': '@sarahstyle'
                }
            },
            {
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Chen',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Tech reviewer and gaming streamer',
                    'niche': 'Technology',
                    'platform': 'YouTube',
                    'follower_count': 100000,
                    'engagement_rate': 4.2,
                    'youtube_channel': 'https://youtube.com/miketech'
                }
            },
            {
                'email': 'lisa@example.com',
                'first_name': 'Lisa',
                'last_name': 'Wong',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Food blogger and recipe creator',
                    'niche': 'Food',
                    'platform': 'Instagram',
                    'follower_count': 75000,
                    'engagement_rate': 5.1,
                    'instagram_handle': '@lisacooks'
                }
            }
        ]

        # Create advertisers
        advertisers_data = [
            {
                'email': 'brand@fashionco.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'ADVERTISER',
                'profile': {
                    'company_name': 'FashionCo',
                    'industry': 'Fashion',
                    'website': 'https://fashionco.com',
                    'description': 'Leading fashion brand looking for creative influencers'
                }
            },
            {
                'email': 'marketing@techstart.com',
                'first_name': 'Emma',
                'last_name': 'Davis',
                'role': 'ADVERTISER',
                'profile': {
                    'company_name': 'TechStart',
                    'industry': 'Technology',
                    'website': 'https://techstart.com',
                    'description': 'Innovative tech company seeking tech enthusiasts'
                }
            }
        ]

        # Create users and profiles
        for data in influencers_data:
            profile_data = data.pop('profile')
            user = User.objects.create_user(
                username=data['email'],
                password='testpass123',
                **data
            )
            InfluencerProfile.objects.create(user=user, **profile_data)
            self.stdout.write(f'Created influencer: {user.get_full_name()}')

        for data in advertisers_data:
            profile_data = data.pop('profile')
            user = User.objects.create_user(
                username=data['email'],
                password='testpass123',
                **data
            )
            AdvertiserProfile.objects.create(user=user, **profile_data)
            self.stdout.write(f'Created advertiser: {user.get_full_name()}')

        # Create projects
        projects_data = [
            {
                'title': 'Summer Fashion Campaign',
                'description': 'Looking for fashion influencers to showcase our new summer collection',
                'budget': 1000,
                'requirements': 'Must have at least 50k followers. Need 3 Instagram posts and 2 stories.',
                'deadline': timezone.now().date() + timezone.timedelta(days=30)
            },
            {
                'title': 'Tech Product Review',
                'description': 'Need detailed review of our new smartphone',
                'budget': 2000,
                'requirements': 'Must create a detailed YouTube review video, minimum 10 minutes',
                'deadline': timezone.now().date() + timezone.timedelta(days=45)
            },
            {
                'title': 'Food Photography Campaign',
                'description': 'Seeking food influencers for our restaurant chain',
                'budget': 800,
                'requirements': 'Need 5 high-quality food photos with captions',
                'deadline': timezone.now().date() + timezone.timedelta(days=20)
            }
        ]

        advertiser = User.objects.filter(role='ADVERTISER').first()
        for data in projects_data:
            project = Project.objects.create(advertiser=advertiser, **data)
            self.stdout.write(f'Created project: {project.title}')

        # Create some collaborations
        influencers = User.objects.filter(role='INFLUENCER')
        projects = Project.objects.all()

        for project in projects:
            influencer = random.choice(influencers)
            Collaboration.objects.create(
                project=project,
                influencer=influencer,
                proposal='I would love to work on this project. I have experience in creating similar content.',
                status='PENDING'
            )
            self.stdout.write(f'Created collaboration for project: {project.title}')

        self.stdout.write(self.style.SUCCESS('Successfully created dummy data')) 