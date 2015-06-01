# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField()),
                ('uuid', models.CharField(default=uuid.uuid1, max_length=36, editable=False)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('graph', models.ForeignKey(to='graph.DiGraph')),
            ],
        ),
        migrations.AddField(
            model_name='arc',
            name='index_from',
            field=models.ForeignKey(related_name='_from', to='graph.Node'),
        ),
        migrations.AddField(
            model_name='arc',
            name='index_to',
            field=models.ForeignKey(related_name='_to', to='graph.Node'),
        ),
    ]
