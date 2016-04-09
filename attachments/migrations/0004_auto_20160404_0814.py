# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0003_auto_20160130_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=core.fields.ContentTypeRestrictedFileField(upload_to='attachments'),
        ),
    ]
