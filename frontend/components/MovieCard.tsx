// components/MovieCard.tsx
"use client"
import React from 'react';
import { Card, CardContent, Typography, CardMedia, Button, Box } from '@mui/material';

interface Movie {
  id: number;
  title: string;
  description: string;
  image_url: string;
}

interface MovieCardProps {
  movie: Movie;
}

const MovieCard: React.FC<MovieCardProps> = ({ movie }) => {
  return (
    <Card sx={{ maxWidth: 345, marginBottom: 2 }}>
      <CardMedia
        component="img"
        alt={movie.title}
        height="200"
        image={movie.image_url || 'https://via.placeholder.com/200'}
        sx={{ objectFit: 'cover' }}
      />
      <CardContent>
        <Typography variant="h6" component="div" noWrap>
          {movie.title}
        </Typography>
        <Typography variant="body2" color="textSecondary" paragraph>
          {movie.description || 'Descrição não disponível.'}
        </Typography>
        <Box display="flex" justifyContent="flex-end">
          <Button variant="contained" color="primary" size="small">
            Assistir
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MovieCard;
