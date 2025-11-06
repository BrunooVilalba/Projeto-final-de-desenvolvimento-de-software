import React, { useState } from 'react';
import { User } from '../types';
import { BrainCircuitIcon, MailIcon, KeyIcon, UserCircleIcon, AcademicCapIcon, SignalIcon } from './icons/Icons';

interface RegisterProps {
  onSuccessfulRegistration: () => void;
  onNavigateToLogin: () => void;
}

const Register: React.FC<RegisterProps> = ({ onSuccessfulRegistration, onNavigateToLogin }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [course, setCourse] = useState('');
  const [experienceLevel, setExperienceLevel] = useState<'Iniciante' | 'Intermediário' | 'Avançado'>('Iniciante');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!name || !email || !password || !course) {
      setError('Por favor, preencha todos os campos.');
      return;
    }
    
    if (password.length < 6) {
        setError('A senha deve ter pelo menos 6 caracteres.');
        return;
    }

    try {
        const { authAPI } = await import('../services/api');
        await authAPI.register({
          username: email.split('@')[0],
          email,
          password,
          first_name: name,
          course,
          experience_level: experienceLevel,
        });
        onSuccessfulRegistration();
    } catch (err: any) {
        setError(err.message || 'Ocorreu um erro ao tentar se cadastrar.');
    }
  };

  return (
    <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-2xl shadow-lg animate-fade-in-fast">
      <div className="text-center">
        <BrainCircuitIcon className="mx-auto h-12 w-12 text-red-800" />
        <h1 className="mt-4 text-3xl font-bold tracking-tight text-slate-900">
          Crie sua Conta
        </h1>
        <p className="mt-2 text-slate-600">
          Comece sua jornada de aprendizado personalizada hoje.
        </p>
      </div>
      <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
        <div className="relative">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <UserCircleIcon className="h-5 w-5 text-slate-400" />
            </div>
            <input
                id="name"
                name="name"
                type="text"
                autoComplete="name"
                required
                className="w-full pl-10 p-3 bg-slate-50 border border-slate-300 rounded-lg text-slate-900 placeholder-slate-400 focus:ring-2 focus:ring-red-800 focus:border-red-800 transition"
                placeholder="Nome completo"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
        </div>
        <div className="relative">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <MailIcon className="h-5 w-5 text-slate-400" />
            </div>
            <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="w-full pl-10 p-3 bg-slate-50 border border-slate-300 rounded-lg text-slate-900 placeholder-slate-400 focus:ring-2 focus:ring-red-800 focus:border-red-800 transition"
                placeholder="E-mail"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
        </div>
        <div className="relative">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <KeyIcon className="h-5 w-5 text-slate-400" />
            </div>
            <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                className="w-full pl-10 p-3 bg-slate-50 border border-slate-300 rounded-lg text-slate-900 placeholder-slate-400 focus:ring-2 focus:ring-red-800 focus:border-red-800 transition"
                placeholder="Senha (mín. 6 caracteres)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
        </div>
        <div className="relative">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <AcademicCapIcon className="h-5 w-5 text-slate-400" />
            </div>
            <input
                id="course"
                name="course"
                type="text"
                required
                className="w-full pl-10 p-3 bg-slate-50 border border-slate-300 rounded-lg text-slate-900 placeholder-slate-400 focus:ring-2 focus:ring-red-800 focus:border-red-800 transition"
                placeholder="Área de Formação (Ex: Ciência da Computação)"
                value={course}
                onChange={(e) => setCourse(e.target.value)}
            />
        </div>
        <div className="relative">
             <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <SignalIcon className="h-5 w-5 text-slate-400" />
            </div>
            <select
                id="experienceLevel"
                name="experienceLevel"
                required
                className="w-full pl-10 p-3 bg-slate-50 border border-slate-300 rounded-lg text-slate-900 focus:ring-2 focus:ring-red-800 focus:border-red-800 transition appearance-none"
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value as 'Iniciante' | 'Intermediário' | 'Avançado')}
            >
                <option value="Iniciante">Nível de Experiência: Iniciante</option>
                <option value="Intermediário">Nível de Experiência: Intermediário</option>
                <option value="Avançado">Nível de Experiência: Avançado</option>
            </select>
        </div>

        {error && <p className="text-sm text-red-600 text-center pt-2">{error}</p>}

        <div className="pt-2">
          <button
            type="submit"
            className="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-800 hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-700 transition-colors"
          >
            Cadastrar
          </button>
        </div>
      </form>
      <p className="text-sm text-center text-slate-600">
        Já tem uma conta?{' '}
        <button onClick={onNavigateToLogin} className="font-medium text-red-800 hover:text-red-700">
          Faça login
        </button>
      </p>
    </div>
  );
};

export default Register;