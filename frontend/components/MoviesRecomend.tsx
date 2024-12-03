import React, { useState } from 'react';
import { Box, Typography, Button, Grid, Card, CardMedia, CardContent, CardActions } from '@mui/material';
import {  MovieList } from '@/types/types';

interface MovieListProps {
  movies: MovieList[]; // Lista de filmes recebida como prop
}

const MovieLisRecomendado: React.FC<MovieListProps> = ({ movies }) => {
  const [currentPage, setCurrentPage] = useState(0); // Estado da página atual
  const moviesPerPage = 5; // Número de filmes por página

  // Calcular os índices para exibir os filmes da página atual
  const startIndex = currentPage * moviesPerPage;
  const endIndex = startIndex + moviesPerPage;
  const currentMovies = movies.slice(startIndex, endIndex);

  // Funções para navegação entre páginas
  const handleNextPage = () => {
    if (endIndex < movies.length) setCurrentPage(currentPage + 1);
  };

  const handlePrevPage = () => {
    if (currentPage > 0) setCurrentPage(currentPage - 1);
  };

  return (
    <Box>
      <Grid container spacing={2}>
        {currentMovies.map((movie) => (
          <Grid item xs={12} sm={6} md={4} key={movie.id}>
            <Card>
              <CardMedia
                component="img"
                height="200"
                image={movie.image_url || '/placeholder-image.png'} // Substitua por uma imagem padrão se não houver URL
                alt={movie.title}
              />
              <CardContent>
                <Typography variant="h6">{movie.title}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {movie.description?.slice(0, 100)}... {/* Limita a descrição a 100 caracteres */}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary">
                  Saiba Mais
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Controles de paginação */}
      <Box display="flex" justifyContent="space-between" mt={2}>
        <Button
          variant="outlined"
          color="primary"
          onClick={handlePrevPage}
          disabled={currentPage === 0}
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

export default MovieLisRecomendado;
