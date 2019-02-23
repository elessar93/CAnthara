from django.urls import path

from webapp.views import CompetenciasAjaxList, PorAsignarAjaxList, GrupoAjaxList
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('competencias/ajax/list/', CompetenciasAjaxList.as_view(), name='competencias_list'),
    path('sin_asignar/<int:pk>/', views.por_asignar, name='por_asignar'),
    path('grupos/<int:pk>/', views.grupos, name='grupos'),
    path('grupo/list/<int:pk>/', views.grupo_list, name='grupo'),
    path('grupo/ajax/list/<int:pk>/', GrupoAjaxList.as_view(), name='grupo_list'),
    path('sin_asignar/ajax/list/<int:pk>/', PorAsignarAjaxList.as_view(), name='por_asignar_list'),
    path('agregar_a_grupo/', views.agregar_a_grupo, name='agregar_a_grupo')

]
