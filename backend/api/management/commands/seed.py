from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import pandas as pd
import ast
from datetime import datetime
from django.utils.text import slugify
from api.models import Movie, Genre  # Certifique-se de importar corretamente seus modelos
from api.OMDbAPI import fetch_movie_by_title

class Command(BaseCommand):
    help = 'Cria gêneros, usuários e filmes no banco de dados'

    def handle(self, *args, **kwargs):
        # Criando os gêneros
        self.stdout.write(self.style.SUCCESS('Criando gêneros...'))
        genres = [
            ("Ação", "Filmes com cenas de ação intensas, incluindo perseguições e batalhas."),
            ("Aventura", "Filmes que envolvem exploração e jornadas emocionantes."),
            ("Comédia", "Filmes focados em fazer o público rir com situações engraçadas."),
            ("Drama", "Filmes que tratam de situações emocionais e complexas."),
            ("Terror", "Filmes destinados a causar medo e tensão."),
            ("Romance", "Filmes que giram em torno de histórias de amor."),
            ("Ficção Científica", "Filmes baseados em ciência ou tecnologias futurísticas."),
            ("Fantasia", "Filmes que exploram mundos imaginários com elementos sobrenaturais."),
            ("Mistério", "Filmes onde o enredo envolve a resolução de um mistério."),
            ("Suspense", "Filmes que geram tensão e expectativa no público."),
            ("Crime", "Filmes focados em atividades criminosas ou investigações policiais."),
            ("Familiar", "Filmes apropriados para todas as idades, geralmente educativos."),
            ("Documentário", "Filmes que exploram temas reais, educando o público."),
            ("Histórico", "Filmes que retratam eventos ou períodos históricos."),
            ("Guerra", "Filmes que tratam de conflitos armados e suas consequências."),
            ("Musical", "Filmes onde a música e a dança desempenham um papel importante."),
            ("Animação", "Filmes feitos por meio de animação, seja 2D ou 3D."),
            ("Western", "Filmes que se passam no contexto do Velho Oeste."),
            ("Ação e Aventura", "Uma mistura de ação intensa e aventuras emocionantes."),
            ("Comédia Romântica", "Filmes que combinam romance e comédia."),
            ("Sci-Fi e Fantasia", "Filmes que misturam ficção científica e fantasia."),
            ("Filme Noir", "Filmes de mistério e crime com uma atmosfera sombria."),
            ("Terror Psicológico", "Filmes que exploram o medo através de psicologia e ambiente."),
            ("Slasher", "Filmes de terror que envolvem assassinatos violentos."),
            ("Artes Marciais", "Filmes que envolvem lutas e combates com técnicas de artes marciais."),
            ("Zumbis", "Filmes que lidam com apocalipses envolvendo mortos-vivos."),
            ("Vingança", "Filmes focados em personagens buscando vingança."),
            ("Cyberpunk", "Filmes ambientados em futuros distópicos, geralmente com temas tecnológicos."),
            ("Espionagem", "Filmes que envolvem espionagem e inteligência internacional."),
            ("Biografia", "Filmes baseados na vida de pessoas reais."),
            ("Ficção Psicológica", "Filmes que exploram a mente humana e seus conflitos internos."),
            ("Aviação", "Filmes com temática de aviões, pilotos e guerra aérea."),
            ("Realidade Virtual", "Filmes que exploram o conceito de mundos digitais imersivos."),
            ("Naval", "Filmes que se passam no mar e envolvem operações navais."),
            ("Mágico", "Filmes com personagens que possuem poderes mágicos ou fantásticos."),
            ("Tecnologia", "Filmes que tratam do impacto da tecnologia na sociedade."),
            ("Criminalidade", "Filmes que abordam a vida do crime e suas repercussões."),
            ("Mistério e Suspense", "Filmes que envolvem mistérios com altas doses de suspense."),
            ("Amizade", "Filmes que exploram os laços de amizade e companheirismo."),
            ("Espiritualidade", "Filmes que abordam questões espirituais e religiosas."),
            ("Conspiração", "Filmes que lidam com teorias e ações secretas de conspiração."),
            ("Super-heróis", "Filmes baseados em heróis com habilidades sobre-humanas."),
            ("Medieval", "Filmes que se passam na Idade Média, com cavaleiros e castelos."),
            ("Viajem no Tempo", "Filmes que exploram a possibilidade de viajar no tempo."),
            ("Comédia Dramática", "Filmes que equilibram drama e momentos de comédia."),
            ("Espaço", "Filmes que se passam no espaço exterior, envolvendo viagens interplanetárias."),
            ("Antologia", "Filmes compostos por várias histórias independentes."),
            ("Artes Cênicas", "Filmes que exploram o mundo das artes cênicas, como teatro e dança."),
            ("Mafia", "Filmes que tratam do mundo do crime organizado e suas dinâmicas."),
            ("Policial", "Filmes sobre atividades policiais e investigações criminais."),
            ("Jogos", "Filmes com enredos focados em competições ou jogos de azar."),
            ("Mitologia", "Filmes que exploram histórias e criaturas mitológicas."),
            ("Desastres Naturais", "Filmes que tratam de eventos catastróficos naturais."),
            ("Satírico", "Filmes que usam a sátira para fazer críticas sociais."),
            ("Independentes", "Filmes de produção independente com orçamentos menores."),
            ("História de Vida", "Filmes que exploram eventos significativos na vida de um personagem."),
            ("Aventura Fantástica", "Filmes com aventuras em mundos fantásticos e mágicos."),
            ("Terror Gótico", "Filmes que combinam elementos de terror com o estilo gótico."),
            ("Realismo Mágico", "Filmes que misturam o real com o sobrenatural de forma sutil."),
            ("Futurologia", "Filmes que exploram possíveis futuros e o impacto das mudanças sociais."),
            ("Retrofuturismo", "Filmes que apresentam visões do futuro baseadas no passado."),
            ("Fable", "Filmes com enredos de fábulas ou contos de fada reimaginados.")
        ]
        
        for name, description in genres:
            slug = slugify(name)  # Cria o slug automaticamente
        
             # Verifica se o slug já existe
            if Genre.objects.filter(slug=slug).exists():
             # Se o slug já existir, cria um novo slug único
                counter = 1
                while Genre.objects.filter(slug=f"{slug}-{counter}").exists():
                    counter += 1
                slug = f"{slug}-{counter}"
            genre, created = Genre.objects.get_or_create(
                name=name,
                description=description,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Gênero "{name}" criado com sucesso.'))
            else:
                self.stdout.write(self.style.WARNING(f'Gênero "{name}" já existe.'))

        # Criando os usuários
        self.stdout.write(self.style.SUCCESS('Criando usuários...'))
        users_data = [
            ("admin", "admin@tg.com", True),
            ("Francemy", "francemy.sebastiao@tg.com", True),  # Admin
            ("Ruslan", "ruslan@tg.com", False),
            ("Kiame", "kiame@tg.com", False),
            ("Kizua", "kizua@tg.com", False),
            ("Otchali", "otchali@tg.com", False),
            ("Malungo", "malungo@tg.com", False),
            ("Mavinga", "mavinga@tg.com", False),
            ("Muñji", "munji@tg.com", False),
            ("Nkosi", "nkosi@tg.com", False),
            ("Samakuva", "samakuva@tg.com", False)
        ]
        
        for username, email, is_admin in users_data:
            try:
                # Criando o usuário
                if is_admin:
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password='1234'
                    )
                    self.stdout.write(self.style.SUCCESS(f'Admin usuário "{username}" criado com sucesso.'))
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password='1234'
                    )
                    self.stdout.write(self.style.SUCCESS(f'Usuário "{username}" criado com sucesso.'))
                
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f'Erro ao criar usuário "{username}": {str(e)}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro desconhecido ao criar usuário "{username}": {str(e)}'))

        