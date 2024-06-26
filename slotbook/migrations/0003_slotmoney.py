# Generated by Django 4.2.11 on 2024-04-17 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctorUser', '0002_alter_customuser_phone'),
        ('slotbook', '0002_slot_store_alter_slot_description_alter_slot_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlotMoney',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField(null=True)),
                ('total_amount', models.TextField(null=True)),
                ('amount', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctorUser.customuser')),
            ],
        ),
    ]
