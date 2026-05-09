from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UsernameForm, CompatibilidadeForm
from .services import buscar_perfil


def home(request):
    if request.method == "POST":
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            return redirect(reverse("zodiac:resultado", args=[username]))
    else:
        form = UsernameForm()
    return render(request, "zodiac/home.html", {"form": form})


def resultado(request, username):
    try:
        perfil = buscar_perfil(username)
        return render(request, "zodiac/result.html", {"perfil": perfil})
    except Exception:
        erro = f"Não foi possível encontrar o usuário '{username}'. Verifique se o nome está correto."
        return render(request, "zodiac/result.html", {"erro": erro})


def compatibilidade(request):
    if request.method == "POST":
        form = CompatibilidadeForm(request.POST)
        if form.is_valid():
            try:
                perfil1 = buscar_perfil(form.cleaned_data["username1"])
                perfil2 = buscar_perfil(form.cleaned_data["username2"])
                resultado = _calcular_compatibilidade(perfil1, perfil2)
                return render(request, "zodiac/compatibilidade.html", {
                    "perfil1": perfil1,
                    "perfil2": perfil2,
                    "resultado": resultado,
                })
            except Exception:
                erro = "Não foi possível encontrar um dos usuários. Verifique os nomes."
                return render(request, "zodiac/compatibilidade.html", {
                    "form": form, "erro": erro,
                })
    else:
        form = CompatibilidadeForm()
    return render(request, "zodiac/compatibilidade.html", {"form": form})


def _calcular_compatibilidade(perfil1, perfil2):
    """Calcula compatibilidade entre dois perfis baseado em gêneros e signo."""
    # Gêneros em comum
    generos1 = {g["nome"] for g in perfil1["generos"]}
    generos2 = {g["nome"] for g in perfil2["generos"]}
    em_comum = generos1 & generos2
    total = generos1 | generos2
    genero_pct = round(len(em_comum) / len(total) * 100) if total else 0

    # Mesmo signo = bonus
    mesmo_signo = perfil1["signo"]["nome"] == perfil2["signo"]["nome"]
    signo_bonus = 20 if mesmo_signo else 0

    # Filmes em comum (dos top rated)
    filmes1 = {f["nome"] for f in perfil1["playlist"]}
    filmes2 = {f["nome"] for f in perfil2["playlist"]}
    filmes_comum = filmes1 & filmes2

    # Score final
    score = min(100, genero_pct + signo_bonus + len(filmes_comum) * 5)

    if score >= 80:
        veredicto = "Almas gêmeas cinematográficas"
        emoji = "🔥"
    elif score >= 60:
        veredicto = "Ótima dupla pra maratona"
        emoji = "🍿"
    elif score >= 40:
        veredicto = "Diferentes mas complementares"
        emoji = "🎭"
    elif score >= 20:
        veredicto = "Vão brigar pelo controle remoto"
        emoji = "📺"
    else:
        veredicto = "Universos paralelos"
        emoji = "🌌"

    return {
        "score": score,
        "veredicto": veredicto,
        "emoji": emoji,
        "mesmo_signo": mesmo_signo,
        "generos_comum": sorted(em_comum),
        "filmes_comum": sorted(filmes_comum),
    }
