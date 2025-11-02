from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from .models import Category, Trail, Step, UserProgress, CustomTrail, LLMConversation
from .forms import CustomUserCreationForm, CustomTrailForm, LLMQuestionForm
from .llm_service import LLMService
import json


def home(request):
    """Página inicial"""
    categories = Category.objects.all()[:6]
    featured_trails = Trail.objects.filter(is_predefined=True)[:3]
    return render(request, 'estudaai/home.html', {
        'categories': categories,
        'featured_trails': featured_trails
    })


def register_view(request):
    """Registro de usuário"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'estudaai/register.html', {'form': form})


def login_view(request):
    """Login de usuário"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return render(request, 'estudaai/login_simple.html')


def logout_view(request):
    """Logout de usuário"""
    logout(request)
    messages.info(request, 'Logout realizado com sucesso!')
    return redirect('home')


@login_required
def dashboard(request):
    """Dashboard do usuário"""
    # Trilhas em progresso (enrolled trails)
    enrolled_trails = Trail.objects.filter(
        steps__userprogress__user=request.user
    ).distinct()
    
    # Estatísticas
    total_steps = Step.objects.filter(trail__in=enrolled_trails).count()
    completed_steps = UserProgress.objects.filter(user=request.user, completed=True).count()
    progress_percentage = int((completed_steps / total_steps * 100)) if total_steps > 0 else 0
    
    # Adicionar progresso para cada trilha
    for trail in enrolled_trails:
        trail_steps = trail.steps.count()
        trail_completed = UserProgress.objects.filter(
            user=request.user, 
            step__trail=trail, 
            completed=True
        ).count()
        trail.progress_percentage = int((trail_completed / trail_steps * 100)) if trail_steps > 0 else 0
        trail.completed_steps = trail_completed
        trail.total_steps = trail_steps
    
    return render(request, 'estudaai/dashboard.html', {
        'enrolled_trails': enrolled_trails,
        'total_steps': total_steps,
        'completed_steps': completed_steps,
        'progress_percentage': progress_percentage,
    })


@login_required
def trail_list(request):
    """Lista de trilhas disponíveis com sistema de recomendação"""
    category_id = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    recommendation_type = request.GET.get('recommendation', 'all')
    
    trails = Trail.objects.filter(is_predefined=True)
    
    if category_id:
        trails = trails.filter(category_id=category_id)
    if difficulty:
        trails = trails.filter(difficulty=difficulty)
    if search:
        trails = trails.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    # Sistema de recomendação
    if recommendation_type == 'recommended' and request.user.is_authenticated:
        # Trilhas recomendadas baseadas no progresso do usuário
        user_completed_categories = Trail.objects.filter(
            steps__userprogress__user=request.user,
            steps__userprogress__completed=True
        ).values_list('category', flat=True).distinct()
        
        # Recomendar trilhas de categorias similares ou novas
        recommended_trails = trails.filter(
            Q(category__in=user_completed_categories) | 
            Q(difficulty='beginner')
        ).distinct()[:6]
        
        trails = recommended_trails
    
    elif recommendation_type == 'popular':
        # Trilhas mais populares (baseado em inscrições)
        trails = trails.annotate(
            enrollment_count=Count('steps__userprogress__user', distinct=True)
        ).order_by('-enrollment_count')[:6]
    
    # Adicionar informações de progresso para cada trilha
    if request.user.is_authenticated:
        for trail in trails:
            trail_steps = trail.steps.count()
            trail_completed = UserProgress.objects.filter(
                user=request.user, 
                step__trail=trail, 
                completed=True
            ).count()
            trail.progress_percentage = int((trail_completed / trail_steps * 100)) if trail_steps > 0 else 0
            trail.is_enrolled = trail_completed > 0
            trail.completed_steps = trail_completed
            trail.total_steps = trail_steps
    
    categories = Category.objects.all()
    difficulties = Trail.DIFFICULTY_CHOICES
    
    return render(request, 'estudaai/trail_list.html', {
        'trails': trails,
        'categories': categories,
        'difficulties': difficulties,
        'selected_category': category_id,
        'selected_difficulty': difficulty,
        'search_query': search,
        'recommendation_type': recommendation_type,
    })


@login_required
def trail_detail(request, trail_id):
    """Detalhes da trilha"""
    trail = get_object_or_404(Trail, id=trail_id)
    steps = trail.steps.all().order_by('order')
    
    # Progresso do usuário
    user_progress = {}
    for step in steps:
        try:
            progress = UserProgress.objects.get(user=request.user, step=step)
            user_progress[step.id] = progress
        except UserProgress.DoesNotExist:
            user_progress[step.id] = None
    
    # Calcular progresso geral
    completed_steps = UserProgress.objects.filter(
        user=request.user,
        step__trail=trail,
        completed=True
    ).count()
    total_steps = steps.count()
    progress_percentage = (completed_steps / total_steps * 100) if total_steps > 0 else 0
    
    return render(request, 'estudaai/trail_detail.html', {
        'trail': trail,
        'steps': steps,
        'user_progress': user_progress,
        'completed_steps': completed_steps,
        'total_steps': total_steps,
        'progress_percentage': progress_percentage
    })


