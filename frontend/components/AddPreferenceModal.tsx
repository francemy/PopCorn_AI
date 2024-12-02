import { useState } from "react";
import axios from "axios";
import {
  Modal,
  Box,
  TextField,
  Button,
  Typography,
  Grid,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";
import { Genre } from "@/types/types";

interface AddPreferenceModalProps {
  open: boolean;
  onClose: () => void;
  genres: Genre[];
}

const AddPreferenceModal: React.FC<AddPreferenceModalProps> = ({
  open,
  onClose,
  genres,
}) => {
  const [selectedGenre, setSelectedGenre] = useState<number | "">("");
  const [preferenceType, setPreferenceType] = useState<string>("favorite");
  const [priority, setPriority] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Função para validar os campos do formulário
  const validateForm = (): boolean => {
    if (!selectedGenre || !preferenceType || !priority) {
      setError("Todos os campos são obrigatórios.");
      return false;
    }
    setError(null);
    return true;
  };

  // Função para limpar o estado após sucesso
  const resetForm = () => {
    setSelectedGenre("");
    setPreferenceType("favorite");
    setPriority(1);
    setError(null);
  };

  // Função para enviar os dados
  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setError("Token de autenticação não encontrado.");
        setLoading(false);
        return;
      }

      await axios.post(
        "http://localhost:8000/api/preferences/",
        {
          genre: selectedGenre,
          preference_type: preferenceType,
          priority,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      resetForm(); // Limpa o formulário após o envio
      onClose(); // Fecha o modal
    } catch (err: unknown) {
      const errorMessage =
        axios.isAxiosError(err) && err.response?.data?.detail
          ? err.response.data.detail
          : "Erro ao adicionar a preferência.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: "90%",
          maxWidth: 400,
          bgcolor: "background.paper",
          borderRadius: 1,
          boxShadow: 24,
          p: 4,
        }}
      >
        <Typography variant="h6" mb={2}>
          Adicionar Preferência
        </Typography>

        {error && (
          <Typography color="error" variant="body2" mb={2}>
            {error}
          </Typography>
        )}

        {/* Dropdown para seleção de gênero */}
        <FormControl fullWidth margin="normal">
          <InputLabel id="genre-select-label">Gênero</InputLabel>
          <Select
            labelId="genre-select-label"
            value={selectedGenre}
            onChange={(e) => setSelectedGenre(Number(e.target.value))}
          >
            {genres.map((genre) => (
              <MenuItem key={genre.id} value={genre.id}>
                {genre.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Campo para tipo de preferência */}
        <FormControl fullWidth margin="normal">
          <InputLabel id="preference-type-label">Tipo de Preferência</InputLabel>
          <Select
            labelId="preference-type-label"
            value={preferenceType}
            onChange={(e) => setPreferenceType(e.target.value)}
          >
            <MenuItem value="favorite">Favorito</MenuItem>
            <MenuItem value="avoid">Evitar</MenuItem>
          </Select>
        </FormControl>

        {/* Campo para prioridade */}
        <TextField
          label="Prioridade"
          type="number"
          variant="outlined"
          fullWidth
          value={priority}
          onChange={(e) => setPriority(Number(e.target.value))}
          margin="normal"
          inputProps={{ min: 1, max: 5 }}
        />

        <Grid container spacing={2} mt={2}>
          <Grid item xs={6}>
            <Button fullWidth onClick={onClose} color="secondary">
              Cancelar
            </Button>
          </Grid>
          <Grid item xs={6}>
            <Button
              fullWidth
              onClick={handleSubmit}
              variant="contained"
              color="primary"
              disabled={loading}
            >
              {loading ? "Carregando..." : "Salvar"}
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Modal>
  );
};

export default AddPreferenceModal;
