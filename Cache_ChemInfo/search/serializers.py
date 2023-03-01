# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ChemIdList, ChemPropertyList, TwConcernedChem,  TwControlledChem, TwPriorityChem,  TwToxicChem
from django.db.models import Q


class ChemPropertyListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChemPropertyList
        fields = ['name', 'cas_no', 'image', 'molecular_formula', 'molecular_mass', 'boiling_point', 'melting_point', 'density']


class ChemIdListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = ChemIdList
        fields = ['name', 'cus_number','cas_rn','cn_code','ec_number','un_number']


class TwConcernedChemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TwConcernedChem
        fields = '__all__' #所有欄位

class  TwControlledChemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model =  TwControlledChem
        fields = '__all__' 

class  TwPriorityChemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model =  TwPriorityChem
        fields = '__all__' 

class   TwToxicChemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model =   TwToxicChem
        fields = '__all__' 



class CheckDataSerializer(serializers.Serializer):
    concern_data = serializers.SerializerMethodField()
    control_data = serializers.SerializerMethodField()
    priority_data = serializers.SerializerMethodField()
    toxic_data = serializers.SerializerMethodField()

    def get_concern_data(self, cas_no):
        queryset = TwConcernedChem.objects.filter(Q(cas_no=cas_no) | Q(cas_no__isnull=True)).first()
        if queryset:
            serializer = TwConcernedChemSerializer(queryset, context={'request': self.context.get('request')})
            return serializer.data
        return None
    
    def get_control_data(self, cas_no):
        queryset = TwControlledChem.objects.filter(Q(cas_no=cas_no) | Q(cas_no__isnull=True)).first()
        if queryset:
            serializer = TwControlledChemSerializer(queryset, context={'request': self.context.get('request')})
            return serializer.data
        return None
    
    def get_priority_data(self, cas_no):
        queryset = TwPriorityChem.objects.filter(Q(cas_no=cas_no) | Q(cas_no__isnull=True)).first()
        if queryset:
            serializer = TwPriorityChemSerializer(queryset, context={'request': self.context.get('request')})
            return serializer.data
        return None
    
    def get_toxic_data (self, cas_no):
        queryset = TwToxicChem.objects.filter(Q(cas_no=cas_no) | Q(cas_no__isnull=True)).first()
        if queryset:
            serializer = TwToxicChemSerializer(queryset, context={'request': self.context.get('request')})
            return serializer.data
        return None
