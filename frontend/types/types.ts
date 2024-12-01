// types.ts

// Tipo para o usuário
export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    password?: string;  // Opcional, usado apenas no cadastro
  }
  
  // Tipo para o gênero de filmes
  export interface Genre {
    id: number;
    name: string;
    description: string;
  }
  
  // Tipo para os filmes
  export interface Movie {
    id: number;
    title: string;
    description: string;
    release_date: string;
    duration: string;  // Duração em formato de string, por exemplo "2h 30m"
    image_url: string;
    genres: Genre[];  // Lista de gêneros associados ao filme
  }
  
  // Tipo para as avaliações dos filmes
  export interface Rating {
    id: number;
    user: User;
    movie: Movie;
    rating: number;  // Classificação entre 1 e 5
    review: string;  // Comentário do usuário sobre o filme
    created_at: string;  // Data de criação da avaliação
  }
  
  // Tipo para as preferências do usuário
  export interface Preference {
    id: number;
    user: User;
    genre: Genre;  // Gênero preferido do usuário
    preference_type: 'like' | 'dislike';  // Tipo de preferência (curtir ou não gostar)
  }
  
  // Tipo para a resposta de uma requisição de filmes
  export interface MovieResponse {
    movies: Movie[];
    total: number;  // Número total de filmes, útil para paginação
  }
  
  // Tipo para o filtro de filmes por gênero
  export interface GenreFilter {
    genreId: number | null;  // Id do gênero para filtro, ou null para mostrar todos os filmes
  }
  