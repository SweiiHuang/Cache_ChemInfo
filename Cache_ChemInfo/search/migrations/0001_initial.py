# Generated by Django 4.1.6 on 2023-02-19 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChemIdList',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('cus_number', models.CharField(max_length=255)),
                ('cas_rn', models.CharField(max_length=255)),
                ('cn_code', models.CharField(blank=True, max_length=255, null=True)),
                ('ec_number', models.CharField(blank=True, max_length=255, null=True)),
                ('un_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'chem_id_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ChemPropertyList',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('cas_no', models.CharField(max_length=255)),
                ('image', models.TextField(blank=True, null=True)),
                ('molecular_formula', models.CharField(blank=True, max_length=255, null=True)),
                ('molecular_mass', models.CharField(blank=True, max_length=255, null=True)),
                ('boiling_point', models.CharField(blank=True, max_length=255, null=True)),
                ('melting_point', models.CharField(blank=True, max_length=255, null=True)),
                ('density', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'chem_property_list',
                'managed': False,
            },
        ),
    ]