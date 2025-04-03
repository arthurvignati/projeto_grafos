"""
Projeto: Sistema de Recomendação de Filmes
Membros do grupo:
  Arthur Vignati Moscardi	10409688
  Pedro Pessuto	10409729
  Ian da Cunha	10409669
  Enzo Bernal	10402685
  Davi Martins	10374878

Descrição:
    Este arquivo contém o código fonte principal para o sistema de recomendação de filmes utilizando grafos.
    A aplicação permite a leitura e gravação do arquivo "grafo.txt", inserção e remoção de vértices e arestas,
    exibição do grafo como lista de adjacência, e análise de conectividade, incluindo a construção e exibição do grafo reduzido.

Histórico de Alterações:
    - 2025-03-29 (Pedro): Criação inicial do arquivo com funcionalidades básicas (leitura, escrita, inserção e remoção).
    - 2025-03-30 (Arthur): Adição da verificação de conectividade para grafos não orientados utilizando DFS.
    - 2025-03-31 (Davi): Implementação do algoritmo de Kosaraju para identificação de componentes fortemente conexas (SCCs) em grafos direcionados.
    - 2025-04-01 (Enzo): Integração da exibição do grafo original e formatação da lista de adjacência.
    - 2025-04-02 (Ian): Revisão geral do código, inclusão de comentários informativos e exibição do grafo reduzido na função de análise de conectividade.
"""

import os
from collections import defaultdict

GRAPH_FILENAME = "grafo.txt"


def read_graph(filename):
    """Lê o arquivo grafo.txt e retorna a estrutura do grafo."""
    if not os.path.exists(filename):
        print(f"Arquivo {filename} não encontrado.")
        return None
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    idx = 0
    graph = {}
    graph["graph_type"] = int(lines[idx])
    idx += 1
    num_vertices = int(lines[idx])
    idx += 1
    graph["vertices"] = {}
    for _ in range(num_vertices):
        # Cada linha: id|título|gêneros (gêneros separados por vírgula)
        parts = lines[idx].split("|")
        vid = parts[0]
        title = parts[1]
        genres = [int(g) for g in parts[2].split(",") if g]
        graph["vertices"][vid] = {"title": title, "genres": genres}
        idx += 1
    num_edges = int(lines[idx])
    idx += 1
    graph["edges"] = []
    for _ in range(num_edges):
        u, v = lines[idx].split()
        graph["edges"].append((u, v))
        idx += 1
    print("Grafo lido com sucesso!")
    return graph


