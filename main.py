from letterboxdpy.user import User

# 1. Instancia o usuário e pega as estatísticas
usuario = User("nysnarc")
print(f"Buscando dados de {usuario.username}...\n")

estatisticas = usuario.stats
total_filmes = estatisticas.get('films', 'Não encontrado')
print(f"=== Total de Filmes Assistidos: {total_filmes} ===\n")

# 2. Puxa os gêneros e ordena do maior para o menor
info_generos = usuario.get_genre_info()
generos_ordenados = sorted(info_generos.items(), key=lambda x: x[1], reverse=True)

# 3. Pega apenas o NOME dos 2 gêneros mais assistidos
# O [0] serve para pegar só o nome (ex: 'Action') e ignorar a quantidade numérica
top_2_generos = [genero[0] for genero in generos_ordenados[:2]]

print(f"Seus gêneros dominantes são: {top_2_generos[0]} e {top_2_generos[1]}\n")

# ==========================================
# LÓGICA DO "ZODÍACO CINÉFILO"
# ==========================================
def descobrir_signo(top_generos):
    # Transforma a lista em um 'set' (conjunto) para facilitar a comparação
    g = set(top_generos)
    
    # .issubset() verifica se os dois gêneros estão dentro do Top 2 da pessoa
    if {"Drama", "Romance"}.issubset(g):
        return "O Romântico Incurável 💌 (Chora com finais felizes e ama um drama bem construído)"
        
    elif {"Horror", "Thriller"}.issubset(g):
        return "O Caçador de Calafrios 👻 (Não tem medo de nada, dorme tranquilo depois de um banho de sangue fictício)"
        
    elif {"Action", "Comedy"}.issubset(g):
        return "O Caos Divertido 💥 (Ama explosões, piadas bobas e não leva a vida tão a sério)"
        
    elif {"Science Fiction", "Fantasy"}.issubset(g):
        return "O Viajante de Mundos 👽 (A realidade é chata, o negócio é fugir para universos que não existem)"
        
    # Se quiser, pode verificar apenas 1 gênero forte
    elif "Documentary" in g:
        return "O Observador Realista 🧐 (Por que ver ficção quando a vida real já é um filme?)"
        
    elif "Animation" in g:
         return "A Criança Interior 🎈 (Conforto, cores vibrantes e lições de moral em 90 minutos)"
         
    else:
        # Um signo padrão caso a combinação da pessoa não caia nas regras acima
        return "O Cinéfilo Eclético 🎬 (Imprevisível! Assiste de tudo um pouco, um verdadeiro mistério)"

# 4. Descobre e imprime o signo final
meu_signo = descobrir_signo(top_2_generos)
print(f"🌟 SEU SIGNO CINÉFILO É: {meu_signo} 🌟")