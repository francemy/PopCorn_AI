# **PopCorn AI** 🎥🍿

**PopCorn AI** é uma plataforma de recomendação de filmes que oferece sugestões personalizadas com base nas preferências dos usuários. Utilizando algoritmos avançados de recomendação, a aplicação analisa dados de avaliação e preferências para criar uma experiência única para cada usuário.

---

## 📖 **Descrição do Projeto**

PopCorn AI conecta usuários a filmes relevantes, utilizando informações detalhadas armazenadas em uma base de dados estruturada.  
O sistema é construído com **Django** no backend e pode ser expandido para integrar algoritmos de machine learning no futuro.

---

Claro! Aqui está uma explicação sobre os **agentes baseados em aprendizado** para o seu `README.md`:

---

## Agentes Baseados em Aprendizado de Máquina para Recomendação Personalizada

No nosso projeto, implementamos agentes inteligentes para gerar recomendações de filmes personalizadas para os usuários, com base em suas preferências e interações. Esses agentes utilizam técnicas de aprendizado de máquina (ML) para melhorar a experiência do usuário, adaptando as sugestões ao longo do tempo.

### Como Funciona?

O sistema de recomendação é projetado para aprender e sugerir filmes de forma personalizada para cada usuário, levando em consideração os seguintes fatores:

#### 1. **Recomendação Baseada em Preferências de Gênero**
O agente usa as preferências de gênero do usuário para sugerir filmes. Essas preferências são baseadas em ações explícitas dos usuários, como "curtir" ou "avaliar positivamente" filmes de certos gêneros, ou em suas interações implícitas (como o tempo gasto assistindo a filmes de um gênero específico).

- **Gêneros Favoritos**: O agente identifica os gêneros mais frequentemente escolhidos e os utiliza como base para sugerir filmes.
- **Gêneros Secundários**: Além dos gêneros favoritos, o agente também considera outros gêneros que o usuário já interagiu positivamente, mas de forma secundária.

#### 2. **Exclusão de Filmes Irrelevantes**
O agente exclui filmes que o usuário já assistiu ou avaliou negativamente. Isso é feito monitorando:
- Filmes assistidos
- Filmes avaliados com "dislike"

Dessa forma, as sugestões se concentram apenas em filmes novos que o usuário ainda não viu e que têm alta probabilidade de agradá-lo.

#### 3. **Ajuste Dinâmico com Feedback**
O agente aprende ao longo do tempo com o feedback do usuário. Sempre que o usuário interage com um filme (por exemplo, avaliando com "like", "dislike" ou uma classificação), o sistema ajusta as recomendações futuras:
- **Feedback Positivo**: Filmes que o usuário gostou (por exemplo, ao marcar como favorito) aumentam a relevância de um determinado gênero ou tipo de filme nas sugestões.
- **Feedback Negativo**: Filmes que o usuário não gostou (por exemplo, ao marcar como "dislike") são removidos das recomendações futuras e ajustam a prioridade de outros gêneros ou tipos de filmes.

#### 4. **Algoritmos de Recomendação**
Para gerar as recomendações personalizadas, o sistema utiliza diferentes abordagens de aprendizado de máquina, como:
- **Filtragem Colaborativa**: O agente recomenda filmes que usuários semelhantes gostaram, com base em interações passadas.
- **Filtragem Baseada em Conteúdo**: A recomendação é feita com base nos atributos dos filmes, como gênero, descrição e características específicas.
- **Modelos Híbridos**: Uma combinação de filtragem colaborativa e baseada em conteúdo, para melhorar a precisão das sugestões.

#### 5. **Processo de Aprendizado**
O agente pode usar dois tipos de aprendizado:
- **Aprendizado Supervisionado**: O agente aprende a partir de dados rotulados, como interações passadas dos usuários (ex: filmes que foram avaliados positivamente ou negativamente).
- **Aprendizado por Reforço**: O agente ajusta suas recomendações com base no feedback contínuo dos usuários, melhorando as sugestões com o tempo.

### Exemplo de Funcionamento

1. O usuário começa a interagir com filmes e faz avaliações de "like", "dislike" ou "rating".
2. O agente usa essas interações para atualizar as preferências do usuário e aprender os gêneros e filmes preferidos.
3. O sistema sugere filmes baseados nos gêneros favoritos do usuário e exclui filmes que já foram assistidos ou avaliados negativamente.
4. Cada nova interação do usuário com os filmes ajusta a recomendação, para que o sistema sempre forneça sugestões mais alinhadas com os gostos do usuário.

