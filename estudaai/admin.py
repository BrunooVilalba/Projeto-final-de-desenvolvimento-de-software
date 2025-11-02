from django.contrib import admin
from .models import Category, Trail, Step, UserProgress, CustomTrail, LLMConversation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'estimated_hours', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']
    search_fields = ['title', 'description']


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['title', 'trail', 'order', 'estimated_hours', 'is_optional']
    list_filter = ['trail', 'is_optional']
    search_fields = ['title', 'description']
    ordering = ['trail', 'order']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'step', 'completed', 'completed_at']
    list_filter = ['completed', 'completed_at']
    search_fields = ['user__username', 'step__title']


@admin.register(CustomTrail)
class CustomTrailAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'title']


@admin.register(LLMConversation)
class LLMConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_type', 'created_at']
    list_filter = ['message_type', 'created_at']
    search_fields = ['user__username', 'message']
