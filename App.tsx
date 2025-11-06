
import React, { useState, useEffect, useCallback } from 'react';
import { LearningPath, User } from './types';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import PathDetail from './components/PathDetail';
import CreatePath from './components/CreatePath';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import AuthModal from './components/AuthModal';

type View = 'dashboard' | 'path-detail' | 'create-path' | 'explore-paths';

const App: React.FC = () => {
  const [userPaths, setUserPaths] = useState<LearningPath[]>([]);
  const [currentView, setCurrentView] = useState<View>('dashboard');
  const [selectedPath, setSelectedPath] = useState<LearningPath | null>(null);
  const [isSidebarOpen, setSidebarOpen] = useState(false);
  
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [authModal, setAuthModal] = useState<'hidden' | 'login' | 'register'>('hidden');

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          const { authAPI } = await import('./services/api');
          const userData = await authAPI.getProfile();
          const user: User = {
            name: userData.first_name || userData.username,
            email: userData.email,
            course: userData.course,
            experienceLevel: userData.experience_level,
          };
          setCurrentUser(user);
          setIsAuthenticated(true);
        } catch (error) {
          console.error("Failed to load user from API", error);
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      }
    };
    checkAuth();
  }, []);

  useEffect(() => {
    const loadPaths = async () => {
      if (currentUser && localStorage.getItem('accessToken')) {
        try {
          const { learningPathsAPI } = await import('./services/api');
          const paths = await learningPathsAPI.getAll();
          // Converter formato da API para formato do frontend
          const formattedPaths: LearningPath[] = paths.map((path: any) => ({
            id: String(path.id),
            title: path.title,
            description: path.description,
            category: path.category,
            difficulty: path.difficulty,
            progress: path.progress,
            steps: path.steps.map((step: any) => ({
              title: step.title,
              description: step.description,
              rationale: step.rationale,
              completed: step.completed,
              subSteps: step.subSteps || [],
            })),
          }));
          setUserPaths(formattedPaths);
        } catch (error) {
          console.error("Failed to load paths from API", error);
          setUserPaths([]);
        }
      }
    };
    loadPaths();
  }, [currentUser]);
  
  const handleLoginSuccess = (user: User) => {
    setCurrentUser(user);
    setIsAuthenticated(true);
    setAuthModal('hidden');
  };

  const handleLogout = async () => {
    const { authAPI } = await import('./services/api');
    authAPI.logout();
    setIsAuthenticated(false);
    setCurrentUser(null);
    setUserPaths([]);
    setSelectedPath(null);
    setCurrentView('dashboard');
  };

  const handleSelectPath = (path: LearningPath) => {
    const existingPath = userPaths.find(p => p.id === path.id);
    if(existingPath) {
        setSelectedPath(existingPath);
    } else {
        setSelectedPath(path);
    }
    setCurrentView('path-detail');
    setSidebarOpen(false);
  };
  
  const handleAddGeneratedPath = async (path: Omit<LearningPath, 'id' | 'progress'>) => {
    try {
      const { learningPathsAPI } = await import('./services/api');
      const createdPath = await learningPathsAPI.create({
        title: path.title,
        description: path.description,
        category: path.category,
        difficulty: path.difficulty,
        steps_data: path.steps.map(step => ({
          title: step.title,
          description: step.description,
          rationale: step.rationale,
          subSteps: step.subSteps || [],
        })),
      });
      
      const newPath: LearningPath = {
        id: String(createdPath.id),
        title: createdPath.title,
        description: createdPath.description,
        category: createdPath.category,
        difficulty: createdPath.difficulty,
        progress: createdPath.progress,
        steps: createdPath.steps.map((step: any) => ({
          title: step.title,
          description: step.description,
          rationale: step.rationale,
          completed: step.completed,
          subSteps: step.subSteps || [],
        })),
      };
      
      setUserPaths([...userPaths, newPath]);
      setSelectedPath(newPath);
      setCurrentView('path-detail');
    } catch (error) {
      console.error("Failed to create path", error);
    }
  };

  const handleToggleStep = async (pathId: string, stepIndex: number) => {
    try {
      const { learningPathsAPI } = await import('./services/api');
      const updatedPath = await learningPathsAPI.toggleStep(pathId, stepIndex);
      
      const formattedPath: LearningPath = {
        id: String(updatedPath.id),
        title: updatedPath.title,
        description: updatedPath.description,
        category: updatedPath.category,
        difficulty: updatedPath.difficulty,
        progress: updatedPath.progress,
        steps: updatedPath.steps.map((step: any) => ({
          title: step.title,
          description: step.description,
          rationale: step.rationale,
          completed: step.completed,
          subSteps: step.subSteps || [],
        })),
      };
      
      const updatedPaths = userPaths.map(p => p.id === pathId ? formattedPath : p);
      setUserPaths(updatedPaths);
      
      if(selectedPath && selectedPath.id === pathId) {
        setSelectedPath(formattedPath);
      }
    } catch (error) {
      console.error("Failed to toggle step", error);
    }
  };

  const handleDeletePath = async (pathId: string) => {
    try {
      const { learningPathsAPI } = await import('./services/api');
      await learningPathsAPI.delete(pathId);
      const updatedPaths = userPaths.filter(p => p.id !== pathId);
      setUserPaths(updatedPaths);
      if (selectedPath?.id === pathId) {
        setSelectedPath(null);
        setCurrentView('dashboard');
      }
    } catch (error) {
      console.error("Failed to delete path", error);
    }
  }
  
  const totalProgress = userPaths.reduce((sum, path) => sum + path.progress, 0);
  const overallProgress = userPaths.length > 0 ? Math.round(totalProgress / userPaths.length) : 0;

  const renderContent = () => {
    switch (currentView) {
      case 'path-detail':
        return selectedPath ? (
          <PathDetail
            path={selectedPath}
            onToggleStep={handleToggleStep}
            onBack={() => setCurrentView('dashboard')}
            onDelete={handleDeletePath}
          />
        ) : null;
      case 'create-path':
        return <CreatePath onPathGenerated={handleAddGeneratedPath} />;
      case 'explore-paths':
          return <Dashboard
            userPaths={userPaths}
            currentUser={currentUser}
            onSelectPath={handleSelectPath}
            overallProgress={overallProgress}
            isExploreView={true}
            />;
      case 'dashboard':
      default:
        return <Dashboard 
          userPaths={userPaths} 
          currentUser={currentUser}
          onSelectPath={handleSelectPath}
          onNavigateToExplore={() => setCurrentView('explore-paths')}
          overallProgress={overallProgress}
        />;
    }
  };

  if (!isAuthenticated) {
    return (
      <>
        <LandingPage 
          onLogin={() => setAuthModal('login')} 
          onRegister={() => setAuthModal('register')} 
        />
        {authModal !== 'hidden' && (
          <AuthModal
            initialView={authModal}
            onClose={() => setAuthModal('hidden')}
            onLoginSuccess={handleLoginSuccess}
          />
        )}
      </>
    );
  }

  return (
    <div className="flex h-screen bg-slate-100 text-slate-800 font-sans">
      <Sidebar 
        currentView={currentView} 
        setCurrentView={setCurrentView}
        isOpen={isSidebarOpen}
        setIsOpen={setSidebarOpen}
      />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header 
          onMenuClick={() => setSidebarOpen(!isSidebarOpen)}
          currentUser={currentUser}
          onLogout={handleLogout}
        />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-slate-100 p-4 sm:p-6 lg:p-8">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default App;
