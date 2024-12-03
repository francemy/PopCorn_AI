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
  TablePagination
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
import { 
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
  Favorite as FavoriteIcon,
  Movie as MovieIcon
} from '@mui/icons-material';

// Importação das tipagens
import { MovieList, Genre, Rating, UserInteractions } from '@/types/types';
import api from '@/services/api';

// Tipo da resposta do dashboard
interface MovieDashboardData {
  movies: MovieList[];
  genres: Genre[];
  ratings: { genre: string; avgRating: number }[];
  interactions: {
    likes: number;
    dislikes: number;
    favorites: number;
    watched: number;
  };
  genreDistribution: { name: string; value: number }[];
}

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
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));  // Responsividade

  useEffect(() => {
    const fetchMovieData = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await api.get(`/dashboard/`, {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          });
          console.log(response.data.data)
        setMovieData(response.data.data);
      } catch (err) {
        setError('Falha ao carregar os dados. Tente novamente mais tarde.');
        console.error(err);
      }
    };

    fetchMovieData();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

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
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Movie Dashboard
      </Typography>

      <Tabs 
        value={selectedTab} 
        onChange={handleTabChange} 
        aria-label="dashboard tabs"
        sx={{ mb: 3, borderBottom: 1, borderColor: 'divider' }}
      >
        <Tab label="Overview" />
        <Tab label="Movies" />
        <Tab label="Interactions" />
      </Tabs>

      {selectedTab === 0 && (
        <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader 
              title="Genre Distribution" 
              sx={{ fontWeight: 'bold', fontSize: '1.2rem', color: '#333' }} 
            />
            <CardContent>
              {movieData.genreDistribution.length > 0 ? (
                <PieChart width={isSmallScreen ? 350 : 500} height={350}>
                  <Pie
                    data={movieData.genreDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
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
            </CardContent>
          </Card>
        </Grid>
      
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader 
              title="Média das Avaliações por Gênero (Nota de 1 a 5)" 
              sx={{ fontWeight: 'bold', fontSize: '1.2rem', color: '#333' }} 
            />
            <CardContent>
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
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
            )}
      {selectedTab === 1 && (
       <MovieTableWithPagination movies={movieData.movies}/>
      
      )}

      {selectedTab === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={6} md={3}>
            <InteractionCard icon={<ThumbUpIcon />} title="Likes" value={movieData.interactions.likes} color="green" />
          </Grid>
          <Grid item xs={6} md={3}>
            <InteractionCard icon={<ThumbDownIcon />} title="Dislikes" value={movieData.interactions.dislikes} color="red" />
          </Grid>
          <Grid item xs={6} md={3}>
            <InteractionCard icon={<FavoriteIcon />} title="Favorites" value={movieData.interactions.favorites} color="purple" />
          </Grid>
          <Grid item xs={6} md={3}>
            <InteractionCard icon={<MovieIcon />} title="Watched" value={movieData.interactions.watched} color="blue" />
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

interface MovieTableWithPaginationProps {
    movies: MovieList[]; // Recebe a lista de filmes como prop
  }

const MovieTableWithPagination: React.FC<MovieTableWithPaginationProps> = ({ movies }) => {
    // Número de filmes por página
    const rowsPerPage = 5;
  
    // Estado da página atual
    const [page, setPage] = useState<number>(0);
  
    // Função para mudar a página
    const handleChangePage = (event: unknown, newPage: number) => {
      setPage(newPage);
    };
  
    // Função para controlar o número de linhas por página
    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
      setPage(0); // Resetar para a primeira página ao mudar o número de linhas por página
    };
  
    // Paginando os filmes
    const paginatedMovies:MovieList[] = movies.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  
    return (
      <Card>
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
                {paginatedMovies.map((movie) => (
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
                ))}
              </TableBody>
            </Table>
          </TableContainer>
  
          {/* Paginação */}
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={movies.length}  // Total de filmes
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </CardContent>
      </Card>
    );
  };

export default MovieDashboard;
