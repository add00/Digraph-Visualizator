# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers

from graph.models import Arc, DiGraph, Node


class NodeSerializer(serializers.ModelSerializer):
    """
    Serializer for DiGraph model.
    """
    arcs = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = ('index', 'x', 'y', 'uuid', 'arcs',)

    def get_arcs(self, obj):
        """
        Get arcs comming out of a given node.
        """
        return [
            arc.index_to.uuid for arc in
            Arc.objects.filter(index_from__pk=obj.pk)
        ]


class DiGraphSerializer(serializers.ModelSerializer):
    """
    Serializer for DiGraph model.
    """
    nodes = NodeSerializer(source='node_set', many=True)

    class Meta:
        model = DiGraph
        fields = ('pk', 'name', 'nodes')
