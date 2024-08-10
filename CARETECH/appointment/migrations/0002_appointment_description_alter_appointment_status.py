# Generated by Django 5.0.8 on 2024-08-08 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('requested', 'requested'), ('scheduled', 'scheduled'), ('completed', 'completed'), ('cancelled', 'cancelled'), ('approved', 'approved')], max_length=100),
        ),
    ]
