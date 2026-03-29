from django.db import models

class Alimento(models.Model):
    # 1. Informações Básicas
    excluido = models.BooleanField(default=False, verbose_name="Excluído")
    nome = models.CharField(max_length=1000, verbose_name="Alimento")
    receita = models.BooleanField(default=False, verbose_name="É uma receita?")
    energia_kj = models.IntegerField(null=True, default=0, blank=True, verbose_name="Energia (KJ)")
    energia_kcal = models.IntegerField(null=True, blank=True, default=0, verbose_name="Energia (Kcal)")
    umidade = models.FloatField(null=True, blank=True, default=0, verbose_name="Umidade (g)")
    cinzas = models.FloatField(null=True, blank=True, default=0, verbose_name="Cinzas (g)")
    alcool = models.FloatField(null=True, blank=True, default=0, verbose_name="Álcool (g)")
    sal_adicao = models.FloatField(null=True, blank=True, default=0, verbose_name="Sal de adição (g)")
    acucar_adicao = models.FloatField(null=True, blank=True, default=0, verbose_name="Açúcar de adição (g)")

    # 2. Macronutrientes
    carboidrato_total = models.FloatField(null=True, blank=True, default=0, verbose_name="Carboidrato total (g)")
    carboidrato_disponivel = models.FloatField(null=True, blank=True, default=0, verbose_name="Carboidrato disponível (g)")
    proteina = models.FloatField(null=True, blank=True, default=0, verbose_name="Proteína (g)")
    lipidios = models.FloatField(null=True, blank=True, default=0, verbose_name="Lipídios (g)")
    fibra_alimentar = models.FloatField(null=True, blank=True, default=0, verbose_name="Fibra alimentar (g)")

    # 3. Perfil Lipídico
    colesterol = models.FloatField(null=True, blank=True, default=0, verbose_name="Colesterol (mg)")
    acidos_graxos_saturados = models.FloatField(null=True, blank=True, default=0, verbose_name="Saturados (g)")
    acidos_graxos_monoinsaturados = models.FloatField(null=True, blank=True, default=0, verbose_name="Monoinsaturados (g)")
    acidos_graxos_polinsaturados = models.FloatField(null=True, blank=True, default=0, verbose_name="Polinsaturados (g)")
    acidos_graxos_trans = models.FloatField(null=True, blank=True, default=0, verbose_name="Trans (g)")

    # 4. Minerais (Onde entra o Sódio!)
    calcio = models.FloatField(null=True, blank=True, default=0, verbose_name="Cálcio (mg)")
    ferro = models.FloatField(null=True, blank=True, default=0, verbose_name="Ferro (mg)")
    sodio = models.FloatField(null=True, blank=True, default=0, verbose_name="Sódio (mg)")
    magnesio = models.FloatField(null=True, blank=True, default=0, verbose_name="Magnésio (mg)")
    fosforo = models.FloatField(null=True, blank=True, default=0, verbose_name="Fósforo (mg)")
    potassio = models.FloatField(null=True, blank=True, default=0, verbose_name="Potássio (mg)")
    zinco = models.FloatField(null=True, blank=True, default=0, verbose_name="Zinco (mg)")
    cobre = models.FloatField(null=True, blank=True, default=0, verbose_name="Cobre (mg)")
    selenio = models.FloatField(null=True, blank=True, default=0, verbose_name="Selênio (mcg)")

    # 5. Vitaminas
    vitamina_a_re = models.FloatField(null=True, blank=True, default=0, verbose_name="Vitamina A (RE)")
    vitamina_a_rae = models.FloatField(null=True, blank=True, default=0, verbose_name="Vitamina A (RAE)")
    vitamina_d = models.FloatField(null=True, blank=True, default=0, verbose_name="Vitamina D (mcg)")
    vitamina_e_alfa_toceferol = models.FloatField(null=True, blank=True, default=0, verbose_name="Vitamina E (mg)")
    vitamina_b1_tiamina = models.FloatField(null=True, blank=True, default=0, verbose_name="Tiamina B1 (mg)")
    vitamina_b2_riboflavina = models.FloatField(null=True, blank=True, default=0, verbose_name="Riboflavina B2 (mg)")
    vitamina_b3_niacina = models.FloatField(null=True, blank=True, default=0, verbose_name="Niacina B3 (mg)")
    vitamina_b6 = models.FloatField(null=True, blank=True, default=0, verbose_name="Vitamina B6 (mg)")
    vitamina_b12 = models.FloatField(null=True, blank=True, default=0, verbose_name="Vitamina B12 (mcg)")
    vitamina_c = models.FloatField(null=True, blank=True, default=0, verbose_name="Vitamina C (mg)")
    vitamina_b9 = models.FloatField(null=True, blank=True, default=0, verbose_name="Folato B9 (mcg)")

    # 6. Mídia
    # O upload_to define em qual subpasta dentro da sua pasta 'media' as fotos serão salvas.
    foto = models.ImageField(upload_to='fotos_alimentos/', null=True, blank=True, default=0, verbose_name="Foto do Alimento")

    def __str__(self):
        return self.nome