"""Gerador de sites profissionais — cria HTML completo, pronto pra publicar."""
import io
import discord

TIPOS = {
    "portfolio": {
        "emoji": "💼", "titulo": "Meu Portfólio", "cor": "#5865F2",
        "tagline": "Criatividade, técnica e compromisso em cada projeto.",
        "nav": [("Início", "hero"), ("Sobre", "sobre"), ("Serviços", "servicos"), ("Contato", "contato")],
        "secoes": [
            ("sobre", "Sobre Mim", ["Profissional dedicado com anos de experiência na área.", "Especialista em entregar resultados com qualidade e prazo.", "Apaixonado pelo que faço — e isso aparece no trabalho."]),
            ("servicos", "Serviços", ["Consultoria personalizada", "Projetos sob medida", "Atendimento dedicado", "Suporte contínuo"]),
        ],
    },
    "loja": {
        "emoji": "🛒", "titulo": "Minha Loja", "cor": "#27AE60",
        "tagline": "Os melhores produtos com entrega rápida e pagamento seguro.",
        "nav": [("Início", "hero"), ("Produtos", "produtos"), ("Entrega", "entrega"), ("Contato", "contato")],
        "secoes": [
            ("produtos", "Nossos Produtos", ["Linha premium com garantia estendida", "Novidades toda semana", "Promoções relâmpago", "Frete grátis acima de R$ 150"]),
            ("entrega", "Entrega e Pagamento", ["Entregamos em até 48h", "Pix, cartão e boleto", "Rastreamento em tempo real", "Troca fácil em 7 dias"]),
        ],
    },
    "landing": {
        "emoji": "🚀", "titulo": "Landing Page", "cor": "#8E44AD",
        "tagline": "O produto que você precisa, no preço que você quer pagar.",
        "nav": [("Início", "hero"), ("Benefícios", "beneficios"), ("Preço", "preco"), ("Comprar", "contato")],
        "secoes": [
            ("beneficios", "Benefícios", ["Resolve seu problema em minutos", "Economia de até 60%", "Resultados garantidos ou seu dinheiro de volta", "Suporte humano de verdade"]),
            ("preco", "Preço Justo", ["Plano básico a partir de R$ 29,90", "Sem taxas escondidas", "Cancele quando quiser", "Garantia de 30 dias"]),
        ],
    },
    "barbearia": {
        "emoji": "💈", "titulo": "Barbearia", "cor": "#C0392B",
        "tagline": "Corte, barba e estilo — você no seu melhor momento.",
        "nav": [("Início", "hero"), ("Serviços", "servicos"), ("Equipe", "equipe"), ("Agendar", "contato")],
        "secoes": [
            ("servicos", "Serviços", ["Corte masculino — R$ 40", "Barba completa — R$ 30", "Corte + barba — R$ 60", "Platinado e coloração"]),
            ("equipe", "Nossa Equipe", ["Profissionais experientes", "Ambiente climatizado", "Atendimento com hora marcada", "Produtos de primeira linha"]),
        ],
    },
    "restaurante": {
        "emoji": "🍽️", "titulo": "Restaurante", "cor": "#E67E22",
        "tagline": "Comida de verdade, feita com carinho todos os dias.",
        "nav": [("Início", "hero"), ("Menu", "menu"), ("Sobre", "sobre"), ("Reservas", "contato")],
        "secoes": [
            ("menu", "Cardápio", ["Pratos executivos de terça a sexta", "Churrasco completo no fim de semana", "Sobremesas artesanais", "Delivery em toda a região"]),
            ("sobre", "Sobre Nós", ["Ingredientes frescos selecionados", "Cozinha aberta — veja tudo", "Espaço para eventos", "Estacionamento próprio"]),
        ],
    },
    "futebol": {
        "emoji": "⚽", "titulo": "Central São Paulo FC", "cor": "#2ECC71",
        "tagline": "Tradição, paixão e glória — o clube do povo.",
        "nav": [("Início", "hero"), ("Elenco", "elenco"), ("Tabela", "tabela"), ("Sócio", "socio")],
        "secoes": [
            ("elenco", "Elenco Profissional", ["Comissão técnica completa", "Departamento médico próprio", "Categorias de base forte", "Centro de treinamento moderno"]),
            ("tabela", "Últimos Jogos", ["Vitórias em casa invictas", "Artilheiro da temporada", "Escalação da próxima partida", "Classificação no estadual"]),
            ("socio", "Seja Sócio", ["Sócio Gold com vantagens", "Cadeira cativa no estádio", "Desconto na loja oficial", "Convocação para eventos do clube"]),
        ],
    },
    "empresa": {
        "emoji": "🏢", "titulo": "Minha Empresa", "cor": "#2980B9",
        "tagline": "Soluções corporativas para o seu negócio crescer.",
        "nav": [("Início", "hero"), ("Serviços", "servicos"), ("Sobre", "sobre"), ("Contato", "contato")],
        "secoes": [
            ("servicos", "Serviços", ["Consultoria estratégica", "Gestão de projetos", "Análise de dados", "Treinamentos corporativos"]),
            ("sobre", "Sobre", ["+10 anos de mercado", "Equipe multidisciplinar", "Clientes em todo o Brasil", "Resultados mensuráveis"]),
        ],
    },
    "musica": {
        "emoji": "🎵", "titulo": "Artista Oficial", "cor": "#E91E63",
        "tagline": "Novo álbum disponível em todas as plataformas.",
        "nav": [("Início", "hero"), ("Lançamentos", "lancamentos"), ("Shows", "shows"), ("Contato", "contato")],
        "secoes": [
            ("lancamentos", "Lançamentos", ["Último single nas plataformas", "Clipe oficial no YouTube", "Prévia do próximo álbum", "Playlists curadas"]),
            ("shows", "Shows e Eventos", ["Agenda da turnê nacional", "Ingressos com preço popular", "Meet & greet com fãs", "Contratações e imprensa"]),
        ],
    },
    "evento": {
        "emoji": "🎪", "titulo": "Meu Evento", "cor": "#F1C40F",
        "tagline": "O evento que você não pode perder — garanta seu lugar!",
        "nav": [("Início", "hero"), ("Programação", "programacao"), ("Ingressos", "ingressos"), ("Contato", "contato")],
        "secoes": [
            ("programacao", "Programação", ["Atrações nacionais confirmadas", "Palcos temáticos", "Área de comida e bebida", "Estacionamento e segurança"]),
            ("ingressos", "Ingressos", ["Lote promocional limitado", "Meia-entrada permitida", "VIP com área exclusiva", "Compre online e evite fila"]),
        ],
    },
    "blog": {
        "emoji": "📰", "titulo": "Meu Blog", "cor": "#16A085",
        "tagline": "Conteúdo novo toda semana, direto ao ponto.",
        "nav": [("Início", "hero"), ("Artigos", "artigos"), ("Categorias", "categorias"), ("Contato", "contato")],
        "secoes": [
            ("artigos", "Últimos Artigos", ["Guia completo para iniciantes", "Análises e opiniões", "Tutoriais passo a passo", "Novidades da área"]),
            ("categorias", "Categorias", ["Tecnologia", "Negócios", "Saúde e bem-estar", "Cultura pop"]),
        ],
    },
    "gaming": {
        "emoji": "🎮", "titulo": "Team Oficial", "cor": "#9B59B6",
        "tagline": "Time profissional — treino duro, vitória certa.",
        "nav": [("Início", "hero"), ("Elenco", "elenco"), ("Resultados", "resultados"), ("Patrocínio", "contato")],
        "secoes": [
            ("elenco", "Elenco", ["Titulares e reservas", "Comissão técnica com coach", "Analista dedicado", "Bootcamp mensal"]),
            ("resultados", "Resultados", ["Campeão da última temporada", "Vagas abertas para testes", "Transmissão dos jogos ao vivo", "Loja oficial de uniformes"]),
        ],
    },
    "fotografia": {
        "emoji": "📷", "titulo": "Estúdio de Fotografia", "cor": "#34495E",
        "tagline": "Momentos eternizados com qualidade profissional.",
        "nav": [("Início", "hero"), ("Serviços", "servicos"), ("Portfólio", "portfolio"), ("Orçamento", "contato")],
        "secoes": [
            ("servicos", "Serviços", ["Ensaio profissional", "Casamentos e eventos", "Book corporativo", "Tratamento e edição"]),
            ("portfolio", "Portfólio", ["Projetos publicados", "Exposições em galerias", "Prêmios e reconhecimentos", "Parcerias com marcas"]),
        ],
    },
}

