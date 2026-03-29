import csv
import io
from .models import Alimento
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "nutri/index.html"

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
        alimentos = Alimento.objects.filter(receita=False) # Exclui receitas da listagem de alimentos

        if query:
            alimentos = alimentos.filter(nome__icontains=query)

        # VALIDAÇÃO DE SEGURANÇA: Checa se a coluna que veio do HTML realmente existe no banco
        campos_validos = [f.name for f in Alimento._meta.get_fields()]
        campo_limpo = ordem.replace('-', '') # Tira o sinal de menos (que indica ordem decrescente)
        
        if campo_limpo in campos_validos:
            alimentos = alimentos.order_by(ordem)
        # else:
        #     alimentos = alimentos.order_by('nome') # Padrão alfabético

        alimentos = alimentos[:30]
        
        context = {
            'alimentos': alimentos,
            'query': query,
            'ordem_atual': ordem
        }
        
        return render(request, 'nutri/alimento.html', context)
    
    
    return render(request, 'nutri/alimento.html')

def alimento_detalhe(request, id):
    # Busca o alimento específico pelo ID
    item = get_object_or_404(Alimento, id=id)
    
    # Envia para a nova página
    return render(request, 'nutri/alimento_detalhe.html', {'item': item})
    
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
        # Troca a vírgula brasileira pelo ponto do padrão americano/banco de dados
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
                # Lendo o arquivo da memória. O encoding 'iso-8859-1' ou 'latin-1' 
                # ajuda com aqueles caracteres zoados que vimos no cabeçalho.
                dataset = arquivo.read().decode('utf-8-sig')
                io_string = io.StringIO(dataset)
                
                # Configuramos o delimitador como ponto e vírgula
                leitor_csv = csv.reader(io_string, delimiter=';')
                
                # Pula a primeira linha (cabeçalho)
                next(leitor_csv) 
                
                lista_alimentos = []
                
                for linha in leitor_csv:
                    # Ignora linhas totalmente vazias no final do arquivo
                    if not linha or len(linha) < 30:
                        continue
                        
                    # Mapeando as colunas do seu CSV para o modelo
                    # Os índices (linha[0], linha[1]) dependem da ordem exata do seu arquivo
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
                
                # O bulk_create salva toda a lista no banco de dados em uma única 
                # operação, deixando a performance incrível!
                Alimento.objects.bulk_create(lista_alimentos)
                
                mensagens.append(f"Sucesso! {len(lista_alimentos)} alimentos importados.")
                
            except Exception as e:
                mensagens.append(f"Ocorreu um erro durante a importação: {str(e)}")

    return render(request, 'nutri/importar_csv.html', {'mensagens': mensagens})