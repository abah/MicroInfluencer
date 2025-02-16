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
                'email': 'rani@example.com',
                'first_name': 'Rani',
                'last_name': 'Kusuma',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Beauty & Lifestyle Content Creator | Jakarta 🇮🇩',
                    'niche': 'Beauty',
                    'platform': 'Instagram',
                    'follower_count': 85000,
                    'engagement_rate': 4.8,
                    'instagram_handle': '@ranikbeauty'
                }
            },
            {
                'email': 'budi@example.com',
                'first_name': 'Budi',
                'last_name': 'Santoso',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Tech Reviewer | Gadget Enthusiast 📱 | Jakarta',
                    'niche': 'Technology',
                    'platform': 'YouTube',
                    'follower_count': 120000,
                    'engagement_rate': 5.2,
                    'youtube_channel': 'https://youtube.com/buditeknologi'
                }
            },
            {
                'email': 'dewi@example.com',
                'first_name': 'Dewi',
                'last_name': 'Pratiwi',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Food Vlogger | Kuliner Nusantara 🍜',
                    'niche': 'Food',
                    'platform': 'Multiple',
                    'follower_count': 95000,
                    'engagement_rate': 6.1,
                    'instagram_handle': '@dewimakan',
                    'tiktok_handle': '@dewimakan'
                }
            },
            {
                'email': 'ahmad@example.com',
                'first_name': 'Ahmad',
                'last_name': 'Fadli',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Travel & Adventure | Explore Indonesia 🌴',
                    'niche': 'Travel',
                    'platform': 'Instagram',
                    'follower_count': 75000,
                    'engagement_rate': 4.5,
                    'instagram_handle': '@ahmadtraveling'
                }
            },
            {
                'email': 'siti@example.com',
                'first_name': 'Siti',
                'last_name': 'Rahma',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Modest Fashion & Lifestyle | Bandung',
                    'niche': 'Fashion',
                    'platform': 'Multiple',
                    'follower_count': 110000,
                    'engagement_rate': 5.8,
                    'instagram_handle': '@sitirahma.style',
                    'tiktok_handle': '@sitirahma.style'
                }
            },
            {
                'email': 'reza@example.com',
                'first_name': 'Reza',
                'last_name': 'Aditya',
                'role': 'INFLUENCER',
                'profile': {
                    'bio': 'Gaming & Esports Content Creator 🎮',
                    'niche': 'Gaming',
                    'platform': 'YouTube',
                    'follower_count': 200000,
                    'engagement_rate': 7.2,
                    'youtube_channel': 'https://youtube.com/rezagaming'
                }
            }
        ]

        # Create advertisers
        advertisers_data = [
            {
                'email': 'marketing@wardahbeauty.com',
                'first_name': 'Sarah',
                'last_name': 'Wardah',
                'role': 'ADVERTISER',
                'profile': {
                    'company_name': 'Wardah Beauty',
                    'industry': 'Beauty',
                    'website': 'https://wardahbeauty.com',
                    'description': 'Brand kosmetik halal terkemuka di Indonesia'
                }
            },
            {
                'email': 'brand@tokopedia.com',
                'first_name': 'Dimas',
                'last_name': 'Tokopedia',
                'role': 'ADVERTISER',
                'profile': {
                    'company_name': 'Tokopedia',
                    'industry': 'Technology',
                    'website': 'https://tokopedia.com',
                    'description': 'Platform e-commerce terbesar di Indonesia'
                }
            },
            {
                'email': 'marketing@sedaap.id',
                'first_name': 'Linda',
                'last_name': 'Sedaap',
                'role': 'ADVERTISER',
                'profile': {
                    'company_name': 'Mie Sedaap',
                    'industry': 'Food',
                    'website': 'https://sedaap.id',
                    'description': 'Produk makanan instan berkualitas untuk keluarga Indonesia'
                }
            },
            {
                'email': 'brand@traveloka.com',
                'first_name': 'Andi',
                'last_name': 'Traveloka',
                'role': 'ADVERTISER',
                'profile': {
                    'company_name': 'Traveloka',
                    'industry': 'Travel',
                    'website': 'https://traveloka.com',
                    'description': 'Platform travel dan lifestyle terdepan di Asia Tenggara'
                }
            }
        ]

        # Create projects
        projects_data = [
            {
                'title': 'Kampanye Produk Skincare Halal',
                'description': 'Mencari beauty influencer untuk review rangkaian produk skincare terbaru',
                'budget': 5000000,
                'requirements': 'Minimal 50k followers, spesialisasi di konten beauty dan skincare, membuat 3 Instagram post dan 2 story',
                'deadline': timezone.now().date() + timezone.timedelta(days=30)
            },
            {
                'title': 'Review Smartphone Gaming',
                'description': 'Review smartphone gaming terbaru dengan fitur unggulan untuk para gamers',
                'budget': 8000000,
                'requirements': 'Minimal 100k subscribers, membuat video review detail 15-20 menit',
                'deadline': timezone.now().date() + timezone.timedelta(days=45)
            },
            {
                'title': 'Eksplorasi Kuliner Nusantara',
                'description': 'Mencari food vlogger untuk mengulas makanan khas daerah',
                'budget': 4000000,
                'requirements': 'Minimal 50k followers, spesialisasi konten kuliner, 5 post Instagram/TikTok',
                'deadline': timezone.now().date() + timezone.timedelta(days=20)
            },
            {
                'title': 'Campaign #JelajahIndonesia',
                'description': 'Dokumentasi perjalanan ke destinasi wisata tersembunyi di Indonesia',
                'budget': 10000000,
                'requirements': 'Minimal 70k followers, kemampuan fotografi/videografi yang baik, 5 post feed dan 3 reels',
                'deadline': timezone.now().date() + timezone.timedelta(days=60)
            },
            {
                'title': 'Fashion Ramadhan Series',
                'description': 'Koleksi modest wear untuk Ramadhan dan Lebaran',
                'budget': 6000000,
                'requirements': 'Minimal 80k followers, fokus pada modest fashion, 4 set konten (feed + reels)',
                'deadline': timezone.now().date() + timezone.timedelta(days=25)
            },
            {
                'title': 'Mobile Legends Tournament Coverage',
                'description': 'Live streaming dan highlight tournament Mobile Legends',
                'budget': 7000000,
                'requirements': 'Minimal 150k subscribers, pengalaman meliput esports, live streaming 3 jam',
                'deadline': timezone.now().date() + timezone.timedelta(days=15)
            }
        ]

        # Create users and profiles
        for data in influencers_data:
            email = data['email']
            if not User.objects.filter(email=email).exists():
                profile_data = data.pop('profile')
                user = User.objects.create_user(
                    username=data['email'],
                    password='testpass123',
                    **data
                )
                InfluencerProfile.objects.create(user=user, **profile_data)
                self.stdout.write(f'Created influencer: {user.get_full_name()}')
            else:
                self.stdout.write(f'Skipping existing influencer: {email}')

        for data in advertisers_data:
            email = data['email']
            if not User.objects.filter(email=email).exists():
                profile_data = data.pop('profile')
                user = User.objects.create_user(
                    username=data['email'],
                    password='testpass123',
                    **data
                )
                AdvertiserProfile.objects.create(user=user, **profile_data)
                self.stdout.write(f'Created advertiser: {user.get_full_name()}')
            else:
                self.stdout.write(f'Skipping existing advertiser: {email}')

        # Create projects with unique titles
        advertisers = User.objects.filter(role='ADVERTISER')
        for data in projects_data:
            title = data['title']
            if not Project.objects.filter(title=title).exists():
                project = Project.objects.create(
                    advertiser=random.choice(advertisers),
                    **data
                )
                self.stdout.write(f'Created project: {project.title}')

                # Create 2-3 random collaborations for each project
                influencers = list(User.objects.filter(role='INFLUENCER'))
                num_collabs = random.randint(2, 3)
                selected_influencers = random.sample(influencers, min(num_collabs, len(influencers)))
                
                for influencer in selected_influencers:
                    if not Collaboration.objects.filter(project=project, influencer=influencer).exists():
                        status = random.choice(['PENDING', 'APPROVED', 'IN_PROGRESS', 'COMPLETED'])
                        proposal = f'Saya tertarik untuk berkolaborasi dalam project ini. Saya memiliki pengalaman dalam membuat konten serupa dan yakin dapat memberikan hasil yang maksimal.'
                        
                        collab = Collaboration.objects.create(
                            project=project,
                            influencer=influencer,
                            proposal=proposal,
                            status=status
                        )
                        
                        if status == 'COMPLETED':
                            collab.completed_at = timezone.now()
                            collab.submission_link = 'https://example.com/submission'
                            collab.save()
                        
                        self.stdout.write(f'Created {status} collaboration for project: {project.title} with {influencer.get_full_name()}')
            else:
                self.stdout.write(f'Skipping existing project: {title}')

        self.stdout.write(self.style.SUCCESS('Successfully created dummy data')) 