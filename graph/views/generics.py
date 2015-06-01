# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.db import transaction
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import FormView, DeleteView
from graph import forms
from graph.models import Arc, DiGraph, Node


class GraphFormView(FormView):
    """
    Home page view.
    """
    template_name = 'home.html'
    form_class = forms.NodeForm
    form_class_graph = forms.DiGraphForm
    form_class_graph_prefix = 'graph'
    form_class_deserialization = forms.DeserializationForm
    form_class_deserialization_prefix = 'deserialization'

    @transaction.atomic
    def _deserialize_data(self, data_json):
        """
        Handles imported data in JSON format.
        """
        defaults = {
            'x': 100,
            'y': 100,
        }

        for graph in data_json:
            di_graph, _ = DiGraph.objects.get_or_create(name=graph['name'])
            for node in graph['nodes']:
                di_node, _ = Node.objects.get_or_create(
                    index=node['index'], graph=di_graph, defaults=defaults
                )
                di_node.x = node['x']
                di_node.y = node['y']
                di_node.uuid = node['uuid']
                di_node.save()

        for graph in data_json:
            for node in graph['nodes']:
                main_di_node = Node.objects.get(uuid=node['uuid'])
                for arc in node['arcs']:
                    di_node = Node.objects.get(uuid=arc)
                    Arc.objects.get_or_create(
                        index_from=main_di_node,
                        index_to=di_node
                    )

    def get_context_data(self, *args, **kwargs):
        """
        Populate context data with forms.
        """
        context = super(GraphFormView, self).get_context_data(*args, **kwargs)

        graph_form = self.form_class_graph(prefix=self.form_class_graph_prefix)
        context['graph_form'] = graph_form

        deserialization_form = self.form_class_deserialization(
            prefix=self.form_class_deserialization_prefix
        )
        context['deserialization_form'] = deserialization_form

        if 'graph_pk' in self.kwargs:
            node_form = self.form_class()
            node_form.initial = {
                'graph': DiGraph.objects.get(pk=self.kwargs['graph_pk'])
            }
            context['form'] = node_form

        return context

    def post(self, request, *args, **kwargs):
        """
        Process data on POST.
        """
        graph_form = self.form_class_graph(
            request.POST, prefix=self.form_class_graph_prefix
        )
        deserialization_form = self.form_class_deserialization(
            request.POST, request.FILES,
            prefix=self.form_class_deserialization_prefix
        )
        node_form = self.form_class(request.POST)
        if node_form.is_valid():
            node = node_form.save()
            return redirect('graph', graph_pk=node.graph.pk)
        elif self.request.FILES and deserialization_form.is_valid():
            data = deserialization_form.cleaned_data['file'].read()
            data_json = json.loads(data)
            self._deserialize_data(data_json)
            return redirect('home')
        elif graph_form.is_valid():
            graph = graph_form.save()
            return redirect('graph', graph_pk=graph.pk)

        return super(GraphFormView, self).post(request, *args, **kwargs)


class DeleteGraphView(DeleteView):
    """
    Delete Graph view.
    """
    model = DiGraph
    success_url = reverse_lazy('home')


class DeleteNodeView(DeleteView):
    """
    Delete Node view.
    """
    model = Node
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """
        Gets particular Node.
        """
        graph = DiGraph.objects.get(pk=self.request.GET['graph'])
        node = graph.node_set.get(index=self.kwargs['index'])
        return node
