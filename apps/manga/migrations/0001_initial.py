# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('number', models.IntegerField(verbose_name='Capitulo #:')),
            ],
            options={
                'verbose_name': 'Chapter',
                'verbose_name_plural': 'Chapters',
            },
        ),
        migrations.CreateModel(
            name='ChapterPicture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('number', models.IntegerField(verbose_name='')),
                ('picture', models.ImageField(upload_to=b'')),
                ('chapter', models.ForeignKey(to='manga.Chapter')),
            ],
            options={
                'verbose_name': 'ChapterPicture',
                'verbose_name_plural': 'ChapterPictures',
            },
        ),
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='name', editable=False)),
            ],
            options={
                'verbose_name': 'Manga',
                'verbose_name_plural': 'Mangas',
            },
        ),
        migrations.AddField(
            model_name='chapter',
            name='manga',
            field=models.ForeignKey(to='manga.Manga'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='upload_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
