# Generated by Django 3.0.8 on 2020-09-28 10:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_listingcomments_listings'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='by',
            field=models.CharField(default=django.utils.timezone.now, max_length=120),
            preserve_default=False,
        ),
    ]
