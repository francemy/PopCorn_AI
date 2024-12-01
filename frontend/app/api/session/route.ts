//api/session/route.ts
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function POST(req: NextRequest) {
  // Pegando os dados enviados do frontend
  const data = await req.json();
  console.log("data:",data)
  const { access_token, refresh_token, user_id, username, role, last_login } =
    data;

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
      { message: "Dados incompletos!" },
      { status: 400 }
    );
  }

  // Pegando a instância dos cookies
  const cookieStore = await cookies(); // Remover o 'await' aqui

  // Salvando os cookies com segurança
  cookieStore.set("access_token", access_token, {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    path: "/",
  });
  cookieStore.set("refresh_token", refresh_token, {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    path: "/",
  });
  cookieStore.set("user_id", user_id.toString(), {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    path: "/",
  });
  cookieStore.set("username", username, {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    path: "/",
  });
  cookieStore.set("role", role, {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    path: "/",
  });
  cookieStore.set("last_login", last_login, {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    path: "/",
  });

  return NextResponse.json(
    { message: "Cookies salvos com sucesso!" },
    { status: 200 }
  );
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export async function DELETE(req: NextRequest) {
  // Pegando a instância dos cookies
  const cookieStore = await cookies();

  // Remover os cookies de autenticação
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
}
