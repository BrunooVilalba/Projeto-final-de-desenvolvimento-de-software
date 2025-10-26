from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.pk and not hasattr(self, 'user'):
            # Cria um usuário Django correspondente
            user = User.objects.create_user(
                username=self.email,
                email=self.email,
                password=self.senha
            )
            self.user = user
        super().save(*args, **kwargs)

class TrilhaEstudo(models.Model):
    nome_trilha = models.CharField(max_length=100)
    descricao_trilha = models.TextField()
    tipo = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_trilha

class TrilhaPersonalizada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='trilhas_personalizadas')
    nome_trilha = models.CharField(max_length=100)
    descricao_trilha = models.TextField()

    def __str__(self):
        return self.nome_trilha

class Atividade(models.Model):
    personalizada = models.ForeignKey(TrilhaPersonalizada, on_delete=models.CASCADE, related_name='atividades')
    trilha = models.ForeignKey(TrilhaEstudo, on_delete=models.CASCADE, related_name='atividades')
    nome_atividade = models.CharField(max_length=100)
    descricao_atividade = models.TextField()
    data_limite = models.DateTimeField()

    def __str__(self):
        return self.nome_atividade

class Progresso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='progresso')
    trilha = models.ForeignKey(TrilhaEstudo, on_delete=models.CASCADE, related_name='progresso')
    percentual_conclusao = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.usuario.nome} - {self.trilha.nome_trilha}'

class Feedback(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='feedbacks')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='feedbacks')
    comentario = models.TextField()
    data_feedback = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback de {self.usuario.nome} - {self.atividade.nome_atividade}'

class Conteudo(models.Model):
    trilha = models.ForeignKey(TrilhaEstudo, on_delete=models.CASCADE, related_name='conteudos')
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    duracao = models.IntegerField(help_text='Duração em minutos')

    def __str__(self):
        return self.titulo
