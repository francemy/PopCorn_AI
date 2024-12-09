import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { NextRequest } from "next/server";
import api from "./services/api";
import axios from "axios";

// Função para verificar se o token de acesso é válido
async function isTokenValid(accessToken: string) {
  try {
    const res = await api.get('/verify-token/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return res.data.data.isValid;
  } catch (error) {
    console.error('Erro ao verificar o token:', error);
    return false;
  }
}

// Função para renovar o token de acesso usando o Refresh Token
async function renewAccessToken(refreshToken: string) {
  try {
    const res = await api.post('/token/refresh/', { refresh: refreshToken });
    return res.data.access;
  } catch (error) {
    console.error('Erro ao renovar o token de acesso:', error);
    return null;
  }
}

// Função que será chamada para todas as requisições
export async function middleware(req: NextRequest) {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;
  const refreshToken = cookieStore.get("refresh_token")?.value;

  const { pathname } = req.nextUrl;

  // Se já estiver autenticado e tentar acessar login ou registro, redireciona para a página inicial
  if (accessToken && (pathname === "/login" || pathname === "/register")) {
    return NextResponse.redirect(new URL("/", req.url));
  }

  // Verifica se o token de acesso está presente
  if (accessToken) {
    const tokenValid = await isTokenValid(accessToken);

    // Se o token não for válido e houver um refreshToken, tenta renová-lo
    if (!tokenValid && refreshToken) {
      const newAccessToken = await renewAccessToken(refreshToken);
      if (newAccessToken) {
        // Se renovação bem-sucedida, atualiza o cookie e continua a requisição
        const response = NextResponse.next();
        response.cookies.set("access_token", newAccessToken, {
          httpOnly: true,
          secure: process.env.NODE_ENV === 'production', // Garantir que seja seguro em produção
          sameSite: 'strict', // Alterado para minúsculas
          path: "/",
        });
        return response;
      }else 
       axios.delete(process.env.NEXT_PUBLIC_APP_URL+'api/session');
      return NextResponse.redirect(new URL("/login", req.url));
    }

    // Se o token ainda for inválido, redireciona para login
    if (!tokenValid) {
      axios.delete(process.env.NEXT_PUBLIC_APP_URL+'api/session');
      return NextResponse.redirect(new URL("/login", req.url));
    }
  }

  // Se não houver token de acesso e não for rota pública, redireciona para login
  if (!accessToken && !pathname.startsWith("/login") && !pathname.startsWith("/register")) {
    axios.delete(process.env.NEXT_PUBLIC_APP_URL+'api/session');
    return NextResponse.redirect(new URL("/login", req.url));
  }

  return NextResponse.next();
}

// Configuração do matcher para aplicar nas rotas
export const config = {
  matcher: ["/dashboard", "/profile", "/movies", "/login", "/register", "/"],
};
