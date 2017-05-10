#!/usr/bin/env python
# -*- coding: utf-8

from django.contrib.auth.models import User, Group  
from rest_framework import serializers  
from .models import Genome, Track, Genecode, Contact 
  
class UserSerializer(serializers.HyperlinkedModelSerializer):  
    class Meta:  
        model = User  
        fields = ('url', 'username', 'email', 'groups')  
        depth = 2  
  
class GroupSerializer(serializers.HyperlinkedModelSerializer):  
    class Meta:  
        model = Group  
        fields = ('url', 'name')

class GenomeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genome
        fields = ("genome_id", "fastaURL", "indexURL", "cytobandURL", "indexed")

class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ("genome_id", "name", "filetype", "url", "indexURL", "sourceType", "order")
        depth = 2

class GenecodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genecode
        fields = "__all__"

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ("node1", "node2", "attr")

        depth = 2

##list(ContactSerializer.Meta.model.objects.all().values())



