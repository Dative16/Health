# Generated by Django 5.0.7 on 2024-08-01 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MedicalHistory', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentmedication',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.patient'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='health_care_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.healthcareprovider'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedicalHistory.hospital'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.patient'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedicalHistory.currentmedication'),
        ),
    ]