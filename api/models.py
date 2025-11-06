from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Modelo de usuário estendido"""
    email = models.EmailField(unique=True, verbose_name='email address')
    course = models.CharField(max_length=100, blank=True, default='')
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('Iniciante', 'Iniciante'),
            ('Intermediário', 'Intermediário'),
            ('Avançado', 'Avançado'),
        ],
        default='Iniciante'
    )
    
    def __str__(self):
        return self.email or self.username


class SubStep(models.Model):
    """Sub-etapa de uma etapa de aprendizagem"""
    topic = models.CharField(max_length=200)
    link = models.URLField(max_length=500)
    
    def __str__(self):
        return self.topic


class Step(models.Model):
    """Etapa de uma trilha de aprendizagem"""
    learning_path = models.ForeignKey('LearningPath', on_delete=models.CASCADE, related_name='step_set', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    rationale = models.TextField()
    completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    sub_steps = models.ManyToManyField(SubStep, blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class LearningPath(models.Model):
    """Trilha de aprendizagem"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('Iniciante', 'Iniciante'),
            ('Intermediário', 'Intermediário'),
            ('Avançado', 'Avançado'),
        ]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    progress = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def calculate_progress(self):
        """Calcula o progresso baseado nas etapas concluídas"""
        total_steps = self.step_set.count()
        if total_steps == 0:
            return 0
        completed_steps = self.step_set.filter(completed=True).count()
        self.progress = int((completed_steps / total_steps) * 100)
        self.save()
        return self.progress
