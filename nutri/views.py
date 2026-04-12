import csv
import io
from .models import Alimento, Rotina, ItemRotina
from django.db.models import F
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin

class CadastroView(CreateView):
    template_name = "nutri/cadastrar_usuario.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

class IndexView(TemplateView):
    template_name = "nutri/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_alimentos'] = Alimento.objects.filter().order_by('-visualizacoes')[:4]
        return context

class ContatoView(TemplateView):
    template_name = "nutri/contato.html"

class SobreView(TemplateView):
    template_name = "nutri/sobre.html"
    
class ContaView(LoginRequiredMixin, TemplateView):
    template_name = "nutri/conta.html"
    login_url = '/login/'
    

class RotinaCreate(LoginRequiredMixin, CreateView):
    model = Rotina
    fields = ['nome', 'data', 'descricao']
    template_name = "nutri/cadastrar_rotina.html"
    success_url = reverse_lazy('conta')

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        return super().form_valid(form)
    

class RotinaDetail(LoginRequiredMixin, DetailView):
    model = Rotina
    template_name = "nutri/rotina_detalhe.html"
    context_object_name = "rotina"

    # Garantir que o usuário só veja as PRÓPRIAS rotinas
    def get_queryset(self):
        return Rotina.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rotina = self.get_object()
        itens = rotina.itens.select_related('alimento').all()

        # 1. AGRUPAR POR REFEIÇÃO
        refeicoes = {
            'cafe': [], 'almoco': [], 'lanche': [], 'jantar': []
        }
        for item in itens:
            refeicoes[item.refeicao].append(item)
        context['refeicoes'] = refeicoes

        # 2. CALCULAR TOTAIS MATEMÁTICOS
        # Defina aqui os campos que você quer somar (use os exatos nomes do seu model Alimento)
        campos_para_somar = [
            # Energia e Outros Componentes
            'energia_kj', 'energia_kcal', 'umidade', 'cinzas', 
            'alcool', 'sal_adicao', 'acucar_adicao',
            
            # Macronutrientes
            'carboidrato_total', 'carboidrato_disponivel', 'proteina', 
            'lipidios', 'fibra_alimentar',
            
            # Perfil Lipídico
            'colesterol', 'acidos_graxos_saturados', 'acidos_graxos_monoinsaturados', 
            'acidos_graxos_polinsaturados', 'acidos_graxos_trans',
            
            # Minerais
            'calcio', 'ferro', 'sodio', 'magnesio', 'fosforo', 
            'potassio', 'zinco', 'cobre', 'selenio',
            
            # Vitaminas
            'vitamina_a_re', 'vitamina_a_rae', 'vitamina_d', 'vitamina_e_alfa_toceferol', 
            'vitamina_b1_tiamina', 'vitamina_b2_riboflavina', 'vitamina_b3_niacina', 
            'vitamina_b6', 'vitamina_b12', 'vitamina_c', 'vitamina_b9'
        ]

        # Inicia todos os totais zerados
        totais = {campo: 0 for campo in campos_para_somar}

        for item in itens:
            # Fator de proporção: se comeu 150g, o fator é 1.5 (150 / 100)
            fator = float(item.quantidade_gramas) / 100.0

            for campo in campos_para_somar:
                valor_alimento = getattr(item.alimento, campo)
                if valor_alimento: # Verifica se o valor não é nulo/None no banco
                    totais[campo] += float(valor_alimento) * fator

        context['totais'] = totais
        return context

class SalvarItemRotinaView(LoginRequiredMixin, View):
    def post(self, request, alimento_id):
        rotina_id = request.POST.get('rotina_id')
        refeicao = request.POST.get('refeicao')
        quantidade = request.POST.get('quantidade')

        rotina = get_object_or_404(Rotina, id=rotina_id, usuario=request.user)
        alimento = get_object_or_404(Alimento, id=alimento_id)

        ItemRotina.objects.create(
            rotina=rotina,
            alimento=alimento,
            refeicao=refeicao,
            quantidade_gramas=quantidade
        )

        # MUDANÇA AQUI: Redireciona para o detalhe DA ROTINA, usando o ID dela
        return redirect('rotina_detalhe', pk=rotina.id)

# --- VIEW PARA EXCLUIR UM ITEM DA ROTINA ---
class RemoverItemRotinaView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(ItemRotina, id=item_id, rotina__usuario=request.user)
        rotina_id = item.rotina.id
        item.delete()
        return redirect('rotina_detalhe', pk=rotina_id)

# --- ÁREA DE ALIMENTOS ---

