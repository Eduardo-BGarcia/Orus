import csv
import io
from .models import Alimento
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

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
    
class ContaView(TemplateView):
    template_name = "nutri/conta.html"
    
class AlimentoView(TemplateView):
    template_name = "nutri/alimento.html"
    
class ReceitaView(TemplateView):
    template_name = "nutri/receita.html"
    

class ImportarCSVView(TemplateView):
    template_name = "nutri/importar_csv.html"
    
    
def alimento(request):
    
    query = request.GET.get('q', '')
    ordem = request.GET.get('ordem', '')

    if query != '' or ordem != '':
        alimentos = Alimento.objects.filter(receita=False)
        if query:
            alimentos = alimentos.filter(nome__icontains=query)

        campos_validos = [f.name for f in Alimento._meta.get_fields()]
        campo_limpo = ordem.replace('-', '')
        
        if campo_limpo in campos_validos:
            alimentos = alimentos.order_by(ordem)

        alimentos = alimentos[:30]

        campo_limpo = ordem.replace('-', '')
        if campo_limpo and campo_limpo in campos_validos:
            for a in alimentos:
                a.valor_destaque = getattr(a, campo_limpo)
                a.label_destaque = campo_limpo.replace('_', ' ')
        
        top_4_alimentos = Alimento.objects.filter(receita=False, visualizacoes__gt=0).order_by('-visualizacoes')[:4]
        
        context = {
            'alimentos': alimentos,
            'query': query,
            'ordem_atual': ordem,
            'top_4_alimentos': top_4_alimentos
        }
        
        return render(request, 'nutri/alimento.html', context)

    top_4_alimentos = Alimento.objects.filter(receita=False, visualizacoes__gt=0).order_by('-visualizacoes')[:4]
        
    context = {
        'alimentos': None,
        'query': query,
        'ordem_atual': None,
        'top_4_alimentos': top_4_alimentos
    }
    
    return render(request, 'nutri/alimento.html', context)

def alimento_detalhe(request, id):
    item = get_object_or_404(Alimento, id=id)
    Alimento.objects.filter(id=id).update(visualizacoes=F('visualizacoes') + 1)
    return render(request, 'nutri/alimento_detalhe.html', {'item': item})

def receita(request):
    query = request.GET.get('q', '')
    ordem = request.GET.get('ordem', '')

    if query != '' or ordem != '':
        receitas = Alimento.objects.filter(receita=True)

        if query:
            receitas = receitas.filter(nome__icontains=query)

        campos_validos = [f.name for f in Alimento._meta.get_fields()]
        campo_limpo = ordem.replace('-', '')
        
        if campo_limpo in campos_validos:
            receitas = receitas.order_by(ordem)

        receitas = receitas[:30]

        campo_limpo = ordem.replace('-', '')
        if campo_limpo and campo_limpo in campos_validos:
            for a in receitas:
                a.valor_destaque = getattr(a, campo_limpo)
                a.label_destaque = campo_limpo.replace('_', ' ')
        
        top_4_receitas = Alimento.objects.filter(receita=True).order_by('-visualizacoes')[:4]
        
        context = {
            'receitas': receitas,
            'query': query,
            'ordem_atual': ordem,
            'top_4_receitas': top_4_receitas
        }
        
        return render(request, 'nutri/receita.html', context)
    
    top_4_receitas = Alimento.objects.filter(receita=True, visualizacoes__gt=0).order_by('-visualizacoes')[:4]
        
    context = {
        'alimentos': None,
        'query': query,
        'ordem_atual': None,
        'top_4_receitas': top_4_receitas
    }
    
    return render(request, 'nutri/receita.html', context)

def receita_detalhe(request, id):
    item = get_object_or_404(Alimento, id=id)
    Alimento.objects.filter(id=id).update(visualizacoes=F('visualizacoes') + 1)
    return render(request, 'nutri/receita_detalhe.html', {'item': item})
    
def limpar_numero(valor):
    """
    Função auxiliar para tratar os números que vêm do CSV.
    Troca vírgula por ponto e converte 'NA' ou vazio para None.
    """
    if not valor:
        return None
    
    valor_limpo = valor.strip().upper()
    if valor_limpo == 'NA' or valor_limpo == '':
        return None
        
    try:
        return float(valor.replace(',', '.'))
    except ValueError:
        return None

def importar_csv(request):
    mensagens = []

    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo_csv')
        
        if not arquivo.name.endswith('.csv'):
            mensagens.append("Erro: O arquivo precisa ser um .csv")
        else:
            try:
                dataset = arquivo.read().decode('utf-8-sig')
                io_string = io.StringIO(dataset)
                leitor_csv = csv.reader(io_string, delimiter=';')
                next(leitor_csv) 
                lista_alimentos = []
                
                for linha in leitor_csv:
                    if not linha or len(linha) < 30:
                        continue
                        
                    alimento = Alimento(
                        nome=linha[1],
                        energia_kj=limpar_numero(linha[2]),
                        energia_kcal=limpar_numero(linha[3]),
                        umidade=limpar_numero(linha[4]),
                        carboidrato_total=limpar_numero(linha[5]),
                        carboidrato_disponivel=limpar_numero(linha[6]),
                        proteina=limpar_numero(linha[7]),
                        lipidios=limpar_numero(linha[8]),
                        fibra_alimentar=limpar_numero(linha[9]),
                        alcool=limpar_numero(linha[10]),
                        cinzas=limpar_numero(linha[11]),
                        colesterol=limpar_numero(linha[12]),
                        acidos_graxos_saturados=limpar_numero(linha[13]),
                        acidos_graxos_monoinsaturados=limpar_numero(linha[14]),
                        acidos_graxos_polinsaturados=limpar_numero(linha[15]),
                        acidos_graxos_trans=limpar_numero(linha[16]),
                        calcio=limpar_numero(linha[17]),
                        ferro=limpar_numero(linha[18]),
                        sodio=limpar_numero(linha[19]),
                        magnesio=limpar_numero(linha[20]),
                        fosforo=limpar_numero(linha[21]),
                        potassio=limpar_numero(linha[22]),
                        zinco=limpar_numero(linha[23]),
                        cobre=limpar_numero(linha[24]),
                        selenio=limpar_numero(linha[25]),
                        vitamina_a_re=limpar_numero(linha[26]),
                        vitamina_a_rae=limpar_numero(linha[27]),
                        vitamina_d=limpar_numero(linha[28]),
                        vitamina_e_alfa_toceferol=limpar_numero(linha[29]),
                        vitamina_b1_tiamina=limpar_numero(linha[30]),
                        vitamina_b2_riboflavina=limpar_numero(linha[31]),
                        vitamina_b3_niacina=limpar_numero(linha[32]),
                        vitamina_b6=limpar_numero(linha[33]),
                        vitamina_b12=limpar_numero(linha[34]),
                        vitamina_c=limpar_numero(linha[35]),
                        vitamina_b9=limpar_numero(linha[36]), 
                    )
                    lista_alimentos.append(alimento)
                
                Alimento.objects.bulk_create(lista_alimentos)
                
                mensagens.append(f"Sucesso! {len(lista_alimentos)} alimentos importados.")
                
            except Exception as e:
                mensagens.append(f"Ocorreu um erro durante a importação: {str(e)}")

    return render(request, 'nutri/importar_csv.html', {'mensagens': mensagens})