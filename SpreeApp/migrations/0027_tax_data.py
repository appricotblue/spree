# Generated by Django 4.1.3 on 2024-01-25 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SpreeApp', '0026_voucher_type_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='tax_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax', models.CharField(default='', max_length=100, null=True)),
                ('rate_perc', models.CharField(default='', max_length=100, null=True)),
                ('description', models.TextField(default='', null=True)),
                ('active', models.BooleanField(default=0, max_length=100)),
                ('created_at', models.DateTimeField(default='', max_length=100)),
                ('updated_at', models.DateTimeField(default='', max_length=100)),
                ('branch_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='SpreeApp.branch_data')),
            ],
        ),
    ]
