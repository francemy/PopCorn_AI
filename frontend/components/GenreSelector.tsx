// components/GenreSelector.tsx
"use client"
import React, { useEffect, useState } from 'react';
import { FormControl, InputLabel, Select, MenuItem, CircularProgress, SelectChangeEvent } from '@mui/material';
import { Genre } from '@/types/types';

interface GenreSelectorProps {
  onChange: (genreId: number) => void;
  genreList: Genre[]
}

const GenreSelector: React.FC<GenreSelectorProps> = ({ onChange,genreList }) => {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedGenre, setSelectedGenre] = useState<number | string>('');  // Adicionando valor inicial vazio

  useEffect(() => {
      setGenres(genreList)
      setLoading(false)
    
  }, [genreList]);

  const handleChange = (event: SelectChangeEvent<string | number>) => {
    //console.log(event.target.value)
    const genreId = Number(event.target.value);
   // console.log(genreId)
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