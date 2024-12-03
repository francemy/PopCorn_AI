import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { NextRequest } from "next/server";
import api from "./services/api";

// Função para verificar se o token de acesso é válido
async function isTokenValid(accessToken: string) {
  try {
    const res = await api.get('/verify-token/', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    // Supondo que o backend retorne { data: { isValid: true/false } }
    return res.data.data.isValid;
  } catch (error) {
    return false;
  }
}

// Função para renovar o token de acesso usando o Refresh Token
async function renewAccessToken(refreshToken: string) {
  try {
    const res = await api.post('/token/refresh/', { refresh: refreshToken });
    // Supondo que o backend retorne { access: "novoAccessToken" }
    return res.data.access;
  } catch (error) {
    return null; // Falha na renovação
  }
}

// Função que será chamada para todas as requisições
export async function middleware(req: NextRequest) {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;
  const refreshToken = cookieStore.get("refresh_token")?.value;

  const { pathname } = req.nextUrl;

  // Roteamento específico para login e registro
  if (accessToken && (pathname === "/login" || pathname === "/register")) {
    return NextResponse.redirect(new URL("/", req.url));
  }

  // Se houver token de acesso, validar
  if (accessToken) {
    const tokenValid = await isTokenValid(accessToken);
    if (!tokenValid && refreshToken) {
      // Tentar renovar o token
      const newAccessToken = await renewAccessToken(refreshToken);
      if (newAccessToken) {
        // Atualiza o cookie com o novo token
        const response = NextResponse.next();
        response.cookies.set("access_token", newAccessToken, {
          httpOnly: true,
          secure: true,
          path: "/",
        });
        return response;
      }

      // Falha na renovação
      return NextResponse.redirect(new URL("/login", req.url));
    }

    if (!tokenValid) {
      return NextResponse.redirect(new URL("/login", req.url));
    }
  }

  // Sem token de acesso e não está em rota pública, redireciona para login
  if (!accessToken && !pathname.startsWith("/login") && !pathname.startsWith("/register")) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  return NextResponse.next();
}

// Configuração do matcher para aplicar nas rotas
export const config = {
  matcher: ["/dashboard", "/profile", "/movies", "/login", "/register", "/"],
};
