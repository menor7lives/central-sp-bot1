"""IA do Slayer: entende pedidos, conversa com memória e gera textos profissionais."""
import json
import config
import dados

SYSTEM_PROMPT = """Você é o bot "Slayer Bot" em um servidor do Discord.
Responda SEMPRE em português brasileiro, direto e amigável.

Você deve responder SOMENTE com um JSON válido, em um destes formatos:

1. Se o usuário pedir para criar/montar/configurar um servidor (com canais, cargos,
   categorias e permissões), use um template pronto quando encaixar:
{"action": "build_server", "template": "futebol", "guild_name": "nome escolhido"}

Templates disponíveis: "futebol" (clube profissional), "comunidade", "gaming",
"fivem" (cidade RP FiveM), "mta" (servidor MTA SA de GTA), "loja" (e-commerce),
"empresa" (corporação), "studio" (estúdio musical), "cla" (clã de e-sports),
"minecraft", "youtube" (criadores de conteúdo), "anime" (otaku),
"estudos" (escola/faculdade), "suporte" (atendimento técnico),
"design" (agência criativa), "podcast", "eventos".

2. Se ele pedir algo que não encaixa em nenhum template, gere um spec customizado:
{"action": "build_server", "template": "custom", "guild_name": "nome", "spec": {
  "name": "nome do servidor",
  "roles": [{"name": "Cargo", "color": 3447003, "permissions": ["manage_messages"], "hoist": true}],
  "categories": [{"name": "CATEGORIA", "channels": [
      {"name": "canal-texto", "type": "text", "overwrites": {"@everyone": {"allow": ["view_channel"], "deny": ["send_messages"]}}},
      {"name": "Canal de Voz", "type": "voice"}]}]}}

REGRAS DE PERMISSÕES:
Nunca conceda estas permissões aos cargos gerados:
administrator, manage_guild, manage_channels, manage_roles.

Permissões comuns permitidas:
manage_messages, kick_members, ban_members, view_channel,
send_messages, attach_files, add_reactions, connect, speak,
moderate_members.

Cargos hierárquicos representam patente e autoridade interna,
não devem receber automaticamente permissões administrativas do Discord.
Nunca conceda permissões perigosas apenas porque o cargo tem nome de comandante,
diretor, dono, presidente ou administrador.

3. Se for só conversa, pergunta ou outro pedido:
{"action": "chat", "reply": "sua resposta"}

Nunca inclua texto fora do JSON."""

KEYWORD_MAP = [
    (("futebol", "clube", "time de futebol", "soccer"), "futebol"),
    (("fivem", "five m", "cidade de rp", "roleplay", " rp", "gta"), "fivem"),
    (("mta", "multi theft", "san andreas", "samp"), "mta"),
    (("minecraft", "servidor de mc"), "minecraft"),
    (("youtube", "youtuber", "criadores de conteúdo", "criacao de conteudo"), "youtube"),
    (("anime", "mangá", "manga", "otaku", "weeb"), "anime"),
    (("estudo", "estudos", "escola", "faculdade", "colegial", "educação"), "estudos"),
    (("suporte técnico", "suporte tecnico", "atendimento", "helpdesk", "central de ajuda"), "suporte"),
    (("design", "designer", "agência", "agencia"), "design"),
    (("podcast", "podcaster"), "podcast"),
    (("evento", "eventos", "festa"), "eventos"),
    (("comunidade", "community"), "comunidade"),
    (("gaming", "jogos", "game", "gamer"), "gaming"),
    (("loja", "shop", "store", "e-commerce", "ecommerce", "vender", "vendas", "mercado"), "loja"),
    (("empresa", "corporação", "corporacao", "corporativo", "business", "firma", "negócio", "negocio"), "empresa"),
    (("estúdio", "estudio", "musical", "música", "music", "gravadora", "records", "beat"), "studio"),
    (("clã", "cla", "clan", "e-sports", "esports", "e sports", "equipe competitiva", "time competitivo"), "cla"),
]


# palavras que o bot recusa (conteúdo adulto é proibido no Discord)
BLOCKED_WORDS = (
    "porno", "pornô", "porn", "pornografia", "nsfw", "+18", "18+",
    "hentai", "sexo", "sexual", "nudez", "nudes", "xxx", "putaria",
    "onlyfans", "tranny", "escort", "garota de programa", "cuzinho",
)


