# Generated by Django 4.2.11 on 2024-04-08 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slotEntry', '0003_slotentry_seat_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='slotentry',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
