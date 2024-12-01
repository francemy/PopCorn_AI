import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import string

nltk.download('stopwords')

# Carregar dados (dados de avaliação de filmes, como MovieLens)
ratings = pd.read_csv('ratings.csv')  # Ajuste o caminho para o arquivo
movies = pd.read_csv('movies.csv')    # Ajuste o caminho para o arquivo

# Criar um objeto Reader para ler os dados no formato Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Dividir os dados em treino e teste
trainset, testset = train_test_split(data, test_size=0.2)

# Usar o algoritmo SVD (Singular Value Decomposition)
model = SVD()
model.fit(trainset)

# Fazer previsões
predictions = model.test(testset)

# Mostrar as recomendações
def get_top_n(predictions, n=10):
    top_n = {}
    for uid, iid, true_r, est, _ in predictions:
        if uid not in top_n:
            top_n[uid] = []
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

top_n = get_top_n(predictions, n=10)

# Exibir os 10 melhores filmes para o usuário com id 1
print("Recomendações para o usuário 1:")
for movie_id, rating in top_n[1]:
    movie_name = movies[movies['movieId'] == movie_id]['title'].values[0]
    print(f'{movie_name}: {rating}')


# Preprocessamento do texto (títulos e descrições dos filmes)
stop_words = set(stopwords.words('english'))

# Função para remover stopwords e pontuação
def preprocess_text(text):
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    return ' '.join([word for word in text.split() if word not in stop_words])

# Preprocessar os dados de filmes
movies['processed_title'] = movies['title'].apply(preprocess_text)

# Usando o TF-IDF para transformar o texto em vetores numéricos
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['processed_title'])

# Calcular a similaridade entre os filmes
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Função para recomendar filmes com base em um filme específico
def get_movie_recommendations(movie_title, cosine_sim=cosine_sim):
    idx = movies.index[movies['title'] == movie_title].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    
    recommended_movies = movies['title'].iloc[movie_indices]
    return recommended_movies

# Testando a recomendação baseada no filme 'The Dark Knight'
recommendations = get_movie_recommendations('The Dark Knight')
print("\nRecomendações baseadas no filme 'The Dark Knight':")
print(recommendations)



# Função híbrida que recomenda filmes combinando os dois métodos
def hybrid_recommendation(user_id, movie_title, top_n, cosine_sim):
    collaborative_recs = top_n[user_id]
    content_based_recs = get_movie_recommendations(movie_title)
    
    # Combina as recomendações
    all_recs = set([rec[0] for rec in collaborative_recs])
    all_recs.update(content_based_recs)
    
    return list(all_recs)

# Recomendando filmes para o usuário 1 com base em 'The Dark Knight'
hybrid_recs = hybrid_recommendation(1, 'The Dark Knight', top_n, cosine_sim)
print("\nRecomendações híbridas para o usuário 1:")
print(hybrid_recs)
