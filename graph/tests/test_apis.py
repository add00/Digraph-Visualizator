# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from graph.models import Arc, Node
from graph.tests.example_data import UPDATE_FORM_DATA


class ApisTestCase(TestCase):
    fixtures = ['graphs.json']

    def test_graph_list_api(self):
        response = self.client.get(reverse('api-graphs'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            [{
                'pk': 1,
                'name': 'Test Graph',
                'nodes': [
                    {
                        'index': 1,
                        'x': 100,
                        'y': 100,
                        'uuid': 'df328bba-07dc-11e5-81e3-48d705d1bf4d',
                        'arcs': [
                            'e7ed5d28-07dc-11e5-bfbd-48d705d1bf4d'
                        ]
                    },
                    {
                        'index': 2,
                        'x': 100,
                        'y': 300,
                        'uuid': 'e25b7338-07dc-11e5-90ab-48d705d1bf4d',
                        'arcs': [
                            'e586780a-07dc-11e5-9448-48d705d1bf4d'
                        ]
                    },
                    {
                        'index': 3,
                        'x': 300,
                        'y': 100,
                        'uuid': 'e586780a-07dc-11e5-9448-48d705d1bf4d',
                        'arcs': [
                            'e25b7338-07dc-11e5-90ab-48d705d1bf4d'
                        ]
                    },
                    {
                        'index': 4,
                        'x': 300,
                        'y': 300,
                        'uuid': 'e7ed5d28-07dc-11e5-bfbd-48d705d1bf4d',
                        'arcs': []
                    }
                ]
            }]
        )

    def test_graph_detail_api(self):
        response = self.client.get(reverse('api-graph', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                'pk': 1,
                'name': 'Test Graph',
                'nodes': [
                    {
                        'index': 1,
                        'x': 100,
                        'y': 100,
                        'uuid': 'df328bba-07dc-11e5-81e3-48d705d1bf4d',
                        'arcs': [
                            'e7ed5d28-07dc-11e5-bfbd-48d705d1bf4d'
                        ]
                    },
                    {
                        'index': 2,
                        'x': 100,
                        'y': 300,
                        'uuid': 'e25b7338-07dc-11e5-90ab-48d705d1bf4d',
                        'arcs': [
                            'e586780a-07dc-11e5-9448-48d705d1bf4d'
                        ]
                    },
                    {
                        'index': 3,
                        'x': 300,
                        'y': 100,
                        'uuid': 'e586780a-07dc-11e5-9448-48d705d1bf4d',
                        'arcs': [
                            'e25b7338-07dc-11e5-90ab-48d705d1bf4d'
                        ]
                    },
                    {
                        'index': 4,
                        'x': 300,
                        'y': 300,
                        'uuid': 'e7ed5d28-07dc-11e5-bfbd-48d705d1bf4d',
                        'arcs': []
                    }
                ]
            }
        )

    def test_arc_create_api(self):
        node = Node.objects.get(pk=1)
        self.assertNotEqual(node.x, 999)
        self.assertNotEqual(node.y, 999)
        self.assertEqual(Arc.objects.count(), 3)

        response = self.client.post(
            reverse('api-arc', kwargs={'graph_pk': 1}), UPDATE_FORM_DATA
        )
        self.assertEqual(response.status_code, 201)

        node = Node.objects.get(pk=1)
        self.assertEqual(node.x, 999)
        self.assertEqual(Arc.objects.count(), 4)
        self.assertEqual(node.y, 999)
