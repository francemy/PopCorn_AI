# **PopCorn AI** 🎥🍿

**PopCorn AI** é uma plataforma de recomendação de filmes que oferece sugestões personalizadas com base nas preferências dos usuários. Utilizando algoritmos avançados de recomendação, a aplicação analisa dados de avaliação e preferências para criar uma experiência única para cada usuário.

---

## 📖 **Descrição do Projeto**

PopCorn AI conecta usuários a filmes relevantes, utilizando informações detalhadas armazenadas em uma base de dados estruturada.  
O sistema é construído com **Django** no backend e pode ser expandido para integrar algoritmos de machine learning no futuro.

---

## 🏛 **Modelos da Base de Dados**

### 1. **User (Usuário)**
- **Descrição:** Contém informações sobre os usuários da plataforma.  
- **Campos principais:**
  - `username` (String): Nome de usuário único.
  - `email` (String): Endereço de e-mail.
  - `password` (String): Senha criptografada.
  - `first_name` (String): Nome do usuário.
  - `last_name` (String): Sobrenome do usuário.

**Baseado no modelo `AbstractUser` do Django**, permitindo personalizações adicionais conforme necessário.

---

### 2. **Genre (Gênero)**
- **Descrição:** Representa os gêneros de filmes disponíveis na plataforma, como "Ação", "Comédia" e "Drama".  
- **Campos principais:**
  - `name` (String): Nome do gênero (único).
  - `description` (String): Descrição do gênero (opcional).

Relacionamento:
- **Muitos para Muitos** com o modelo **Movie**: Um gênero pode estar associado a vários filmes, e um filme pode pertencer a vários gêneros.

---

### 3. **Movie (Filme)**
- **Descrição:** Armazena informações sobre os filmes disponíveis na plataforma.  
- **Campos principais:**
  - `title` (String): Título do filme.
  - `description` (Text): Descrição do filme.
  - `release_date` (Date): Data de lançamento.
  - `duration` (Integer): Duração em minutos.
  - `image_url` (URL): Link da imagem do filme (opcional).

Relacionamento:
- **Muitos para Muitos** com o modelo **Genre**.

---

### 4. **Rating (Avaliação)**
- **Descrição:** Contém as avaliações feitas pelos usuários sobre os filmes.  
- **Campos principais:**
  - `user` (ForeignKey): Relaciona o usuário que avaliou.
  - `movie` (ForeignKey): Relaciona o filme avaliado.
  - `rating` (Float): Nota (escala de 1.0 a 5.0).
  - `review` (Text): Comentário opcional.
  - `created_at` (DateTime): Data e hora da avaliação.

**Restrições:**  
Um usuário pode avaliar cada filme apenas uma vez, utilizando a restrição **`unique_together`** para os campos `user` e `movie`.

---

### 5. **Preference (Preferência)**
- **Descrição:** Representa as preferências de gênero de um usuário.  
- **Campos principais:**
  - `user` (ForeignKey): Relaciona o usuário.
  - `genre` (ForeignKey): Relaciona o gênero.
  - `preference_type` (String): Tipo de preferência (`favorito` ou `evitar`).

---

## 🔗 **Relacionamentos entre Modelos**

- **User ↔ Rating ↔ Movie:**  
  Usuários avaliam filmes, com notas e comentários.

- **Movie ↔ Genre:**  
  Filmes pertencem a um ou mais gêneros.

- **User ↔ Preference ↔ Genre:**  
  Usuários definem seus gêneros favoritos ou evitados.

---

## 🚀 **Funcionalidades Planejadas**

1. **Recomendações Personalizadas:**
   - Baseadas em avaliações de filmes.
   - Consideram preferências definidas pelo usuário.

2. **Busca e Filtros:**
   - Busca por título.
   - Filtragem por gênero, data de lançamento e duração.

3. **Interface Intuitiva:**
   - Exibição de filmes com capas, descrições e trailers.

4. **Sistema de Avaliações:**
   - Usuários podem classificar filmes e escrever resenhas.

---

## 🛠️ **Tecnologias Utilizadas**

- **Backend:**
  - Python 3.x
  - Django 4.x
  - Django REST Framework
  - SQLite (pode ser migrado para PostgreSQL)

- **Frontend (planejado):**
  - React.js ou Next.js
  - Tailwind CSS ou Material-UI

---

## 📚 **Como Rodar o Projeto**

### Backend
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/francemy/PopCorn_AI.git
   cd popcorn-ai/backend
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realize as migrações:**
   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor:**
   ```bash
   python manage.py runserver
   ```

