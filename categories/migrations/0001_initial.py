# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.TextField(unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunSQL([
            ('INSERT INTO categories_category (id, created, modified, name) VALUES (%s,%s,%s,%s);',
                [1, '2016/1/1', '2016/1/1', '/(not categorized)/'])],
        )

    ]
