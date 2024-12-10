"use client"
import React, { useEffect, useState } from 'react';
import { 
  Container, Typography, Box, Grid 
} from '@mui/material';
import GenreSelector from '@/components/GenreSelector';
import MovieListP from '@/components/MovieList';
import { Genre } from '@/types/types';
import { fetchGenres } from '@/services/api';
import MovieLisRecomendado from '@/components/MoviesRecomend';

const HomePage: React.FC = () => {
  const [selectedGenre, setSelectedGenre] = useState<number | null>(null);
  const [genreList, setGenreList] = useState<Genre[]>([]);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        // Buscar gêneros
        const { data: genres } = await fetchGenres();
        if (genres) {
          setGenreList(genres as Genre[]);
        }
        // Buscar recomendações de filmes
       
      } catch (error) {
        console.error('Erro ao carregar dados iniciais:', error);
      }
    };
    fetchInitialData();
  }, []);

  const handleGenreChange = (genreId: number) => {
    setSelectedGenre(genreId);
  };



  return (
    <Container>
      <Typography variant="h4" gutterBottom sx={{ marginTop: 2 }}>
        PopCorn AI - Recomendação de Filmes
      </Typography>

      <Grid container spacing={4}>
        {/* Coluna Esquerda */}
        <Grid item xs={12} md={8}>
          <Box mb={4}>
            <Typography variant="h5" gutterBottom>
              Preferências
            </Typography>
            
          </Box>
          <Box mb={4}>
            <Typography variant="h6" gutterBottom>
              Sobre o PopCorn AI
            </Typography>
            <Typography variant="body1">
              PopCorn AI é uma plataforma de recomendação de filmes desenvolvida para oferecer aos usuários sugestões personalizadas com base em suas preferências.
              Explore novos filmes e gêneros que combinam com você!
            </Typography>
          </Box>
          <Box mb={6}>
            <Typography variant="h6" gutterBottom>
              Selecione um Gênero
            </Typography>
            <GenreSelector onChange={handleGenreChange} genreList={genreList} />
          </Box>
          <Box>
            <MovieListP genreId={selectedGenre} />
          </Box>
        </Grid>

        {/* Coluna Direita */}
        <Grid item xs={12} md={4}>
          <Box>
            <Typography variant="h5" gutterBottom>
              Filmes Recomendados
            </Typography>
            <MovieLisRecomendado />
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default HomePage;
