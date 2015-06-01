# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models


class DiGraph(models.Model):
    name = models.CharField(max_length=255, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Node(models.Model):
    index = models.IntegerField()
    graph = models.ForeignKey(DiGraph)
    uuid = models.CharField(max_length=36, editable=False, default=uuid.uuid1)
    x = models.IntegerField()
    y = models.IntegerField()

    def __unicode__(self):
        return '{} #{}'.format(self.graph.name, self.index)


class Arc(models.Model):
    index_from = models.ForeignKey(Node, related_name='_from')
    index_to = models.ForeignKey(Node, related_name='_to')

    def __unicode__(self):
        return '{} ===> {}'.format(self.index_from.index, self.index_to.index)
