/**
 * Componente Dashboard - Painel principal com trilhas do usuário
 * 
 * Este componente exibe o dashboard principal da aplicação, mostrando:
 * - Progresso geral do usuário
 * - Lista de trilhas criadas pelo usuário
 * - Trilhas recomendadas baseadas no perfil (geradas pela IA)
 * - Opção de explorar trilhas recomendadas
 * 
 * Funcionalidades:
 * - Carrega trilhas do usuário da API
 * - Gera recomendações personalizadas usando IA (apenas uma vez por usuário)
 * - Salva trilhas recomendadas permanentemente no banco de dados
 * - Estados de loading e erro
 * - Visualização de trilhas em cards
 * 
 * Autor: Desenvolvedor do EstudaAI
 */

import React, { useState, useEffect, useRef } from 'react';
import { LearningPath, User } from '../types';
import PathCard from './PathCard';
import OverallProgress from './OverallProgress';
import { ArrowRightIcon, SparklesIcon, CompassIcon } from './icons/Icons';
import { generateRecommendedPaths } from '../services/geminiService';

/**
 * Props do componente Dashboard.
 */
interface DashboardProps {
  /** Lista de trilhas do usuário */
  userPaths: LearningPath[];
  /** Callback quando uma trilha é selecionada para visualização */
  onSelectPath: (path: Omit<LearningPath, 'progress'>) => void;
  /** Dados do usuário autenticado */
  currentUser: User | null;
  /** Progresso geral do usuário (média de todas as trilhas) */
  overallProgress: number;
  /** Callback para navegar para a view de exploração (opcional) */
  onNavigateToExplore?: () => void;
  /** Indica se está na view de exploração (mostra recomendações) */
  isExploreView?: boolean;
  /** Callback para salvar trilhas recomendadas no banco de dados */
  onSaveRecommendedPaths?: (paths: Omit<LearningPath, 'id' | 'progress'>[]) => Promise<void>;
}

/**
 * Componente de skeleton (loading) para cards de trilhas.
 * 
 * Exibido enquanto as trilhas estão sendo carregadas, proporcionando
 * uma melhor experiência visual (evita layout shift).
 * 
 * @returns JSX.Element - Card de skeleton
 */
const PathCardSkeleton: React.FC = () => (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden animate-pulse">
        <div className="p-6">
            {/* Skeleton do título */}
            <div className="h-4 bg-slate-200 rounded w-2/4 mb-2"></div>
            {/* Skeleton da categoria */}
            <div className="h-3 bg-slate-200 rounded w-1/4 mb-4"></div>
            {/* Skeleton da descrição */}
            <div className="h-6 bg-slate-300 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-slate-200 rounded w-full mt-3"></div>
            <div className="h-4 bg-slate-200 rounded w-5/6"></div>
        </div>
        {/* Skeleton do footer */}
        <div className="bg-white px-6 py-3 h-[53px] mt-auto flex items-center justify-end">
            <div className="h-4 bg-slate-200 rounded w-1/3"></div>
        </div>
    </div>
);

/**
 * Componente Dashboard principal.
 * 
 * Gerencia a exibição de trilhas do usuário e recomendações personalizadas.
 * As trilhas recomendadas são geradas apenas UMA VEZ por usuário e salvas
 * permanentemente no banco de dados.
 * 
 * @param props - Props do componente Dashboard
 * @returns JSX.Element - Dashboard com trilhas e recomendações
 */
