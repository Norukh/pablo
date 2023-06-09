# Generated by Django 4.2 on 2023-04-25 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pablo_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("years", models.CharField(max_length=50)),
                ("nationality", models.CharField(max_length=255)),
                ("bio", models.CharField(max_length=4000)),
                ("wikipedia", models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name="Painting",
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
                ("name", models.CharField(max_length=4000)),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pablo_app.artist",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(max_length=255)),
                ("artist", models.ManyToManyField(to="pablo_app.artist")),
            ],
        ),
    ]
