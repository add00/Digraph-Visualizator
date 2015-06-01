# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase

from graph.models import DiGraph, Node
from graph.tests.example_data import SERIALIZED_GRAPH


class GraphFormViewTestCase(TestCase):
    fixtures = ['graphs.json']

    def test_post_new_node(self):
        self.assertEqual(Node.objects.count(), 4)
        response = self.client.post(
            reverse('graph', kwargs={'graph_pk': 1}),
            {
                'csrfmiddlewaretoken': '8QRzYgXPc6LIOwtCKdhxF0t99RLcF8Vn',
                'graph': '1',
                'index': '5',
                'x': '10',
                'y': '11'
            }
        )
        self.assertEqual(response.status_code, 302)

        new_node = Node.objects.last()
        self.assertEqual(Node.objects.count(), 5)
        self.assertEqual(new_node.x, 10)
        self.assertEqual(new_node.y, 11)
        self.assertEqual(new_node.index, 5)

    def test_post_new_graph(self):
        self.assertEqual(DiGraph.objects.count(), 1)
        response = self.client.post(
            reverse('graph', kwargs={'graph_pk': 1}),
            {
                'csrfmiddlewaretoken': '8QRzYgXPc6LIOwtCKdhxF0t99RLcF8Vn',
                'graph-name': 'New graph'
            }
        )
        self.assertEqual(response.status_code, 302)

        new_graph = DiGraph.objects.last()
        self.assertEqual(DiGraph.objects.count(), 2)
        self.assertEqual(new_graph.name, 'New graph')

    def test_post_new_arc(self):
        self.assertEqual(DiGraph.objects.count(), 1)
        response = self.client.post(
            reverse('graph', kwargs={'graph_pk': 1}),
            {
                'csrfmiddlewaretoken': '8QRzYgXPc6LIOwtCKdhxF0t99RLcF8Vn',
                'graph-name': 'New graph'
            }
        )
        self.assertEqual(response.status_code, 302)

        new_graph = DiGraph.objects.last()
        self.assertEqual(DiGraph.objects.count(), 2)
        self.assertEqual(new_graph.name, 'New graph')

    def test_deserialize_data(self):
        json_file = SimpleUploadedFile(
            'serialized_graph.json', json.dumps(SERIALIZED_GRAPH)
        )

        self.assertEqual(DiGraph.objects.count(), 1)

        response = self.client.post(
            reverse('graph', kwargs={'graph_pk': 1}),
            {
                'csrfmiddlewaretoken': '8QRzYgXPc6LIOwtCKdhxF0t99RLcF8Vn',
                'deserialization-file': json_file
            }
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DiGraph.objects.count(), 3)
        first_new_graph = DiGraph.objects.get(pk=2)
        second_new_graph = DiGraph.objects.get(pk=3)
        self.assertEqual(first_new_graph.name, 'gX')
        self.assertEqual(first_new_graph.node_set.count(), 4)
        self.assertEqual(second_new_graph.name, 'gY')
        self.assertEqual(second_new_graph.node_set.count(), 4)
