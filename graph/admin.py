from django.contrib import admin
from graph.models import DiGraph, Node, Arc


class ArcInline(admin.TabularInline):
    model = Arc
    extra = 1
    fk_name = 'index_from'


class NodeInline(admin.StackedInline):
    model = Node
    extra = 0


class DiGraphAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    inlines = [NodeInline]


class NodeAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)
    search_fields = ['index']
    inlines = [ArcInline]


admin.site.register(DiGraph, DiGraphAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Arc)
