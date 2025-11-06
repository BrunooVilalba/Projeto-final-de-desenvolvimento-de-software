
import { GoogleGenAI, Type } from "@google/genai";
import { LearningPath, Step, User, SubStep } from '../types';

const API_KEY = "AIzaSyBz534EGdxp8XF3LrPft_6p6LiuX8jk2-c";

let ai: GoogleGenAI | null = null;

function getAI() {
    if (!API_KEY) {
        throw new Error("API_KEY environment variable not set");
    }
    if (!ai) {
        ai = new GoogleGenAI({ apiKey: API_KEY });
    }
    return ai;
}

// Schema for a single learning path object, extracted for reusability.
const learningPathObjectSchema = {
    type: Type.OBJECT,
    properties: {
        title: {
            type: Type.STRING,
            description: "Um título conciso e informativo para a trilha de aprendizagem. Ex: 'Fundamentos de JavaScript para Web'."
        },
        description: {
            type: Type.STRING,
            description: "Uma breve descrição (1-2 frases) sobre o que o aluno aprenderá nesta trilha."
        },
        category: {
            type: Type.STRING,
            description: "A categoria principal do conhecimento. Ex: 'Desenvolvimento Frontend', 'Ciência de Dados', 'Design'."
        },
        difficulty: {
            type: Type.STRING,
            description: "O nível de dificuldade da trilha. Valores possíveis: 'Iniciante', 'Intermediário', 'Avançado'."
        },
        steps: {
            type: Type.ARRAY,
            description: "Uma lista de 5 a 7 etapas sequenciais que compõem a trilha de aprendizagem.",
            items: {
                type: Type.OBJECT,
                properties: {
                    title: {
                        type: Type.STRING,
                        description: "O título de uma etapa específica. Ex: 'Variáveis e Tipos de Dados'."
                    },
                    description: {
                        type: Type.STRING,
                        description: "Uma descrição detalhada (1-2 frases) do que será aprendido ou feito nesta etapa."
                    },
                    rationale: {
                        type: Type.STRING,
                        description: "Uma breve explicação (1 frase) sobre o porquê desta etapa ser importante e o que ela conecta."
                    },
                    subSteps: {
                        type: Type.ARRAY,
                        description: "Uma lista de 4 a 6 subtópicos ou conceitos específicos a serem aprendidos dentro desta etapa. Cada item deve conter o tópico e um link de sugestão.",
                        items: {
                            type: Type.OBJECT,
                            properties: {
                                topic: {
                                    type: Type.STRING,
                                    description: "O tópico ou conceito específico a ser aprendido."
                                },
                                link: {
                                    type: Type.STRING,
                                    description: "Um link de sugestão (URL) para um recurso externo de alta qualidade (artigo, documentação, tutorial em vídeo) sobre este tópico."
                                }
                            },
                            required: ["topic", "link"]
                        }
                    }
                },
                required: ["title", "description", "rationale", "subSteps"],
            },
        },
    },
    required: ["title", "description", "category", "difficulty", "steps"],
};

// Schema for the 'generateLearningPath' function, now using the reusable object schema.
const responseSchema = learningPathObjectSchema;

// Schema for the new 'generateRecommendedPaths' function.
const recommendedPathsSchema = {
    type: Type.OBJECT,
    properties: {
        paths: {
            type: Type.ARRAY,
            description: "Uma lista de 3 trilhas de aprendizagem recomendadas.",
            items: learningPathObjectSchema
        }
    },
    required: ["paths"]
};

