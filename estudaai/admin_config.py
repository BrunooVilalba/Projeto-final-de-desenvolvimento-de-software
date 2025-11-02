from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from .models import Category, Trail, Step, UserProgress, CustomTrail, LLMConversation


class EstudaAIAdminSite(AdminSite):
    site_header = "EstudaAI - Administração"
    site_title = "EstudaAI Admin"
    index_title = "Painel de Administração"


# Registrar o site personalizado
admin_site = EstudaAIAdminSite(name='estudaai_admin')

# Registrar modelos no admin personalizado
@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']


@admin.register(Trail, site=admin_site)
class TrailAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'estimated_hours', 'is_predefined', 'created_at']
    list_filter = ['category', 'difficulty', 'is_predefined', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['steps']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(Step, site=admin_site)
class StepAdmin(admin.ModelAdmin):
    list_display = ['title', 'trail', 'order', 'estimated_hours', 'is_optional']
    list_filter = ['trail', 'is_optional', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['trail', 'order']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('trail')


@admin.register(UserProgress, site=admin_site)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'step', 'completed', 'completed_at', 'created_at']
    list_filter = ['completed', 'completed_at', 'created_at']
    search_fields = ['user__username', 'user__email', 'step__title']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'step')


@admin.register(CustomTrail, site=admin_site)
class CustomTrailAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'title', 'description']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(LLMConversation, site=admin_site)
class LLMConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_type', 'message_preview', 'created_at']
    list_filter = ['message_type', 'created_at']
    search_fields = ['user__username', 'message', 'response']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Mensagem"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
