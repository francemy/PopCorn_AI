import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, Card } from '@mui/material';
import { MovieList } from '@/types/types';
import MovieCard from './MovieCardRecomend';
import { fetchMovieRecommendations } from '@/services/api';

const MovieListRecomendado: React.FC = () => {
  const [currentPage, setCurrentPage] = useState(1); // Página inicial
  const [recommendedMovies, setRecommendedMovies] = useState<MovieList[]>([]);
  const [nextPageUrl, setNextPageUrl] = useState<string | null>(null); // URL da próxima página
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetch() {
      const data = await fetchMovieRecommendations(currentPage); // Passar a página atual para a API
      if (data) {
        setRecommendedMovies(data.movies); // Filmes da página atual
        setNextPageUrl(data.nextPageUrl); // URL da próxima página
        setLoading(false)
      }
    }
    setLoading(true)
    fetch();
  }, [currentPage]); // Recarregar os filmes sempre que a página mudar

  const handleNextPage = () => {
    if (nextPageUrl) {
      setCurrentPage((prevPage) => prevPage + 1); // Aumenta a página
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prevPage) => prevPage - 1); // Diminui a página
    }
  };

  return (
    <Box sx={{ flex: 1, overflowY: 'auto', padding: 2 }}>
      <Typography variant="h6" align="center" gutterBottom>
        Recomendados
      </Typography>

      <section className="flex items-center justify-center flex-col">
        {loading ? <Card>Carregando...</Card> : recommendedMovies.map((movie, index) => (
          <MovieCard movie={movie} key={index + "cardrecomend" + movie.id} />
        ))}
      </section>

      {/* Navegação de Páginas */}
      <Box display="flex" justifyContent="center" mt={2}>
        <Button
          variant="outlined"
          color="primary"
          onClick={handlePrevPage}
          disabled={!(currentPage > 1)} // Desabilitar se não houver página anterior
          sx={{ marginRight: 2 }}
        >
          Anterior
        </Button>
        <Button
          variant="outlined"
          color="primary"
          onClick={handleNextPage}
          disabled={!nextPageUrl} // Desabilitar se não houver próxima página
        >
          Próximo
        </Button>
      </Box>
    </Box>
  );
};

export default MovieListRecomendado;
