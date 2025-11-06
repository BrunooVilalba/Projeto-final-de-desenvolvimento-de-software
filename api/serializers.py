from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import LearningPath, Step, SubStep

User = get_user_model()


class SubStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStep
        fields = ['id', 'topic', 'link']


class StepSerializer(serializers.ModelSerializer):
    subSteps = SubStepSerializer(many=True, read_only=True, source='sub_steps')
    
    class Meta:
        model = Step
        fields = ['id', 'title', 'description', 'rationale', 'completed', 'order', 'subSteps']


class LearningPathSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True, source='step_set')
    steps_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = LearningPath
        fields = ['id', 'title', 'description', 'category', 'difficulty', 'progress', 
                  'created_at', 'updated_at', 'steps', 'steps_data']
        read_only_fields = ['id', 'created_at', 'updated_at', 'progress']
    
    def create(self, validated_data):
        steps_data = validated_data.pop('steps_data', [])
        user = self.context['request'].user
        learning_path = LearningPath.objects.create(user=user, **validated_data)
        
        for order, step_data in enumerate(steps_data):
            sub_steps_data = step_data.pop('subSteps', [])
            step = Step.objects.create(
                learning_path=learning_path,
                order=order,
                completed=False,
                **step_data
            )
            
            for sub_step_data in sub_steps_data:
                sub_step, _ = SubStep.objects.get_or_create(
                    topic=sub_step_data['topic'],
                    defaults={'link': sub_step_data.get('link', '')}
                )
                step.sub_steps.add(sub_step)
        
        return learning_path


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'course', 'experience_level']
        extra_kwargs = {'password': {'write_only': True}}


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'course', 'experience_level']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': False, 'allow_blank': True},
            'course': {'required': False, 'allow_blank': True},
            'experience_level': {'required': False},
        }
    
    def validate_email(self, value):
        """Valida se o email já existe no banco de dados"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está cadastrado.")
        return value
    
    def create(self, validated_data):
        # Se username não foi fornecido, usar email antes do @
        if 'username' not in validated_data or not validated_data['username']:
            validated_data['username'] = validated_data['email'].split('@')[0]
        user = User.objects.create_user(**validated_data)
        return user

