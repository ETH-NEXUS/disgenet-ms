from rest_framework.generics import ListAPIView
from rest_framework.reverse import reverse
from api.models import VariantAttributes
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import VariantDiseaseNetwork
from api.serializers import VariantDiseaseNetworkSerializer
from rest_framework.pagination import CursorPagination
from django_filters.rest_framework import DjangoFilterBackend


class CursorSetPagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = 'nid'


class Vda(APIView):
    def get_object(self, variantid):
        try:
            return VariantAttributes.objects.filter(variantid=variantid)[0]
        except VariantAttributes.DoesNotExist:
            raise Http404

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('year', 'source', 'score', 'ei', 'pmid')

    def get(self, request, variantid):
        variant = self.get_object(variantid)
        variantid = variant.variantid
        association = VariantDiseaseNetwork.objects.filter(
            variantid=variantid)[0]
        serializer = VariantDiseaseNetworkSerializer(association)
        return Response(serializer.data)


class VdaList(ListAPIView):
    queryset = VariantDiseaseNetwork.objects.all()
    serializer_class = VariantDiseaseNetworkSerializer
    pagination_class = CursorSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('year', 'source', 'score', 'ei', 'pmid')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'vdaList': reverse('vda_list', request=request, format=format),
    })
