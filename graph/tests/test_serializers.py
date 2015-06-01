# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from graph.models import DiGraph, Node
from graph.serializers import DiGraphSerializer, NodeSerializer


class SerializersTestCase(TestCase):
    fixtures = ['graphs.json']

    def test_digraph_serializer(self):
        di_graph = DiGraph.objects.get(pk=1)
        data = DiGraphSerializer(di_graph).data
        self.assertEqual(
            data,
            {
                'pk': 1,
                'name': 'Test Graph',
                'nodes': [{
                    'index': 1,
                    'x': 100,
                    'y': 100,
                    'uuid': 'df328bba-07dc-11e5-81e3-48d705d1bf4d',
                    'arcs': ['e7ed5d28-07dc-11e5-bfbd-48d705d1bf4d']
                }, {
                    'index': 2,
                    'x': 100,
                    'y': 300,
                    'uuid': 'e25b7338-07dc-11e5-90ab-48d705d1bf4d',
                    'arcs': ['e586780a-07dc-11e5-9448-48d705d1bf4d']
                }, {
                    'index': 3,
                    'x': 300,
                    'y': 100,
                    'uuid': 'e586780a-07dc-11e5-9448-48d705d1bf4d',
                    'arcs': ['e25b7338-07dc-11e5-90ab-48d705d1bf4d']
                }, {
                    'index': 4,
                    'x': 300,
                    'y': 300,
                    'uuid': 'e7ed5d28-07dc-11e5-bfbd-48d705d1bf4d',
                    'arcs': []
                }]
            }
        )

    def test_node_serializer(self):
        node = Node.objects.get(pk=1)
        data = NodeSerializer(node).data
        self.assertEqual(
            data,
            {
                'arcs': ['e7ed5d28-07dc-11e5-bfbd-48d705d1bf4d'],
                'index': 1,
                'uuid': 'df328bba-07dc-11e5-81e3-48d705d1bf4d',
                'x': 100,
                'y': 100
            }
        )
