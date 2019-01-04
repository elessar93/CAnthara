from django import forms
from django.contrib import admin

from config.models import Aparato, Gimnasio, Nivel, Competencia, Competidor, Grupo, Calificacion


class CatalogoAdmin(admin.ModelAdmin):
    actions = ['custom_delete']
    fields = ('nombre',)
    list_display = ('nombre',)
    empty_value_display = '-Vacio-'
    search_fields = ['nombre', ]

    def custom_delete(self, request, queryset):
        queryset.update(estatus=False)

    custom_delete.short_description = "Eliminar"

    def get_actions(self, request):
        actions = super(CatalogoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        qs = super(CatalogoAdmin, self).get_queryset(request)
        return qs.filter(estatus=True)


class CompetenciaAdmin(admin.ModelAdmin):
    actions = ['custom_delete']
    fields = ('fecha', 'estatus')
    list_display = ('fecha', 'estatus')
    empty_value_display = '-Vacio-'
    search_fields = ['fecha', ]

    def custom_delete(self, request, queryset):
        queryset.update(estatus=False)

    custom_delete.short_description = "Desactivar"

    def get_actions(self, request):
        actions = super(CompetenciaAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class CompetidorAdmin(admin.ModelAdmin):
    fields = ('nombre', 'apellidos', 'nivel', 'gimnasio', 'edad', 'competencia')
    list_display = ('nombre', 'apellidos', 'nivel', 'gimnasio', 'edad', 'competencia', 'fecha_registro')
    empty_value_display = '-Vacio-'
    search_fields = ('nombre', 'apellidos', 'nivel', 'gimnasio', 'edad', 'competencia', 'fecha_registro')


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ('competencia', 'aparato')

    competidors = forms.ModelMultipleChoiceField(queryset=Competidor.objects.filter(competencia__estatus=True))

    def __init__(self, *args, **kwargs):
        super(GrupoForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['competidors'].initial = self.instance.competidor_set.all()

    def save(self, *args, **kwargs):
        # FIXME: 'commit' argument is not handled
        # TODO: Wrap reassignments into transaction
        # NOTE: Previously assigned Foos are silently reset
        instance = super(GrupoForm, self).save(commit=False)
        self.fields['competidors'].initial.update(grupo=None)
        self.cleaned_data['competidors'].update(grupo=instance)
        return instance


class GrupoAdmin(admin.ModelAdmin):
    form = GrupoForm
    list_display = ['competencia', 'aparato', ]
    empty_value_display = ['competencia', 'aparato', ]
    search_fields = ['competencia', 'aparato', ]


class CalificacionAdmin(admin.ModelAdmin):
    fields = ('aparato', 'calificacion', 'competidor',)
    list_display = ('aparato', 'calificacion', 'competidor',)
    empty_value_display = '-Vacio-'
    search_fields = ('aparato', 'calificacion', 'competidor',)


admin.site.register(Aparato, CatalogoAdmin)
admin.site.register(Gimnasio, CatalogoAdmin)
admin.site.register(Nivel, CatalogoAdmin)
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Competidor, CompetidorAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Calificacion, CalificacionAdmin)
