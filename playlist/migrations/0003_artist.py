# Generated by Django 4.0.3 on 2022-03-17 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0002_alter_sections_confidence_alter_sections_duration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('avg_tempo', models.FloatField()),
                ('avg_energy', models.FloatField()),
                ('avg_valence', models.FloatField()),
                ('avg_loudness', models.FloatField()),
                ('avg_key', models.FloatField()),
                ('search_count', models.IntegerField()),
            ],
        ),
    ]