# Generated by Django 3.1.2 on 2020-10-20 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201020_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usrListings', to='auctions.user'),
        ),
    ]
