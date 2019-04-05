# Generated by Django 2.1.7 on 2019-04-05 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0002_auto_20190405_1616'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='availableability',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='availableability',
            name='ability',
        ),
        migrations.RemoveField(
            model_name='availableability',
            name='species',
        ),
        migrations.DeleteModel(
            name='AvailableAbility',
        ),
    ]
