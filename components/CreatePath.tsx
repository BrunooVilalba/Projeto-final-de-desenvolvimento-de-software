import React, { useState } from 'react';
import { generateLearningPath } from '../services/geminiService';
import { LearningPath } from '../types';
import { SparklesIcon, LoaderIcon } from './icons/Icons';

interface CreatePathProps {
  onPathGenerated: (path: Omit<LearningPath, 'id' | 'progress'>) => void;
}

const CreatePath: React.FC<CreatePathProps> = ({ onPathGenerated }) => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) {
      setError('Por favor, descreva o que você quer aprender.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const generatedPath = await generateLearningPath(prompt);
      onPathGenerated(generatedPath);
    } catch (err: any) {
      setError(err.message || 'Ocorreu um erro desconhecido.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
        <div className="text-center">
            <SparklesIcon className="mx-auto h-12 w-12 text-red-800" />
            <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">Crie sua Trilha de Aprendizagem com IA</h1>
            <p className="mt-4 text-lg text-slate-600">
                Descreva o que você deseja aprender, e nossa IA criará um plano de estudos personalizado para você. Seja específico para melhores resultados!
            </p>
        </div>
      
        <form onSubmit={handleSubmit} className="mt-10">
            <div className="relative">
                <textarea
                    rows={4}
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Seja específico! Ex: 'Quero me tornar um desenvolvedor backend com Node.js, incluindo APIs REST, bancos de dados SQL e NoSQL, e implantação com Docker.'"
                    disabled={isLoading}
                    className="w-full p-4 pr-10 bg-white border-2 border-slate-300 rounded-lg text-slate-900 placeholder-slate-400 focus:ring-2 focus:ring-red-800 focus:border-red-800 transition disabled:opacity-50"
                />
            </div>

            {error && <p className="mt-3 text-sm text-red-500">{error}</p>}
            
            <div className="mt-6">
                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-red-800 hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-100 focus:ring-red-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors"
                >
                    {isLoading ? (
                        <>
                            <LoaderIcon className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
                            Gerando sua trilha...
                        </>
                    ) : (
                       <>
                         <SparklesIcon className="-ml-1 mr-2 h-5 w-5" />
                         Gerar Trilha Personalizada
                       </>
                    )}
                </button>
            </div>
        </form>
        <div className="mt-8 text-center text-xs text-slate-500">
            <p>A IA pode cometer erros. Considere verificar informações importantes.</p>
        </div>
    </div>
  );
};

export default CreatePath;