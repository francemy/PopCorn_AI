// components/GenreSelector.tsx
"use client"
import React, { useEffect, useState } from 'react';
import { fetchGenres } from '../services/api';
import { FormControl, InputLabel, Select, MenuItem, CircularProgress, SelectChangeEvent } from '@mui/material';
import { Genre } from '@/types/types';

interface GenreSelectorProps {
  onChange: (genreId: number) => void;
}

const GenreSelector: React.FC<GenreSelectorProps> = ({ onChange }) => {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedGenre, setSelectedGenre] = useState<number | string>('');  // Adicionando valor inicial vazio

  useEffect(() => {
    const getGenres = async () => {
      try {
        const {data} = await fetchGenres();
        if (data) {
          setGenres(data);
          setLoading(false); // Ao finalizar o carregamento, defina 'loading' como false
        }
      } catch (error) {
        console.error('Erro ao buscar gêneros:', error);
        setLoading(false); // Finaliza o loading mesmo se houver erro
      }
    };

    getGenres();
  }, []);

  const handleChange = (event: SelectChangeEvent<string | number>) => {
    const genreId = Number(event.target.value);
    setSelectedGenre(genreId);  // Atualiza o estado local
    onChange(genreId);  // Chama a função onChange para passar o valor selecionado
  };

  if (loading) {
    return (
      <FormControl fullWidth>
        <InputLabel>Gênero</InputLabel>
        <Select value={selectedGenre} label="Gênero" disabled>
          <MenuItem value="">
            <CircularProgress size={24} />
          </MenuItem>
        </Select>
      </FormControl>
    );
  }

  return (
    <FormControl fullWidth>
      <InputLabel>Gênero</InputLabel>
      <Select value={selectedGenre} onChange={handleChange} label="Gênero">
        <MenuItem value="">
          <em>Selecione um gênero</em>
        </MenuItem>
        {genres.map((genre, index) => (
          <MenuItem key={genre.id || "genre-" + index} value={genre.id}>
            {genre.name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default GenreSelector;
