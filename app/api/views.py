from rest_framework import viewsets
from api.models import Variantattributes, Variantdiseasenetwork, Diseaseattributes, Disease2Class, Geneattributes, Genediseasenetwork
from api.serializers import VariantAttributesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch


class Vda(viewsets.ReadOnlyModelViewSet):
    serializer_class = VariantAttributesSerializer
    filter_backends = (DjangoFilterBackend,)
    lookup_field = 'variantid'

    def get_queryset(self):
        return Variantattributes.objects.prefetch_related(
            Prefetch(
                'variantdiseasenetwork_set',
                queryset=Variantdiseasenetwork.objects
                .prefetch_related(
                    Prefetch(
                        'diseasenid',
                        queryset=Diseaseattributes.objects.prefetch_related(
                            Prefetch(
                                'disease2class_set',
                                queryset=Disease2Class.objects
                                .select_related('diseaseclassnid')
                            ),
                            Prefetch(
                                'genediseasenetwork_set',
                                queryset=Genediseasenetwork.objects
                                .select_related('genenid')
                            )
                        )
                    )
                )
            )
        )
