from django.urls import path
from .views import (
    IndexView, ContatoView, SobreView, ContaView, 
    AlimentoList, AlimentoDetail, 
    ReceitaList, ReceitaDetail, 
    ImportarCSVView,
    CadastroView,
    RotinaCreate, RotinaDetail, RemoverItemRotinaView, SalvarItemRotinaView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    
    path("listar/alimento", AlimentoList.as_view(), name="alimento"),
    path("detalhar/alimento/<int:pk>/", AlimentoDetail.as_view(), name="alimento_detalhe"),
    
    path("receita/", ReceitaList.as_view(), name="receita"),
    path("detalhar/receita/<int:pk>/", ReceitaDetail.as_view(), name="receita_detalhe"),
    
    path("sobre/", SobreView.as_view(), name="sobre"),
    path("contato/", ContatoView.as_view(), name="contato"),
    
    path("conta/", ContaView.as_view(), name="conta"),
    
    path('cadastrar/rotina/', RotinaCreate.as_view(), name='criar_rotina'),
    path("detalhar/rotina/<int:pk>/", RotinaDetail.as_view(), name="rotina_detalhe"),
    path("rotina/salvar-item/<int:alimento_id>/", SalvarItemRotinaView.as_view(), name="salvar_item_rotina"),
    path("rotina/remover-item/<int:item_id>/", RemoverItemRotinaView.as_view(), name="remover_item_rotina"),
    
    path("importar/", ImportarCSVView.as_view(), name="importar_csv"),
    
    path('login/', auth_views.LoginView.as_view(next_page='index',template_name='nutri/login.html'), name='login'),
    path('login/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    
    path('cadastrar/usuario/', CadastroView.as_view(), name='cadastro'),
]