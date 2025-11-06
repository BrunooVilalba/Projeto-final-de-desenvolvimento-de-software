const API_BASE_URL = 'http://localhost:8000/api';

// Função auxiliar para fazer requisições autenticadas
async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('accessToken');
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
  
  if (response.status === 401) {
    // Token expirado, tentar refresh
    const refreshed = await refreshToken();
    if (refreshed) {
      headers['Authorization'] = `Bearer ${localStorage.getItem('accessToken')}`;
      return fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });
    }
  }
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Erro na requisição' }));
    throw new Error(error.detail || error.message || 'Erro na requisição');
  }
  
  return response.json();
}

async function refreshToken(): Promise<boolean> {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) return false;
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('accessToken', data.access);
      return true;
    }
  } catch (error) {
    console.error('Erro ao refresh token:', error);
  }
  
  return false;
}

// Auth API
export const authAPI = {
  async register(userData: {
    username: string;
    email: string;
    password: string;
    first_name: string;
    course: string;
    experience_level: string;
  }) {
    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Erro no cadastro' }));
      throw new Error(error.detail || error.message || 'Erro no cadastro');
    }
    
    const data = await response.json();
    localStorage.setItem('accessToken', data.tokens.access);
    localStorage.setItem('refreshToken', data.tokens.refresh);
    return data.user;
  },
  
  async login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: email, password }),
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Credenciais inválidas' }));
      throw new Error(error.detail || 'Credenciais inválidas');
    }
    
    const data = await response.json();
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    
    // Retornar dados do usuário da resposta
    return data.user || data;
  },
  
  async getProfile() {
    return apiRequest('/auth/profile/');
  },
  
  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },
};

// Learning Paths API
export const learningPathsAPI = {
  async getAll() {
    return apiRequest('/learning-paths/');
  },
  
  async getById(id: string) {
    return apiRequest(`/learning-paths/${id}/`);
  },
  
  async create(pathData: any) {
    return apiRequest('/learning-paths/', {
      method: 'POST',
      body: JSON.stringify(pathData),
    });
  },
  
  async update(id: string, pathData: any) {
    return apiRequest(`/learning-paths/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(pathData),
    });
  },
  
  async delete(id: string) {
    return apiRequest(`/learning-paths/${id}/`, {
      method: 'DELETE',
    });
  },
  
  async toggleStep(pathId: string, stepIndex: number) {
    return apiRequest(`/learning-paths/${pathId}/toggle_step/`, {
      method: 'POST',
      body: JSON.stringify({ step_index: stepIndex }),
    });
  },
};

