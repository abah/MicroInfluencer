from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Project, Collaboration, ProjectUpdate
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates dummy interaction data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy interaction data...')

        # Get existing collaborations that are APPROVED or IN_PROGRESS
        active_collaborations = Collaboration.objects.filter(
            status__in=['APPROVED', 'IN_PROGRESS']
        )

        update_contents = {
            'BRIEF': [
                'Tolong buat konten yang menampilkan penggunaan produk dalam kehidupan sehari-hari. Fokus pada manfaat dan kemudahan penggunaannya.',
                'Untuk konten ini, kita ingin menampilkan sisi lifestyle yang natural. Gunakan pencahayaan natural dan setting yang casual.',
                'Brief untuk campaign ini: tolong highlight fitur utama produk dengan cara yang kreatif. Bisa dalam format tutorial atau daily vlog.',
            ],
            'PROGRESS': [
                'Sudah selesai syuting untuk konten pertama. Draft video sedang dalam proses editing. Akan selesai dalam 2 hari.',
                'Update progress: 70% konten sudah selesai. Tinggal finishing touch untuk color grading dan musik background.',
                'Konten sudah siap 90%. Sedang menambahkan caption dan hashtag yang sesuai dengan brief.',
            ],
            'REVISION': [
                'Mohon tambahkan close-up shot untuk detail produk. Perlu lebih jelas menampilkan packaging dan tekstur produk.',
                'Tolong sesuaikan tone warna agar lebih cerah dan sesuai dengan brand guidelines yang sudah diberikan.',
                'Perlu revisi untuk bagian opening, tolong buat lebih catchy dan tambahkan key message di 10 detik pertama.',
            ],
            'FEEDBACK': [
                'Hasil konten sudah bagus! Angle pengambilan gambar sangat sesuai dengan yang diharapkan. Lanjutkan untuk konten berikutnya.',
                'Sangat puas dengan hasil akhirnya. Engagement dari followers juga sangat positif. Good job!',
                'Terima kasih atas kerja kerasnya. Konten yang dihasilkan sangat sesuai dengan brief dan target market kita.',
            ]
        }

        attachment_urls = [
            'https://drive.google.com/file/sample1',
            'https://drive.google.com/file/sample2',
            'https://wetransfer.com/sample1',
            'https://wetransfer.com/sample2',
        ]

        for collab in active_collaborations:
            # Create BRIEF from advertiser
            ProjectUpdate.objects.create(
                collaboration=collab,
                sender=collab.project.advertiser,
                update_type='BRIEF',
                content=random.choice(update_contents['BRIEF']),
                attachment_url=random.choice(attachment_urls) if random.choice([True, False]) else ''
            )

            # Create 2-3 PROGRESS updates from influencer
            for _ in range(random.randint(2, 3)):
                ProjectUpdate.objects.create(
                    collaboration=collab,
                    sender=collab.influencer,
                    update_type='PROGRESS',
                    content=random.choice(update_contents['PROGRESS']),
                    attachment_url=random.choice(attachment_urls) if random.choice([True, False]) else ''
                )

            # Maybe add revision request (50% chance)
            if random.choice([True, False]):
                ProjectUpdate.objects.create(
                    collaboration=collab,
                    sender=collab.project.advertiser,
                    update_type='REVISION',
                    content=random.choice(update_contents['REVISION']),
                    attachment_url=random.choice(attachment_urls) if random.choice([True, False]) else ''
                )

                # Add progress update after revision
                ProjectUpdate.objects.create(
                    collaboration=collab,
                    sender=collab.influencer,
                    update_type='PROGRESS',
                    content='Revisi sudah selesai dikerjakan sesuai permintaan. Mohon dicek kembali.',
                    attachment_url=random.choice(attachment_urls) if random.choice([True, False]) else ''
                )

            # Add final feedback
            ProjectUpdate.objects.create(
                collaboration=collab,
                sender=collab.project.advertiser,
                update_type='FEEDBACK',
                content=random.choice(update_contents['FEEDBACK']),
                attachment_url=''
            )

            self.stdout.write(f'Created interaction data for collaboration: {collab.project.title} - {collab.influencer.get_full_name()}') 