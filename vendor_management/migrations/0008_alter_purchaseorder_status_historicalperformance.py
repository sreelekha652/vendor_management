# Generated by Django 5.0.1 on 2024-05-02 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_management', '0007_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('completed', 'completed')], default='Pending', max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='HistoricalPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('on_time_delivery_rate', models.FloatField()),
                ('quality_rating_avg', models.FloatField()),
                ('average_response_time', models.FloatField()),
                ('fulfillment_rate', models.FloatField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor_management.vendor')),
            ],
        ),
    ]