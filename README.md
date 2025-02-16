# MicroInfluencer Platform

Platform yang menghubungkan micro-influencer dengan brand untuk kolaborasi yang lebih efektif.

## Fitur Utama

### Untuk Influencer
- Profil lengkap dengan statistik engagement dan follower count
- Integrasi dengan Instagram, TikTok, dan YouTube
- Manajemen kolaborasi dengan interface yang intuitif
- Status tracking untuk setiap proyek (Aktif, Menunggu, Selesai, Dibatalkan)
- Sistem komunikasi terintegrasi dengan advertiser
- Interface modern dengan efek visual yang menarik

### Untuk Advertiser
- Dashboard manajemen proyek yang komprehensif
- Sistem review aplikasi influencer yang efisien
- Tracking status kolaborasi real-time
- Manajemen multi-proyek dalam satu interface
- Sistem feedback dan rating terintegrasi
- Analisis performa kampanye

## Teknologi

- Backend: Django 5.0.2
- Frontend: Bootstrap 5, SASS, JavaScript
- Database: PostgreSQL
- Authentication: Django-allauth
- UI/UX: Modern design dengan gradient dan efek visual
- Responsive design untuk semua device

## Persyaratan Sistem

- Python 3.11+
- PostgreSQL 14+
- Node.js 18+ (untuk asset compilation)

## Instalasi

1. Clone repository:
```bash
git clone https://github.com/abah/MicroInfluencer.git
cd MicroInfluencer
```

2. Buat virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup database:
```bash
python manage.py migrate
```

5. Buat superuser:
```bash
python manage.py createsuperuser
```

6. Jalankan server:
```bash
python manage.py runserver
```

## Fitur Terbaru

### UI/UX Improvements
- Modern gradient design untuk header dan cards
- Efek hover yang responsif pada semua elemen
- Status badges dengan warna yang intuitif
- Layout grid yang adaptif
- Optimasi untuk mobile devices

### Sistem Kolaborasi
- Status tracking yang lebih detail
- Interface komunikasi yang terintegrasi
- Sistem notifikasi real-time
- Manajemen multi-proyek
- Timeline aktivitas proyek

### Profil Influencer
- Statistik engagement yang detail
- Integrasi multi-platform social media
- Portfolio showcase
- Analytics dashboard
- Performance metrics

## Struktur Proyek

```
MicroInfluencer/
├── core/                   # App utama
│   ├── templates/         # Template HTML
│   ├── static/           # Assets
│   ├── models.py         # Model data
│   └── views.py          # Logic
├── static/               # Global static files
│   ├── css/             # Compiled CSS
│   ├── js/              # JavaScript
│   └── images/          # Media files
├── templates/           # Global templates
└── microinfluencer/    # Konfigurasi proyek
```

## Kontribusi

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

## Kontak

Abah - [@abahraditya](https://twitter.com/abahraditya)

Project Link: [https://github.com/abah/MicroInfluencer](https://github.com/abah/MicroInfluencer) 