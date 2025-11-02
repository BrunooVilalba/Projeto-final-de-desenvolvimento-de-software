from openai import OpenAI
import json
import os
from django.conf import settings
from .models import Trail, Step, Category


class LLMService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_custom_trail(self, user_description, user):
        """
        Gera uma trilha personalizada baseada na descrição do usuário
        """
        if not self.client:
            return self._fallback_trail_response()
        
        try:
            prompt = f"""
            Você é um especialista em educação e desenvolvimento de trilhas de aprendizado.
            
            Com base na seguinte descrição do usuário, crie uma trilha de estudos personalizada:
            
            Descrição: {user_description}
            
            Retorne um JSON com a seguinte estrutura:
            {{
                "title": "Título da trilha",
                "description": "Descrição detalhada da trilha",
                "difficulty": "beginner|intermediate|advanced",
                "estimated_hours": número_total_de_horas,
                "steps": [
                    {{
                        "title": "Título da etapa",
                        "description": "Descrição detalhada da etapa",
                        "order": 1,
                        "estimated_hours": número_de_horas,
                        "is_optional": false,
                        "resources": ["recurso1", "recurso2"]
                    }}
                ]
            }}
            
            A trilha deve ter entre 5 e 10 etapas, ser prática e progressiva.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um especialista em educação e desenvolvimento de trilhas de aprendizado."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            # Extrair JSON da resposta
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            trail_data = json.loads(json_str)
            return self._create_trail_from_data(trail_data, user)
            
        except Exception as e:
            print(f"Erro ao gerar trilha personalizada: {e}")
            return self._fallback_trail_response()
    
    def answer_question(self, question, user):
        """
        Responde perguntas do usuário sobre trilhas de estudo
        """
        if not self.client:
            return self._fallback_answer(question)
        
        try:
            # Buscar trilhas do usuário para contexto
            user_trails = Trail.objects.filter(created_by=user)
            context = ""
            if user_trails.exists():
                context = f"Trilhas do usuário: {', '.join([t.title for t in user_trails])}"
            
            prompt = f"""
            Você é um assistente educacional especializado em trilhas de aprendizado.
            
            Contexto: {context}
            
            Pergunta do usuário: {question}
            
            Responda de forma clara, útil e encorajadora. Se a pergunta for sobre uma trilha específica,
            forneça orientações práticas e recursos úteis.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente educacional especializado em trilhas de aprendizado."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Erro ao responder pergunta: {e}")
            return self._fallback_answer(question)
    
    def _fallback_answer(self, question):
        """
        Resposta de fallback quando a API não está disponível
        """
        question_lower = question.lower()
        
        if 'python' in question_lower:
            return """🐍 **Para começar a aprender Python:**

1. **Instale o Python** no seu computador
2. **Escolha um editor** como VS Code ou PyCharm
3. **Pratique diariamente** com exercícios simples
4. **Faça projetos** para aplicar o conhecimento
5. **Participe de comunidades** online

💡 **Dica:** Comece com conceitos básicos como variáveis, loops e funções. A prática constante é a chave do sucesso!"""
        
        elif 'react' in question_lower or 'frontend' in question_lower:
            return """⚛️ **Para aprender React e Frontend:**

1. **Domine HTML/CSS** primeiro
2. **Aprenda JavaScript** essencial
3. **Entenda conceitos** de componentes
4. **Pratique com projetos** reais
5. **Use ferramentas** como Create React App

💡 **Dica:** Comece com projetos pequenos e vá aumentando a complexidade gradualmente!"""
        
        elif 'dados' in question_lower or 'data' in question_lower:
            return """📊 **Para aprender Ciência de Dados:**

1. **Python** é fundamental
2. **Aprenda Pandas** para manipulação
3. **Estude estatística** básica
4. **Pratique visualização** com Matplotlib
5. **Faça projetos** com datasets reais

💡 **Dica:** Comece com datasets simples e explore diferentes tipos de análise!"""
        
        elif 'segurança' in question_lower or 'cyber' in question_lower:
            return """🔒 **Para aprender Segurança da Informação:**

1. **Conceitos básicos** de segurança
2. **Criptografia** fundamental
3. **Redes** e protocolos
4. **Práticas** de proteção
5. **Ferramentas** de segurança

💡 **Dica:** A segurança é uma área em constante evolução, mantenha-se sempre atualizado!"""
        
        else:
            return """🎓 **Dicas gerais para aprender:**

1. **Defina objetivos** claros
2. **Crie um cronograma** de estudos
3. **Pratique regularmente**
4. **Faça projetos** práticos
5. **Busque ajuda** quando necessário

💡 **Dica:** O aprendizado é uma jornada, não uma corrida. Seja consistente e paciente consigo mesmo!"""
    
    def _create_trail_from_data(self, trail_data, user):
        """
        Cria uma trilha no banco de dados a partir dos dados gerados pela LLM
        """
        try:
            # Criar categoria personalizada se não existir
            category, created = Category.objects.get_or_create(
                name="Personalizada",
                defaults={
                    'description': 'Trilhas personalizadas criadas por IA',
                    'icon': 'fas fa-magic'
                }
            )
            
            # Criar trilha
            trail = Trail.objects.create(
                title=trail_data['title'],
                description=trail_data['description'],
                category=category,
                difficulty=trail_data['difficulty'],
                estimated_hours=trail_data['estimated_hours'],
                is_predefined=False,
                created_by=user
            )
            
            # Criar etapas
            for step_data in trail_data['steps']:
                Step.objects.create(
                    trail=trail,
                    title=step_data['title'],
                    description=step_data['description'],
                    order=step_data['order'],
                    estimated_hours=step_data['estimated_hours'],
                    is_optional=step_data.get('is_optional', False),
                    resources=step_data.get('resources', [])
                )
            
            return trail
            
        except Exception as e:
            print(f"Erro ao criar trilha no banco: {e}")
            return None
    
    def _fallback_trail_response(self):
        """
        Resposta de fallback quando a API não está disponível
        """
        return {
            'error': 'Serviço de IA temporariamente indisponível. Tente novamente mais tarde.'
        }
