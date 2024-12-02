"use client"
import React from 'react';
import { Button } from '@mui/material';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const LogoutButton: React.FC = () => {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      // Enviar a requisição DELETE para a API de logout
      const response = await axios.delete('/api/session'); // Ajuste a URL de acordo com sua API
      console.log('Logout realizado com sucesso:', response.data);
      localStorage.removeItem("access_token")
      // Redirecionar o usuário para a página de login após o logout
      router.push('/login');
    } catch (error) {
      console.error('Erro ao realizar o logout', error);
    }
  };

  return (
    <Button
      variant="contained"
      color="secondary"
      onClick={handleLogout}
      fullWidth
      sx={{
        marginTop: 2, // margem superior
        padding: '10px 20px', // ajuste de padding
      }}
    >
      Logout
    </Button>
  );
};

export default LogoutButton;