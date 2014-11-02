# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_key', models.CharField(max_length=250)),
                ('user_ip', models.GenericIPAddressField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
