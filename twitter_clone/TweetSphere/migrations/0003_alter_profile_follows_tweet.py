# Generated by Django 5.0.6 on 2024-07-19 17:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TweetSphere', '0002_profile_date_modified'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='TweetSphere.profile'),
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tweets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]