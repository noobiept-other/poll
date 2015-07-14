# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('text', models.CharField(max_length=20)),
                ('votes_count', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, help_text='Date Created')),
                ('is_single_choice', models.BooleanField(default=True)),
                ('is_opened', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('poll', models.ForeignKey(to='poll.Poll')),
                ('voter', models.ForeignKey(related_name='voter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='option',
            name='poll',
            field=models.ForeignKey(to='poll.Poll'),
        ),
    ]