### Benefícios
- **Recomendações Personalizadas**: Filmes são sugeridos com base nos interesses específicos de cada usuário.
- **Adaptação ao Longo do Tempo**: O sistema aprende continuamente com o feedback dos usuários, garantindo que as sugestões sejam sempre relevantes.
- **Experiência de Usuário Aprimorada**: O agente ajusta suas recomendações para fornecer uma experiência mais precisa e satisfatória, aumentando a probabilidade de o usuário encontrar filmes que realmente goste
O agente utilizado nesse código é um **Agente Utilitário**. 

### Por que é um Agente Utilitário?

1. **Otimizando Resultados:**  
   O algoritmo busca recomendações que maximizem a "satisfação" do usuário, calculando uma pontuação para cada filme com base em preferências (como gêneros favoritos) e interações passadas (como likes e dislikes).  

2. **Consideração de Preferências:**  
   Ele dá mais peso aos gêneros favoritos do usuário, ajusta a pontuação de filmes conforme prioridades, e leva em conta feedback explícito (ex.: likes e dislikes).  

3. **Exclusão de Opções Relevantes:**  
   Ao excluir filmes já assistidos ou avaliados negativamente, o agente está agindo para melhorar a utilidade percebida das recomendações, evitando redundâncias ou sugestões indesejadas.

4. **Cálculo de Utilidade:**  
   A função `calculate_movie_score` é claramente um modelo de cálculo de utilidade, somando pesos baseados em interações e preferências para otimizar o resultado final.

### Resumo:  
O comportamento desse agente é projetado para encontrar e recomendar os filmes que oferecem o maior valor para o usuário, dado o histórico de interações e as preferências registradas, características típicas de um **Agente Utilitário**.

### Como Usar

- **Endpoints da API**:
  - `/api/movies/recomendado/`: Endpoint que gera as recomendações personalizadas de filmes com base nas preferências do usuário.
  - **Feedback**: Ao avaliar ou interagir com filmes (curtindo, assistindo ou avaliando), o agente de aprendizado ajusta as futuras recomendações automaticamente.

---

Esta seção do README descreve como os agentes baseados em aprendizado funcionam no seu projeto, garantindo que os usuários tenham uma experiência de recomendação mais inteligente e personalizada.


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

<<<<<<< HEAD
Se você precisar adicionar ou modificar os dados a serem populados, basta editar o arquivo de comando `seed.py`, localizado em `backend/api/management/commands/seed.py`. Você pode adicionar novos itens na lista de gêneros ou qualquer outro tipo de dado relevante para a aplicação.

#### Exemplo de dados:

```python
def seed_genres(self):
    genres = [
        ("Ação", "Filmes com cenas de grande energia e movimento, como perseguições e batalhas."),
        ("Comédia", "Filmes feitos para provocar risadas e entretenimento leve."),
        ("Drama", "Filmes que exploram emoções e situações intensas."),
        # Adicione mais gêneros aqui...
    ]
    
    for genre_name, description in genres:
        slug = slugify(genre_name)
        genre, created = Genre.objects.get_or_create(
            slug=slug, 
            defaults={'name': genre_name, 'description': description}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Gênero {genre_name} criado com sucesso!"))
        else:
            self.stdout.write(self.style.WARNING(f"Gênero {genre_name} já existe."))
```
## API Documentation

### Overview

Esta API oferece funcionalidades para gerenciar filmes, preferências de gêneros, avaliações e recomendações personalizadas para os usuários. A API permite que os usuários registrem-se, avaliem filmes, interajam com eles e recebam recomendações personalizadas com base em seus gostos e histórico.

### Endpoints da API

1. **`POST /api/register/`**  
   **Descrição**: Registra um novo usuário na plataforma.  
   **Request Body**:
   ```json
   {
       "username": "example",
       "email": "user@example.com",
       "password": "password123"
   }
   ```
   **Response**:
   - `201 Created`: Usuário criado com sucesso.
   - `400 Bad Request`: Erro nos dados fornecidos.

---

2. **`POST /api/token/`**  
   **Descrição**: Obtém o token JWT após fornecer as credenciais do usuário.  
   **Request Body**:
   ```json
   {
       "username": "example",
       "password": "password123"
   }
   ```
   **Response**:
   ```json
   {
       "access": "jwt-access-token",
       "refresh": "jwt-refresh-token"
   }
   ```

---

3. **`POST /api/token/refresh/`**  
   **Descrição**: Obtém um novo token de acesso utilizando o refresh token.  
   **Request Body**:
   ```json
   {
       "refresh": "jwt-refresh-token"
   }
   ```
   **Response**:
   ```json
   {
       "access": "new-jwt-access-token"
   }
   ```

---

