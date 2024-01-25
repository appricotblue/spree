# Generated by Django 4.1.3 on 2024-01-24 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SpreeApp', '0025_product_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='voucher_type_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('description', models.TextField(default='', null=True)),
                ('start_index', models.CharField(default='', max_length=100, null=True)),
                ('created_at', models.DateTimeField(default='', max_length=100)),
                ('updated_at', models.DateTimeField(default='', max_length=100)),
                ('branch_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='SpreeApp.branch_data')),
                ('type_of_voucher', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voucher_type', to='SpreeApp.voucher_type_data')),
            ],
        ),
    ]
