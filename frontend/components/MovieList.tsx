"use client";
import React, { useEffect, useState } from "react";
import {
  Box,
  Grid,
  Typography,
  CircularProgress,
  Container,
  Pagination,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";

import { fetchMovies } from "../services/api";
import MovieCard from "./MovieCard";
import { MovieList } from "@/types/types";

interface MovieListProps {
  genreId?: number | null;
}

const MovieListP: React.FC<MovieListProps> = ({ genreId }) => {
  const [movies, setMovies] = useState<MovieList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1); // Página atual
  const [totalPages, setTotalPages] = useState(1); // Total de páginas retornado pelo backend

  const theme = useTheme();

  useEffect(() => {
    const getMovies = async () => {
      try {
        setLoading(true);

        const { results, count } = await fetchMovies(page, 12, genreId); // Inclui parâmetros de página e gênero

        setMovies(results); // Define os filmes da página atual
        setTotalPages(Math.ceil(count / 12)); // Calcula o total de páginas baseado no backend
        setError(null);
      } catch (error) {
        console.error("Error fetching movies:", error);
        setError("Não foi possível carregar os filmes. Verifique sua conexão.");
      } finally {
        setLoading(false);
      }
    };

    getMovies();
  }, [page, genreId]);

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    setPage(value); // Atualiza a página ao clicar na paginação
  };

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
        <Typography variant="h6" color="error" align="center" gutterBottom>
          {error}
        </Typography>
        <Typography variant="body1" align="center" color="textSecondary">
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
          <Typography variant="body1" align="center" color="textSecondary">
            Não há filmes neste gênero no momento.
          </Typography>
        )}
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      <Grid
        container
        spacing={{ xs: 1, sm: 2, md: 2 }}
        columns={{ xs: 2, sm: 6, md: 10 }}
      >
        {movies.map((movie) => (
          <Grid
            item
            key={movie.id}
            xs={2}
            sm={4}
            md={3}
            sx={{
              display: "flex",
              justifyContent: "center",
              mb: 2,
            }}
          >
            <MovieCard movie={movie} />
          </Grid>
        ))}
      </Grid>

      {/* Paginação */}
      <Box display="flex" justifyContent="center" sx={{ mt: 4 }}>
        <Pagination
          count={totalPages}
          page={page}
          onChange={handlePageChange}
          color="primary"
        />
      </Box>
    </Container>
  );
};

export default MovieListP;
