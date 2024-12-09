import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Habilita o modo estrito do React
  reactStrictMode: true,

  // Habilita a compactação para melhorar o desempenho
  compress: true,


  // Configurações para reescritas de API (opcional)
  async rewrites() {
    return [
      {
        source: "/api/:path*", // Rota do Next.js
        destination: `${
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/"
        }/:path*`, // API Backend, com fallback
      },
    ];
  },

   // Headers de segurança com CSP ajustada
   async headers() {
    return [
      {
        source: "/(.*)", // Aplica a todos os caminhos
        headers: [
          {
            key: "Content-Security-Policy",
            value: `
              default-src 'self';
              script-src 'self' 'unsafe-inline';
              style-src 'self' 'unsafe-inline';
              img-src 'self' data: https:;
              connect-src 'self' http://localhost:8000;
            `.replace(/\s{2,}/g, " ").trim(),
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
        ],
      },
    ];
  },


  // Configuração de otimização de imagens
  images: {
    domains: ["localhost"], // Permitir domínios para carregar imagens
    formats: ["image/avif", "image/webp"],
  },
};

export default nextConfig;
