# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.forms.formsets import formset_factory
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from graph.forms import ArcForm, NodePositionForm
from graph.models import DiGraph, Arc, Node
from graph import serializers


class GraphListAPI(generics.ListAPIView):
    """
    Get list of graphs.
    """
    model = DiGraph
    queryset = DiGraph.objects.all()
    serializer_class = serializers.DiGraphSerializer


class GraphDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, delete single graph.
    """
    model = DiGraph
    queryset = DiGraph.objects.all()
    serializer_class = serializers.DiGraphSerializer
    pk_url_kwarg = 'pk'


class ArcCreateAPI(generics.CreateAPIView):
    """
    Create new arc.
    """
    model = Arc

    def post(self, *args, **kwargs):
        data = self.request.POST
        created = False

        graph = DiGraph.objects.get(pk=kwargs['graph_pk'])
        arcs = Arc.objects.filter(
            Q(index_from__graph=graph) | Q(index_to__graph=graph)
        )
        arcs.delete()

        ArcFormFormSet = formset_factory(ArcForm)
        forms = ArcFormFormSet(self.request.POST, prefix='arc')
        for form in forms:
            if form.is_valid():
                data = form.cleaned_data
                try:
                    _from = Node.objects.get(uuid=data.get('index_from'))
                except:
                    raise exceptions.NotFound('Node `from` doesn\'t exist.')
                try:
                    _to = Node.objects.get(uuid=data.get('index_to'))
                except:
                    raise exceptions.NotFound('Node `to` doesn\'t exist.')
                arc, created = Arc.objects.get_or_create(
                    index_from=_from, index_to=_to
                )

        NodePositionFormSet = formset_factory(NodePositionForm)
        forms = NodePositionFormSet(self.request.POST, prefix='node')
        for form in forms:
            if form.is_valid():
                data = form.cleaned_data
                node, _ = Node.objects.get_or_create(uuid=data['uuid'])
                node.x = data['x']
                node.y = data['y']
                node.save()

        if created:
            return Response("Updated", status=status.HTTP_201_CREATED)
        return Response("Updated", status=status.HTTP_304_NOT_MODIFIED)
