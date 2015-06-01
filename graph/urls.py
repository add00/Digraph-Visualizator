# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin
from graph import views

urlpatterns = patterns(
    '',
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^$',
        views.GraphFormView.as_view(),
        name='home'
    ),
    url(
        r'^graph/(?P<graph_pk>.+)/?$',
        views.GraphFormView.as_view(),
        name='graph'
    ),
    url(
        r'^remove/graph/(?P<pk>.+)?$',
        views.DeleteGraphView.as_view(),
        name='remove-graph'
    ),
    url(
        r'^remove/node/(?P<index>.+)?$',
        views.DeleteNodeView.as_view(),
        name='remove-node'
    ),
    url(
        r'^api/v1/graph/(?P<pk>.+)/?$',
        views.GraphDetailAPI.as_view(),
        name='api-graph'
    ),
    url(
        r'^api/v1/graphs/?$',
        views.GraphListAPI.as_view(),
        name='api-graphs'
    ),
    url(
        r'^api/v1/arc/(?P<graph_pk>.+)/?$',
        views.ArcCreateAPI.as_view(),
        name='api-arc'
    )
)