def _is_blocked(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in BLOCKED_WORDS)


BLOCKED_REPLY = (
    "🚫 **Não posso criar esse tipo de servidor!**\n"
    "Conteúdo adulto é **proibido pelas regras do Discord** e pode fazer o servidor "
    "e o bot serem banidos.\n\n"
    "✅ Posso criar: **futebol, comunidade, gaming, Minecraft, MTA, FiveM, loja, "
    "empresa, estúdio, clã** e muito mais. É só pedir!"
)


async def get_intent(message_text: str, author: str) -> dict:
    """Retorna {"action": "chat"|"build_server", ...}."""
    if _is_blocked(message_text):
        return {"action": "chat", "reply": BLOCKED_REPLY}
    if config.AI_API_KEY:
        result = await _ask_ai(message_text, author)
        if result:
            if _is_blocked(str(result)):
                return {"action": "chat", "reply": BLOCKED_REPLY}
            return result
    return _fallback(message_text)


async def _chat(mensagens) -> str | None:
    """Chamada de chat comum (resposta em texto livre)."""
    import aiohttp
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(
                f"{config.AI_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {config.AI_API_KEY}"},
                json={"model": config.AI_MODEL,
                      "messages": mensagens, "temperature": 0.8},
                timeout=aiohttp.ClientTimeout(total=30),
            ) as r:
                data = await r.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


async def _ask_ai(message_text: str, author: str) -> dict | None:
    import aiohttp
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(
                f"{config.AI_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {config.AI_API_KEY}"},
                json={
                    "model": config.AI_MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Usuário {author} disse: {message_text}"},
                    ],
                    "temperature": 0.3,
                },
                timeout=aiohttp.ClientTimeout(total=30),
            ) as r:
                data = await r.json()
        content = data["choices"][0]["message"]["content"].strip()
        content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(content)
    except Exception:
        return None


BUILD_VERBS = ("criar", "crie", "montar", "monte", "cria", "configurar", "configure",
               "monta", "faz", "faça", "faca", "quero", "preciso", "montagem", "setar")


def _fallback(text: str) -> dict:
    t = text.lower()
    mentions_template = any(any(w in t for w in words) for words, _ in KEYWORD_MAP)
    wants_build = any(w in t for w in BUILD_VERBS) or "servidor" in t
    if mentions_template and wants_build:
        for words, template in KEYWORD_MAP:
            if any(w in t for w in words):
                return {"action": "build_server", "template": template}
    if any(w in t for w in BUILD_VERBS) and "servidor" in t:
        return {"action": "build_server", "template": "comunidade"}
    return {
        "action": "chat",
        "reply": (
            "🤖 **Consigo fazer tudo por aqui!** Me mencione e peça, por exemplo:\n"
            "> `@Slayer BOT crie um servidor profissional de futebol`\n"
            "> `@Slayer BOT monte um servidor de minecraft`\n"
            "> `@Slayer BOT painel` — abre o painel completo\n"
            "> `@Slayer BOT premium` — personalização exclusiva\n"
            "Ou só converse comigo à vontade! 😉"
        ),
    }


# ---------------- conversa com memória + personalidade ----------------
PERSONALIDADE_PROMPT = """Você é o "Slayer BOT", assistente de um servidor do Discord.
Sua personalidade: {personalidade}.
Responda em português brasileiro, natural e útil, em no máximo 3 parágrafos curtos.
Você monta servidores completos, cria sites, gerencia tickets, moderação e automação
quando pedido — quando alguém pedir algo do tipo, confirme e oriente usar os comandos."""


async def conversar(gid, uid, texto) -> str | None:
    """Conversa com memória por usuário e personalidade do servidor (se premium)."""
    if not config.AI_API_KEY or _is_blocked(texto):
        return None
    d = dados.get(gid)
    personalidade = d.get("personalidade") or "amigável, direta e profissional"
    historico = []
    if d.get("memoria_ativa", True):
        historico = d["memoria"].get(str(uid), [])[-10:]

    mensagens = [{"role": "system",
                  "content": PERSONALIDADE_PROMPT.format(personalidade=personalidade)}]
    for h in historico:
        mensagens.append({"role": "user", "content": h["r"]})
        mensagens.append({"role": "assistant", "content": h["s"]})
    mensagens.append({"role": "user", "content": texto[:1500]})

    resposta = await _chat(mensagens)
    if resposta:
        historico.append({"r": texto[:500], "s": resposta[:800]})
        d["memoria"][str(uid)] = historico[-10:]
        dados.salvar()
    return resposta


