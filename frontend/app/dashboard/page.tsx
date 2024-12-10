"use client";
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Skeleton,
  useMediaQuery,
  useTheme,
  TablePagination,
  Container
} from '@mui/material';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';
// Importação das tipagens
import { MovieList, MovieDashboardData } from '@/types/types';
import api, { fetchMovies } from '@/services/api';
import { Favorite, Movie, ThumbDown, ThumbUp } from '@mui/icons-material';

// Tipo da resposta do dashboard

const InteractionCard: React.FC<{ icon: JSX.Element; title: string; value: number; color: string }> = ({ icon, title, value, color }) => {
  // Verifica se o valor é NaN, e se for, retorna 0 (ou outro valor padrão)
  const safeValue = isNaN(value) ? 0 : value;

  return (
    <Card>
      <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', p: 2 }}>
        {React.cloneElement(icon, { sx: { fontSize: 40, mb: 1, color } })}
        <Typography variant="subtitle1">{title}</Typography>
        <Typography variant="h5" fontWeight="bold">
          {safeValue}
        </Typography>
      </CardContent>
    </Card>
  );
};

const MovieDashboard: React.FC = () => {
  const [movieData, setMovieData] = useState<MovieDashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState<number>(0);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    const fetchMovieData = async () => {
      try {
        const cachedData = localStorage.getItem('dashboardData'); // Tenta buscar do cache
        if (cachedData) {
          setMovieData(JSON.parse(cachedData)); // Usa os dados do cache
          return;
        }

        const token = localStorage.getItem('access_token');
        const response = await api.get(`/dashboard/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const fetchedData = response.data.data;
        setMovieData(fetchedData);

        // Armazena os dados no cache para reutilização futura
        localStorage.setItem('dashboardData', JSON.stringify(fetchedData));
      } catch (err) {
        console.log(err)
        setError('Falha ao carregar os dados. Tente novamente mais tarde.');
      }
    };

    fetchMovieData();
  }, []);


  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => setSelectedTab(newValue);

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <Typography color="error" variant="h6">{error}</Typography>
      </Box>
    );
  }

  if (!movieData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <Skeleton variant="rectangular" width={300} height={200} />
      </Box>
    );
  }

  return (
    <Container>
      <Box sx={{ flexGrow: 1, p: 3 }}>
        <Typography variant="h4" gutterBottom>Movie Dashboard</Typography>
        <Button variant="outlined" onClick={() => {
          localStorage.removeItem('dashboardData'); // Remove os dados armazenados
          window.location.reload(); // Recarrega a página para buscar novos dados
        }}>
          Atualizar Dados
        </Button>

        <Tabs value={selectedTab} onChange={handleTabChange} sx={{ mb: 3 }}>
          <Tab label="Overview" />
          <Tab label="Movies" />
          <Tab label="Interactions" />
          <Tab label="Preferences" />
        </Tabs>

        {selectedTab === 0 && (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Genre Distribution" />
                <Box p={2}>
                  {movieData.genreDistribution.length > 0 ? (
                    <PieChart width={isSmallScreen ? 350 : 500} height={350}>
                      <Pie
                        data={movieData.genreDistribution}
                        cx="50%"
                        cy="50%"
                        outerRadius={120}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      >
                        {movieData.genreDistribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  ) : (
                    <Typography color="textSecondary">Nenhum dado disponível</Typography>
                  )}
                </Box>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Média das Avaliações por Gênero" />
                <Box p={2}>
                  {movieData.ratings.length > 0 ? (
                    <BarChart width={isSmallScreen ? 350 : 500} height={350} data={movieData.ratings}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="genre" />
                      <YAxis domain={[0, 5]} />
                      <Tooltip formatter={(value) => value.toString()} />
                      <Bar dataKey="avgRating" fill="#FF8042" />
                    </BarChart>
                  ) : (
                    <Typography color="textSecondary">Nenhum dado disponível</Typography>
                  )}
                </Box>
              </Card>
            </Grid>
          </Grid>
        )}

        {selectedTab === 1 && <MovieTableWithPagination />}
        {selectedTab === 2 && (
          <Grid container spacing={3}>
            <Grid item xs={6} md={3}>
              <InteractionCard icon={<ThumbUp />} title="Likes" value={movieData.interactions.likes} color="green" />
            </Grid>
            <Grid item xs={6} md={3}>
              <InteractionCard icon={<ThumbDown  />} title="Dislikes" value={movieData.interactions.dislikes} color="red" />
            </Grid>
            <Grid item xs={6} md={3}>
              <InteractionCard icon={<Favorite />} title="Favorites" value={movieData.interactions.favorites} color="purple" />
            </Grid>
            <Grid item xs={6} md={3}>
              <InteractionCard icon={<Movie />} title="Watched" value={movieData.interactions.watched} color="blue" />
            </Grid>
          </Grid>
        )}
        {selectedTab === 3 && (
          <Grid container spacing={3} >
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Preferências de Gênero" />
                <CardContent>
                  {movieData.preferences && movieData.preferences.length > 0 ? (
                    <TableContainer component={Paper}>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>Gênero</TableCell>
                            <TableCell>Tipo de Preferência</TableCell>
                            <TableCell>user</TableCell>
                            <TableCell>Nº prioridade</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {movieData.preferences.map((pref, index) => (
                            <TableRow key={index}>
                              <TableCell>{pref.genre.name}</TableCell>
                              <TableCell>{pref.preference_type}</TableCell>
                              <TableCell>{pref.username}</TableCell>
                              <TableCell>{pref.priority}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  ) : (
                    <Typography color="textSecondary">Nenhuma preferência disponível</Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </Box>
    </Container>
  );
};
const MovieTableWithPagination: React.FC = () => {

  const [movies, setMovies] = useState<MovieList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1); // Página atual
  const [totalPages, setTotalPages] = useState(1); // Total de páginas retornado pelo backend

  useEffect(() => {
    const getMovies = async () => {
      try {
        setLoading(true);

        const { results, count } = await fetchMovies(page, 5); // Inclui parâmetros de página e gênero

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
  }, [page]);

  // Função para mudar a página
  const handleChangePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
    event?.preventDefault();
    setPage(newPage);
  };

  // Função para controlar o número de linhas por página
  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    event.stopPropagation();
    setPage(0); // Resetar para a primeira página ao mudar o número de linhas por página
  };



  return (
    <Container>
      <CardHeader title="Top Movies" />
      <CardContent>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Title</TableCell>
                <TableCell>Genre</TableCell>
                <TableCell>Rating</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {error ? <Card>{error}</Card> : (loading ? <Card>carregando...</Card> : movies.map((movie) => (
                <TableRow key={movie.id}>
                  <TableCell>{movie.title}</TableCell>
                  <TableCell>{movie.genres.map((g) => g.name).join(', ')}</TableCell>
                  <TableCell>
                    {movie.rating && movie.rating.length > 0
                      ? (movie.rating.reduce((acc, r) => acc + r.rating, 0) / movie.rating.length).toFixed(1)
                      : 'No rating'}
                  </TableCell>
                  <TableCell>
                    <Button variant="outlined" size="small">
                      View Details
                    </Button>
                  </TableCell>
                </TableRow>
              )))}
            </TableBody>
          </Table>
        </TableContainer>

        {/* Paginação */}
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={totalPages}  // Total de filmes
          rowsPerPage={5}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </CardContent>
    </Container>
  );
};

export default MovieDashboard;
