# Generated by Django 3.0.8 on 2020-09-28 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200928_1049'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ListingComments',
            new_name='ListingComment',
        ),
        migrations.AddField(
            model_name='listings',
            name='isClosed',
            field=models.BooleanField(default=False),
        ),
    ]
