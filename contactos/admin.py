from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Contacto
from django.http import HttpResponse
import csv
from django.contrib.admin import SimpleListFilter


@admin.action(description='Exportar contactos seleccionados a CSV')
def exportar_a_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contactos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Teléfono', 'Fecha de Creación'])

    for contacto in queryset:
        writer.writerow([contacto.nombre, contacto.correo, contacto.telefono, contacto.fecha_creacion])

    return response


class FechaCreacionFilter(SimpleListFilter):
    title = 'Fecha de Creación'
    parameter_name = 'fecha_creacion'

    def lookups(self, request, model_admin):
        return [
            ('hoy', 'Hoy'),
            ('ayer', 'Ayer'),
            ('ultimos_7_dias', 'Últimos 7 días'),
            ('este_mes', 'Este mes'),
            ('ultimo_mes', 'Último mes'),
        ]

    def queryset(self, request, queryset):
        hoy = timezone.now().date()

        if self.value() == 'hoy':
            return queryset.filter(fecha_creacion__date=hoy)
        elif self.value() == 'ayer':
            ayer = hoy - timedelta(days=1)
            return queryset.filter(fecha_creacion__date=ayer)
        elif self.value() == 'ultimos_7_dias':
            semana_pasada = hoy - timedelta(days=7)
            return queryset.filter(fecha_creacion__date__gte=semana_pasada)
        elif self.value() == 'este_mes':
            return queryset.filter(fecha_creacion__month=hoy.month, fecha_creacion__year=hoy.year)
        elif self.value() == 'ultimo_mes':
            ultimo_mes = hoy.month - 1 if hoy.month > 1 else 12
            ultimo_ano = hoy.year if hoy.month > 1 else hoy.year - 1
            return queryset.filter(fecha_creacion__month=ultimo_mes, fecha_creacion__year=ultimo_ano)

        return queryset


class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'fecha_creacion')
    search_fields = ('nombre', 'correo', 'telefono')
    list_filter = (FechaCreacionFilter,)
    ordering = ('-fecha_creacion',)
    actions = [exportar_a_csv]
    readonly_fields = ('fecha_creacion',)

    fieldsets = (
        ('Información personal', {
            'fields': ('nombre', 'correo', 'telefono')
        }),
        ('Información adicional', {
            'fields': ('fecha_creacion',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change and not obj.fecha_creacion:
            obj.fecha_creacion = timezone.now()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-fecha_creacion')

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(Contacto, ContactoAdmin)

admin.site.site_header = "Administración de Contactos Personales"
admin.site.site_title = "Contactos Personales"
admin.site.index_title = "Panel de Administración"

