# Generated by Django 5.0.2 on 2025-02-16 07:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_advertiserprofile_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collaboration",
            options={"ordering": ["-updated_at"]},
        ),
        migrations.CreateModel(
            name="ProjectUpdate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "update_type",
                    models.CharField(
                        choices=[
                            ("BRIEF", "Brief dari Advertiser"),
                            ("PROGRESS", "Update Progress"),
                            ("REVISION", "Permintaan Revisi"),
                            ("FEEDBACK", "Feedback"),
                        ],
                        max_length=20,
                    ),
                ),
                ("content", models.TextField(help_text="Isi update/brief/feedback")),
                (
                    "attachment_url",
                    models.URLField(
                        blank=True,
                        help_text="Link ke file pendukung (gambar/video/dokumen)",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "collaboration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="updates",
                        to="core.collaboration",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_updates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Project Update",
                "verbose_name_plural": "Project Updates",
                "ordering": ["-created_at"],
            },
        ),
    ]
