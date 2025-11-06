
import React, { useState, useEffect } from 'react';
import { LearningPath, User } from '../types';
import PathCard from './PathCard';
import OverallProgress from './OverallProgress';
import { ArrowRightIcon, SparklesIcon, CompassIcon } from './icons/Icons';
import { generateRecommendedPaths } from '../services/geminiService';

interface DashboardProps {
  userPaths: LearningPath[];
  onSelectPath: (path: Omit<LearningPath, 'progress'>) => void;
  currentUser: User | null;
  overallProgress: number;
  onNavigateToExplore?: () => void;
  isExploreView?: boolean;
}

const PathCardSkeleton: React.FC = () => (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden animate-pulse">
        <div className="p-6">
            <div className="h-4 bg-slate-200 rounded w-2/4 mb-2"></div>
            <div className="h-3 bg-slate-200 rounded w-1/4 mb-4"></div>
            <div className="h-6 bg-slate-300 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-slate-200 rounded w-full mt-3"></div>
            <div className="h-4 bg-slate-200 rounded w-5/6"></div>
        </div>
        <div className="bg-white px-6 py-3 h-[53px] mt-auto flex items-center justify-end">
            <div className="h-4 bg-slate-200 rounded w-1/3"></div>
        </div>
    </div>
);


const Dashboard: React.FC<DashboardProps> = ({ userPaths, onSelectPath, currentUser, overallProgress, onNavigateToExplore, isExploreView = false }) => {
  const [recommendedPaths, setRecommendedPaths] = useState<Omit<LearningPath, 'progress'>[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (currentUser) {
      const fetchRecommendations = async () => {
        setIsLoading(true);
        setError(null);
        try {
          const cachedPathsRaw = localStorage.getItem(`recommendedPaths_${currentUser.email}`);
          if (cachedPathsRaw) {
            const cachedPaths = JSON.parse(cachedPathsRaw);
            setRecommendedPaths(cachedPaths);
          } else {
            const paths = await generateRecommendedPaths(currentUser.course, currentUser.experienceLevel);
            const pathsWithIds = paths.map((p, index) => ({
              ...p,
              id: `ai-rec-${currentUser.email}-${index}`,
            }));
            setRecommendedPaths(pathsWithIds);
            localStorage.setItem(`recommendedPaths_${currentUser.email}`, JSON.stringify(pathsWithIds));
          }
        } catch (err: any) {
          console.error("AI Recommendation failed.", err);
          setError(`Não foi possível gerar recomendações personalizadas. Mostrando sugestões gerais.`);
          setRecommendedPaths([]);
        } finally {
          setIsLoading(false);
        }
      };
      fetchRecommendations();
    }
  }, [currentUser]);

  const pathsToDisplay = isExploreView
    ? Array.from(new Map([...recommendedPaths, ...userPaths].map(p => [p.id, p])).values())
    : recommendedPaths;

  return (
    <div className="space-y-8 animate-fade-in">
      {!isExploreView && currentUser && (
        <>
        <section>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Bem-vindo(a) de volta, {currentUser.name?.split(' ')[0]}!</h1>
          <p className="mt-2 text-slate-600">Continue de onde parou ou explore novas trilhas de conhecimento.</p>
          <OverallProgress progress={overallProgress} />
        </section>

        <section>
            <h2 className="text-2xl font-semibold text-red-800 mb-4">Minhas Trilhas</h2>
            {userPaths.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {userPaths.map(path => (
                <PathCard key={path.id} path={path} onSelect={() => onSelectPath(path)} />
                ))}
            </div>
            ) : (
            <div className="text-center py-10 px-6 bg-white shadow-sm rounded-lg">
                <p className="text-slate-600">Você ainda não iniciou nenhuma trilha.</p>
                <button onClick={onNavigateToExplore} className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-800 hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-100 focus:ring-red-700">
                Explorar Trilhas Agora
                </button>
            </div>
            )}
        </section>
        </>
      )}

      <section>
        <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-red-800">{isExploreView ? "Todas as Trilhas" : "Trilhas Recomendadas para Você"}</h2>
            {!isExploreView && onNavigateToExplore && (
                <button onClick={onNavigateToExplore} className="flex items-center text-sm font-medium text-red-800 hover:text-red-700">
                    Ver todas <ArrowRightIcon className="ml-1 h-4 w-4" />
                </button>
            )}
        </div>
        {error && !isExploreView && (
            <div className="mb-4 p-3 text-sm text-yellow-800 bg-yellow-100 border-l-4 border-yellow-500 rounded-r-lg" role="alert">
                <p>{error}</p>
            </div>
        )}
        
        {isLoading ? (
            <>
                {!isExploreView && (
                    <div className="text-center p-4 bg-white rounded-lg shadow-sm mb-6">
                        <div className="flex items-center justify-center">
                            <SparklesIcon className="h-6 w-6 text-red-800 animate-pulse mr-3" />
                            <p className="text-slate-600 font-medium">Gerando recomendações personalizadas para você com a IA...</p>
                        </div>
                    </div>
                )}
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                    {[...Array(3)].map((_, i) => <PathCardSkeleton key={i} />)}
                </div>
            </>
        ) : pathsToDisplay.length > 0 ? (
             <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {pathsToDisplay.map(path => {
                    const userPath = userPaths.find(p => p.id === path.id);
                    return (
                        <PathCard key={path.id} path={{ ...path, progress: userPath?.progress ?? 0 }} onSelect={() => onSelectPath(path)} isPredefined={!userPath} />
                    );
                })}
            </div>
        ) : (
            <div className="text-center py-10 px-6 bg-white shadow-sm rounded-lg">
                {isExploreView ? (
                     <>
                        <CompassIcon className="mx-auto h-10 w-10 text-slate-400" />
                        <p className="mt-4 text-slate-600">Nenhuma trilha encontrada.</p>
                        <p className="mt-1 text-sm text-slate-500">Use a seção "Criar com IA" para gerar suas próprias trilhas de estudo.</p>
                     </>
                ) : (
                     <>
                        <SparklesIcon className="mx-auto h-10 w-10 text-red-800" />
                        <p className="mt-4 text-slate-600">Não foi possível gerar recomendações personalizadas no momento.</p>
                        {onNavigateToExplore && (
                            <button onClick={onNavigateToExplore} className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-800 hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-100 focus:ring-red-700">
                                Ver minhas trilhas criadas
                            </button>
                        )}
                    </>
                )}
           </div>
        )}
      </section>
    </div>
  );
};

export default Dashboard;