const Dashboard: React.FC<DashboardProps> = ({ 
  userPaths, 
  onSelectPath, 
  currentUser, 
  overallProgress, 
  onNavigateToExplore, 
  isExploreView = false,
  onSaveRecommendedPaths
}) => {
  // Estado das trilhas recomendadas (geradas pela IA)
  const [recommendedPaths, setRecommendedPaths] = useState<Omit<LearningPath, 'progress'>[]>([]);
  
  // Estado de loading das recomendações
  const [isLoading, setIsLoading] = useState(false);
  
  // Estado de erro ao carregar recomendações
  const [error, setError] = useState<string | null>(null);
  
  // Ref para rastrear se já tentamos gerar recomendações (evita loops infinitos)
  const hasTriedGenerating = useRef(false);

  /**
   * Effect para carregar trilhas recomendadas do banco de dados.
   * 
   * Carrega trilhas recomendadas que já foram salvas no banco de dados.
   * Se não existirem trilhas recomendadas para o usuário, gera novas
   * usando a IA e salva permanentemente no banco.
   * 
   * IMPORTANTE: As trilhas recomendadas são geradas APENAS UMA VEZ por usuário.
   * Uma vez salvas no banco, serão sempre carregadas do banco, nunca regeneradas.
   */
  useEffect(() => {
    if (currentUser) {
      // Busca trilhas recomendadas do banco de dados (is_recommended = true)
      const recommendedFromDB = userPaths.filter(path => 
        (path as any).is_recommended === true
      );
      
      if (recommendedFromDB.length > 0) {
        // Se já existem trilhas recomendadas no banco, usa elas
        setRecommendedPaths(recommendedFromDB.map(path => ({
          id: path.id,
          title: path.title,
          description: path.description,
          category: path.category,
          difficulty: path.difficulty,
          steps: path.steps,
        })));
        setIsLoading(false);
        hasTriedGenerating.current = false; // Reset para permitir nova tentativa se necessário
      } else if (onSaveRecommendedPaths && !hasTriedGenerating.current) {
        // Se não existem trilhas recomendadas e ainda não tentamos gerar, gera novas
        hasTriedGenerating.current = true; // Marca que tentamos gerar
        
        const fetchRecommendations = async () => {
          setIsLoading(true);
          setError(null);
          
          try {
            // Gera novas trilhas usando IA e salva permanentemente no banco de dados
            const paths = await generateRecommendedPaths(
              currentUser.course || 'Desenvolvimento', 
              currentUser.experienceLevel || 'Iniciante'
            );
            
            // Adiciona flag is_recommended = true para cada trilha
            const pathsWithFlag = paths.map((p) => ({
              ...p,
              is_recommended: true,
            }));
            
            // Salva as trilhas recomendadas permanentemente no banco de dados
            // Esta função também atualiza userPaths no App.tsx
            await onSaveRecommendedPaths(pathsWithFlag);
            
            // Atualiza o estado local (será atualizado quando userPaths mudar)
            setRecommendedPaths(pathsWithFlag);
          } catch (err: any) {
            // Em caso de erro (API indisponível, etc.), mostra mensagem
            console.error("AI Recommendation failed.", err);
            setError(`Não foi possível gerar recomendações personalizadas. Tente novamente mais tarde.`);
            setRecommendedPaths([]);
            hasTriedGenerating.current = false; // Permite tentar novamente em caso de erro
          } finally {
            setIsLoading(false);
          }
        };
        
        // Executa a geração de recomendações apenas uma vez
        fetchRecommendations();
      }
    }
  }, [currentUser, userPaths.length, onSaveRecommendedPaths]); // Re-executa apenas quando o número de trilhas muda

  /**
   * Decide quais trilhas devem ser exibidas.
   * 
   * Se estiver na view de exploração, mostra recomendações.
   * Se estiver no dashboard normal, mostra as trilhas recomendadas.
   * Remove duplicatas caso uma trilha recomendada já tenha sido adicionada.
   */
  const pathsToDisplay = isExploreView
    ? Array.from(new Map([...recommendedPaths, ...userPaths].map(p => [p.id, p])).values())
    : recommendedPaths;

  return (
    <div className="animate-fade-in">
      {/* Seção de progresso geral (apenas no dashboard principal) */}
      {!isExploreView && (
        <div className="mb-8">
          <OverallProgress progress={overallProgress} />
        </div>
      )}

      {/* Cabeçalho da seção */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          {isExploreView ? (
            <>
              <CompassIcon className="h-6 w-6 text-red-800 mr-2" />
              <h2 className="text-2xl font-bold text-slate-900">Explorar Trilhas</h2>
            </>
          ) : (
            <>
              <SparklesIcon className="h-6 w-6 text-red-800 mr-2" />
              <h2 className="text-2xl font-bold text-slate-900">Trilhas Recomendadas para Você</h2>
            </>
          )}
        </div>
        
        {/* Botão para explorar (apenas no dashboard principal) */}
        {!isExploreView && onNavigateToExplore && (
          <button
            onClick={onNavigateToExplore}
            className="flex items-center text-red-800 hover:text-red-900 font-medium transition-colors"
          >
            Explorar todas
            <ArrowRightIcon className="ml-1 h-5 w-5" />
          </button>
        )}
      </div>

      {/* Mensagem de erro (se houver) */}
      {error && (
        <div className="mb-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-r-lg">
          <p className="text-sm text-yellow-800">{error}</p>
        </div>
      )}

      {/* Grid de trilhas */}
      {isLoading ? (
        // Skeleton loading enquanto carrega
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <PathCardSkeleton key={i} />
          ))}
        </div>
      ) : pathsToDisplay.length > 0 ? (
        // Lista de trilhas
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {pathsToDisplay.map((path) => (
            <PathCard
              key={path.id}
              path={path}
              onClick={() => onSelectPath(path)}
            />
          ))}
        </div>
      ) : (
        // Mensagem quando não há trilhas
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <p className="text-slate-600">
            {isExploreView 
              ? 'Nenhuma trilha recomendada disponível no momento.'
              : 'Ainda não há trilhas recomendadas. Complete seu perfil para receber recomendações personalizadas!'}
          </p>
        </div>
      )}
      
      {/* Seção de trilhas do usuário (apenas no dashboard principal) */}
      {!isExploreView && userPaths.filter(p => !(p as any).is_recommended).length > 0 && (
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-slate-900 mb-6">Minhas Trilhas</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {userPaths
              .filter(p => !(p as any).is_recommended) // Mostra apenas trilhas personalizadas
              .map((path) => (
                <PathCard
                  key={path.id}
                  path={path}
                  onClick={() => onSelectPath(path)}
                />
              ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
