from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ChemIdList, ChemPropertyList, TwConcernedChem, TwControlledChem, TwPriorityChem,  TwToxicChem
from .serializers import ChemIdListSerializer, ChemPropertyListSerializer, TwConcernedChemSerializer, TwControlledChemSerializer, TwPriorityChemSerializer, TwToxicChemSerializer, CheckDataSerializer


from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django_filters import rest_framework

def home(request):
    return render(request,'home.html')


#控制最後輸出API，是一次顯示全部還是10個資料(page_size )
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page"

#Create your views here.
class ChemIdListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ChemIdList.objects.all().order_by('id')   #ModelViewSet擁有 CRUD 的全部功能
    http_method_names = ['get']   #限制只能使用get

    serializer_class = ChemIdListSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cas_rn', 'ec_number']

    permission_classes = (AllowAny,)



class ChemPropertyListViewSet(viewsets.ModelViewSet):

    queryset = ChemPropertyList.objects.all().order_by('id')
    http_method_names = ['get'] 
    serializer_class = ChemPropertyListSerializer

    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cas_no']

    permission_classes = (AllowAny,)



class TwConcernedChemViewSet(viewsets.ModelViewSet):

    queryset = TwConcernedChem.objects.all().order_by('index')
    http_method_names = ['get'] 
    serializer_class = TwConcernedChemSerializer

    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cas_no']

    permission_classes = (AllowAny,)



class TwControlledChemViewSet(viewsets.ModelViewSet):

    queryset = TwControlledChem.objects.all().order_by('index')
    http_method_names = ['get'] 
    serializer_class = TwControlledChemSerializer

    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cas_no']

    permission_classes = (AllowAny,)


class TwPriorityChemViewSet(viewsets.ModelViewSet):

    queryset = TwPriorityChem.objects.all().order_by('index')
    http_method_names = ['get'] 
    serializer_class = TwPriorityChemSerializer 

    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cas_no']

    permission_classes = (AllowAny,)


class TwToxicChemViewSet(viewsets.ModelViewSet):

    queryset = TwToxicChem.objects.all().order_by('index')
    http_method_names = ['get'] 
    serializer_class = TwToxicChemSerializer

    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cas_no']

    permission_classes = (AllowAny,)



class CheckDataViewSet(viewsets.ModelViewSet):
    http_method_names = ['get'] 
    filterset_fields = ['cas_no']
    filter_backends = [DjangoFilterBackend]
    serializer_class = CheckDataSerializer

    def list(self, request):
        cas_no = request.query_params.get('cas_no')
        data = {}
        for model in [TwConcernedChem, TwControlledChem, TwPriorityChem, TwToxicChem]:
            if cas_no:
                # print(f"Querying model {model.__name__} with cas_no={cas_no}")
                queryset = model.objects.filter(Q(cas_no=cas_no) | Q(cas_no__isnull=True))
                # print(f"Resulting queryset for model {model.__name__}: {queryset}")
                if queryset.exists():
                    serializer = self.serializer_class(context={'request': request})
                    data[model.__name__.lower()] = serializer.data
                    data['concern_data'] = serializer.get_concern_data(cas_no)
                    data['control_data'] = serializer.get_control_data(cas_no)
                    data['priority_data'] = serializer.get_priority_data(cas_no)
                    data['toxic_data'] = serializer.get_toxic_data(cas_no)

        if not data:
            return Response({'message': '無相關資料'})
        return Response(data)













