from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import time

from letterboxdpy.constants.project import DOMAIN, GENRES
from letterboxdpy.core.scraper import parse_url
from letterboxdpy.user import User

# Gêneros slug -> nome de exibição (para os que diferem)
GENRE_DISPLAY = {
    "science-fiction": "Science Fiction",
    "tv-movie": "TV Movie",
}

# Famosos associados a cada signo
FAMOSOS = {
    "Áries": ["Quentin Tarantino", "Akira Kurosawa", "Jackie Chan"],
    "Touro": ["Adele", "Al Pacino", "George Clooney"],
    "Gêmeos": ["Wes Anderson", "Angelina Jolie", "Chris Pratt"],
    "Câncer": ["Robin Williams", "Meryl Streep", "Tom Hanks"],
    "Leão": ["Christopher Nolan", "Stanley Kubrick", "Arnold Schwarzenegger"],
    "Virgem": ["Tim Burton", "Keanu Reeves", "Zendaya"],
    "Libra": ["Guillermo del Toro", "Kate Winslet", "Ryan Reynolds"],
    "Escorpião": ["Martin Scorsese", "Leonardo DiCaprio", "Joaquin Phoenix"],
    "Sagitário": ["Steven Spielberg", "Brad Pitt", "Scarlett Johansson"],
    "Capricórnio": ["David Lynch", "Denzel Washington", "Timothée Chalamet"],
    "Aquário": ["Denis Villeneuve", "Christian Bale", "Harry Styles"],
    "Peixes": ["David Fincher", "Daniel Craig", "Rihanna"],
    "Plutão": ["Jordan Peele", "Ari Aster", "Robert Eggers"],
    "Netuno": ["Hayao Miyazaki", "Peter Jackson", "Guillermo del Toro"],
    "Saturno": ["Steven Spielberg", "Ridley Scott", "Clint Eastwood"],
    "Júpiter": ["Pixar", "Studio Ghibli", "Edgar Wright"],
    "Marte": ["James Cameron", "Ridley Scott", "Paul Verhoeven"],
    "Vênus": ["Damien Chazelle", "Sofia Coppola", "Wong Kar-wai"],
    "Mercúrio": ["Christopher Nolan", "David Fincher", "Denis Villeneuve"],
    "Ofiúco": ["Andrei Tarkovsky", "Terrence Malick", "David Lynch"],
}

