"""
Projeto: Sistema de Recomendação de Filmes 
Membros do grupo:
    - Pedro
    - Ian
    - Arthur
    - Enzo
    - Davi

Descrição:
    Este arquivo contém o código responsável por:
      1) Buscar filmes utilizando a API TheMovieDB e gerar o arquivo "grafo.txt" contendo os vértices
         (filmes com seus IDs, títulos e gêneros) e as arestas (conectando filmes que compartilham ao menos um gênero).
      2) Ler o arquivo "grafo.txt" para gerar um arquivo de edge list estendida, "listaParaOGrafoOnline.txt",
         no formato: a-(peso)-b, onde o peso representa o menor gênero em comum entre dois filmes.

Histórico de Alterações:
    - 2025-03-29 (Pedro): Criação inicial do arquivo com a função fetch_movies e geração de "grafo.txt".
    - 2025-03-30 (Ian): Ajuste no fetch para garantir pelo menos 60 filmes e montagem correta dos vértices.
    - 2025-03-31 (Arthur): Implementação da lógica para criação das arestas baseadas em gêneros comuns.
    - 2025-04-01 (Enzo): Revisão e melhoria na formatação do arquivo "grafo.txt" e adição de comentários.
    - 2025-04-02 (Davi): Inclusão da geração do arquivo de edge list estendida ("listaParaOGrafoOnline.txt"),
                             documentação interna e comentários informativos.
"""

import requests

# Dicionário de gêneros (IDs para nomes)
GENEROS = {
    28: "Ação",
    12: "Aventura",
    16: "Animação",
    35: "Comédia",
    80: "Crime",
    99: "Documentário",
    18: "Drama",
    10751: "Família",
    14: "Fantasia",
    36: "História",
    27: "Terror",
    10402: "Música",
    9648: "Mistério",
    10749: "Romance",
    878: "Ficção científica",
    10770: "Cinema TV",
    53: "Thriller",
    10752: "Guerra",
    37: "Faroeste",
}


def fetch_movies(min_count=60):
    """
    Faz o fetch dos filmes a partir da API TheMovieDB, iterando pelas páginas
    até coletar pelo menos 'min_count' filmes.
    Retorna uma lista de filmes (dicionários) com as informações necessárias.
    """
    movies = []
    page = 1
    while len(movies) < min_count:
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"include_adult=false&include_video=false&language=pt-BR&page={page}"
            f"&sort_by=popularity.desc&with_genres=28%7C12%7C16%7C35%7C80%7C99%7C18%7C10751%7C14%7C36%7C27%7C10402%7C9648%7C10749%7C878%7C10770%7C53%7C10752%7C37"
        )
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMzEyYTA0MTYzODAxMjVmZThlODQwMWI1MjA2MGMwZSIsIm5iZiI6MTc0MzQ2NTc2My45MDEsInN1YiI6IjY3ZWIyZDIzMDNiYWJkY2VkMjdhOWE0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-tb5nI8dlWuLVae0G2YLBvDV948ndMxTw-D7vYka6SE",
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Erro ao buscar a página {page}: {response.status_code}")
            break
        data = response.json()
        movies.extend(data["results"])
        print(f"Página {page} carregada, total de filmes: {len(movies)}")
        page += 1
    return movies


# Parte 1: Geração do arquivo grafo.txt

# Faz o fetch dos filmes (garante pelo menos 60 filmes)
movies = fetch_movies(min_count=60)

# Define o tipo do grafo.
# Para este exemplo, usamos 0: grafo não orientado sem peso.
graph_type = 0

# Monta os vértices (filmes) e gera as linhas para o arquivo.
vertex_lines = []
vertices = (
    {}
)  # dicionário para armazenar os dados dos vértices (chave: id, valor: dict com 'title' e 'genres')
for movie in movies:
    vid = str(movie["id"])
    title = movie["title"]
    # Converte a lista de IDs de gênero para uma string separada por vírgula.
    genres = ",".join(str(g) for g in movie["genre_ids"])
    vertices[vid] = {"title": title, "genres": movie["genre_ids"]}
    vertex_lines.append(f"{vid}|{title}|{genres}")

# Geração das arestas: conectamos dois filmes se eles compartilham ao menos um gênero.
edge_list = []
vertex_ids = list(vertices.keys())
# Para evitar repetição, usamos dois loops com j > i (grafo não orientado)
for i in range(len(vertex_ids)):
    for j in range(i + 1, len(vertex_ids)):
        vid_i = vertex_ids[i]
        vid_j = vertex_ids[j]
        genres_i = set(vertices[vid_i]["genres"])
        genres_j = set(vertices[vid_j]["genres"])
        common = genres_i & genres_j
        if common:
            # Se houver gêneros em comum, cria a aresta.
            # O "peso" da aresta é definido como o menor gênero em comum (usando conversão para int)
            weight = min(int(g) for g in common)
            edge_list.append((vid_i, vid_j, weight))

# Gera o arquivo "grafo.txt"
graph_filename = "grafo.txt"
with open(graph_filename, "w", encoding="utf-8") as f:
    # Escreve o tipo do grafo e o número de vértices
    f.write(f"{graph_type}\n")
    f.write(f"{len(vertex_lines)}\n")
    # Escreve cada vértice no formato: id|título|gêneros
    for line in vertex_lines:
        f.write(line + "\n")
    # Escreve o número de arestas e cada aresta (somente os vértices, sem salvar o peso)
    f.write(f"{len(edge_list)}\n")
    for edge in edge_list:
        f.write(f"{edge[0]} {edge[1]}\n")

print(f"Arquivo '{graph_filename}' gerado com sucesso!")

# Parte 2: Geração do arquivo de Edge List Estendida

# Lê o arquivo "grafo.txt" para construir a estrutura dos vértices e arestas.
with open(graph_filename, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]

line_index = 0
graph_type_line = lines[line_index]
line_index += 1
n = int(lines[line_index])
line_index += 1

# Lê os vértices e armazena em um dicionário
vertices_data = {}
for _ in range(n):
    parts = lines[line_index].split("|")
    vid = parts[0]
    title = parts[1]
    genres = [int(g) for g in parts[2].split(",") if g]
    vertices_data[vid] = {"title": title, "genres": genres}
    line_index += 1

# Lê as arestas (sem o peso salvo)
m = int(lines[line_index])
line_index += 1
edges_data = []
for _ in range(m):
    u, v = lines[line_index].split()
    edges_data.append((u, v))
    line_index += 1

# Gera o arquivo de edge list estendida: formato "u-(peso)-v"
extended_edges = []
for u, v in edges_data:
    genres_u = set(vertices_data[u]["genres"])
    genres_v = set(vertices_data[v]["genres"])
    common = genres_u & genres_v
    if common:
        weight_id = min(common)
        weight = weight_id  # O peso é o menor gênero em comum
        extended_edges.append(f"{u}-({weight})-{v}")
    else:
        # Caso não haja gênero comum (não deve ocorrer)
        extended_edges.append(f"{u}-{v}")

# Gera o arquivo "listaParaOGrafoOnline.txt" com a edge list estendida
edge_list_filename = "listaParaOGrafoOnline.txt"
with open(edge_list_filename, "w", encoding="utf-8") as f:
    for edge_line in extended_edges:
        f.write(edge_line + "\n")

print(f"Arquivo '{edge_list_filename}' gerado com sucesso!")
