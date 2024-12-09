import React, { useState } from 'react';
import { Box, Typography, Button } from '@mui/material';
import { MovieList } from '@/types/types';
import MovieCard from './MovieCardRecomend';

interface MovieListProps {
  movies: MovieList[];
}

const MovieListRecomendado: React.FC<MovieListProps> = ({ movies }) => {
  const [currentPage, setCurrentPage] = useState(0);
  const moviesPerPage = 5;

  const startIndex = currentPage * moviesPerPage;
  const endIndex = startIndex + moviesPerPage;
  const currentMovies = movies.slice(startIndex, endIndex);

  const handleNextPage = () => {
    if (endIndex < movies.length) setCurrentPage((prev) => prev + 1);
  };

  const handlePrevPage = () => {
    if (currentPage > 0) setCurrentPage((prev) => prev - 1);
  };

  if (!movies || movies.length === 0) {
    return <Typography variant="h6" align="center">Carregando filmes ou nenhum filme encontrado...</Typography>;
  }

  return (
    <Box sx={{ flex: 1, overflowY: 'auto', padding: 2 }}>
      <Typography variant="h6" align="center" gutterBottom>
        Recomendados
      </Typography>
      
      <section className='flex items-center justify-center flex-col'>
        {currentMovies.map((movie, index) => (
            <MovieCard movie={movie} key={index+"cardrecomend"+movie.id}/>
        ))}
      </section>

      {/* Navegação de Páginas */}
      <Box display="flex" justifyContent="center" mt={2}>
        <Button
          variant="outlined"
          color="primary"
          onClick={handlePrevPage}
          disabled={currentPage === 0}
          sx={{ marginRight: 2 }}
        >
          Anterior
        </Button>
        <Button
          variant="outlined"
          color="primary"
          onClick={handleNextPage}
          disabled={endIndex >= movies.length}
        >
          Próximo
        </Button>
      </Box>
    </Box>
  );
};

export default MovieListRecomendado;