4. **`POST /api/preferences/`**  
   **Descrição**: Cria ou atualiza preferências de gênero para o usuário autenticado.  
   **Request Body**:
   ```json
   {
       "genre": 1,  // ID do gênero
       "preference_type": "favorite",  // "favorite" ou "avoid"
       "priority": 5  // Prioridade do gênero (1 a 5)
   }
   ```
   **Response**:
   - `201 Created`: Preferência criada com sucesso.
   - `400 Bad Request`: Erro nos dados fornecidos.

---

5. **`GET /api/preferences/list/`**  
   **Descrição**: Lista as preferências de gênero do usuário autenticado.  
   **Response**:
   ```json
   [
       {
           "genre": 1,
           "preference_type": "favorite",
           "priority": 5
       },
       {
           "genre": 2,
           "preference_type": "avoid",
           "priority": 1
       }
   ]
   ```

---

6. **`GET /api/movies/recomendado/`**  
   **Descrição**: Gera recomendações personalizadas de filmes com base nas preferências de gênero do usuário.  
   **Response**:
   ```json
   [
       {
           "id": 1,
           "title": "Movie Title",
           "description": "Movie Description",
           "release_date": "2024-12-01",
           "duration": "120 min",
           "image_url": "http://example.com/image.jpg",
           "score": 8.5,
           "user_interactions": {
               "liked": true,
               "disliked": false
           }
       },
       ...
   ]
   ```

---

7. **`POST /api/ratings/create/`**  
   **Descrição**: Cria ou atualiza uma avaliação para um filme pelo usuário autenticado.  
   **Request Body**:
   ```json
   {
       "movie": 1,  // ID do filme
       "rating": 4  // Avaliação (1 a 5)
   }
   ```
   **Response**:
   - `201 Created`: Avaliação criada com sucesso.
   - `200 OK`: Avaliação atualizada com sucesso.
   - `400 Bad Request`: Erro nos dados fornecidos.

---

8. **`GET /api/genres/`**  
   **Descrição**: Lista todos os gêneros disponíveis.  
   **Response**:
   ```json
   [
       {
           "id": 1,
           "name": "Action"
       },
       {
           "id": 2,
           "name": "Drama"
       },
       ...
   ]
   ```

---

9. **`GET /api/dashboard/`**  
   **Descrição**: Retorna um resumo do estado do usuário, como filmes assistidos, avaliações, etc.  
   **Response**:
   ```json
   {
       "watched_movies_count": 10,
       "liked_movies_count": 5,
       "disliked_movies_count": 2
   }
   ```

---

10. **`GET /swagger/`**  
    **Descrição**: Exibe a documentação interativa da API utilizando o Swagger UI.  
    **Acesso**: Navegue até `/swagger/` para visualizar a documentação.

---

11. **`GET /redoc/`**  
    **Descrição**: Exibe a documentação da API utilizando o Redoc UI.  
    **Acesso**: Navegue até `/redoc/` para visualizar a documentação.

---

### Como Usar

1. **Autenticação**: Para acessar a maioria dos endpoints da API, você precisará de um token JWT. Primeiro, registre-se no endpoint `/api/register/` e depois obtenha o token de acesso através de `/api/token/`.
2. **Token JWT**: Inclua o token JWT nos headers de autenticação de todas as requisições subsequentes, usando o formato:
   ```text
   Authorization: Bearer <token_jwt>
   ```
3. **Swagger e Redoc**: Para visualizar a documentação interativa da API, acesse `/swagger/` ou `/redoc/` no navegador.

---

### Respostas da API

- **200 OK**: A requisição foi bem-sucedida.
- **201 Created**: O recurso foi criado com sucesso.
- **400 Bad Request**: A requisição contém erros, como dados inválidos.
- **404 Not Found**: O recurso não foi encontrado.
- **401 Unauthorized**: O usuário não está autenticado ou o token é inválido.

--- 

### Como Funciona o `get_or_create`

O método `get_or_create` tenta buscar um registro no banco de dados baseado no parâmetro fornecido (neste caso, `slug`). Se o registro já existir, ele retorna o objeto existente; caso contrário, cria um novo.
=======
Para adicionar ou modificar os dados a serem populados, edite o arquivo `seed.py` localizado em `backend/api/management/commands/seed.py`.
>>>>>>> 75c00042b761ce01cb2a088c48567e846b851ee1

---

## 📄 **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 👤 **Autor**

- **Francemy Eduardo Sebastião**  
  Desenvolvedor Full Stack | Angola  
  🌍 Luanda, Angola 

- **Nome:** Francemy Eduardo Sebastião
- **Contato:** [francemysebastiaofrancemy@gmail.com](mailto:gelson23tg@gmail.com)
- **GitHub:** ([https://github.com/seuusuario](https://github.com/francemy))
Sinta-se à vontade para contribuir ou relatar problemas!
```
