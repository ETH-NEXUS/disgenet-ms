from rest_framework import serializers
from api.models import Variantdiseasenetwork, Variantattributes, Diseaseattributes, Variantgene, Geneattributes


class GeneAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geneattributes
        fields = '__all__'


class VariantGeneSerializer(serializers.ModelSerializer):
    gene = GeneAttributeSerializer(source='genenid')

    class Meta:
        model = Variantgene
        fields = '__all__'


class DiseaseAttributesSerializer(serializers.ModelSerializer):
    disease_class = serializers.SerializerMethodField()
    disease_class_name = serializers.SerializerMethodField()

    # gene_symbol = serializers.SerializerMethodField()

    def __get_gene_attributes_property(self, obj, property):
        geneDiseaseNetworks = obj.genediseasenetwork_set.all()
        if not geneDiseaseNetworks:
            return None
        gene_diseases = []
        for gdn in geneDiseaseNetworks:
            gene_diseases.append(getattr(gdn.genenid, property).strip())
        return gene_diseases

    def __get_disease_class_property(self, obj, property):
        disease2class = obj.disease2class_set.all()
        if not disease2class:
            return None
        classes = []
        for cls in disease2class:
            classes.append(getattr(cls.diseaseclassnid, property).strip())
        return classes

    def get_disease_class(self, obj):
        return self.__get_disease_class_property(obj, 'diseaseclass')

    def get_disease_class_name(self, obj):
        return self.__get_disease_class_property(obj, 'diseaseclassname')

    def get_gene_symbol(self, obj):
        return self.__get_gene_attributes_property(obj, 'genename')

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

    gene_network = VariantGeneSerializer(source='variantgene_set', many=True)

    # Because the model is setup diffently from the output we'd like to see
    # we go convert evidences with diseases and aggregate the evidences into
    # the diseases.
    def to_representation(self, instance):
        data = super(serializers.ModelSerializer,
                     self).to_representation(instance)
        temp = {}
        gene_symbols = []
        for item in data.get('gene_network'):
            gene = item.get('gene')
            gene_symbols.append(gene.get('genename'))
        data['gene_symbols'] = gene_symbols
        del data['gene_network']
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
                     "disease_semantic_type": disease.get('umlssemantictypename'),
                    "year_initial": evidence.get('year'),
                    "year_final": evidence.get('year'),
                    # "gene_symbol": disease.get('gene_symbol'),
                    "evidences": []
                }
            # Check if there is an evidence
            if evidence.get('source'):
                temp[diseaseid]['evidences'].append(
                    {
                        "source": evidence.get('source'),
                        "sentence": evidence.get('sentence'),
                        "pmid": evidence.get('pmid'),
                        "year": evidence.get('year')
                    }
                )
                if evidence.get('year'):
                    temp[diseaseid]['year_initial'] = min(
                        temp[diseaseid]['year_initial'], evidence.get('year'))
                    temp[diseaseid]['year_final'] = max(
                        temp[diseaseid]['year_final'], evidence.get('year'))
            else:
                [diseaseid]['evidences'] = None
        del data['evidences']
        data['diseases'] = []
        for t in temp.values():
            data['diseases'].append(t)
        return data

    class Meta:
        model = Variantattributes
        fields = '__all__'
