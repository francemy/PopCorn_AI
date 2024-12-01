// components/MovieList.tsx
"use client"
import React, { useEffect, useState } from 'react';
import { fetchMovies } from '../services/api';
import MovieCard from './MovieCard';
import { Grid, CircularProgress, Typography, Box } from '@mui/material';
import { Genre, Movie } from '@/types/types';

const MovieList: React.FC<{ genreId?: number | null }> = ({ genreId }) => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null); // Estado para capturar erros

  useEffect(() => {
    const getMovies = async () => {
      try {
        const {data} = await fetchMovies();
        if (genreId) {
          
          const filteredMovies = data.filter((movie: Movie) =>
            movie.genres.some((genre: Genre) => genre.id === genreId)
          );
          console.log("filteredMovies:",filteredMovies)
          setMovies(filteredMovies);
        } else {
          console.log("data: ",data)
          setMovies(data);
        }
      } catch (error) {
        console.error('Error fetching movies:', error);
        setError('Falha ao carregar os filmes. Tente novamente mais tarde.');
      } finally {
        setLoading(false);
      }
    };

    getMovies();
  }, [genreId]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <Typography variant="h6" color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Grid container spacing={2}>
      {movies.map((movie, index) => (
        <Grid item key={movie.id || index} xs={12} sm={6} md={4}>
          <MovieCard movie={movie} />
        </Grid>
      ))}
    </Grid>
  );
};

export default MovieList;
