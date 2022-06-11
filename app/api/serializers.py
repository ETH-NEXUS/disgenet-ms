from rest_framework import serializers

from api.models import VariantDiseaseNetwork


class VariantDiseaseNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantDiseaseNetwork
        fields = ('nid', 'source', 'sentence',
                  'year',
                  'diseaseid',
                  'disease_name',
                  'disease_type',
                  'score',
                  'ei',
                  'variantid',
                  'variant_dsi',
                  'variant_dpi',
                  'variant_consequence_type',
                  'gene_symbol',
                  )

