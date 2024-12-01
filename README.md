```markdown
# **PopCorn AI** 🎥🍿

PopCorn AI é uma plataforma de recomendação de filmes desenvolvida para oferecer sugestões personalizadas com base nas preferências dos usuários. Utilizando algoritmos de recomendação, o sistema analisa dados de avaliação para criar uma experiência única para cada usuário.

---

## **Índice**
- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)

---

## **Visão Geral**
PopCorn AI combina ciência de dados, aprendizado de máquina e uma interface amigável para criar recomendações eficazes de filmes. Com um backend robusto em Flask, um frontend dinâmico em Vue.js e um banco de dados eficiente em PostgreSQL, o projeto visa atender a todos os públicos, desde cinéfilos casuais até entusiastas de tecnologia.

---

## **Tecnologias Utilizadas**
- **Backend**: Python (Flask)
- **Frontend**: Vue.js
- **Banco de Dados**: PostgreSQL
- **Manipulação de Dados**: pandas, scikit-learn
- **Containerização**: Docker e Docker Compose
- **Dataset**: Arquivos CSV estruturados

---

## **Instalação e Configuração**

### **Requisitos**
- Docker e Docker Compose instalados
- Python 3.9+ e Node.js 16+ (opcional para execução sem Docker)

### **Passos de Instalação**

#### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/PopCorn_AI.git
cd PopCorn_AI
```

#### 2. Configure o banco de dados
Certifique-se de que o PostgreSQL esteja rodando e execute o script `setup.sql`:
```bash
psql -U seu_usuario -f setup.sql
```

#### 3. Execute com Docker
```bash
docker-compose up --build
```

#### 4. Acesse o sistema
- **Frontend**: [http://localhost:8080](http://localhost:8080)
- **Backend**: [http://localhost:5000](http://localhost:5000)

---

## **Estrutura do Projeto**

```
PopCornAI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── recommender.py
│   │   └── utils.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── router.js
│   ├── package.json
│   └── Dockerfile
├── dataset/
│   ├── movies.csv
│   └── ratings.csv
├── docker-compose.yml
├── setup.sql
└── README.md
```

---

## **Funcionalidades**
1. **Recomendações Personalizadas**
   - Sugestões de filmes com base no histórico de avaliações dos usuários.
2. **Pesquisa de Filmes**
   - Busque por filmes específicos ou por gênero.
3. **Avaliação de Filmes**
   - Avalie filmes para melhorar as recomendações futuras.
4. **Classificação Dinâmica**
   - Listas de filmes mais populares baseadas em dados reais.

---

## **Como Contribuir**
1. Faça um fork do repositório.
2. Crie uma branch para sua funcionalidade:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça o commit das alterações:
   ```bash
   git commit -m "Descrição da minha feature"
   ```
4. Envie o pull request.

---

# PopCorn AI - Base de Dados

PopCorn AI é uma plataforma de recomendação de filmes desenvolvida para oferecer sugestões personalizadas com base nas preferências dos usuários. A base de dados do projeto armazena informações sobre usuários, filmes, gêneros, avaliações e preferências. Abaixo estão os detalhes da estrutura da base de dados.

## Modelos da Base de Dados

### 1. **User (Usuário)**
- **Descrição**: Armazena informações sobre os usuários da plataforma.
- **Campos principais**:
  - `username`: Nome de usuário (único).
  - `email`: Endereço de e-mail.
  - `password`: Senha de autenticação.
  - `first_name`: Nome do usuário.
  - `last_name`: Sobrenome do usuário.

O modelo de **Usuário** é baseado no modelo `AbstractUser` do Django, o que permite personalizar as informações do usuário conforme necessário.

### 2. **Genre (Gênero)**
- **Descrição**: Armazena os gêneros de filmes disponíveis na plataforma (por exemplo, "Ação", "Comédia", "Drama").
- **Campos principais**:
  - `name`: Nome do gênero (único).
  - `description`: Descrição do gênero (opcional).

A tabela **Genre** está relacionada com o modelo **Movie**, permitindo que cada filme tenha múltiplos gêneros e que cada gênero tenha vários filmes associados.

### 3. **Movie (Filme)**
- **Descrição**: Armazena informações sobre os filmes disponíveis na plataforma.
- **Campos principais**:
  - `title`: Título do filme.
  - `description`: Descrição do filme.
  - `release_date`: Data de lançamento do filme.
  - `duration`: Duração do filme em minutos.
  - `image_url`: URL da imagem do filme (opcional).
  - `genres`: Relacionamento de **Muitos para Muitos** com o modelo **Genre**, permitindo que cada filme tenha vários gêneros.

### 4. **Rating (Avaliação)**
- **Descrição**: Armazena as avaliações feitas pelos usuários sobre os filmes.
- **Campos principais**:
  - `user`: Relacionamento com o usuário que fez a avaliação.
  - `movie`: Relacionamento com o filme avaliado.
  - `rating`: Nota dada ao filme (escala de 1.0 a 5.0).
  - `review`: Comentário opcional sobre o filme.
  - `created_at`: Data e hora da avaliação.

A tabela **Rating** garante que um usuário só possa avaliar um filme uma vez, utilizando a restrição **unique_together**.

### 5. **Preference (Preferência)**
- **Descrição**: Armazena as preferências de gêneros dos usuários (favoritos ou evitados).
- **Campos principais**:
  - `user`: Relacionamento com o usuário.
  - `genre`: Relacionamento com o gênero preferido ou evitado.
  - `preference_type`: Tipo de preferência (favorito ou evitar).

A tabela **Preference** permite que os usuários definam gêneros de filmes que preferem ou evitam.

## Relacionamentos entre Modelos

- **Usuário e Avaliação**: Um usuário pode avaliar múltiplos filmes, e cada filme pode ter múltiplas avaliações de diferentes usuários.
- **Filme e Gênero**: Um filme pode pertencer a vários gêneros, e um gênero pode incluir vários filmes.
- **Usuário e Preferência**: Um usuário pode definir preferências sobre gêneros de filmes (favorito ou evitar), com um gênero podendo ser preferido ou evitado por vários usuários.

## Como Configurar a Base de Dados

1. **Criação de Migrações**: Após definir os modelos, você precisa criar as migrações para a base de dados com o comando:
   ```bash
   python manage.py makemigrations


## **Licença**
Este projeto está licenciado sob a **MIT License**. Sinta-se livre para usá-lo, modificá-lo e distribuí-lo.

---

Desfrute de uma experiência personalizada com PopCorn AI! 🎬🍿 Se tiver dúvidas ou sugestões, não hesite em abrir uma issue. 🚀
```
