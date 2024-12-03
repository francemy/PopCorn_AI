"use client"
import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Typography,
  CircularProgress,
  useMediaQuery,
  Container,
  Pagination
} from '@mui/material';
import { useTheme } from '@mui/material/styles';

import { fetchMovieRecommendations, fetchMovies } from '../services/api';
import MovieCard from './MovieCard';
import { Genre, MovieList } from '@/types/types';

interface MovieListProps {
  genreId?: number | null;
}

const MovieListP: React.FC<MovieListProps> = ({ genreId }) => {
  const [movies, setMovies] = useState<MovieList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);  // Estado para controlar a página
  const [moviesPerPage] = useState(12); // Número de filmes por página

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));

  // Determine grid columns based on screen size
  const getGridColumns = () => {
    if (isMobile) return 2;
    if (isTablet) return 3;
    return 4;
  };

  useEffect(() => {
    const getMovies = async () => {

      try {
        setLoading(true);

        if (genreId === 0) {
          const { data } = await fetchMovieRecommendations();

          setMovies(data);
        }
        else {
          const { data } = await fetchMovies();

          const filteredMovies = genreId
            ? data.filter((movie: MovieList) =>
              movie.genres.some((genre: Genre) => genre.id === genreId)
            )
            : data;
            setMovies(filteredMovies);
        }
        
        setError(null);
      } catch (error) {
        console.error('Error fetching movies:', error);
        setError('Não foi possível carregar os filmes. Verifique sua conexão.');
      } finally {
        setLoading(false);
      }
    };

    getMovies();
  }, [genreId]);

  const handlePageChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value); // Atualiza a página
  };

  // Filmes a serem exibidos para a página atual
  const indexOfLastMovie = page * moviesPerPage;
  const indexOfFirstMovie = indexOfLastMovie - moviesPerPage;
  const currentMovies = movies.slice(indexOfFirstMovie, indexOfLastMovie);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        height="100vh"
        sx={{ backgroundColor: theme.palette.background.default }}
      >
        <CircularProgress color="primary" size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        height="100vh"
        sx={{ backgroundColor: theme.palette.background.default, p: 2 }}
      >
        <Typography
          variant="h6"
          color="error"
          align="center"
          gutterBottom
        >
          {error}
        </Typography>
        <Typography
          variant="body1"
          align="center"
          color="textSecondary"
        >
          Tente atualizar a página ou verificar sua conexão com a internet.
        </Typography>
      </Box>
    );
  }

  if (movies.length === 0) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        height="100vh"
        sx={{ backgroundColor: theme.palette.background.default, p: 2 }}
      >
        <Typography
          variant="h6"
          color="textSecondary"
          align="center"
          gutterBottom
        >
          Nenhum filme encontrado
        </Typography>
        {genreId && (
          <Typography
            variant="body1"
            align="center"
            color="textSecondary"
          >
            Não há filmes neste gênero no momento.
          </Typography>
        )}
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Grid
        container
        spacing={{ xs: 2, sm: 3, md: 4 }}
        columns={{ xs: 4, sm: 8, md: 12 }}
      >
        {currentMovies.map((movie, index) => (
          <Grid
            item
            key={movie.id || index}
            xs={2}
            sm={4}
            md={3}
            sx={{
              display: 'flex',
              justifyContent: 'center',
              mb: 2
            }}
          >
            <MovieCard movie={movie} />
          </Grid>
        ))}
      </Grid>

      {/* Paginação */}
      <Box display="flex" justifyContent="center" sx={{ mt: 4 }}>
        <Pagination
          count={Math.ceil(movies.length / moviesPerPage)}
          page={page}
          onChange={handlePageChange}
          color="primary"
        />
      </Box>
    </Container>
  );
};

export default MovieListP;
