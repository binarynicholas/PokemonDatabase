# Generated by Django 2.1.7 on 2019-04-10 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0012_auto_20190410_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='form',
            field=models.CharField(default='Base', max_length=10),
        ),
    ]