from typing import OrderedDict
from django.forms import SlugField
from rest_framework import serializers
from api.models import Variantdiseasenetwork, Variantattributes, Diseaseattributes, Disease2Class, Diseaseclass
from django .core.exceptions import ObjectDoesNotExist


class DiseaseAttributesSerializer(serializers.ModelSerializer):
    disease_class = serializers.SerializerMethodField()
    disease_class_name = serializers.SerializerMethodField()

    def get_disease_class(self, obj):
        disease2class = obj.disease2class_set.all()
        if not disease2class:
            return None
        classes = []
        for cls in disease2class:
            classes.append(cls.diseaseclassnid.diseaseclass)
        return classes

    def get_disease_class_name(self, obj):
        disease2class = obj.disease2class_set.all()
        if not disease2class:
            return None
        classes = []
        for cls in disease2class:
            classes.append(cls.diseaseclassnid.diseaseclassname.strip())
        return classes

    class Meta:
        model = Diseaseattributes
        fields = '__all__'


class VariantDiseaseNetworkSerializer(serializers.ModelSerializer):
    disease = DiseaseAttributesSerializer(source='diseasenid')

    class Meta:
        model = Variantdiseasenetwork
        fields = '__all__'


class VariantAttributesSerializer(serializers.ModelSerializer):
    evidences = VariantDiseaseNetworkSerializer(
        source='variantdiseasenetwork_set', many=True)

    def to_representation(self, instance):
        data = super(serializers.ModelSerializer,
                     self).to_representation(instance)
        temp = {}
        for evidence in data.get('evidences'):
            disease = evidence.get('disease')
            diseaseid = disease.get('diseaseid')
            if not diseaseid in temp:
                temp[diseaseid] = {
                    "diseaseid": disease.get('diseaseid'),
                    "disease_name": disease.get('diseasename'),
                    "disease_type": disease.get('type'),
                    "disease_class": disease.get('disease_class'),
                    "disease_class_name": disease.get('disease_class_name'),
                    "year_initial": evidence.get('year'),
                    "year_final": evidence.get('year'),
                    "evidences": []
                }
            temp[diseaseid]['evidences'].append(
                {
                    "source": evidence.get('source'),
                    "sentence": evidence.get('sentence'),
                    "pmid": evidence.get('pmid'),
                    "year": evidence.get('year')
                }
            )
            temp[diseaseid]['year_initial'] = min(
                temp[diseaseid]['year_initial'], evidence.get('year'))
            temp[diseaseid]['year_final'] = max(
                temp[diseaseid]['year_final'], evidence.get('year'))
        del data['evidences']
        data['diseases'] = []
        for t in temp.values():
            data['diseases'].append(t)
        return data

    class Meta:
        model = Variantattributes
        fields = '__all__'
