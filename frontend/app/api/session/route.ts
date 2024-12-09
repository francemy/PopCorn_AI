//api/session/route.ts
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function POST(req: NextRequest) {
  try {
    // Pegando os dados enviados do frontend
    const data = await req.json();
    console.log("Dados recebidos:", data);
   // console.log("process.env.NODE_ENV: ",process.env.NODE_ENV)

    const { access_token, refresh_token, user_id, username, role, last_login } = data;

    // Verificar se os dados necessários estão presentes
    if (
      !access_token ||
      !refresh_token ||
      !user_id ||
      !username ||
      !role ||
      !last_login
    ) {
      return NextResponse.json(
        { message: "Dados incompletos! Verifique as informações enviadas." },
        { status: 400 }
      );
    }

    // Pegando a instância dos cookies
    const cookieStore = await cookies();

    if(cookieStore.get(access_token))
      return NextResponse.json(
        { message: "Dados já exite!" },
        { status: 400 }
      );

    // Salvando os cookies com segurança
    cookieStore.set("access_token", access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/",
    });
    cookieStore.set("refresh_token", refresh_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/",
    });
    cookieStore.set("user_id", String(user_id), {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/",
    });
    cookieStore.set("username", username, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/",
    });
    cookieStore.set("role", role, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/",
    });
    cookieStore.set("last_login", last_login, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/",
    });

    // Resposta de sucesso
    return NextResponse.json(
      { message: "Cookies salvos com sucesso!" },
      { status: 200 }
    );
  } catch (error) {
    // Tratamento de erro em caso de falhas inesperadas
    console.error("Erro ao salvar cookies:", error);
    return NextResponse.json(
      { message: "Erro ao salvar os cookies. Tente novamente." },
      { status: 500 }
    );
  }
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars

export async function DELETE() {
  // Pegando a instância dos cookies
  const cookieStore = await cookies();

  // Verifica se o token de acesso está presente antes de tentar excluir os cookies
  const accessToken = cookieStore.get("access_token");

  if (!accessToken) {
    // Se não houver o token, significa que o usuário já está deslogado
    return NextResponse.json(
      { message: "Usuário já está deslogado." },
      { status: 200 }
    );
  }

  // Remover os cookies de autenticação, caso existam
  try {
    cookieStore.delete("access_token");
    cookieStore.delete("refresh_token");
    cookieStore.delete("user_id");
    cookieStore.delete("username");
    cookieStore.delete("role");
    cookieStore.delete("last_login");

    // Retornar uma resposta indicando que o logout foi bem-sucedido
    return NextResponse.json(
      { message: "Logout realizado com sucesso!" },
      { status: 200 }
    );
  } catch (error) {
    // Caso ocorra algum erro ao remover os cookies
    console.error("Erro ao tentar realizar o logout:", error);
    return NextResponse.json(
      { message: "Erro ao realizar o logout. Tente novamente." },
      { status: 200 }
    );
  }
}
