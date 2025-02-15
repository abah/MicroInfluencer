# MicroInfluencer Platform

Platform yang menghubungkan pengiklan dengan micro-influencer untuk kolaborasi kampanye pemasaran yang efektif.

## Fitur Utama

### Untuk Influencer
- Buat profil influencer dengan detail follower, niche, dan bio
- Jelajahi proyek yang tersedia dari pengiklan
- Ajukan diri untuk proyek yang diminati
- Pantau status kolaborasi (Pending, Approved, In Progress, Completed)
- Lihat riwayat proyek yang telah diselesaikan

### Untuk Pengiklan (Advertiser)
- Buat profil perusahaan dengan detail industri dan deskripsi
- Posting proyek kampanye dengan detail budget dan persyaratan
- Kelola aplikasi dari influencer
- Pantau progress kolaborasi yang sedang berjalan
- Lihat riwayat kampanye yang telah selesai

## Teknologi

- Django 5.0.2
- Python 3.11
- Bootstrap 5
- SQLite Database
- Django Allauth untuk autentikasi

## Instalasi

1. Clone repository
```bash
git clone https://github.com/username/MicroInfluencer.git
cd MicroInfluencer
```

2. Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Jalankan migrasi database
```bash
python manage.py migrate
```

5. Buat superuser
```bash
python manage.py createsuperuser
```

6. Jalankan server
```bash
python manage.py runserver
```

## Status Proyek dan Kolaborasi

### Status Proyek
- PENDING: Proyek baru dibuat dan menunggu aplikasi dari influencer
- IN_PROGRESS: Minimal satu influencer telah disetujui dan sedang mengerjakan
- COMPLETED: Semua kolaborasi telah selesai
- CANCELLED: Proyek dibatalkan

### Status Kolaborasi
- PENDING: Influencer mengajukan diri dan menunggu persetujuan
- APPROVED: Pengajuan diterima, menunggu dimulai
- IN_PROGRESS: Influencer sedang mengerjakan konten
- COMPLETED: Kolaborasi selesai
- REJECTED: Pengajuan ditolak
- CANCELLED: Kolaborasi dibatalkan

## Alur Kerja

1. Pengiklan membuat proyek baru (status: PENDING)
2. Influencer mengajukan diri (status kolaborasi: PENDING)
3. Pengiklan menyetujui/menolak pengajuan
4. Jika disetujui:
   - Status kolaborasi berubah menjadi APPROVED
   - Status proyek berubah menjadi IN_PROGRESS
5. Influencer mulai mengerjakan (status kolaborasi: IN_PROGRESS)
6. Setelah selesai, pengiklan menandai sebagai COMPLETED
7. Jika semua kolaborasi selesai, proyek otomatis ditandai COMPLETED

## Kontribusi

Silakan buat pull request untuk kontribusi. Untuk perubahan besar, harap buka issue terlebih dahulu.

## Lisensi

[MIT License](LICENSE) 