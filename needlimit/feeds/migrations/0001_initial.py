# Generated by Django 3.2 on 2021-04-26 16:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crawling_interval', models.DurationField(default=datetime.timedelta(seconds=3600))),
                ('html_link', models.URLField()),
                ('last_crawled', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('xml_link', models.URLField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('published', models.DateTimeField()),
                ('summary', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feeds.feed')),
            ],
            options={
                'verbose_name_plural': 'feed entries',
            },
        ),
    ]