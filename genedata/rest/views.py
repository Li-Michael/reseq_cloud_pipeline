#! /usr/bin/env python
# -*- coding: utf-8
from django.contrib.auth.models import User, Group  
from rest_framework import viewsets, generics  
from rest.serializers import UserSerializer, GroupSerializer, GenomeSerializer, TrackSerializer, GenecodeSerializer, ContactSerializer 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
import networkx as nx
from networkx.readwrite import json_graph
from rest.forms import GeneForm
from time import time

class UserViewSet(viewsets.ModelViewSet):  
    """ 
    API endpoint that allows users to be viewed or edited. 
    """  
    queryset = User.objects.all()  
    serializer_class = UserSerializer  
  
  
class GroupViewSet(viewsets.ModelViewSet):  
    """ 
    API endpoint that allows groups to be viewed or edited. 
    """  
    queryset = Group.objects.all() 
    serializer_class = GroupSerializer 

from .models import Genome, Track, Genecode, Contact

class GenomeList(generics.ListCreateAPIView):
    queryset = Genome.objects.all()
    serializer_class = GenomeSerializer

class GenomeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genome.objects.all()
    serializer_class = GenomeSerializer

class TrackList(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

def igv_index(request):
    return render(request, 'beta.html')

class GenecodeList(generics.ListCreateAPIView):
    queryset = Genecode.objects.all()
    serializer_class = GenecodeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("geneName", "geneID",)

class GenecodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = GenecodeSerializer

class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("node1",)
    
class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class networkx_calc(object):
    def __init__(self):
        pass
    
    ## 获取与genename有关的所有gene和基因属性
    def get_value(self, genename, ):
        #network_node = [(unicode(genename), Genecode.objects.filter(geneName=genename).values("chrom","start","end")[0]),]
        time1 = time() 
        network_node = [unicode(genename),]
        #network_edge = []
        #contact_list = ContactSerializer.Meta.model.objects.filter(node1__geneName=genename).select_related("node1")
        contact_list = Contact.objects.filter(node1__geneName=genename).select_related("node1")

        #node_list = [ contact_list[0]["node1_id"] ] + [ node["node2_id"] for node in contact_list ]      
        #for contact in contact_list:	
            #g = GenecodeSerializer.Meta.model.objects.filter(pk=contact["node2_id"]).values() #"geneName", "chrom", "start", "end")
        #g = Genecode.objects.filter(pk__in=[contact["node2_id"] for contact in contact_list]) #.values() #"geneName", "chrom", "start", "end")
        g= contact_list   
        #nodename = a.geneName
        #a.pop("geneName")
        [ network_node.append(( a.node2.geneName, { "chrom":a.node2.chrom, "start":a.node2.start, "end":a.node2.end } )) for a in g ]
        network_edge= [(unicode(genename), a.node2.geneName, { "attr":a.attr }) for a in g ]
        time2 = time()
        print time2-time1
        return {"nodes":network_node, "edges":network_edge}

def networkx_json(request,genename="MUC3A"):
    time3 = time()
    G=nx.Graph()
    net = networkx_calc()
    values = net.get_value(genename)
    G.add_nodes_from(values["nodes"])
    G.add_edges_from(values["edges"])

    nodes = G.nodes()
    edges = G.edges()
    
    time4=time()
    for node in nodes:
        #net = networkx_calc()
        network_dict = net.get_value(node)
        #G.add_nodes_from(network_dict["nodes"])
        contact_list = ContactSerializer.Meta.model.objects.filter(node1__geneName=node).values()
        G.add_edges_from(network_dict["edges"])

    time5 = time()
    diff_nodes = list(set(G.nodes()).difference(set(nodes)))
    G.remove_nodes_from(diff_nodes)

    data = json_graph.node_link_data(G)
    time6 = time()    
    print time6 - time3, time4-time3, time5-time4, time6-time5    
    return  JsonResponse(data, safe=False)

def network_test(request):
    if request.method == 'POST':
        form = GeneForm(request.POST)
        
        if form.is_valid():
            gene = form.cleaned_data['gene']
            #return render(request, 'network2.html', {'form':form, 'gene': gene})
            return render(request, 'mcmaster-2.html', {'form':form, 'gene': gene})
    else:
        form = GeneForm()

    #return render(request, 'network2.html', {'form':form, 'gene':'MUC3A'})
    return render(request, 'mcmaster-2.html', {'form':form, 'gene':'MUC3A'})



