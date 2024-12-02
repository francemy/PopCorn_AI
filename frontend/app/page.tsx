"use client"
import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button, AppBar, Toolbar, IconButton, Menu, MenuItem } from '@mui/material';
import AddPreferenceModal from "../components/AddPreferenceModal";
import GenreSelector from '../components/GenreSelector';
import MovieList from '../components/MovieList';
import LogoutButton from '../components/LogoutButton';
import { Genre } from '@/types/types';
import { fetchGenres } from '@/services/api';
// Ícone para o Menu

const setaBaixo: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 17.25 12 21m0 0-3.75-3.75M12 21V3" />
</svg>

const setaCima: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 6.75 12 3m0 0 3.75 3.75M12 3v18" />
</svg>


const menu: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
</svg>



const HomePage: React.FC = () => {
  const [selectedGenre, setSelectedGenre] = useState<number | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [genreList,setGenreList] = useState<Genre[]>([])

  const handleGenreChange = (genreId: number) => {
    setSelectedGenre(genreId);
  };

  useEffect(() => {
    const getGenres = async () => {
      try {
        const {data} = await fetchGenres();
        if (data) {
          setGenreList(data as Genre[]);// Ao finalizar o carregamento, defina 'loading' como false
        }
      } catch (error) {
        console.error('Erro ao buscar gêneros:', error);
      }
    };

    getGenres();
  }, []);

  // Abre o menu
  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  // Fecha o menu
  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <Container>
      {/* AppBar com Menu e Logout */}
      <AppBar position="sticky" sx={{ padding: 1 }}>
        {/* Título da Aplicação */}
        <Typography variant="h6" sx={{ flexGrow: 1, textAlign: 'center', color: 'white' }}>
          PopCorn AI
        </Typography>

        <Toolbar>
          {/* Botão de Menu */}
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleMenuOpen}
            sx={{ marginRight: 2 }}
          >
            {menu} {anchorEl ? setaCima : setaBaixo}
          </IconButton>

          {/* Menu Dropdown */}
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            sx={{ mt: 2 }}
          >
            {/* Opção de Adicionar Preferência */}
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

            {/* Opções de Navegação */}
            <MenuItem onClick={handleMenuClose}>Perfil</MenuItem>
            <MenuItem onClick={handleMenuClose}>Configurações</MenuItem>

            {/* Opção de Logout */}
            <MenuItem onClick={handleMenuClose}>
              <LogoutButton /> {/* Botão de Logout dentro do Menu */}
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>


      {/* Título Principal */}
      <Typography variant="h4" gutterBottom sx={{ marginTop: 2 }}>
        PopCorn AI - Recomendação de Filmes
      </Typography>

      {/* Seção de Preferências */}
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

      {/* Seção "Sobre" */}
      <Box mb={4}>
        <Typography variant="h6" gutterBottom>
          Sobre o PopCorn AI
        </Typography>
        <Typography variant="body1">
          PopCorn AI é uma plataforma de recomendação de filmes desenvolvida para oferecer aos usuários sugestões personalizadas com base em suas preferências.
          Explore novos filmes e gêneros que combinam com você!
        </Typography>
      </Box>

      {/* Selector de Gêneros */}
      <Box mb={4}>
        <Typography variant="h6" gutterBottom>
          Selecione um Gênero
        </Typography>
        <GenreSelector onChange={handleGenreChange} genreList={genreList} />
      </Box>

      {/* Lista de Filmes */}
      <Box>
        <MovieList genreId={selectedGenre} />
      </Box>
    </Container>
  );
};

export default HomePage;