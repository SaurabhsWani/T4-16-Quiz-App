# Generated by Django 3.0.5 on 2021-05-02 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main_Quiz_App', '0002_auto_20210501_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='formtitle',
            name='User_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]