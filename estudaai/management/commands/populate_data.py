from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from estudaai.models import Category, Trail, Step


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando população de dados...')
        
        # Criar usuário admin se não existir
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@estudaai.com',
                password='admin123',
                first_name='Administrador',
                last_name='EstudaAI'
            )
            self.stdout.write(self.style.SUCCESS('Usuário admin criado'))
        
        # Criar categorias
        categories_data = [
            {
                'name': 'Desenvolvimento Web',
                'description': 'Aprenda a criar sites e aplicações web modernas',
                'icon': 'fas fa-code'
            },
            {
                'name': 'Ciência de Dados',
                'description': 'Análise de dados, estatística e machine learning',
                'icon': 'fas fa-chart-bar'
            },
            {
                'name': 'Inteligência Artificial',
                'description': 'Fundamentos de IA, machine learning e deep learning',
                'icon': 'fas fa-robot'
            },
            {
                'name': 'Segurança da Informação',
                'description': 'Cibersegurança, ethical hacking e proteção de dados',
                'icon': 'fas fa-shield-alt'
            },
            {
                'name': 'Soft Skills & Carreira',
                'description': 'Desenvolvimento pessoal e habilidades profissionais',
                'icon': 'fas fa-users'
            }
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Categoria criada: {category.name}')
        
        # Criar trilhas
        trails_data = [
            {
                'title': 'Front-End com React',
                'description': 'Aprenda a criar interfaces modernas e interativas com React, HTML, CSS e JavaScript',
                'category': 'Desenvolvimento Web',
                'difficulty': 'beginner',
                'estimated_hours': 40,
                'steps': [
                    {
                        'title': 'Fundamentos de HTML e CSS',
                        'description': 'Aprenda a estrutura básica de páginas web e estilização',
                        'order': 1,
                        'estimated_hours': 8,
                        'resources': ['MDN Web Docs', 'W3Schools HTML Tutorial']
                    },
                    {
                        'title': 'JavaScript Essencial',
                        'description': 'Domine os conceitos fundamentais de JavaScript',
                        'order': 2,
                        'estimated_hours': 12,
                        'resources': ['JavaScript.info', 'Eloquent JavaScript']
                    },
                    {
                        'title': 'Introdução ao React',
                        'description': 'Conceitos básicos do React e JSX',
                        'order': 3,
                        'estimated_hours': 10,
                        'resources': ['React Official Docs', 'React Tutorial']
                    },
                    {
                        'title': 'Componentes e Props',
                        'description': 'Criação e reutilização de componentes',
                        'order': 4,
                        'estimated_hours': 6,
                        'resources': ['React Components Guide']
                    },
                    {
                        'title': 'Estado e Ciclo de Vida',
                        'description': 'Gerenciamento de estado com useState e useEffect',
                        'order': 5,
                        'estimated_hours': 8,
                        'resources': ['React Hooks Guide']
                    },
                    {
                        'title': 'Roteamento com React Router',
                        'description': 'Navegação entre páginas em aplicações React',
                        'order': 6,
                        'estimated_hours': 6,
                        'resources': ['React Router Docs']
                    }
                ]
            },
            {
                'title': 'Análise de Dados com Python',
                'description': 'Domine Python para manipulação, análise e visualização de dados',
                'category': 'Ciência de Dados',
                'difficulty': 'intermediate',
                'estimated_hours': 50,
                'steps': [
                    {
                        'title': 'Python para Análise de Dados',
                        'description': 'Fundamentos do Python aplicado à análise de dados',
                        'order': 1,
                        'estimated_hours': 10,
                        'resources': ['Python Data Science Handbook']
                    },
                    {
                        'title': 'Pandas - Manipulação de Dados',
                        'description': 'Aprenda a usar Pandas para manipular DataFrames',
                        'order': 2,
                        'estimated_hours': 15,
                        'resources': ['Pandas Documentation', '10 Minutes to Pandas']
                    },
                    {
                        'title': 'NumPy - Computação Numérica',
                        'description': 'Arrays multidimensionais e operações matemáticas',
                        'order': 3,
                        'estimated_hours': 8,
                        'resources': ['NumPy User Guide']
                    },
                    {
                        'title': 'Visualização com Matplotlib e Seaborn',
                        'description': 'Criação de gráficos e visualizações de dados',
                        'order': 4,
                        'estimated_hours': 12,
                        'resources': ['Matplotlib Tutorial', 'Seaborn Gallery']
                    },
                    {
                        'title': 'Análise Estatística',
                        'description': 'Conceitos de estatística aplicada à análise de dados',
                        'order': 5,
                        'estimated_hours': 5,
                        'resources': ['Think Stats', 'Statistics for Data Science']
                    }
                ]
            },
            {
                'title': 'Fundamentos de Machine Learning',
                'description': 'Introdução aos conceitos e algoritmos de machine learning',
                'category': 'Inteligência Artificial',
                'difficulty': 'intermediate',
                'estimated_hours': 60,
                'steps': [
                    {
                        'title': 'Matemática para ML',
                        'description': 'Álgebra linear, cálculo e estatística para machine learning',
                        'order': 1,
                        'estimated_hours': 15,
                        'resources': ['Mathematics for Machine Learning']
                    },
                    {
                        'title': 'Regressão Linear e Logística',
                        'description': 'Algoritmos de regressão e classificação básicos',
                        'order': 2,
                        'estimated_hours': 12,
                        'resources': ['Scikit-learn User Guide']
                    },
                    {
                        'title': 'Árvores de Decisão e Random Forest',
                        'description': 'Algoritmos baseados em árvores de decisão',
                        'order': 3,
                        'estimated_hours': 10,
                        'resources': ['Decision Trees in ML']
                    },
                    {
                        'title': 'Clustering e Dimensionalidade',
                        'description': 'K-means, PCA e técnicas de redução de dimensionalidade',
                        'order': 4,
                        'estimated_hours': 8,
                        'resources': ['Clustering Algorithms Guide']
                    },
                    {
                        'title': 'Redes Neurais Básicas',
                        'description': 'Introdução às redes neurais e perceptron',
                        'order': 5,
                        'estimated_hours': 15,
                        'resources': ['Neural Networks and Deep Learning']
                    }
                ]
            },
            {
                'title': 'Introdução à Cibersegurança',
                'description': 'Conceitos fundamentais de segurança da informação',
                'category': 'Segurança da Informação',
                'difficulty': 'beginner',
                'estimated_hours': 35,
                'steps': [
                    {
                        'title': 'Conceitos de Segurança',
                        'description': 'Fundamentos da segurança da informação',
                        'order': 1,
                        'estimated_hours': 8,
                        'resources': ['CISSP Study Guide']
                    },
                    {
                        'title': 'Criptografia Básica',
                        'description': 'Conceitos de criptografia simétrica e assimétrica',
                        'order': 2,
                        'estimated_hours': 10,
                        'resources': ['Applied Cryptography']
                    },
                    {
                        'title': 'Segurança de Redes',
                        'description': 'Proteção de redes e protocolos de segurança',
                        'order': 3,
                        'estimated_hours': 8,
                        'resources': ['Network Security Essentials']
                    },
                    {
                        'title': 'Boas Práticas de Segurança',
                        'description': 'Implementação de medidas de segurança',
                        'order': 4,
                        'estimated_hours': 9,
                        'resources': ['OWASP Top 10', 'NIST Cybersecurity Framework']
                    }
                ]
            },
            {
                'title': 'Comunicação e Trabalho em Equipe',
                'description': 'Desenvolva habilidades interpessoais e de colaboração',
                'category': 'Soft Skills & Carreira',
                'difficulty': 'beginner',
                'estimated_hours': 25,
                'steps': [
                    {
                        'title': 'Comunicação Eficaz',
                        'description': 'Técnicas para comunicação clara e assertiva',
                        'order': 1,
                        'estimated_hours': 6,
                        'resources': ['Crucial Conversations', 'Nonviolent Communication']
                    },
                    {
                        'title': 'Trabalho em Equipe',
                        'description': 'Colaboração e dinâmicas de grupo',
                        'order': 2,
                        'estimated_hours': 8,
                        'resources': ['The Five Dysfunctions of a Team']
                    },
                    {
                        'title': 'Resolução de Conflitos',
                        'description': 'Estratégias para lidar com conflitos no ambiente de trabalho',
                        'order': 3,
                        'estimated_hours': 6,
                        'resources': ['Getting to Yes', 'Difficult Conversations']
                    },
                    {
                        'title': 'Liderança e Influência',
                        'description': 'Desenvolvimento de habilidades de liderança',
                        'order': 4,
                        'estimated_hours': 5,
                        'resources': ['The Leadership Challenge', 'Influence: The Psychology of Persuasion']
                    }
                ]
            }
        ]
        
        for trail_data in trails_data:
            category = Category.objects.get(name=trail_data['category'])
            trail, created = Trail.objects.get_or_create(
                title=trail_data['title'],
                defaults={
                    'description': trail_data['description'],
                    'category': category,
                    'difficulty': trail_data['difficulty'],
                    'estimated_hours': trail_data['estimated_hours'],
                    'is_predefined': True
                }
            )
            
            if created:
                self.stdout.write(f'Trilha criada: {trail.title}')
                
                # Criar etapas da trilha
                for step_data in trail_data['steps']:
                    Step.objects.create(
                        trail=trail,
                        title=step_data['title'],
                        description=step_data['description'],
                        order=step_data['order'],
                        estimated_hours=step_data['estimated_hours'],
                        resources=step_data['resources']
                    )
                    self.stdout.write(f'  Etapa criada: {step_data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('Dados populados com sucesso!'))
