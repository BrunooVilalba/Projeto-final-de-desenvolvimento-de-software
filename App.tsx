
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
    try {
      const savedUser = localStorage.getItem('currentUser');
      if (savedUser) {
        const user = JSON.parse(savedUser);
        setCurrentUser(user);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error("Failed to load user from localStorage", error);
    }
  }, []);

  useEffect(() => {
    if (currentUser) {
      try {
        const savedPaths = localStorage.getItem(`userLearningPaths_${currentUser.email}`);
        if (savedPaths) {
          setUserPaths(JSON.parse(savedPaths));
        } else {
          setUserPaths([]);
        }
      } catch (error) {
        console.error("Failed to load paths from localStorage", error);
      }
    }
  }, [currentUser]);

  const savePaths = useCallback((paths: LearningPath[]) => {
    if (currentUser) {
      try {
        localStorage.setItem(`userLearningPaths_${currentUser.email}`, JSON.stringify(paths));
      } catch (error) {
        console.error("Failed to save paths to localStorage", error);
      }
    }
  }, [currentUser]);
  
  const handleLoginSuccess = (user: User) => {
    setCurrentUser(user);
    setIsAuthenticated(true);
    localStorage.setItem('currentUser', JSON.stringify(user));
    setAuthModal('hidden');
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentUser(null);
    setUserPaths([]);
    setSelectedPath(null);
    setCurrentView('dashboard');
    localStorage.removeItem('currentUser');
  };

  const handleSelectPath = (path: LearningPath) => {
    const existingPath = userPaths.find(p => p.id === path.id);
    if(existingPath) {
        setSelectedPath(existingPath);
    } else {
        const newPathWithId = { ...path, id: path.id || `user-${Date.now()}`, progress: 0 };
        const updatedPaths = [...userPaths, newPathWithId];
        setUserPaths(updatedPaths);
        savePaths(updatedPaths);
        setSelectedPath(newPathWithId);
    }
    setCurrentView('path-detail');
    setSidebarOpen(false);
  };
  
  const handleAddGeneratedPath = (path: Omit<LearningPath, 'id' | 'progress'>) => {
    const newPath: LearningPath = {
      ...path,
      id: `ai-${Date.now()}`,
      progress: 0,
      steps: path.steps.map(step => ({ ...step, completed: false }))
    };
    const updatedPaths = [...userPaths, newPath];
    setUserPaths(updatedPaths);
    savePaths(updatedPaths);
    setSelectedPath(newPath);
    setCurrentView('path-detail');
  };

  const handleToggleStep = (pathId: string, stepIndex: number) => {
    const updatedPaths = userPaths.map(path => {
      if (path.id === pathId) {
        const newSteps = [...path.steps];
        newSteps[stepIndex].completed = !newSteps[stepIndex].completed;
        const completedCount = newSteps.filter(s => s.completed).length;
        const progress = Math.round((completedCount / newSteps.length) * 100);
        return { ...path, steps: newSteps, progress };
      }
      return path;
    });
    setUserPaths(updatedPaths);
    savePaths(updatedPaths);
    if(selectedPath && selectedPath.id === pathId) {
        const updatedSelectedPath = updatedPaths.find(p => p.id === pathId);
        if(updatedSelectedPath) setSelectedPath(updatedSelectedPath);
    }
  };

  const handleDeletePath = (pathId: string) => {
    const updatedPaths = userPaths.filter(p => p.id !== pathId);
    setUserPaths(updatedPaths);
    savePaths(updatedPaths);
    if (selectedPath?.id === pathId) {
        setSelectedPath(null);
        setCurrentView('dashboard');
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
