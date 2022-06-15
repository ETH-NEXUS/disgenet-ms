from rest_framework import serializers

from api.models import VariantDiseaseNetwork


class VariantDiseaseNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantDiseaseNetwork
        fields = (
            'variantid',
            'gene_symbol',
            'variant_dsi',
            'variant_dpi',
            'variant_consequence_type',
            'diseaseid',
            'disease_name',
            'disease_class',
            'disease_class_name',
            'disease_type',
            'disease_semantic_type',
            'score',
            'ei',
            'year_initial',
            'year_final',
            'details'
        )