---

## 🏛 **Estrutura do Projeto**

### **Frontend (Next.js)**

#### 📋 **Descrição**
O frontend da plataforma foi desenvolvido utilizando **Next.js**, um framework de React que permite renderização server-side e oferece otimização de desempenho para aplicações web modernas. A interface foi projetada para ser responsiva e intuitiva, proporcionando uma experiência de usuário agradável.

#### 🌟 **Funcionalidades**
1. **Página Inicial:**
   - Exibe os filmes mais populares e recomendados.
   - Layout dinâmico com imagens e descrições chamativas.

2. **Sistema de Login e Registro:**
   - Autenticação de usuários via integração com o backend.
   - Suporte a validação de formulários com mensagens de erro claras.

3. **Recomendações Personalizadas:**
   - Interface interativa para exibir filmes recomendados.
   - Filtros para explorar filmes por gêneros e preferências.

4. **Sistema de Avaliação:**
   - Usuários podem avaliar filmes diretamente na interface.
   - Exibição de médias de avaliação e resenhas de outros usuários.

5. **Configurações do Usuário:**
   - Permite gerenciar preferências de gênero (favoritos/evitados).
   - Atualização de dados pessoais.

---

#### 🛠️ **Tecnologias do Frontend**
- **Next.js:** Framework React para renderização otimizada.
- **Axios:** Comunicação com o backend Django via API.
- **Tailwind CSS:** Biblioteca CSS para estilização responsiva.
- **material-ui:** biblioteca de componentes feitos e responsivos.
- **React Hook Form:** Gerenciamento de formulários eficiente.

#### Passos:
1. Navegue até a pasta `frontend`:
   ```bash
   cd ../frontend
   ```

2. Instale as dependências:
   ```bash
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

4. Acesse a aplicação:
   - URL: `http://localhost:3000`

---

## 🔗 **Estrutura de Pastas**

```plaintext
PopCorn AI
├── backend/        # Código do backend em Django
│   ├── manage.py
│   ├── db.sqlite3
│   ├── popcorn_ai/  # Configurações do projeto Django
│   └── app/         # Aplicação principal
├── frontend/       # Código do frontend em Next.js
│   ├── app/       # Páginas da aplicação
│   ├── components/  # Componentes reutilizáveis
│   ├── services/      # Arquivos de estilo
│   └── public/      # Imagens e arquivos estáticos
└── README.md        # Documentação do projeto

PopCorn_AI/
├── backend/
│   ├── api/
│   │   ├── migrations/
│   │   └── __pycache__/
│   ├── backend/
│   │   └── __pycache__/
│   ├── staticfiles/
│   │   ├── admin/
│   │   │   ├── css/
│   │   │   ├── img/
│   │   │   └── js/
│   │   └── rest_framework/
│   ├── templates/
│   └── venv/
├── frontend/
│   ├── .next/
│   ├── app/
│   ├── components/
│   ├── node_modules/
│   ├── public/
│   ├── services/
│   ├── types/
│   ├── .dockerignore
│   ├── .eslintrc.json
│   ├── Dockerfile
│   ├── middleware

.js
│   ├── next.config.js
│   └── package.json
└── README.md
```

---

## 🛠️ **Comando Seed**

O comando `seed` é utilizado para popular o banco de dados com dados iniciais ou de teste, facilitando o desenvolvimento e a realização de testes com dados realistas. Esse comando é útil para inserir informações como gêneros de filmes ou outros dados essenciais para a aplicação.

### Como Utilizar o Comando Seed

1. **Instalar as dependências**:
   Certifique-se de que todas as dependências estão instaladas:

   ```bash
   pip install -r requirements.txt
   ```

2. **Rodar o Seed**:
   Para popular o banco de dados com dados iniciais (como gêneros de filmes), execute:

   ```bash
   python manage.py seed
   ```

   Este comando irá:
   - Inserir os gêneros de filmes predefinidos no banco de dados, caso ainda não existam.
   - Ignorar os registros que já existem, evitando duplicações.

### Personalizando o Comando Seed

Para adicionar ou modificar os dados a serem populados, edite o arquivo `seed.py` localizado em `backend/api/management/commands/seed.py`.

---

## 📄 **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 👤 **Autor**

- **Francemy Eduardo Sebastião**  
  Desenvolvedor Full Stack | Angola  
  🌍 Luanda, Angola  

Sinta-se à vontade para contribuir ou relatar problemas!
```

Agora, o `README.md` está ajustado, com a explicação sobre o comando `seed` incorporada corretamente, sem mudar a estrutura original.
