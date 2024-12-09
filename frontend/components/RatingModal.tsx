import React, { useState } from 'react';
import { Modal, Box, Button, TextField, Typography } from '@mui/material';
import { Rating as MuiRating } from '@mui/lab';
import { useSnackbar } from 'notistack';
import api from '@/services/api';

interface RatingModalProps {
  open: boolean;
  onClose: () => void;
  id_movie: number; // ID do filme passado como parâmetro
}

const RatingModal: React.FC<RatingModalProps> = ({ open, onClose, id_movie }) => {
  const [ratingValue, setRatingValue] = useState<number>(2.5);  // Valor inicial de 2.5 para o rating
  const [review, setReview] = useState<string>('');  // Review inicial
  const { enqueueSnackbar } = useSnackbar();  // Para exibir notificações de feedback
  
  const handleSubmit = async () => {
    if (!review || ratingValue === 0) {
      enqueueSnackbar('Avaliação e comentário são obrigatórios!', { variant: 'error' });
      return;
    }

    const data = {
      movie: id_movie,  // ID do filme sendo avaliado
      rating: ratingValue,
      review: review,
      created_at: new Date().toISOString(), // Data e hora da avaliação
    };

    try {
      const token = localStorage.getItem("access_token");

      // Envia a requisição para o backend
      const response = await api.post('/ratings/create/', data, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // Passando o token de autenticação
        },
      });

      if (response.status === 200 || response.status === 201) {
        enqueueSnackbar('Avaliação salva com sucesso!', { variant: 'success' });
        onClose();  // Fecha a modal
      } else {
        const errorData = await response.data;
        enqueueSnackbar(errorData.message || 'Erro ao salvar avaliação', { variant: 'error' });
      }
    } catch (error) {
      enqueueSnackbar('Erro de rede. Tente novamente mais tarde.'+error, { variant: 'error' });
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box className="modal-container">
        <div className="bg-white p-8 rounded-lg w-full max-w-sm mx-auto shadow-lg">
          <Typography variant="h6" className="text-xl mb-4">Avalie o Filme</Typography>

          <div className="mb-4">
            <MuiRating
              value={ratingValue}
              onChange={(event, newValue) => setRatingValue(newValue as number)}
              size="large"
            />
          </div>

          <TextField
            label="Comentário"
            multiline
            rows={4}
            variant="outlined"
            fullWidth
            value={review}
            onChange={(e) => setReview(e.target.value)}
            className="mb-4"
          />

          <div className="flex justify-between mt-4">
            <Button onClick={onClose} variant="outlined" color="secondary">Cancelar</Button>
            <Button onClick={handleSubmit} variant="contained" color="primary">Salvar</Button>
          </div>
        </div>
      </Box>
    </Modal>
  );
};

export default RatingModal;
