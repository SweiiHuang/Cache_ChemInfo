from django.db import models

# Create your models here.
class ChemPropertyList(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.TextField()
    cas_no = models.CharField(max_length=255)
    image = models.TextField(blank=True, null=True)
    molecular_formula = models.CharField(max_length=255, blank=True, null=True)
    molecular_mass = models.CharField(max_length=255, blank=True, null=True)
    boiling_point = models.CharField(max_length=255, blank=True, null=True)
    melting_point = models.CharField(max_length=255, blank=True, null=True)
    density = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  
        # Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
        db_table = 'chem_property_list' 
        # define models that match the tables in existing database



class ChemIdList(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.TextField()
    cus_number = models.CharField(max_length=255)
    cas_rn = models.CharField(max_length=255)
    cn_code = models.CharField(max_length=255, blank=True, null=True)
    ec_number = models.CharField(max_length=255, blank=True, null=True)
    un_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'chem_id_list'



class TwConcernedChem(models.Model):
    index = models.BigIntegerField(primary_key=True, db_column='index')
    item = models.BigIntegerField(blank=True, null=True)
    list_no = models.TextField(blank=True, null=True)
    en_name = models.TextField(blank=True, null=True)
    cn_name = models.TextField(blank=True, null=True)
    cas_no = models.TextField(blank=True, null=True,db_index=True)
    control_conc = models.TextField(blank=True, null=True)
    grading_volume = models.TextField(blank=True, null=True)
    hazardous = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tw_concerned_chem'


class TwControlledChem(models.Model):
    index = models.BigIntegerField(primary_key=True, db_column='index')
    cas_no = models.TextField(blank=True, null=True,db_index=True)
    cn_name = models.TextField(blank=True, null=True)
    en_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tw_controlled_chem'


class TwPriorityChem(models.Model):
    index = models.BigIntegerField(primary_key=True, db_column='index')
    cas_no = models.TextField(blank=True, null=True,db_index=True)
    en_name = models.TextField(blank=True, null=True)
    cn_name = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tw_priority_chem'


class TwToxicChem(models.Model):
    index = models.BigIntegerField(primary_key=True, db_column='index')
    item = models.BigIntegerField(blank=True, null=True)
    list_no = models.TextField(blank=True, null=True)
    en_name = models.TextField(blank=True, null=True)
    cn_name = models.TextField(blank=True, null=True)
    cas_no = models.TextField(blank=True, null=True,db_index=True)
    control_conc = models.TextField(blank=True, null=True)
    grading_volume = models.FloatField(blank=True, null=True)
    toxic_class = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tw_toxic_chem'