_KEYWORDS = {
    "portfolio": ("portfólio", "portfolio", "currículo", "curriculo"),
    "loja": ("loja", "shop", "loja online", "e-commerce", "ecommerce", "vender", "vitrine"),
    "landing": ("landing", "captura", "vender produto", "lançamento", "pagina de vendas", "página de vendas"),
    "barbearia": ("barbearia", "barbeiro", "salão", "salao", "cabelo"),
    "restaurante": ("restaurante", "comida", "pizzaria", "lanche", "delivery", "food", "cozinha"),
    "futebol": ("futebol", "clube", "time", "soccer"),
    "empresa": ("empresa", "corporativo", "negócio", "negocio", "serviços", "servicos"),
    "musica": ("música", "musica", "cantor", "banda", "artista", "dj", "show"),
    "evento": ("evento", "festa", "festival", "show ", "cerimônia", "cerimonia"),
    "blog": ("blog", "notícias", "noticias", "artigos", "revista"),
    "gaming": ("gaming", "game", "e-sports", "esports", "time de jogo", "organização", "organizacao"),
    "fotografia": ("foto", "fotografia", "fotógrafo", "fotografo", "estúdio", "estudio", "ensaio"),
}

SITE_WORDS = ("site", "website", "página", "pagina", "web", "landing")


def match_tipo(text: str):
    """Retorna a chave do tipo de site se o pedido for pra criar um site."""
    t = text.lower()
    if not any(w in t for w in SITE_WORDS):
        return None
    for key, words in _KEYWORDS.items():
        if any(w in t for w in words):
            return key
    return "portfolio"