def limpar_memoria(gid, uid) -> int:
    d = dados.get(gid)
    n = len(d["memoria"].pop(str(uid), []))
    dados.salvar()
    return n


# ---------------- geradores de texto profissional ----------------
REGRAS_PADRAO = (
    "📜 **REGRAS DO SERVIDOR** — {tema}\n\n"
    "**1.** Respeite todos os membros — sem ofensas, racismo, homofobia ou qualquer "
    "tipo de discriminação.\n"
    "**2.** Proibido spam, flood ou poluir os canais com mensagens repetidas.\n"
    "**3.** Não divulgue links, convites ou propaganda sem permissão da staff.\n"
    "**4.** Mantenha cada assunto no canal certo (leia os tópicos dos canais).\n"
    "**5.** Proibido conteúdo +18, NSFW ou ilegal (regras do Discord).\n"
    "**6.** Não compartilhe dados pessoais (seus ou de outros).\n"
    "**7.** Denúncias e problemas: use o sistema de tickets ou fale com a staff.\n"
    "**8.** Respeite as decisões da administração — divergências no canal adequado.\n"
    "**9.** Contas falsas, self-bot e emoji de terceiros = punição imediata.\n"
    "**10.** Desconhecimento das regras não desculpa quebra.\n\n"
    "⚖️ **Punições:** advertência → timeout → ban. Grave = punição direta."
)

ANUNCIO_PADRAO = (
    "📢 **{titulo}**\n\n"
    "{detalhes}\n\n"
    "📣 Comunicado oficial da equipe — {data}.\n"
    "Dúvidas? Fale com a staff ou abra um ticket. 🎫"
)

BOAS_VINDAS_PADRAO = (
    "Três opções de mensagem de boas-vindas:\n\n"
    "**1.** Bem-vindo(a) {membro} ao **{servidor}**! Leia as regras e aproveite "
    "a comunidade. 🎉\n\n"
    "**2.** Chegou gente boa! {membro}, seja bem-vindo(a) ao **{servidor}** — "
    "pegue seus cargos e se apresente. 👋\n\n"
    "**3.** ⚔️ **{servidor}** ganhou um reforço: {membro}! Boas-vindas, "
    "qualquer coisa chama a staff. 💜"
)


async def gerar_regras(tema: str) -> str:
    if config.AI_API_KEY:
        r = await _chat([
            {"role": "system",
             "content": "Você escreve regras de servidores de Discord de forma profissional, "
                        "numeradas, em português do Brasil, com emojis moderados."},
            {"role": "user",
             "content": f"Crie 10 regras completas para um servidor de {tema}. "
                        f"Termine com a linha de punições (advertência → timeout → ban)."},
        ])
        if r:
            return r
    return REGRAS_PADRAO.format(tema=tema or "comunidade")


async def gerar_anuncio(titulo: str, detalhes: str = "") -> str:
    if config.AI_API_KEY:
        r = await _chat([
            {"role": "system",
             "content": "Você redige comunicados oficiais de Discord de forma profissional "
                        "e impactante, em português do Brasil."},
            {"role": "user",
             "content": f"Escreva um anúncio sobre: {titulo}. "
                        f"Detalhes: {detalhes or 'crie você mesmo'}. Use markdown."},
        ])
        if r:
            return r
    import datetime
    data = datetime.date.today().strftime("%d/%m/%Y")
    return ANUNCIO_PADRAO.format(titulo=titulo or "Comunicado",
                                 detalhes=detalhes or "(detalhes em breve)", data=data)


async def sugerir_boas_vindas(nome_servidor: str = "") -> str:
    if config.AI_API_KEY:
        r = await _chat([
            {"role": "system", "content": "Você cria mensagens de boas-vindas curtas e "
                                          "criativas para Discord, em português do Brasil."},
            {"role": "user",
             "content": "Gere 3 opções de mensagem de boas-vindas usando os marcadores "
                        "{membro} e {servidor}."},
        ])
        if r:
            return r
    return BOAS_VINDAS_PADRAO.format(membro="{membro}", servidor=nome_servidor or "{servidor}")
