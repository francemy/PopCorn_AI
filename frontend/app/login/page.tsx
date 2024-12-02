// app/login/page.tsx
"use client"
import React, { useState } from 'react';
import { TextField, Button, Typography } from '@mui/material';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      // Enviar a requisição de login para o backend Django
      const response = await axios.post('http://localhost:8000/api/token/', {
        username,
        password,
      });

      // console.log(response.data)
      const { access, refresh, user_id, username: loggedUsername, custom_data } = response.data.data;
      // Garantir valores válidos para os cookies
      const role = custom_data?.role || 'user'; // Valor padrão para role
      const last_login = custom_data?.last_login || new Date().toISOString(); // Substitui null por uma data padrão
      localStorage.setItem("access_token",access);
      // Armazenar os dados no localStorage
      const saveCookiesResponse = await axios.post('/api/session', {
        access_token: access,
        refresh_token: refresh,
        user_id,
        username: loggedUsername,
        role: role,
        last_login: last_login,
      });
      if (saveCookiesResponse.status === 200) {
        router.push('/');
      } else {
        setError('Erro ao salvar os dados da sessão.');
        console.error(saveCookiesResponse);
      }
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      if (err.response && err.response.status === 401) {
        setError('Credenciais inválidas! Tente novamente.');
      } else {
        setError('Erro no servidor. Tente novamente mais tarde.');
      }
      console.error('Erro ao realizar login:', err);
    }
  };

  const handleRegisterRedirect = () => {
    router.push('/register'); // Redireciona para a página de registro
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <TextField
              label="Username"
              variant="outlined"
              fullWidth
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mb-4"
            />
          </div>
          <div className="mb-6">
            <TextField
              label="Password"
              type="password"
              variant="outlined"
              fullWidth
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mb-4"
            />
          </div>

          {error && <div className="text-red-600 text-center mb-4">{error}</div>}

          <Button
            variant="contained"
            color="primary"
            type="submit"
            fullWidth
            className="mt-4"
          >
            Login
          </Button>
        </form>

        {/* Botão para ir para a página de registro */}
        <div className="mt-4 text-center">
          <Typography variant="body2">
            Não tem uma conta?{' '}
            <Button onClick={handleRegisterRedirect} color="primary">
              Registre-se
            </Button>
          </Typography>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;