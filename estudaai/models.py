from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Ícone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Iniciante'),
        ('intermediate', 'Intermediário'),
        ('advanced', 'Avançado'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, verbose_name="Dificuldade")
    estimated_hours = models.PositiveIntegerField(verbose_name="Horas Estimadas")
    is_predefined = models.BooleanField(default=True, verbose_name="Trilha Pré-definida")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Criado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Trilha"
        verbose_name_plural = "Trilhas"
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    @property
    def total_steps(self):
        return self.steps.count()
    
    @property
    def completed_steps_for_user(self, user):
        return UserProgress.objects.filter(
            user=user, 
            step__trail=self, 
            completed=True
        ).count()


class Step(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name='steps', verbose_name="Trilha")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    order = models.PositiveIntegerField(verbose_name="Ordem")
    estimated_hours = models.PositiveIntegerField(verbose_name="Horas Estimadas")
    is_optional = models.BooleanField(default=False, verbose_name="Opcional")
    resources = models.JSONField(default=list, blank=True, verbose_name="Recursos")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Etapa"
        verbose_name_plural = "Etapas"
        ordering = ['trail', 'order']
        unique_together = ['trail', 'order']
    
    def __str__(self):
        return f"{self.trail.title} - {self.title}"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, verbose_name="Etapa")
    completed = models.BooleanField(default=False, verbose_name="Concluída")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Concluída em")
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Progresso do Usuário"
        verbose_name_plural = "Progressos dos Usuários"
        unique_together = ['user', 'step']
    
    def __str__(self):
        return f"{self.user.username} - {self.step.title}"
    
    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        super().save(*args, **kwargs)


class CustomTrail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    llm_prompt = models.TextField(verbose_name="Prompt para LLM")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Trilha Personalizada"
        verbose_name_plural = "Trilhas Personalizadas"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class LLMConversation(models.Model):
    MESSAGE_TYPES = [
        ('trail_request', 'Solicitação de Trilha'),
        ('question', 'Pergunta'),
        ('suggestion', 'Sugestão'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    message = models.TextField(verbose_name="Mensagem")
    response = models.TextField(blank=True, verbose_name="Resposta")
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, verbose_name="Tipo de Mensagem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Conversa com LLM"
        verbose_name_plural = "Conversas com LLM"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.message_type} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
