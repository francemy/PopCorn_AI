import { Rating } from '@/types/types';
import axios from 'axios';

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
  try {
    const response = await api.get('movies/', {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status === 200) return response.data;
    return { data: [] };
  } catch (error) {
    handleApiError(error);
  }
};

// Função para buscar gêneros
export const fetchGenres = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await api.get('genres/', {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status === 200) return response.data;
    return { data: [] };
  } catch (error) {
    handleApiError(error);
  }
};

// Função para criar avaliação
export const createRating = async (rating: Rating) => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await api.post('ratings/', {
      rating,
    }, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

// Função para buscar recomendações de filmes
export const fetchMovieRecommendations = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await api.get('/movies/recomendado/', {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    console.log(response.data)
    if (response.status === 200) {
      return response.data; // Aqui retornamos os títulos dos filmes recomendados
    }
    return [];
  } catch (error) {
    handleApiError(error);
  }
};

// Função para buscar filmes baseados no gênero
export const fetchMoviesByGenre = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await api.get(`/movies/genre/`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    
    return response.data; // Retorna os filmes recomendados por gênero
  
  } catch (error) {
    handleApiError(error);
  }
};


// Função para buscar filmes baseados nas visualizações do usuário
export const fetchMoviesByViews = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await api.get('/movies/views/', {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status === 200) {
      return response.data; // Retorna os filmes recomendados com base nas visualizações
    }
    return [];
  } catch (error) {
    handleApiError(error);
  }
};


export default api;
