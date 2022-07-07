# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Disease2Class(models.Model):
    # Field name made lowercase.
    diseasenid = models.ForeignKey(
        'Diseaseattributes', models.DO_NOTHING, db_column='diseaseNID')
    # Field name made lowercase.
    diseaseclassnid = models.ForeignKey(
        'Diseaseclass', models.DO_NOTHING, db_column='diseaseClassNID')

    class Meta:
        managed = False
        db_table = 'disease2class'
        unique_together = ('diseasenid', 'diseaseclassnid')


class Diseaseattributes(models.Model):
    # Field name made lowercase.
    diseasenid = models.AutoField(db_column='diseaseNID', primary_key=True)
    # Field name made lowercase.
    diseaseid = models.CharField(db_column='diseaseId', max_length=255)
    # Field name made lowercase.
    diseasename = models.CharField(db_column='diseaseName', max_length=255)
    type = models.CharField(max_length=255)
    umlssemantictypeid = models.TextField(
        db_column='umlsSemanticTypeId', blank=True, null=True)
    # Field name made lowercase.
    umlssemantictypename = models.TextField(
        db_column='umlsSemanticTypeName', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diseaseAttributes'


class Diseaseclass(models.Model):
    # Field name made lowercase. This field type is a guess.
    diseaseclassnid = models.TextField(
        db_column='diseaseClassNID', primary_key=True)
    vocabulary = models.CharField(max_length=255)
    # Field name made lowercase.
    diseaseclass = models.CharField(db_column='diseaseClass', max_length=255)
    # Field name made lowercase.
    diseaseclassname = models.CharField(
        db_column='diseaseClassName', max_length=255)

    class Meta:
        managed = False
        db_table = 'diseaseClass'


class Geneattributes(models.Model):
    # Field name made lowercase.
    genenid = models.AutoField(db_column='geneNID', primary_key=True)
    # Field name made lowercase.
    geneid = models.IntegerField(db_column='geneId', blank=True, null=True)
    # Field name made lowercase.
    genename = models.CharField(
        db_column='geneName', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    genedescription = models.CharField(
        db_column='geneDescription', max_length=255, blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    pli = models.TextField(db_column='pLI', blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    dsi = models.TextField(db_column='DSI', blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    dpi = models.TextField(db_column='DPI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geneAttributes'


class Genediseasenetwork(models.Model):
    # Field name made lowercase.
    nid = models.AutoField(db_column='NID', primary_key=True)
    # Field name made lowercase.
    diseasenid = models.ForeignKey(
        Diseaseattributes, on_delete=models.DO_NOTHING, db_column='diseaseNID', null=True, to_field='diseasenid')
    # Field name made lowercase.
    genenid = models.ForeignKey(
        Geneattributes, models.DO_NOTHING, db_column='geneNID', null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    # This field type is a guess.
    association = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    associationtype = models.TextField(
        db_column='associationType', blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)
    pmid = models.IntegerField(blank=True, null=True)
    # This field type is a guess.
    score = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    el = models.CharField(db_column='EL', max_length=255,
                          blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    ei = models.TextField(db_column='EI', blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geneDiseaseNetwork'


class Umls(models.Model):
    # Field name made lowercase.
    diseaseid = models.ForeignKey(
        Diseaseattributes, on_delete=models.DO_NOTHING, db_column='diseaseId', primary_key=True)
    name = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    diseaseclassmsh = models.TextField(
        db_column='diseaseClassMSH', blank=True, null=True)
    # Field name made lowercase.
    diseaseclassnamemsh = models.TextField(
        db_column='diseaseClassNameMSH', blank=True, null=True)
    # Field name made lowercase.
    hpoclassid = models.TextField(
        db_column='hpoClassId', blank=True, null=True)
    # Field name made lowercase.
    hpoclassname = models.TextField(
        db_column='hpoClassName', blank=True, null=True)
    # Field name made lowercase.
    doclassid = models.TextField(db_column='doClassId', blank=True, null=True)
    # Field name made lowercase.
    doclassname = models.TextField(
        db_column='doClassName', blank=True, null=True)
    # Field name made lowercase.
    umlssemantictypeid = models.TextField(
        db_column='umlsSemanticTypeId', blank=True, null=True)
    # Field name made lowercase.
    umlssemantictypename = models.TextField(
        db_column='umlsSemanticTypeName', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'umls'


class Variantattributes(models.Model):
    # Field name made lowercase.
    variantnid = models.AutoField(db_column='variantNID', primary_key=True)
    # Field name made lowercase.
    variantid = models.CharField(db_column='variantId', max_length=255)
    s = models.TextField(blank=True, null=True)  # This field type is a guess.
    chromosome = models.CharField(blank=True, null=True, max_length=255)
    coord = models.CharField(blank=True, null=True, max_length=255)
    most_severe_consequence = models.CharField(
        blank=True, null=True, max_length=255)
    # Field name made lowercase. This field type is a guess.
    dsi = models.TextField(db_column='DSI', blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    dpi = models.TextField(db_column='DPI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variantAttributes'


class Variantdiseasenetwork(models.Model):
    # Field name made lowercase.
    nid = models.AutoField(db_column='NID', primary_key=True)
    # Field name made lowercase.
    diseasenid = models.ForeignKey(
        Diseaseattributes, models.DO_NOTHING, db_column='diseaseNID')
    # Field name made lowercase.
    variantnid = models.ForeignKey(
        Variantattributes, models.DO_NOTHING, db_column='variantNID')
    source = models.CharField(blank=True, null=True, max_length=255)
    # This field type is a guess.
    association = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    associationtype = models.TextField(
        db_column='associationType', blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)
    pmid = models.IntegerField(blank=True, null=True)
    # This field type is a guess.
    score = models.TextField(blank=True, null=True)
    # Field name made lowercase. This field type is a guess.
    ei = models.TextField(db_column='EI', blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variantDiseaseNetwork'


class Variantgene(models.Model):
    # Field name made lowercase.
    genenid = models.ForeignKey(
        Geneattributes, models.DO_NOTHING, db_column='geneNID')
    # Field name made lowercase.
    variantnid = models.ForeignKey(
        Variantattributes, models.DO_NOTHING, db_column='variantNID')

    class Meta:
        managed = False
        db_table = 'variantGene'
        unique_together = ('genenid', 'variantnid')
