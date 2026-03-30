from . import views
from django.urls import path
from .views import IndexView, ContatoView, SobreView, ContaView, ReceitaView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("alimento/", views.alimento, name="alimento"),
    path("alimento/<int:id>/", views.alimento_detalhe, name="alimento_detalhe"),
    path("receita/", views.receita, name="receita"),
    path("receita/<int:id>/", views.receita_detalhe, name="receita_detalhe"),
    path("sobre/", SobreView.as_view(), name="sobre"),
    path("contato/", ContatoView.as_view(), name="contato"),
    path("conta/", ContaView.as_view(), name="conta"),
    path('importar/', views.importar_csv, name='importar_csv'),
]
