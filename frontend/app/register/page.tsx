"use client"
import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const RegisterPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [preference, setPreference] = useState(''); // Novo estado para preferência
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Verificar se as senhas coincidem
    if (password !== confirmPassword) {
      setError('As senhas não coincidem');
      return;
    }

    setLoading(true);
    try {
      // Enviar a requisição de registro para o backend Django
      const response = await axios.post('http://localhost:8000/api/register/', {
        username,
        email,
        password,
        preference, // Enviar a preferência junto com os outros dados
      });

      // Se o registro for bem-sucedido, redirecionar para a página de login
      if (response.status === 201) {
        router.push('/login');
      }
    } catch {
      setError('Erro ao registrar. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Criar Conta</h2>
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
          <div className="mb-4">
            <TextField
              label="Email"
              type="email"
              variant="outlined"
              fullWidth
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mb-4"
            />
          </div>
          <div className="mb-4">
            <TextField
              label="Senha"
              type="password"
              variant="outlined"
              fullWidth
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mb-4"
            />
          </div>
          <div className="mb-6">
            <TextField
              label="Confirmar Senha"
              type="password"
              variant="outlined"
              fullWidth
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="mb-4"
            />
          </div>

          {/* Campo de Preferência */}
          <div className="mb-4">
            <TextField
              label="Preferência"
              variant="outlined"
              fullWidth
              value={preference}
              onChange={(e) => setPreference(e.target.value)}
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
            disabled={loading}
          >
            {loading ? 'Registrando...' : 'Registrar'}
          </Button>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;