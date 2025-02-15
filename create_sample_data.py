import os
import django
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'microinfluencer.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import InfluencerProfile, AdvertiserProfile, Project
from django.utils import timezone

User = get_user_model()

# Data untuk generasi random
NICHES = [
    'Fashion', 'Beauty', 'Lifestyle', 'Food', 'Travel', 'Fitness', 
    'Technology', 'Gaming', 'Education', 'Business', 'Art', 'Music'
]

COMPANY_TYPES = [
    'Clothing', 'Cosmetics', 'Food & Beverage', 'Technology', 'Healthcare',
    'Education', 'Entertainment', 'Financial Services', 'Travel', 'Sports'
]

def create_sample_data():
    # Create 10 Advertisers
    advertisers = []
    for i in range(1, 11):
        company_type = random.choice(COMPANY_TYPES)
        advertiser = User.objects.create_user(
            username=f'brand{i}',
            email=f'brand{i}@example.com',
            password='brand123',
            role='ADVERTISER',
            first_name=f'Brand {i}',
            last_name='Company'
        )
        
        profile = AdvertiserProfile.objects.create(
            user=advertiser,
            company_name=f'{company_type} Brand {i}',
            website=f'https://brand{i}.com',
            bio=f'Leading {company_type.lower()} company specializing in innovative products and solutions.'
        )
        advertisers.append(advertiser)
        print(f'Created advertiser: {profile.company_name}')

    # Create 10 Influencers
    influencers = []
    for i in range(1, 11):
        niche = random.choice(NICHES)
        follower_count = random.randint(1000, 50000)
        influencer = User.objects.create_user(
            username=f'influencer{i}',
            email=f'influencer{i}@example.com',
            password='influencer123',
            role='INFLUENCER',
            first_name=f'Influencer',
            last_name=f'#{i}'
        )
        
        profile = InfluencerProfile.objects.create(
            user=influencer,
            bio=f'Creative content creator specializing in {niche.lower()}. Passionate about creating engaging content.',
            niche=niche,
            follower_count=follower_count,
            instagram_handle=f'influencer_{i}',
            tiktok_handle=f'influencer_{i}',
            youtube_channel=f'https://youtube.com/influencer{i}'
        )
        influencers.append(influencer)
        print(f'Created influencer: {profile.user.get_full_name()} ({niche})')

    # Create sample projects
    project_titles = [
        'Summer Fashion Campaign', 'Beauty Product Launch', 'Food Review Series',
        'Travel Vlog Collaboration', 'Fitness Challenge', 'Tech Product Review',
        'Gaming Stream Sponsorship', 'Educational Content Series'
    ]

    for i in range(8):
        advertiser = random.choice(advertisers)
        budget = random.randint(500, 5000)
        days_to_deadline = random.randint(14, 60)
        
        project = Project.objects.create(
            title=project_titles[i],
            description=f'Looking for influencers to promote our products/services through creative content.',
            advertiser=advertiser,
            status=random.choice(['PENDING', 'IN_PROGRESS']),
            budget=budget,
            requirements=f'''Requirements:
- Minimum {random.randint(1000, 5000)} followers
- Experience in content creation
- Creative storytelling ability
- Professional communication
- Deadline adherence''',
            deadline=timezone.now().date() + timedelta(days=days_to_deadline)
        )
        print(f'Created project: {project.title} by {advertiser.get_full_name()}')

    print("\nSample data created successfully!")
    print("\nLogin credentials:")
    print("\nAdvertisers:")
    for i in range(1, 11):
        print(f"Email: brand{i}@example.com")
        print(f"Password: brand123")
        print("---")
    
    print("\nInfluencers:")
    for i in range(1, 11):
        print(f"Email: influencer{i}@example.com")
        print(f"Password: influencer123")
        print("---")

if __name__ == '__main__':
    create_sample_data() 