def gerar_html(tipo: str, nome: str = None) -> str:
    d = TIPOS.get(tipo, TIPOS["portfolio"])
    titulo = nome or d["titulo"]
    cor = d["cor"]

    nav = "".join(f'<a href="#{aidx}">{label}</a>' for label, aidx in d["nav"])
    secoes = ""
    for aidx, stitulo, itens in d["secoes"]:
        cards = "".join(
            f'<div class="card"><h3>✦</h3><p>{i}</p></div>' for i in itens)
        secoes += f'''
    <section id="{aidx}">
      <h2>{stitulo}</h2>
      <div class="grid">{cards}</div>
    </section>'''

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI',Arial,sans-serif; }}
  body {{ background:#0d1117; color:#e6edf3; }}
  header {{ position:sticky; top:0; background:#161b22; padding:16px 8%; display:flex;
           justify-content:space-between; align-items:center; box-shadow:0 2px 12px #0008; z-index:9; }}
  .logo {{ font-size:1.3rem; font-weight:bold; color:{cor}; }}
  nav a {{ color:#e6edf3; text-decoration:none; margin-left:22px; font-size:.95rem; }}
  nav a:hover {{ color:{cor}; }}
  .hero {{ text-align:center; padding:110px 8% 90px; background:linear-gradient(160deg,{cor}22,#0d1117 70%); }}
  .hero h1 {{ font-size:3rem; margin-bottom:18px; }}
  .hero p {{ font-size:1.25rem; color:#9aa4b2; max-width:640px; margin:0 auto 34px; }}
  .btn {{ display:inline-block; background:{cor}; color:#fff; padding:15px 42px; border-radius:50px;
         text-decoration:none; font-weight:bold; font-size:1.05rem; transition:.25s; }}
  .btn:hover {{ transform:translateY(-3px); box-shadow:0 10px 26px {cor}66; }}
  section {{ padding:70px 8%; }}
  section:nth-child(even) {{ background:#161b22; }}
  h2 {{ text-align:center; font-size:2rem; margin-bottom:44px; color:{cor}; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:22px; max-width:1100px; margin:0 auto; }}
  .card {{ background:#21262d; border:1px solid #30363d; border-radius:14px; padding:26px; transition:.25s; }}
  .card:hover {{ transform:translateY(-6px); border-color:{cor}; }}
  .card h3 {{ font-size:1.4rem; margin-bottom:12px; color:{cor}; }}
  .card p {{ color:#9aa4b2; line-height:1.55; }}
  footer {{ text-align:center; padding:44px 8%; background:#161b22; color:#8b949e; font-size:.9rem; }}
  footer strong {{ color:{cor}; }}
  @media(max-width:640px){{ .hero h1{{font-size:2.1rem}} nav a{{margin-left:12px;font-size:.85rem}} }}
</style>
</head>
<body>
<header><span class="logo">{d["emoji"]} {titulo}</span><nav>{nav}</nav></header>
<div class="hero" id="hero">
  <h1>{titulo}</h1>
  <p>{d["tagline"]}</p>
  <a class="btn" href="#contato">Fale com a gente</a>
</div>
{secoes}
<section id="contato">
  <h2>Contato</h2>
  <div class="grid">
    <div class="card"><h3>📧 E-mail</h3><p>contato@exemplo.com</p></div>
    <div class="card"><h3>📱 WhatsApp</h3><p>(00) 90000-0000</p></div>
    <div class="card"><h3>📍 Endereço</h3><p>Sua cidade, estado — Brasil</p></div>
    <div class="card"><h3>🕒 Horário</h3><p>Seg a Sáb, 9h às 18h</p></div>
  </div>
</section>
<footer>Feito com 💜 por <strong>Central SP Bot</strong> — edite este site à vontade!</footer>
</body>
</html>'''


def site_embed(tipo: str, nome: str = None) -> discord.Embed:
    d = TIPOS.get(tipo, TIPOS["portfolio"])
    e = discord.Embed(
        title=f"🌐 Site criado: {nome or d['titulo']}",
        description=(
            f"**{d['emoji']} {nome or d['titulo']}** — {d['tagline']}\n\n"
            "📦 O arquivo **`.html`** está anexado. Pra usar:\n"
            "1️⃣ **Baixe o arquivo** (clique nele → salvar)\n"
            "2️⃣ **Dê dois cliques** — abre no navegador, pronto!\n"
            "3️⃣ Pra publicar online de graça: arraste o arquivo no **app.netlify.com/drop**\n\n"
            "🎨 Edite textos e cores com qualquer editor (Bloco de Notas serve)."
        ),
        color=0x5865F2)
    e.set_footer(text="Slayer Bot • gerador de sites profissionais")
    return e


def site_file(tipo: str, nome: str = None) -> discord.File:
    html = gerar_html(tipo, nome)
    data = io.BytesIO(html.encode("utf-8"))
    filename = (nome or tipo).lower().replace(" ", "-") + ".html"
    return discord.File(data, filename=filename)