@login_required
def enroll_trail(request, trail_id):
    """Inscrever usuário em uma trilha"""
    trail = get_object_or_404(Trail, id=trail_id)
    
    # Verificar se já está inscrito
    user_has_progress = UserProgress.objects.filter(
        user=request.user,
        step__trail=trail
    ).exists()
    
    if not user_has_progress:
        # Criar progresso para todas as etapas da trilha
        for step in trail.steps.all():
            UserProgress.objects.get_or_create(
                user=request.user,
                step=step,
                defaults={'completed': False}
            )
        messages.success(request, f'Você foi inscrito na trilha "{trail.title}"!')
    else:
        messages.info(request, f'Você já está inscrito na trilha "{trail.title}".')
    
    return redirect('trail_detail', trail_id=trail.id)


@login_required
@require_POST
def mark_step_complete(request, step_id):
    """Marcar etapa como concluída"""
    step = get_object_or_404(Step, id=step_id)
    
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        step=step
    )
    
    if request.POST.get('completed') == 'true':
        progress.completed = True
        progress.save()
        message = f'Etapa "{step.title}" marcada como concluída!'
    else:
        progress.completed = False
        progress.save()
        message = f'Etapa "{step.title}" marcada como não concluída.'
    
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({
            'success': True,
            'message': message,
            'completed': progress.completed
        })
    
    messages.success(request, message)
    return redirect('trail_detail', trail_id=step.trail.id)


@login_required
def create_custom_trail(request):
    """Criar trilha personalizada com IA"""
    if request.method == 'POST':
        form = CustomTrailForm(request.POST)
        if form.is_valid():
            # Salvar descrição da trilha personalizada
            custom_trail = form.save(commit=False)
            custom_trail.user = request.user
            custom_trail.llm_prompt = form.cleaned_data['description']
            custom_trail.save()
            
            # Gerar trilha com IA
            llm_service = LLMService()
            trail = llm_service.generate_custom_trail(
                form.cleaned_data['description'], 
                request.user
            )
            
            if trail:
                messages.success(request, 'Trilha personalizada criada com sucesso!')
                return redirect('trail_detail', trail_id=trail.id)
            else:
                messages.error(request, 'Erro ao gerar trilha personalizada. Tente novamente.')
    else:
        form = CustomTrailForm()
    
    return render(request, 'estudaai/create_custom_trail.html', {'form': form})


@login_required
def ai_chat(request):
    """Interface de chat com IA"""
    if request.method == 'POST':
        form = LLMQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['message']
            
            # Salvar pergunta
            conversation = form.save(commit=False)
            conversation.user = request.user
            conversation.message_type = 'question'
            conversation.save()
            
            # Obter resposta da IA
            llm_service = LLMService()
            response = llm_service.answer_question(question, request.user)
            
            # Salvar resposta
            conversation.response = response
            conversation.save()
            
            messages.success(request, 'Pergunta enviada!')
            return redirect('ai_chat')
    else:
        form = LLMQuestionForm()
    
    # Histórico de conversas
    conversations = LLMConversation.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    return render(request, 'estudaai/ai_chat.html', {
        'form': form,
        'conversations': conversations
    })


@login_required
def my_trails(request):
    """Minhas trilhas (em progresso e concluídas)"""
    # Trilhas em progresso
    trails_in_progress = Trail.objects.filter(
        steps__userprogress__user=request.user,
        steps__userprogress__completed=False
    ).distinct()
    
    # Trilhas concluídas
    completed_trails = Trail.objects.filter(
        steps__userprogress__user=request.user,
        steps__userprogress__completed=True
    ).distinct()
    
    return render(request, 'estudaai/my_trails.html', {
        'trails_in_progress': trails_in_progress,
        'completed_trails': completed_trails
    })


def category_list(request):
    """Lista de categorias"""
    categories = Category.objects.annotate(
        trail_count=Count('trail', filter=Q(trail__is_predefined=True))
    ).order_by('name')
    
    return render(request, 'estudaai/category_list.html', {
        'categories': categories
    })


def category_detail(request, category_id):
    """Detalhes da categoria"""
    category = get_object_or_404(Category, id=category_id)
    trails = category.trail_set.filter(is_predefined=True)
    
    return render(request, 'estudaai/category_detail.html', {
        'category': category,
        'trails': trails
    })
