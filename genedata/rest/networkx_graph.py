#!/usr/bin/env python
#-*-coding:utf-8-*-

from .models import Genome, Track, Genecode, Contact
from .serializers import GenomeSerializer, TrackSerializer, GenecodeSerializer, ContactSerializer
import networkx as nx

#>>> G.add_nodes_from([(1,dict(size=11)), (2,{'color':'blue'})])

class Networkx_clac(object):
    def __init__(self):
        #self.G = nx.Graph()

    def get_value(self, genename):
        #networkx_list = [(genename, Genecode.objects.filter(geneName=genename).values()[0].pop(genename)),]
		networkx_list = [(genename, Genecode.objects.filter(geneName=genename).values("chrom","start","end")),]
        contact_list = ContactSerializer.Meta.model.objects.filter(node1__geneName=genename).select_related("node1").values()
        #ContactSerializer.Meta.model.objects.all().values()	
        for contact in contact_list:	
            g = GenecodeSerializer.Meta.model.objects.filter(pk=contact["node2_id"]).values("geneName","chrom","start","end")
            networkx_list.append((g["geneName"], g[0].pop("geneName")),)

        return networkx_list


