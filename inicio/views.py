from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse


def home(request):
    return render(request, 'inicio/inicio.html')


def pagina_cadastro(request):
    """Renderiza o formulário de cadastro e processa submissões POST."""
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')

        if not username or not email or not password or not confirm:
            context['error'] = 'Todos os campos são obrigatórios.'
            return render(request, 'inicio/cadastro.html', context)

        if password != confirm:
            context['error'] = 'As senhas não coincidem.'
            return render(request, 'inicio/cadastro.html', context)

        if User.objects.filter(username=username).exists():
            context['error'] = 'Nome de usuário já cadastrado.'
            return render(request, 'inicio/cadastro.html', context)

        if User.objects.filter(email=email).exists():
            context['error'] = 'E-mail já cadastrado.'
            return render(request, 'inicio/cadastro.html', context)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            # Autenticar e fazer login do usuário após o cadastro
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')  # Redireciona para a página principal após o login
            else:
                context['error'] = 'Erro ao criar usuário. Tente novamente.'
                return render(request, 'inicio/cadastro.html', context)
        except Exception as e:
            context['error'] = f'Erro ao criar usuário: {str(e)}'
            return render(request, 'inicio/cadastro.html', context)

    return render(request, 'inicio/cadastro.html', context)


def api_login(request):
    """API endpoint para login via fetch (POST JSON).

    Recebe JSON: { email, password }
    Retorna JSON { redirect: '/' } em sucesso ou { error: '...'} em falha.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'Corpo inválido.'}, status=400)

    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return JsonResponse({'error': 'E-mail e senha são obrigatórios.'}, status=400)

    try:
        # Tentar encontrar o usuário pelo email
        user = User.objects.get(email__iexact=email)
        # Autenticar usando o username e senha
        user_auth = authenticate(request, username=user.username, password=password)
        
        if user_auth is None:
            return JsonResponse({'error': 'Senha incorreta.'}, status=400)
            
        login(request, user_auth)
        return JsonResponse({'redirect': '/homepage'})  # Redirecionar para a página homepage
        
    except User.DoesNotExist:
        return JsonResponse({'error': 'E-mail não encontrado.'}, status=400)


def homepage(request):
    # exigir autenticação: se não estiver logado, redireciona para a página inicial (login)
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'inicio/homepage2.html')


def logout_view(request):
    """Desloga o usuário e redireciona para a página inicial."""
    logout(request)
    return redirect('home')


def configuracoes(request):
    """Renderiza a página de configurações do usuário."""
    # exigir autenticação: se não estiver logado, redireciona para a página inicial (login)
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'inicio/configuracoes.html')