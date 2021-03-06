from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView

from config.models import Competencia, Competidor, Grupo


def index(request):
    template_name = 'webapp/index.html'
    # if request.user.is_authenticated:
    return render(request, template_name)


def por_asignar(request, pk):
    c = get_object_or_404(Competencia, pk=pk)
    template_name = 'webapp/por_asignar.html'
    return render(request, template_name, {"c": c})


def grupos(request, pk):
    c = get_object_or_404(Competencia, pk=pk)
    sin_grupo = Competidor.objects.filter(competencia=c,grupo__isnull=True).count()
    template_name = 'webapp/grupos.html'
    return render(request, template_name, {"c": c,"sin":sin_grupo})


def grupo_list(request, pk):
    g = get_object_or_404(Grupo, pk=pk)
    template_name = 'webapp/tab_grupo.html'
    return render(request, template_name, {"g": g})


class CompetenciasAjaxList(LoginRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login/'

    model = Competencia
    columns = ['id', 'nombre']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):
        if column == 'nombre':
            return '<a class="" href ="' + reverse('webapp:grupos',
                                                   kwargs={
                                                       'pk': row.pk}) + '">' + row.nombre + '</a>'
        return super(CompetenciasAjaxList, self).render_column(row, column)


class PorAsignarAjaxList(LoginRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login/'

    model = Competidor
    columns = ['id', 'nombre', 'apellidos', 'nivel.nombre', 'gimnasio.nombre', 'edad', 'genero.nombre']
    order_columns = ['id', 'nombre', 'apellidos', 'nivel.nombre', 'gimnasio.nombre', 'edad', 'genero.nombre']
    max_display_length = 100

    def render_column(self, row, column):
        if column == 'id':
            return "<input type='checkbox' class='chk-competidor' data-id='" + str(row.pk) + "' />"
        return super(PorAsignarAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Competidor.objects.filter(competencia__pk=self.kwargs['pk'], grupo__isnull=True)


class GrupoAjaxList(LoginRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/webapp/login/'

    model = Competidor
    columns = ['id', 'nombre', 'apellidos', 'nivel.nombre', 'gimnasio.nombre', 'edad', 'genero.nombre']
    order_columns = ['id', 'nombre', 'apellidos', 'nivel.nombre', 'gimnasio.nombre', 'edad', 'genero.nombre']
    max_display_length = 100

    def render_column(self, row, column):
        if column == 'id':
            return "<input type='checkbox' class='chk-competidor' data-id='" + str(row.pk) + "' />"
        return super(GrupoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Competidor.objects.filter(grupo__pk=self.kwargs['pk'])


@login_required(redirect_field_name='next', login_url='/webapp/login/')
def agregar_a_grupo(request):
    competidores = request.POST.get('competidores')
    grupo = request.POST.get('grupo')
    array = []
    for c in competidores.split(','):
        array.append(int(c))
    c = Competidor.objects.filter(pk__in=array)
    g = Grupo.objects.filter(pk=grupo)
    if g.exists():
        g = g.first()
    else:
        return JsonResponse({'result': 0, "error": "El grupo no existe"})
    c.update(grupo=g)
    return JsonResponse({'result': 1})


@login_required(redirect_field_name='next', login_url='/webapp/login/')
def sacar_grupo(request):
    competidores = request.POST.get('competidores')
    array = []
    for c in competidores.split(','):
        array.append(int(c))
    c = Competidor.objects.filter(pk__in=array)
    c.update(grupo=None)
    return JsonResponse({'result': 1})
