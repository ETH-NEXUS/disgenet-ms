from django.db import models


class Disease2Class(models.Model):
    diseasenid = models.OneToOneField('DiseaseAttributes', models.DO_NOTHING,
                                      db_column='diseaseNID')  # Field name made lowercase.
    diseaseclassnid = models.ForeignKey('DiseaseClass', models.DO_NOTHING,
                                        db_column='diseaseClassNID')  # Field name made lowercase.

    def diseaseClassName(self):
        return self.diseaseclassnid.diseaseclassname

    def diseaseClass(self):
        return self.diseaseclassnid.diseaseclass

    class Meta:
        managed = False
        db_table = 'disease2class'


class DiseaseAttributes(models.Model):
    diseasenid = models.IntegerField(db_column='diseaseNID', primary_key=True)
    diseaseid = models.CharField(db_column='diseaseId', max_length=255)
    diseasename = models.CharField(db_column='diseaseName', max_length=255)
    type = models.CharField(max_length=255)

    def class_name(self):
        if len(Disease2Class.objects.filter(diseasenid=self.diseasenid)) > 0:
            disease_class = Disease2Class.objects.filter(
                diseasenid=self.diseasenid)
            result = []
            for i in disease_class:
                result.append(i.diseaseClassName().lstrip())
            return result

    def class_(self):
        if len(Disease2Class.objects.filter(diseasenid=self.diseasenid)) > 0:
            disease_class = Disease2Class.objects.filter(
                diseasenid=self.diseasenid)
            result = []
            for i in disease_class:
                result.append(i.diseaseClass())
            return result

    class Meta:
        managed = False
        db_table = 'diseaseAttributes'


class DiseaseClass(models.Model):
    diseaseclassnid = models.TextField(
        db_column='diseaseClassNID', primary_key=True)
    vocabulary = models.CharField(max_length=255)
    diseaseclass = models.CharField(db_column='diseaseClass', max_length=255)
    diseaseclassname = models.CharField(
        db_column='diseaseClassName', max_length=255)

    class Meta:
        managed = False
        db_table = 'diseaseClass'


class GeneAttributes(models.Model):
    genenid = models.IntegerField(db_column='geneNID', primary_key=True)
    geneid = models.IntegerField(db_column='geneId', blank=True, null=True)
    genename = models.CharField(db_column='geneName', max_length=255, blank=True,
                                null=True)
    genedescription = models.CharField(db_column='geneDescription', max_length=255, blank=True,
                                       null=True)
    pli = models.TextField(db_column='pLI', blank=True,
                           null=True)  # Field name made lowercase. This field type is a guess.
    dsi = models.TextField(db_column='DSI', blank=True,
                           null=True)  # Field name made lowercase. This field type is a guess.
    dpi = models.TextField(db_column='DPI', blank=True,
                           null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'geneAttributes'


class GeneDiseaseNetwork(models.Model):
    nid = models.IntegerField(db_column='NID')
    diseasenid = models.ForeignKey(DiseaseAttributes, models.DO_NOTHING,
                                   db_column='diseaseNID')
    genenid = models.ForeignKey(
        GeneAttributes, models.DO_NOTHING, db_column='geneNID')
    source = models.CharField(max_length=255, blank=True, null=True)
    association = models.TextField(blank=True, null=True)
    associationtype = models.TextField(
        db_column='associationType', blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)
    pmid = models.IntegerField(blank=True, null=True)
    score = models.TextField(blank=True, null=True)
    el = models.CharField(db_column='EL', max_length=255,
                          blank=True, null=True)
    ei = models.TextField(db_column='EI', blank=True,
                          null=True)
    year = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'geneDiseaseNetwork'


class VariantAttributes(models.Model):
    variantnid = models.IntegerField(db_column='variantNID', primary_key=True)
    variantid = models.CharField(db_column='variantId', max_length=255)
    s = models.TextField(blank=True, null=True)
    chromosome = models.CharField(blank=True, null=True, max_length=255)
    coord = models.CharField(blank=True, null=True, max_length=255)
    most_severe_consequence = models.CharField(
        blank=True, null=True, max_length=255)
    dsi = models.TextField(db_column='DSI', blank=True,
                           null=True)
    dpi = models.TextField(db_column='DPI', blank=True,
                           null=True)

    def gene_name(self):
        if len(VariantGene.objects.filter(variantnid=self.variantnid)) > 0:
            gene = VariantGene.objects.filter(variantnid=self.variantnid)[0]
            return gene.gene_name()
        else:
            return ""

    class Meta:
        db_table = 'variantAttributes'


class Umls(models.Model):
    diseaseId = models.TextField(primary_key=True,
                                 db_column='diseaseId')
    name = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    diseaseClassMSH = models.TextField(blank=True, null=True)
    diseaseClassNameMSH = models.TextField(blank=True, null=True)
    hpoClassId = models.TextField(blank=True, null=True)
    hpoClassName = models.TextField(blank=True, null=True)
    umlsSemanticTypeId = models.TextField(blank=True, null=True)
    umlsSemanticTypeName = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'umls'


class VariantDiseaseNetwork(models.Model):
    nid = models.IntegerField(db_column='NID', primary_key=True)
    diseasenid = models.ForeignKey(DiseaseAttributes, models.DO_NOTHING,
                                   db_column='diseaseNID')
    variantnid = models.ForeignKey(VariantAttributes, models.DO_NOTHING,
                                   db_column='variantNID')
    source = models.CharField(blank=True, null=True, max_length=255)
    association = models.TextField(blank=True, null=True)
    associationtype = models.TextField(
        db_column='associationType', blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)
    pmid = models.TextField(blank=True, null=True)
    score = models.TextField(blank=True, null=True)
    ei = models.TextField(db_column='EI', blank=True,
                          null=True)
    year = models.IntegerField(blank=True, null=True)

    def year_initial(self):
        objects = VariantDiseaseNetwork.objects.filter(
            variantnid=self.variantnid)
        return objects[0].year

    def year_final(self):
        objects = VariantDiseaseNetwork.objects.filter(
            variantnid=self.variantnid)
        return objects[objects.count() - 1].year

    def disease_name(self):
        return self.diseasenid.diseasename

    def diseaseid(self):
        return self.diseasenid.diseaseid

    def disease_type(self):
        return self.diseasenid.type

    def variantid(self):
        return self.variantnid.variantid

    def variant_dsi(self):
        return self.variantnid.dsi

    def variant_dpi(self):
        return self.variantnid.dpi

    def variant_consequence_type(self):
        return self.variantnid.most_severe_consequence

    def gene_symbol(self):
        return self.variantnid.gene_name()

    def disease_class_name(self):
        return self.diseasenid.class_name()

    def disease_class(self):
        return self.diseasenid.class_()

    def disease_class(self):
        return self.diseasenid.class_()

    def disease_semantic_type(self):
        umls_object = Umls.objects.filter(diseaseId=self.diseaseid())[0]
        return umls_object.umlsSemanticTypeName

    def details(self):
        return [{"year": object.year, "source": object.source, "sentence": object.sentence} for object in VariantDiseaseNetwork.objects.filter(
            variantnid=self.variantnid)]

    class Meta:
        db_table = 'variantDiseaseNetwork'


class VariantGene(models.Model):
    genenid = models.ForeignKey(
        GeneAttributes, models.DO_NOTHING, db_column='geneNID')
    variantnid = models.OneToOneField(VariantAttributes, models.DO_NOTHING,
                                      db_column='variantNID')

    def gene_name(self):
        return self.genenid.genename

    class Meta:
        db_table = 'variantGene'
