#! /usr/bin/env python
# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import cPickle as pickle

from django.db import models
# Create your models here.
from django.contrib.auth.models import User


#class SerializedField(models.TextField):

#    """序列化域
#    用 pickle 来实现存储 Python 对象
#    """
#    __metaclass__ = models.SubfieldBase  # 必须指定该 metaclass 才能使用 to_python

#    def validate(self, val):
#        raise isinstance(val, basestring)

#    def to_python(self, val):
#        """从数据库中取出字符串，解析为 python 对象"""
#        if val and isinstance(val, unicode):
#            return pickle.loads(val.rstrip("}").lstrip("{").encode('utf-8'))

#        return val

#    def get_prep_value(self, val):
#        """将 python object 存入数据库"""
#        return pickle.dumps(val)

class Genome(models.Model):
    genome_id = models.CharField(u'GenomeID', max_length=20)
    fastaURL = models.URLField(u'fastaURL', max_length=200)
    indexURL = models.URLField(u'indexRUL', max_length=200)
    cytobandURL = models.URLField(u'cytobandURL', max_length=200)
    indexed = models.BooleanField(u'indexed', default=True)

    def __unicode__(self):
        return self.genome_id

    class Meta:
        ordering = ['-genome_id']


class Track(models.Model):
    creat_time = models.DateTimeField(auto_now_add=True)
    # 注意这里建立了一个外键
    genome_id = models.ForeignKey(Genome,related_name='my_tracks')
    name = models.CharField(max_length=20)
    filetype = models.CharField(blank=True, null=True, choices=[("annotation","annotation"), ("alignment","alignment"), ("wig","wig"), ("ga4gh","ga4gh"), ("variant","variant"), ("seg","seg")], max_length=10)
    url = models.URLField(max_length=200)
    indexURL = models.URLField(blank=True, null=True, max_length=200)
    sourceType = models.CharField(blank=True, null=True, choices=[("file","file"), ("gcs","gcs"), ("ga4gh","ga4gh")], default="file", max_length=10)
    #displayMode = models.CharField(blank=True, null=True,choices=[("COLLAPSED","COLLAPSED"), ("EXPANDED","EXPANDED"), ("SQUISHED","SQUISHED"),( None,"None")], max_length=10)
    order = models.CharField(blank=True, null=True,max_length=30)    
    descript = models.CharField(blank=True, null=True, max_length=200)
#    options = SerializedField(blank=True, null=True, max_length=1000, default={})

    def __unicode__(self):
        return self.name
            
    class Meta:
        ordering = ['-name']


class Genecode(models.Model):
    """    
    chromosome name	chr{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,X,Y,M} or GRC accession a
    annotation source	{ENSEMBL,HAVANA}
    feature type	{gene,transcript,exon,CDS,UTR,start_codon,stop_codon,Selenocysteine}
    genomic start location	integer-value (1-based)
    genomic end location	integer-value
    score (not used) 	.
    genomic strand	{+,-}
    genomic phase (for CDS features) 	{0,1,2,.}
    additional information as key-value pairs	see below
    
    gene_id	        ENSGXXXXXXXXXXX.X b,c _Xg
    transcript_id d	ENSTXXXXXXXXXXX.X b,c _Xg
    gene_type	        list of biotypes
    gene_status e	{KNOWN, NOVEL, PUTATIVE}
    gene_name	        string
    transcript_type d	list of biotypes
    transcript_status   d,e	{KNOWN, NOVEL, PUTATIVE}
    transcript_name     d	string
    exon_number         f	indicates the biological position of the exon in the transcript
    exon_id         f	ENSEXXXXXXXXXXX.X b _Xg
    level           1 (verified loci),
                    2 (manually annotated loci),
                    3 (automatically annotated loci)
    """
    genome = models.ForeignKey(Genome)
    chrom = models.IntegerField(u"Chromosome")
    #annoSource = models.CharField(u"Annotation Source", choices=[("ENSEMBL", "ENSEMBL"),("HAVANA", "HAVANA")],max_length=7)
    #featureType = models.CharField(u"Feature Type", choices=[("gene", "gene"), ("transcript", "transcript"), ("exon", "exon"), ("CDS", "CDS"), ("UTR", "UTR"), ("start_codon", "stop_codon"), ( "Selenocysteine", "Selenocysteine")], default="gene", max_length=15)
    start = models.IntegerField(u'Start')
    end = models.IntegerField(u'End')
    #score = models.CharField()
    strand = models.CharField(u'Strand', max_length=1)
    geneID = models.CharField(u'Gene ID', max_length=20)
    geneType = models.CharField(u'Gene Type', max_length=35)
    geneStatus = models.CharField(u'Gene Status', choices=[("KNOWN", "KNOWN"), ("NOVEL", "NOVEL"), ("PUTATIVE", "PUTATIVE")], max_length=8)
    geneName = models.CharField(u'Gene Name', max_length=15)
    level = models.IntegerField(u'Level', choices=[(1, 1), (2, 2), (3, 3)])

    def __unicode__(self):
        return self.geneName
    
    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
	    ##serializers.serialize('json', Contact.objects.filter(node1__geneName='gg1'))

    class Meta:
        ordering = ['geneName']

class Contact(models.Model):
    #geneID = models.ManyToMany()
    #node2 = models.ManyToManyField(Genecode, related_name="t2node", symmetrical=False)  #  symmetrical = False
    node1 = models.ForeignKey(Genecode, related_name="f2node")
    node2 = models.ForeignKey(Genecode, related_name="t2node")    
    attr = models.CharField(u'Attribute', choices=[("Co-expression", "Co-expression"), ("Predicted", "Predicted"), ("Physical_Interactions", "Physical_Interactions")], max_length=22) 

    #def __unicode__(self):
        #return self.node1


    class Meta:
        ordering = ['node1']
        #unique_together = (('node1', 'node2'),)
        
    
