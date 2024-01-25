# Generated by Django 4.1.3 on 2024-01-21 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SpreeApp', '0012_location_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='supplier_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='', null=True)),
                ('created_at', models.DateTimeField(default='', max_length=100)),
                ('updated_at', models.DateTimeField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='supplier_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('phone', models.CharField(default='', max_length=100, null=True)),
                ('email', models.CharField(default='', max_length=100, null=True)),
                ('supplier_code', models.CharField(default='', max_length=100, null=True)),
                ('opening_balance', models.CharField(default='', max_length=100, null=True)),
                ('entry_type', models.CharField(default='', max_length=100, null=True)),
                ('bill_by_bill', models.CharField(default='', max_length=100, null=True)),
                ('credit_period', models.CharField(default='', max_length=100, null=True)),
                ('credit_limit', models.CharField(default='', max_length=100, null=True)),
                ('address', models.CharField(default='', max_length=100, null=True)),
                ('city', models.CharField(default='', max_length=100, null=True)),
                ('state', models.CharField(default='', max_length=100, null=True)),
                ('country', models.CharField(default='', max_length=100, null=True)),
                ('pincode', models.CharField(default='', max_length=100, null=True)),
                ('account_number', models.CharField(default='', max_length=100, null=True)),
                ('branch_name', models.CharField(default='', max_length=100, null=True)),
                ('branch_code', models.CharField(default='', max_length=100, null=True)),
                ('tin', models.CharField(default='', max_length=100, null=True)),
                ('pan', models.CharField(default='', max_length=100, null=True)),
                ('cst', models.CharField(default='', max_length=100, null=True)),
                ('active', models.BooleanField(default=0, max_length=100)),
                ('created_at', models.DateTimeField(default='', max_length=100)),
                ('updated_at', models.DateTimeField(default='', max_length=100)),
                ('branch_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='SpreeApp.branch_data')),
                ('supplier_type_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='SpreeApp.supplier_type')),
            ],
        ),
        migrations.CreateModel(
            name='customer_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('phone', models.CharField(default='', max_length=100, null=True)),
                ('email', models.CharField(default='', max_length=100, null=True)),
                ('customer_code', models.CharField(default='', max_length=100, null=True)),
                ('opening_balance', models.CharField(default='', max_length=100, null=True)),
                ('entry_type', models.CharField(default='', max_length=100, null=True)),
                ('bill_by_bill', models.CharField(default='', max_length=100, null=True)),
                ('credit_period', models.CharField(default='', max_length=100, null=True)),
                ('credit_limit', models.CharField(default='', max_length=100, null=True)),
                ('address', models.CharField(default='', max_length=100, null=True)),
                ('city', models.CharField(default='', max_length=100, null=True)),
                ('state', models.CharField(default='', max_length=100, null=True)),
                ('country', models.CharField(default='', max_length=100, null=True)),
                ('pincode', models.CharField(default='', max_length=100, null=True)),
                ('account_number', models.CharField(default='', max_length=100, null=True)),
                ('branch_name', models.CharField(default='', max_length=100, null=True)),
                ('branch_code', models.CharField(default='', max_length=100, null=True)),
                ('tin', models.CharField(default='', max_length=100, null=True)),
                ('pan', models.CharField(default='', max_length=100, null=True)),
                ('cst', models.CharField(default='', max_length=100, null=True)),
                ('active', models.BooleanField(default=0, max_length=100)),
                ('created_at', models.DateTimeField(default='', max_length=100)),
                ('updated_at', models.DateTimeField(default='', max_length=100)),
                ('branch_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='SpreeApp.branch_data')),
                ('customer_type_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='SpreeApp.customer_type')),
                ('location_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='SpreeApp.location_data')),
            ],
        ),
    ]