SIGNOS = [
    # Combinações de 2 gêneros → signo real do zodíaco
    ({"Drama", "Romance"}, "Peixes", "♓",
     "Sente tudo intensamente — um filme de amor bem feito é terapia pra alma",
     ["Eternal Sunshine of the Spotless Mind", "Call Me by Your Name", "In the Mood for Love", "Pride & Prejudice"]),
    ({"Horror", "Thriller"}, "Escorpião", "♏",
     "Intenso, magnético e não tem medo do escuro — quanto mais sombrio, mais em casa se sente",
     ["The Silence of the Lambs", "Hereditary", "Se7en", "The Shining"]),
    ({"Action", "Comedy"}, "Sagitário", "♐",
     "Aventureiro e bem-humorado — a vida é curta demais pra filme parado",
     ["Hot Fuzz", "Rush Hour", "Kung Fu Hustle", "The Nice Guys"]),
    ({"Science Fiction", "Fantasy"}, "Aquário", "♒",
     "Visionário e fora da caixa — prefere universos que ainda não existem",
     ["Blade Runner 2049", "The Matrix", "Interstellar", "Pan's Labyrinth"]),
    ({"Drama", "Comedy"}, "Gêmeos", "♊",
     "Dual por natureza — ri e chora no mesmo filme sem contradição nenhuma",
     ["The Grand Budapest Hotel", "Little Miss Sunshine", "Jojo Rabbit", "The Truman Show"]),
    ({"Drama", "Thriller"}, "Virgem", "♍",
     "Analítico e atento — percebe cada detalhe que o diretor escondeu na cena",
     ["Gone Girl", "Zodiac", "Prisoners", "Black Swan"]),
    ({"Action", "Thriller"}, "Áries", "♈",
     "Pura energia — não consegue ficar parado e ama quando o filme também não para",
     ["Mad Max: Fury Road", "John Wick", "Die Hard", "The Raid"]),
    ({"Comedy", "Romance"}, "Libra", "♎",
     "Harmonia, beleza e amor — acredita que todo mundo merece um final feliz",
     ["When Harry Met Sally", "Amélie", "10 Things I Hate About You", "Crazy, Stupid, Love"]),
    ({"Action", "Adventure"}, "Leão", "♌",
     "Grandioso e destemido — quer épicos que façam o coração acelerar",
     ["Indiana Jones: Raiders of the Lost Ark", "Top Gun: Maverick", "Gladiator", "The Dark Knight"]),
    ({"Crime", "Thriller"}, "Capricórnio", "♑",
     "Estratégico e frio — admira mentes brilhantes, mesmo as criminosas",
     ["No Country for Old Men", "Heat", "The Departed", "Sicario"]),
    ({"Horror", "Mystery"}, "Plutão", "♇",
     "Atraído pelo inexplicável — quanto mais macabro o mistério, melhor",
     ["Midsommar", "The Others", "It Follows", "The Witch"]),
    ({"Drama", "History"}, "Saturno", "♄",
     "Conectado com o peso do tempo — filmes que ensinam algo real tocam mais fundo",
     ["Schindler's List", "12 Years a Slave", "The Pianist", "Oppenheimer"]),
    ({"Comedy", "Animation"}, "Júpiter", "♃",
     "Expansivo e otimista — nunca perde a capacidade de se encantar",
     ["Spider-Man: Into the Spider-Verse", "Shrek", "The Lego Movie", "Ratatouille"]),
    ({"Science Fiction", "Action"}, "Marte", "♂",
     "Combativo e futurista — se tem explosão no espaço, já tem a atenção",
     ["Aliens", "Edge of Tomorrow", "The Terminator", "District 9"]),
    ({"Drama", "Crime"}, "Escorpião", "♏",
     "Fascinado pelo submundo — morais cinzentas e personagens complexos são seu vício",
     ["The Godfather", "Goodfellas", "There Will Be Blood", "City of God"]),
    ({"Fantasy", "Adventure"}, "Netuno", "♆",
     "Sonhador nato — vive pra jornadas épicas em mundos que queria que existissem",
     ["The Lord of the Rings", "Princess Mononoke", "The NeverEnding Story", "Spirited Away"]),
    ({"Mystery", "Thriller"}, "Mercúrio", "☿",
     "Mente inquieta — adora desvendar o que ninguém viu e prever o plot twist",
     ["Shutter Island", "Memento", "Mulholland Drive", "Knives Out"]),
    ({"Comedy", "Crime"}, "Gêmeos", "♊",
     "Caótico e esperto — adora quando o crime vira piada genial",
     ["Snatch", "The Big Lebowski", "Fargo", "Pulp Fiction"]),
    ({"Action", "Science Fiction"}, "Marte", "♂",
     "Guerreiro do futuro — se tem tecnologia e porrada, tá dentro",
     ["The Matrix", "Inception", "Total Recall", "Minority Report"]),
    ({"Drama", "Music"}, "Vênus", "♀",
     "Sensível à beleza — quando drama e música se encontram, a magia acontece",
     ["Whiplash", "Amadeus", "La La Land", "Inside Llewyn Davis"]),
    # Gêneros solo
    ({"Documentary"}, "Virgem", "♍",
     "Busca a verdade nos detalhes — prefere fatos a ficção",
     ["Won't You Be My Neighbor?", "Free Solo", "Jiro Dreams of Sushi", "13th"]),
    ({"Animation"}, "Júpiter", "♃",
     "Acredita que arte sem limites físicos é a forma mais pura de cinema",
     ["Spirited Away", "Akira", "WALL-E", "Coco"]),
    ({"Horror"}, "Plutão", "♇",
     "Atraído pela escuridão — o medo é só outra forma de se sentir vivo",
     ["The Exorcist", "A Quiet Place", "Get Out", "Suspiria"]),
    ({"Drama"}, "Câncer", "♋",
     "Emocional e profundo — um bom drama vale mais que qualquer terapia",
     ["Moonlight", "Manchester by the Sea", "Paris, Texas", "A Separation"]),
    ({"Comedy"}, "Sagitário", "♐",
     "A vida já é séria demais — cinema é pra rir e viver leve",
     ["Superbad", "Airplane!", "Monty Python and the Holy Grail", "The Hangover"]),
    ({"Action"}, "Áries", "♈",
     "Pura adrenalina — se não tem perseguição de carro, nem começa",
     ["Die Hard", "Mad Max: Fury Road", "Kill Bill", "Mission: Impossible – Fallout"]),
    ({"Crime"}, "Capricórnio", "♑",
     "Estrategista nato — já sabe quem é o culpado antes da metade do filme",
     ["The Godfather Part II", "L.A. Confidential", "Chinatown", "Zodiac"]),
    ({"Romance"}, "Peixes", "♓",
     "Acredita no amor de cinema e não tem vergonha nenhuma disso",
     ["Before Sunrise", "The Notebook", "Casablanca", "Portrait of a Lady on Fire"]),
    ({"Thriller"}, "Escorpião", "♏",
     "Vive na tensão — quanto mais apertado o nó, mais satisfeito fica",
     ["Parasite", "Nightcrawler", "Oldboy", "The Handmaiden"]),
]