class AlimentoList(ListView):
    model = Alimento
    template_name = "nutri/alimento.html"
    context_object_name = "alimentos"

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        ordem = self.request.GET.get('ordem', '')

        if not query and not ordem:
            return Alimento.objects.none() 

        alimentos = Alimento.objects.filter(receita=False)

        if query:
            alimentos = alimentos.filter(nome__icontains=query)

        campos_validos = [f.name for f in Alimento._meta.get_fields()]
        campo_limpo = ordem.replace('-', '')

        if campo_limpo in campos_validos:
            alimentos = alimentos.order_by(ordem)
            
        alimentos = list(alimentos[:30])

        if campo_limpo and campo_limpo in campos_validos:
            for a in alimentos:
                a.valor_destaque = getattr(a, campo_limpo, 0)
                a.label_destaque = campo_limpo.replace('_', ' ')

        return alimentos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        ordem = self.request.GET.get('ordem', '')
        
        context['top_4_alimentos'] = Alimento.objects.filter(
            receita=False, visualizacoes__gt=0
        ).order_by('-visualizacoes')[:4]

        context['query'] = query
        context['ordem_atual'] = ordem
        context['houve_busca'] = bool(query or ordem)
        
        return context

class AlimentoDetail(DetailView):
    model = Alimento
    template_name = "nutri/alimento_detalhe.html"
    context_object_name = "item"
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Alimento.objects.filter(pk=obj.pk).update(visualizacoes=F('visualizacoes') + 1)
        obj.visualizacoes += 1
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['minhas_rotinas'] = Rotina.objects.filter(usuario=self.request.user).order_by('-criado_em')
        return context

# --- ÁREA DE RECEITAS ---

class ReceitaList(ListView):
    model = Alimento
    template_name = "nutri/receita.html"
    context_object_name = "receitas"

    def get_queryset(self):
        
        
        query = self.request.GET.get('q', '')
        ordem = self.request.GET.get('ordem', '')

        if not query and not ordem:
            return Alimento.objects.none() 
        
        receitas = Alimento.objects.filter(receita=True)

        if query:
            receitas = receitas.filter(nome__icontains=query)

        campos_validos = [f.name for f in Alimento._meta.get_fields()]
        campo_limpo = ordem.replace('-', '')
        
        if campo_limpo in campos_validos:
            receitas = receitas.order_by(ordem)

        receitas = list(receitas[:30])

        if campo_limpo and campo_limpo in campos_validos:
            for a in receitas:
                a.valor_destaque = getattr(a, campo_limpo, 0)
                a.label_destaque = campo_limpo.replace('_', ' ')

        return receitas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        ordem = self.request.GET.get('ordem', '')

        context['top_4_receitas'] = Alimento.objects.filter(
            receita=True, visualizacoes__gt=0
        ).order_by('-visualizacoes')[:4]
        
        context['query'] = query
        context['ordem_atual'] = ordem
        context['houve_busca'] = bool(query or ordem)
        return context


class ReceitaDetail(DetailView):
    model = Alimento
    template_name = "nutri/receita_detalhe.html"
    context_object_name = "item"
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Alimento.objects.filter(pk=obj.pk).update(visualizacoes=F('visualizacoes') + 1)
        obj.visualizacoes += 1
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['minhas_rotinas'] = Rotina.objects.filter(usuario=self.request.user).order_by('-criado_em')
        return context

# --- IMPORTAÇÃO DE CSV ---

def limpar_numero(valor):
    """Função auxiliar para tratar os números que vêm do CSV."""
    if not valor:
        return None
    
    valor_limpo = valor.strip().upper()
    if valor_limpo == 'NA' or valor_limpo == '':
        return None
        
    try:
        return float(valor.replace(',', '.'))
    except ValueError:
        return None

class ImportarCSVView(View):
    template_name = "nutri/importar_csv.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        mensagens = []
        arquivo = request.FILES.get('arquivo_csv')
        
        if not arquivo or not arquivo.name.endswith('.csv'):
            mensagens.append("Erro: O arquivo não foi enviado ou precisa ser um .csv")
        else:
            try:
                dataset = arquivo.read().decode('utf-8-sig')
                io_string = io.StringIO(dataset)
                leitor_csv = csv.reader(io_string, delimiter=';')
                next(leitor_csv) # Pula o cabeçalho
                
                lista_alimentos = []
                
                for linha in leitor_csv:
                    if not linha or len(linha) < 30:
                        continue
                        
                    alimento = Alimento(
                        nome=linha[1],
                        energia_kj=limpar_numero(linha[2]),
                        energia_kcal=limpar_numero(linha[3]),
                        # ... Resto dos seus campos ...
                        vitamina_b9=limpar_numero(linha[36]), 
                    )
                    lista_alimentos.append(alimento)
                
                Alimento.objects.bulk_create(lista_alimentos)
                mensagens.append(f"Sucesso! {len(lista_alimentos)} itens importados.")
                
            except Exception as e:
                mensagens.append(f"Ocorreu um erro durante a importação: {str(e)}")

        return render(request, self.template_name, {'mensagens': mensagens})