from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import LearningPath, Step
from .serializers import (
    LearningPathSerializer, 
    UserSerializer, 
    UserRegistrationSerializer,
    StepSerializer
)

User = get_user_model()


class UserRegistrationView(APIView):
    """View para registro de novos usuários"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """View para login que aceita email ou username"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email_or_username = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        
        if not email_or_username or not password:
            return Response(
                {'detail': 'Email/username e senha são obrigatórios'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Tentar autenticar com email ou username
        try:
            user = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=email_or_username)
            except User.DoesNotExist:
                return Response(
                    {'detail': 'Credenciais inválidas'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        user = authenticate(username=user.username, password=password)
        if user is None:
            return Response(
                {'detail': 'Credenciais inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })


class UserProfileView(APIView):
    """View para obter perfil do usuário autenticado"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LearningPathViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar trilhas de aprendizagem"""
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LearningPath.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Converte o formato do frontend para o formato esperado
        data = request.data.copy()
        if 'steps' in data:
            steps = data.pop('steps')
            data['steps_data'] = steps
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def toggle_step(self, request, pk=None):
        """Alterna o status de conclusão de uma etapa"""
        learning_path = self.get_object()
        step_index = request.data.get('step_index')
        
        try:
            steps = list(learning_path.step_set.all().order_by('order'))
            if 0 <= step_index < len(steps):
                step = steps[step_index]
                step.completed = not step.completed
                step.save()
                learning_path.calculate_progress()
                
                serializer = self.get_serializer(learning_path)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Índice de etapa inválido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
