from rest_framework import serializers

from api.models import VariantDiseaseNetwork


class VariantDiseaseNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantDiseaseNetwork
        fields = ('nid',
                  'variantid',
                  'gene_symbol',
                  'variant_dsi',
                  'variant_dpi',
                  'variant_consequence_type',
                  'diseaseid',
                  'disease_name',
                  'disease_class',
                  'class_name',
                  'disease_type',
                  'score',
                  'ei',
                  'year',
                  'source'
                  )