export const generateLearningPath = async (
  prompt: string
): Promise<Omit<LearningPath, 'id' | 'progress'>> => {
  try {
    const fullPrompt = `
      Você é um especialista em design instrucional e um engenheiro de software sênior. Sua tarefa é criar uma trilha de aprendizagem EXTREMAMENTE COMPLETA E ROBUSTA com base na solicitação de um estudante.
      A trilha deve ser estruturada logicamente, desde os conceitos mais básicos até tópicos avançados. A profundidade do conteúdo deve refletir a dificuldade definida: uma trilha 'Avançada' deve ser desafiadora, enquanto 'Iniciante' deve ser detalhada nos fundamentos.
      A resposta DEVE estar em formato JSON, seguindo estritamente o schema fornecido.

      - **Título:** Crie um título claro e impactante.
      - **Descrição:** Escreva uma sinopse que motive o estudante.
      - **Categoria:** Atribua a categoria mais relevante.
      - **Dificuldade:** Avalie e defina a dificuldade geral da trilha ('Iniciante', 'Intermediário', 'Avançado').
      - **Etapas (Steps):** Crie de 8 a 10 etapas principais. Para cada etapa:
        - **Título e Descrição:** Devem ser claros e objetivos.
        - **Rationale:** Explique em uma frase por que esta etapa é crucial.
        - **Sub-etapas (subSteps):** Liste de 4 a 6 subtópicos detalhados. Para cada subtópico, forneça o **tópico** em si e um **link (URL)** para um recurso de alta qualidade (artigo, documentação, tutorial) que aprofunde o assunto.

      Solicitação do Aluno: "${prompt}"
    `;

    const response = await getAI().models.generateContent({
      model: "gemini-2.5-flash",
      contents: fullPrompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: responseSchema,
        temperature: 0.7,
      },
    });

    const jsonText = response.text.trim();
    // FIX: Added parentheses around the step type definition to ensure the `steps` property is correctly typed as an array of objects.
    const generatedPath = JSON.parse(jsonText) as Omit<LearningPath, 'id' | 'progress' | 'steps'> & { steps: (Omit<Step, 'completed' | 'subSteps'> & { subSteps: SubStep[] })[] };

    const pathWithCompletion = {
      ...generatedPath,
      steps: generatedPath.steps.map(step => ({ ...step, completed: false })),
    };
    
    return pathWithCompletion;
  } catch (error) {
    console.error("Error generating learning path:", error);
    throw new Error("Não foi possível gerar a trilha de aprendizagem. Por favor, tente novamente.");
  }
};

export const generateRecommendedPaths = async (
  course: string,
  experienceLevel: User['experienceLevel']
): Promise<Omit<LearningPath, 'id' | 'progress'>[]> => {
  try {
    const fullPrompt = `
      Você é um especialista em design instrucional e um mentor de carreira sênior. Sua tarefa é criar 3 trilhas de aprendizagem FUNDAMENTAIS, DIVERSIFICADAS e COMPLETAS para um estudante com o seguinte perfil:
      - Área de Formação: "${course}"
      - Nível de Experiência: "${experienceLevel}"

      IMPORTANTE: As trilhas devem ser estritamente focadas em sub-áreas DENTRO do campo de "${course}". O conteúdo deve ser profundo e relevante para o nível de dificuldade atribuído.
      
      Para cada uma das 3 trilhas, forneça uma estrutura completa:
      - Título, descrição, categoria (deve ser "${course}") e dificuldade ('Iniciante', 'Intermediário', 'Avançado').
      - Uma lista de 5 a 7 etapas principais.
      - Para cada etapa: título, descrição, a rationale (por que é importante), e 4-6 sub-etapas detalhadas.
      - Para cada sub-etapa, forneça o **tópico** e um **link (URL)** para um recurso externo de alta qualidade sobre o assunto.

      A resposta DEVE ser um objeto JSON com uma chave "paths", contendo um array de 3 objetos de trilha, seguindo estritamente o schema fornecido.
    `;

    const response = await getAI().models.generateContent({
      model: "gemini-2.5-flash",
      contents: fullPrompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: recommendedPathsSchema,
        temperature: 0.8,
      },
    });

    const jsonText = response.text.trim();
    // FIX: Added parentheses around the step type definition to ensure the `steps` property is correctly typed as an array of objects within each path.
    const result = JSON.parse(jsonText) as { paths: (Omit<LearningPath, 'id' | 'progress' | 'steps'> & { steps: (Omit<Step, 'completed' | 'subSteps'> & { subSteps: SubStep[] })[] })[] };


    if (!result.paths || !Array.isArray(result.paths)) {
        throw new Error("A resposta da IA não continha um array de trilhas válido.");
    }
    
    const pathsWithCompletion = result.paths.map(path => ({
        ...path,
        steps: path.steps.map(step => ({ ...step, completed: false })),
    }));

    return pathsWithCompletion;
  } catch (error) {
    console.error("Error generating recommended paths:", error);
    throw new Error("Não foi possível gerar as recomendações. Por favor, recarregue a página para tentar novamente.");
  }
};
