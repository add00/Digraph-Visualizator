# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django import forms

from graph.models import Node, DiGraph


class DiGraphForm(forms.ModelForm):

    class Meta:
        model = DiGraph
        fields = ('name',)


class NodeForm(forms.ModelForm):
    index = forms.IntegerField(required=True)
    uuid = forms.CharField(max_length=36, required=False)
    graph = forms.ModelChoiceField(
        queryset=DiGraph.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control input_100px', 'onChange': 'loadGraph()'
        })
    )

    class Meta:
        model = Node
        fields = (
            'index', 'uuid', 'graph', 'x', 'y',
        )

    def clean(self):
        cleaned_data = super(NodeForm, self).clean()
        if cleaned_data.get('graph', ''):
            vertex = cleaned_data.get('index', '')
            if (
                vertex and vertex in
                cleaned_data['graph'].node_set.values_list('index', flat=True)
            ):
                raise forms.ValidationError(
                    u'Given vertex already exists in selected graph.'
                )

        return cleaned_data


class NodePositionForm(NodeForm):

    def __init__(self, *args, **kwargs):
        super(NodePositionForm, self).__init__(*args, **kwargs)
        self.fields['index'].required = False


class ArcForm(forms.Form):
    index_from = forms.CharField()
    index_to = forms.CharField()


class DeserializationForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control input_100px'})
    )

    def clean(self):
        cleaned_data = super(DeserializationForm, self).clean()
        try:
            json.loads(cleaned_data['file'].read())
        except ValueError:
            raise forms.ValidationError('File not in JSON format')

        return cleaned_data
