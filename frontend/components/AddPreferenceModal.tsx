import { useState } from "react";
import axios from "axios";
import { Modal, Box, TextField, Button, Typography, Grid } from "@mui/material";

interface AddPreferenceModalProps {
  open: boolean;
  onClose: () => void;
}


const AddPreferenceModal: React.FC<AddPreferenceModalProps> = ({
  open,
  onClose,
}) => {
  const [preferenceName, setPreferenceName] = useState<string>("");
  const [preferenceDescription, setPreferenceDescription] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Validação simples
  const validateForm = (): boolean => {
    if (!preferenceName || !preferenceDescription) {
      setError("Todos os campos são obrigatórios.");
      return false;
    }
    setError(null);
    return true;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      // Enviar para a API Django
         await axios.post(
        "http://localhost:8000/api/preferences/",
        {
          name: preferenceName,
          description: preferenceDescription,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setPreferenceName("");
      setPreferenceDescription("");
      onClose();
    } catch {
      setError("Erro ao adicionar a preferência.");
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

        <TextField
          label="Nome"
          variant="outlined"
          fullWidth
          value={preferenceName}
          onChange={(e) => setPreferenceName(e.target.value)}
          margin="normal"
        />
        <TextField
          label="Descrição"
          variant="outlined"
          fullWidth
          multiline
          rows={4}
          value={preferenceDescription}
          onChange={(e) => setPreferenceDescription(e.target.value)}
          margin="normal"
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
