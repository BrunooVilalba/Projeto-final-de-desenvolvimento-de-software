
import React from 'react';
import { MenuIcon, UserCircleIcon, LogoutIcon } from './icons/Icons';
import { User } from '../types';

interface HeaderProps {
  onMenuClick: () => void;
  currentUser: User | null;
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick, currentUser, onLogout }) => {
  return (
    <header className="flex-shrink-0 bg-red-900 text-white shadow-md">
      <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
        <button
          onClick={onMenuClick}
          className="lg:hidden text-slate-200 hover:text-white focus:outline-none"
          aria-label="Abrir menu"
        >
          <MenuIcon className="h-6 w-6" />
        </button>
        <div className="flex items-center lg:hidden">
            <h1 className="text-xl font-bold text-white">EstudaAI</h1>
        </div>
        <div className="flex items-center justify-end">
            <UserCircleIcon className="h-8 w-8 text-slate-200" />
            <div className="ml-2 hidden sm:block">
              <p className="font-medium text-white text-sm leading-tight">{currentUser?.name || 'Aluno'}</p>
              <p className="text-xs text-slate-300 leading-tight">{currentUser?.course || 'Estudante'}</p>
            </div>
            <button
              onClick={onLogout}
              className="ml-4 p-2 rounded-full text-slate-200 hover:bg-red-800 hover:text-white focus:outline-none focus:ring-2 focus:ring-white"
              aria-label="Sair"
            >
              <LogoutIcon className="h-5 w-5" />
            </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
