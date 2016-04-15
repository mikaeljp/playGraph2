# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-14 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BggPlay',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField(db_index=True)),
                ('quantity', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BggThing',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('thumbnail', models.CharField(max_length=255)),
                ('year_published', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BggUser',
            fields=[
                ('id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('avatar_link', models.CharField(blank=True, max_length=255)),
                ('year_registered', models.IntegerField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='bggplay',
            name='thing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playgraph.BggThing'),
        ),
        migrations.AddField(
            model_name='bggplay',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plays', to='playgraph.BggUser'),
        ),
    ]
