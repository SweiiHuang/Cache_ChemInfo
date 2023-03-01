from django.urls import path, include
from rest_framework import routers
from .views import ChemIdListViewSet, ChemPropertyListViewSet,TwConcernedChemViewSet, TwControlledChemViewSet, TwPriorityChemViewSet, TwToxicChemViewSet, CheckDataViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ChemIdList', ChemIdListViewSet, basename='ChemIdList')
router.register(r'ChemPropertyList', ChemPropertyListViewSet, basename='ChemPropertyList')

router.register(r'TwConcernedChem', TwConcernedChemViewSet, basename='twconcernedchem')
router.register(r'TwControlledChem', TwControlledChemViewSet, basename='twcontrolledchem')
router.register(r'TwPriorityChem', TwPriorityChemViewSet, basename='twprioritychem')
router.register(r'TwToxicChem', TwToxicChemViewSet, basename='twtoxicchem')

router.register(r'CheckData', CheckDataViewSet, basename='checkdata')


urlpatterns = router.urls