SIGNO_PADRAO = {
    "nome": "Ofiúco",
    "emoji": "⛎",
    "descricao": "O 13° signo — tão raro e eclético que o zodíaco não deu conta de classificar",
    "filmes": ["2001: A Space Odyssey", "Mulholland Drive", "The Tree of Life", "Stalker"],
}


def descobrir_signo(top_generos):
    g = set(top_generos)
    for generos_req, nome, emoji, descricao, filmes in SIGNOS:
        if generos_req.issubset(g):
            signo = {"nome": nome, "emoji": emoji, "descricao": descricao, "filmes": filmes}
            signo["famosos"] = FAMOSOS.get(nome, [])
            return signo
    result = SIGNO_PADRAO.copy()
    result["famosos"] = FAMOSOS.get("Ofiúco", [])
    return result


def _descobrir_ascendente(terceiro_genero):
    """Descobre o signo ascendente baseado no 3° gênero mais assistido."""
    for generos_req, nome, emoji, descricao, _filmes in SIGNOS:
        if len(generos_req) == 1 and terceiro_genero in generos_req:
            return {"nome": nome, "emoji": emoji}
    return None


def _contar_genero(username, slug):
    """Scrape film count for a single genre."""
    dom = parse_url(f"{DOMAIN}/{username}/films/genre/{slug}/")
    count = len(dom.select(".poster-grid li"))
    nome = GENRE_DISPLAY.get(slug, slug.title())
    return nome, count


def _extrair_generos(username):
    """Scrape film count per genre in parallel."""
    with ThreadPoolExecutor(max_workers=19) as pool:
        futures = [pool.submit(_contar_genero, username, slug) for slug in GENRES]
        return {nome: count for f in futures for nome, count in [f.result()] if count > 0}


def _buscar_top_filmes(usuario):
    """Filmes com nota >= 4.0, ordenados por rating desc."""
    top = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(usuario.get_films_by_rating, r): r
            for r in [5, 4.5, 4]
        }
        for f in futures:
            top.update(f.result().get("movies", {}))

    filmes = [
        {
            "nome": m["name"],
            "ano": m.get("year", ""),
            "url": m.get("url", ""),
            "nota": m.get("rating", 0),
            "liked": m.get("liked", False),
        }
        for m in top.values()
    ]
    filmes.sort(key=lambda x: (-x["nota"], x["nome"]))
    return filmes


# Cache simples com TTL de 2 horas
_cache = {}
_CACHE_TTL = 2 * 60 * 60


def buscar_perfil(username):
    username = username.strip().lower()

    # Verifica cache
    if username in _cache:
        resultado, timestamp = _cache[username]
        if time.time() - timestamp < _CACHE_TTL:
            return resultado

    usuario = User(username)

    estatisticas = usuario.stats
    total_filmes = estatisticas.get("films", 0)

    # Avatar
    avatar_data = usuario.avatar
    avatar_url = avatar_data.get("url") if avatar_data and avatar_data.get("exists") else None

    # Filmes favoritos (já vem no init, sem request extra)
    favoritos = []
    if usuario.favorites:
        for fav in usuario.favorites.values():
            favoritos.append({
                "nome": fav.get("name", ""),
                "ano": fav.get("year", ""),
                "url": fav.get("url", ""),
            })

    # Gêneros e top filmes em paralelo
    with ThreadPoolExecutor(max_workers=2) as pool:
        generos_future = pool.submit(_extrair_generos, usuario.username)
        filmes_future = pool.submit(_buscar_top_filmes, usuario)
        info_generos = generos_future.result()
        top_filmes = filmes_future.result()

    generos_ordenados = sorted(info_generos.items(), key=lambda x: x[1], reverse=True)

    top_generos = [g[0] for g in generos_ordenados[:2]]

    # Gêneros com porcentagem relativa ao maior (para barras no template)
    max_count = generos_ordenados[0][1] if generos_ordenados else 1
    generos_com_pct = [
        {"nome": nome, "count": count, "pct": round(count / max_count * 100)}
        for nome, count in generos_ordenados
    ]

    signo = descobrir_signo(top_generos)

    # Ascendente (3° gênero)
    ascendente = None
    if len(generos_ordenados) >= 3:
        terceiro = generos_ordenados[2][0]
        if terceiro not in top_generos:
            ascendente = _descobrir_ascendente(terceiro)

    resultado = {
        "username": usuario.username,
        "display_name": usuario.display_name,
        "avatar_url": avatar_url,
        "bio": usuario.bio,
        "total_filmes": total_filmes,
        "este_ano": estatisticas.get("this_year", 0),
        "following": estatisticas.get("following", 0),
        "followers": estatisticas.get("followers", 0),
        "watchlist": usuario.watchlist_length or 0,
        "favoritos": favoritos,
        "generos": generos_com_pct,
        "top_generos": top_generos,
        "signo": signo,
        "ascendente": ascendente,
        "playlist": top_filmes[:12],
    }

    _cache[username] = (resultado, time.time())
    return resultado
