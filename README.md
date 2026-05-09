# Bodeboxd

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![License](https://img.shields.io/badge/license-unlicensed-lightgrey)

Bodeboxd é um projeto Django que conecta Letterboxd e zodíaco. A aplicação analisa o perfil de um usuário do Letterboxd e gera um "signo cinéfilo" com base nos gêneros mais assistidos, além de oferecer uma página de compatibilidade entre dois perfis.

## Funcionalidades

- Consulta um perfil público do Letterboxd
- Descobre o signo cinéfilo com base nos gêneros favoritos
- Mostra estatísticas, filmes favoritos e uma seleção de filmes relacionados ao perfil
- Compara dois usuários e calcula a compatibilidade cinéfila
- Interface em português, com visual responsivo e carregamento dinâmico

## Tecnologias

- Python
- Django 6
- `letterboxdpy`
- HTML, CSS e JavaScript

## Capturas de Tela

Adicione imagens em `docs/screenshots/` para mostrar a interface do projeto.

- `home.png` - tela inicial
- `result.png` - resultado do signo cinéfilo
- `compatibilidade.png` - comparação entre usuários

Se preferir, use este bloco como base no README:

```md
![Home](docs/screenshots/home.png)
![Resultado](docs/screenshots/result.png)
![Compatibilidade](docs/screenshots/compatibilidade.png)
```

## Pré-requisitos

- Python 3.12 ou superior
- Acesso a perfis públicos do Letterboxd

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/bodeboxd.git
cd bodeboxd
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

No Windows:

```bash
venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute as migrações:

```bash
python manage.py migrate
```

5. Rode o servidor local:

```bash
python manage.py runserver
```

6. Abra no navegador:

```bash
http://127.0.0.1:8000/
```

## Como usar

1. Digite o nome de usuário do Letterboxd
2. Veja o signo cinéfilo gerado para o perfil
3. Acesse a página de compatibilidade para comparar dois usuários

## Estrutura do projeto

- `latterboxd/`: configuração do projeto Django
- `zodiac/`: app principal com views, forms, serviços, templates e CSS
- `main.py`: script experimental/auxiliar com lógica de teste
- `manage.py`: comando principal do Django

## Observações

- O projeto depende de perfis públicos do Letterboxd.
- Se você for publicar no GitHub, não envie `venv/`, `db.sqlite3` ou caches de Python.

## Licença

Adicione a licença que você preferir antes de publicar.
