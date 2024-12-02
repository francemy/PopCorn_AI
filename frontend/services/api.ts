import { Rating } from '@/types/types';
import axios from 'axios';
import Cookies  from 'js-cookie';
// Criação da instância do axios
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/',
});

// Função para lidar com erros de requisição
const handleApiError = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    // Aqui você pode personalizar o erro, por exemplo, mostrar uma mensagem mais amigável ao usuário
    console.error('Erro na requisição:', error.message);
  } else {
    console.error('Erro desconhecido:', error);
  }
  throw error; // Lançar o erro para que o chamador possa lidar com ele
};

// Função para buscar filmes
export const fetchMovies = async () => {
  const token = localStorage.getItem("access_token");
  console.log(`Bearer ${token}`)
  try {
    
    const response = await api.get('movies/',{
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status === 200) return response.data;
    return {data: []};
  } catch (error) {
    handleApiError(error);
  }
};

// Função para buscar gêneros
export const fetchGenres = async () => {
  try {
    const response = await api.get('genres/');
    if (response.status === 200) return response.data;
    return {data: []};
  } catch (error) {
    handleApiError(error);
  }
};

// Função para criar avaliação
export const createRating = async (rating: Rating) => {
  try {
    const response = await api.post('ratings/', {
      rating,
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Função para buscar recomendações de filmes
export const fetchMovieRecommendations = async (userId: string) => {
  try {
    const response = await api.get('movie-recommendations/', {
      params: {
        user_id: userId,
      },
    });
    if (response.status === 200) {
      return response.data; // Aqui retornamos os títulos dos filmes recomendados
    }
    return [];
  } catch (error) {
    handleApiError(error);
  }
};

// Interceptor para adicionar os cookies no cabeçalho da requisição
api.interceptors.request.use(
  async (config) => {
    // Recuperando o token de acesso do cookie
    const token = Cookies.get('access_token');
    const userId = Cookies.get('user_id');
    const username = Cookies.get('username');
    const role = Cookies.get('role');
    const lastLogin = Cookies.get('last_login');

    // Definindo o cabeçalho Authorization com o token, se existir
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    // Se você precisar passar outros cookies em um formato específico ou como parâmetros, pode adicionar aqui.
    config.headers['X-User-Id'] = userId || '';  // Exemplo de envio de user_id como header, se necessário
    config.headers['X-Username'] = username || '';  // Exemplo de envio de username como header
    config.headers['X-Role'] = role || '';  // Exemplo de envio de role como header
    config.headers['X-Last-Login'] = lastLogin || '';  // Exemplo de envio de last_login como header

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
