"use client"
import React, { useEffect, useState } from 'react';
import { 
  Container, Typography, Box, Button, AppBar, Toolbar, IconButton, Menu, MenuItem, Grid 
} from '@mui/material';
import AddPreferenceModal from "../components/AddPreferenceModal";
import GenreSelector from '../components/GenreSelector';
import MovieListP from '../components/MovieList';
import LogoutButton from '../components/LogoutButton';
import { Genre, MovieList } from '@/types/types';
import { fetchGenres, fetchMoviesByGenre, fetchMoviesByViews } from '@/services/api';
import MovieLisRecomendado from '@/components/MoviesRecomend';

// Ícones SVG
const setaBaixo: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 17.25 12 21m0 0-3.75-3.75M12 21V3" />
</svg>;

const setaCima: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 6.75 12 3m0 0 3.75 3.75M12 3v18" />
</svg>;

const menu: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
</svg>;

const HomePage: React.FC = () => {
  const [selectedGenre, setSelectedGenre] = useState<number | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [genreList, setGenreList] = useState<Genre[]>([]);
  const [recommendedMovies, setRecommendedMovies] = useState<MovieList[]>([]);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        // Buscar gêneros
        const { data: genres } = await fetchGenres();
        if (genres) {
          setGenreList(genres as Genre[]);
        }
        // Buscar recomendações de filmes
        const {data} = await fetchMoviesByViews();
        console.log("data movies:",data)
        if (data) {
          setRecommendedMovies([]);
        }
      } catch (error) {
        console.error('Erro ao carregar dados iniciais:', error);
      }
    };
    fetchInitialData();
  }, []);

  const handleGenreChange = (genreId: number) => {
    setSelectedGenre(genreId);
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <Container>
      {/* Barra de Navegação */}
      <AppBar position="sticky" sx={{ padding: 1 }}>
        <Typography variant="h6" sx={{ flexGrow: 1, textAlign: 'center', color: 'white' }}>
          PopCorn AI
        </Typography>
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleMenuOpen}
            sx={{ marginRight: 2 }}
          >
            {menu} {anchorEl ? setaCima : setaBaixo}
          </IconButton>
          <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose} sx={{ mt: 2 }}>
            <MenuItem>
              <Button
                variant="contained"
                color="primary"
                onClick={() => setModalOpen(true)}
                sx={{ width: '100%' }}
              >
                Adicionar Nova Preferência
              </Button>
            </MenuItem>
            <MenuItem onClick={handleMenuClose}>Perfil</MenuItem>
            <MenuItem onClick={handleMenuClose}>Configurações</MenuItem>
            <MenuItem onClick={handleMenuClose}>
              <LogoutButton />
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      <Typography variant="h4" gutterBottom sx={{ marginTop: 2 }}>
        PopCorn AI - Recomendação de Filmes
      </Typography>

      <Grid container spacing={4}>
        {/* Coluna Esquerda */}
        <Grid item xs={14} md={10}>
          <Box mb={4}>
            <Typography variant="h5" gutterBottom>
              Preferências
            </Typography>
            <AddPreferenceModal
              open={modalOpen}
              onClose={() => setModalOpen(false)}
              genres={genreList}
            />
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
          <Box mb={4}>
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
        <Grid item xs={10} md={2}>
          <Box>
            <Typography variant="h5" gutterBottom>
              Filmes Recomendados
            </Typography>
            <MovieLisRecomendado movies={recommendedMovies} /> {/* Reutiliza o componente MovieList */}
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default HomePage;
