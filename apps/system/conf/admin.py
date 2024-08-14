from django.contrib import admin
from .models import Configuracao


@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('ativo', 'cf_codigo', 'cf_descricao', 'cf_valor')
    list_filter = ('ativo', 'cf_codigo', 'cf_descricao')
    search_fields = ('cf_codigo',)
    ordering = ('cf_codigo',)