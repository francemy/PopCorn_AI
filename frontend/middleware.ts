// middleware.ts (ou middleware.js, dependendo do seu projeto)
import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { NextRequest } from "next/server";

// Função que será chamada para todas as requisições
export async function middleware(req: NextRequest) {
  // Verificar se o token de autenticação está presente no cookie
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token");
  // Se o token não existir, redirecionar para a página de login
  if (!accessToken) {
    return NextResponse.redirect(new URL("/login", req.url)); // Página de login
  }

  // Se o token existir, prosseguir com a requisição
  return NextResponse.next();
}

// Configuração do matcher para aplicar nas rotas que precisam de autenticação
export const config = {
  matcher: ["/dashboard", "/profile", "/movies", "/"], // Aplique apenas nessas rotas
};
