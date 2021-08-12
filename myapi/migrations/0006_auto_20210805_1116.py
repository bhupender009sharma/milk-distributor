# Generated by Django 3.2.6 on 2021-08-05 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0005_alter_dailydistribution_type_of_milk'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailydistribution',
            name='customer_id',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='distributionrequired',
            name='customer_id',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='customers',
            name='mobile',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='customers',
            name='pincode',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]