def write_graph(graph, filename):
    """Grava a estrutura do grafo no arquivo grafo.txt com o formato especificado."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{graph['graph_type']}\n")
        f.write(f"{len(graph['vertices'])}\n")
        for vid, data in graph["vertices"].items():
            genres_str = ",".join(str(g) for g in data["genres"])
            f.write(f"{vid}|{data['title']}|{genres_str}\n")
        f.write(f"{len(graph['edges'])}\n")
        for u, v in graph["edges"]:
            f.write(f"{u} {v}\n")
    print(f"Arquivo '{filename}' gravado com sucesso!")


def insert_vertex(graph):
    """Insere um novo vértice no grafo."""
    vid = input("Digite o ID do novo vértice: ").strip()
    if vid in graph["vertices"]:
        print("Vértice já existe!")
        return
    title = input("Digite o título ou rótulo do vértice: ").strip()
    genres_input = input("Digite os gêneros (IDs separados por vírgula): ").strip()
    genres = [int(g.strip()) for g in genres_input.split(",") if g.strip().isdigit()]
    graph["vertices"][vid] = {"title": title, "genres": genres}
    print("Vértice inserido com sucesso!")


def insert_edge(graph):
    """Insere uma nova aresta no grafo conectando dois vértices."""
    u = input("Digite o ID do vértice de origem: ").strip()
    v = input("Digite o ID do vértice de destino: ").strip()
    if u not in graph["vertices"] or v not in graph["vertices"]:
        print("Um ou ambos os vértices não existem!")
        return
    if (u, v) in graph["edges"] or (v, u) in graph["edges"]:
        print("Aresta já existe!")
        return
    graph["edges"].append((u, v))
    print("Aresta inserida com sucesso!")


def remove_vertex(graph):
    """Remove um vértice e todas as arestas incidentes a ele."""
    vid = input("Digite o ID do vértice a ser removido: ").strip()
    if vid not in graph["vertices"]:
        print("Vértice não encontrado!")
        return
    del graph["vertices"][vid]
    graph["edges"] = [edge for edge in graph["edges"] if vid not in edge]
    print("Vértice e suas arestas removidos com sucesso!")


def remove_edge(graph):
    """Remove uma aresta do grafo."""
    u = input("Digite o ID do vértice de origem da aresta a ser removida: ").strip()
    v = input("Digite o ID do vértice de destino da aresta a ser removida: ").strip()
    if (u, v) in graph["edges"]:
        graph["edges"].remove((u, v))
        print("Aresta removida com sucesso!")
    elif (v, u) in graph["edges"]:
        graph["edges"].remove((v, u))
        print("Aresta removida com sucesso!")
    else:
        print("Aresta não encontrada!")


def show_file_content(filename):
    """Exibe o conteúdo do arquivo grafo.txt."""
    if not os.path.exists(filename):
        print(f"Arquivo {filename} não encontrado.")
        return
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    print("Conteúdo do arquivo:")
    print("-" * 40)
    print(content)
    print("-" * 40)


def show_graph(graph):
    """Exibe o grafo como uma lista de adjacência."""
    adj_list = {vid: [] for vid in graph["vertices"]}
    for u, v in graph["edges"]:
        adj_list[u].append(v)
        if graph["graph_type"] in [0, 1, 2, 3]:  # Grafo não orientado
            adj_list[v].append(u)
    print("Grafo original - Lista de adjacência:")
    for vid, neighbors in adj_list.items():
        print(f"{vid} -> {neighbors}")


# Funções para análise de componentes fortemente conexas (SCC) em grafos direcionados
def kosaraju_scc(graph):
    """Implementa o algoritmo de Kosaraju e retorna uma lista de SCCs e um mapeamento vértice -> componente."""
    adj = defaultdict(list)
    for u, v in graph["edges"]:
        adj[u].append(v)
    visited = set()
    stack = []

    def dfs(v):
        visited.add(v)
        for w in adj[v]:
            if w not in visited:
                dfs(w)
        stack.append(v)

    for v in graph["vertices"]:
        if v not in visited:
            dfs(v)
    rev_adj = defaultdict(list)
    for u, v in graph["edges"]:
        rev_adj[v].append(u)
    visited.clear()
    sccs = []
    vertex_to_component = {}

    def dfs_reverse(v, comp):
        visited.add(v)
        vertex_to_component[v] = comp
        scc.append(v)
        for w in rev_adj[v]:
            if w not in visited:
                dfs_reverse(w, comp)

    comp_id = 0
    while stack:
        v = stack.pop()
        if v not in visited:
            scc = []
            dfs_reverse(v, comp_id)
            sccs.append(scc)
            comp_id += 1
    return sccs, vertex_to_component


def build_reduced_graph(graph, vertex_to_component):
    """Constrói o grafo reduzido (condensação) a partir do mapeamento vértice -> componente."""
    reduced_adj = defaultdict(set)
    for u, v in graph["edges"]:
        comp_u = vertex_to_component[u]
        comp_v = vertex_to_component[v]
        if comp_u != comp_v:
            reduced_adj[comp_u].add(comp_v)
    reduced_graph = {comp: list(neighbors) for comp, neighbors in reduced_adj.items()}
    return reduced_graph


def print_reduced_graph(reduced_graph):
    """Exibe o grafo reduzido na forma de lista de adjacência."""
    print("Grafo reduzido - Lista de adjacência:")
    for comp, neighbors in reduced_graph.items():
        print(f"{comp} -> {neighbors}")


def analyze_connectivity(graph):
    """
    Apresenta a conexidade do grafo e exibe o grafo original e o grafo reduzido.
    Para grafos não orientados: utiliza DFS para verificar a conectividade.
    Para grafos direcionados: utiliza Kosaraju para identificar componentes fortemente conexas,
    exibe o grafo original, e em seguida o grafo reduzido.
    """
    print("=" * 40)
    if graph["graph_type"] in [0, 1, 2, 3]:
        print("Tipo do grafo: NÃO ORIENTADO")
        # Verifica conectividade com DFS
        visited = set()
        vertices = list(graph["vertices"].keys())
        if not vertices:
            print("Grafo vazio.")
            return

        def dfs(v):
            visited.add(v)
            for neighbor in [w for (u, w) in graph["edges"] if u == v] + [
                u for (u, w) in graph["edges"] if w == v
            ]:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(vertices[0])
        if len(visited) == len(vertices):
            print("O grafo é CONEXO.")
        else:
            print("O grafo é DESCONEXO.")
        # Exibe o grafo original
        show_graph(graph)
    else:
        print("Tipo do grafo: ORIENTADO")
        # Usa Kosaraju para identificar SCCs
        sccs, vertex_to_component = kosaraju_scc(graph)
        num_scc = len(sccs)
        if num_scc == 1:
            print("O grafo direcionado é fortemente conexo.")
        else:
            print(
                f"O grafo direcionado não é fortemente conexo. Possui {num_scc} componentes fortemente conexas."
            )
        for idx, comp in enumerate(sccs):
            print(f"Componente {idx}: {comp}")
        # Exibe o grafo original
        show_graph(graph)
        # Constrói e exibe o grafo reduzido
        reduced_graph = build_reduced_graph(graph, vertex_to_component)
        print_reduced_graph(reduced_graph)
    print("=" * 40)


def menu():
    """Menu interativo da aplicação."""
    graph = read_graph(GRAPH_FILENAME)
    if graph is None:
        graph = {"graph_type": 0, "vertices": {}, "edges": []}
    while True:
        print("\n========== Sistema de Recomendação de Filmes ==========")
        print("1. Ler dados do arquivo grafo.txt")
        print("2. Gravar dados no arquivo grafo.txt")
        print("3. Inserir vértice")
        print("4. Inserir aresta")
        print("5. Remover vértice")
        print("6. Remover aresta")
        print("7. Mostrar conteúdo do arquivo")
        print("8. Mostrar grafo (lista de adjacência)")
        print("9. Apresentar conexidade e grafo reduzido")
        print("0. Encerrar a aplicação")
        opc = input("Escolha uma opção: ").strip()
        if opc == "1":
            graph = read_graph(GRAPH_FILENAME)
        elif opc == "2":
            write_graph(graph, GRAPH_FILENAME)
        elif opc == "3":
            insert_vertex(graph)
        elif opc == "4":
            insert_edge(graph)
        elif opc == "5":
            remove_vertex(graph)
        elif opc == "6":
            remove_edge(graph)
        elif opc == "7":
            show_file_content(GRAPH_FILENAME)
        elif opc == "8":
            show_graph(graph)
        elif opc == "9":
            analyze_connectivity(graph)
        elif opc == "0":
            print("Encerrando a aplicação.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
