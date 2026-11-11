"""Modelos de servidores profissionais — estilo completo para venda."""

# ---------- helpers ----------
def _role(name, color=0x99AAB5, perms=(), hoist=False):
    return {"name": name, "color": color, "permissions": list(perms), "hoist": hoist}

def _cat(name, channels, overwrites=None):
    return {"name": name, "channels": channels, "overwrites": overwrites or {}}

def _txt(name, overwrites=None):
    return {"name": name, "type": "text", "overwrites": overwrites or {}}

def _vc(name, overwrites=None, limit=None):
    return {"name": name, "type": "voice", "overwrites": overwrites or {}, "user_limit": limit}

def _lock(*allow):
    return {"@everyone": {"allow": [], "deny": ["view_channel"]},
            **{a: {"allow": ["view_channel"], "deny": []} for a in allow}}

def _readonly(*allow):
    return {"@everyone": {"allow": ["view_channel"], "deny": ["send_messages"]},
            **{a: {"allow": ["view_channel", "send_messages"], "deny": []} for a in allow}}



# ---------- 🏆 FUTEBOL PROFISSIONAL (ULTIMATE) ----------
def futebol(name="CF Central São Paulo ⚽"):
    # CARGOS
    PRES = "🎯・Presidente"
    VICE = "💼・Vice-Presidente"
    DIR = "👔・Diretoria"
    CEO = "🏛️・CEO do Clube"
    FIN = "💰・Financeiro"
    JUR = "⚖️・Jurídico"
    MKT = "📣・Marketing"
    COM = "🤝・Comercial"
    COORD = "🧠・Coordenador"
    TEC = "📋・Treinador"
    AUX = "📑・Auxiliar-Técnico"
    PREP = "🏋️・Preparador-Físico"
    GOLEIRO = "🧤・Treinador-de-Goleiros"
    MED = "🩺・Departamento-Médico"
    FISIO = "💉・Fisioterapeuta"
    ANA = "📊・Analista-de-Desempenho"
    OLH = "🔎・Olheiro"
    PSICO = "🧠・Psicólogo"
    CAP = "©️・Capitão"
    SUBCAP = "🥈・Vice-Capitão"
    ELENCO = "⚽・Elenco-Profissional"
    RESERVA = "🔄・Reservas"
    BASE = "🌱・Categoria-de-Base"
    SUB20 = "⭐・Sub-20"
    SUB17 = "🌟・Sub-17"
    SUB15 = "⚡・Sub-15"
    GOLD = "🏅・Sócio-Gold"
    SOCIO = "🎖️・Sócio-Torcedor"
    TORCIDA = "🥁・Torcida-Organizada"
    IMPRENSA = "📰・Imprensa"
    PARC = "🤝・Parceiro"
    PATRO = "💎・Patrocinador"
    VIP = "👑・VIP"

    DIRECAO = (PRES, VICE, DIR, CEO)
    STAFF_TEC = (COORD, TEC, AUX, PREP, GOLEIRO, ANA)

    return {
        "name": name,

        # ---------- CARGOS ----------
        "roles": [
            _role(PRES, 0xD4AF37, ["administrator"], True),
            _role(VICE, 0xF1C40F, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log"], True),
            _role(DIR, 0x1ABC9C, ["manage_channels", "manage_messages", "view_audit_log"], True),
            _role(CEO, 0x8E44AD, ["manage_messages", "view_audit_log"], True),
            _role(FIN, 0x2ECC71, [], True),
            _role(JUR, 0x34495E, [], True),
            _role(MKT, 0xE91E63, ["manage_messages", "embed_links", "attach_files"], True),
            _role(COM, 0x16A085, [], True),
            _role(COORD, 0x5B6DD1, ["manage_messages"], True),
            _role(TEC, 0x3498DB, ["manage_messages"], True),
            _role(AUX, 0x2980B9, [], True),
            _role(PREP, 0x11806A, [], True),
            _role(GOLEIRO, 0x00A8A8, [], True),
            _role(MED, 0xE74C3C, [], True),
            _role(FISIO, 0xC0392B, [], True),
            _role(ANA, 0x9B59B6, ["attach_files", "embed_links"], True),
            _role(OLH, 0xE67E22, [], True),
            _role(PSICO, 0xA569BD, [], True),
            _role(CAP, 0xFFD700, [], True),
            _role(SUBCAP, 0xBDC3C7, [], True),
            _role(ELENCO, 0x2ECC71, ["attach_files", "add_reactions", "embed_links"], True),
            _role(RESERVA, 0x27AE60, ["attach_files", "add_reactions"], True),
            _role(BASE, 0xA3E4B0, ["add_reactions"], True),
            _role(SUB20, 0x76D7C4, [], True),
            _role(SUB17, 0x48C9B0, [], True),
            _role(SUB15, 0x45B39D, [], True),
            _role(GOLD, 0xFFD700, ["attach_files", "add_reactions", "embed_links"], True),
            _role(SOCIO, 0xE67E22, ["add_reactions", "embed_links"], True),
            _role(TORCIDA, 0xE74C3C, ["add_reactions"], True),
            _role(IMPRENSA, 0x95A5A6, ["attach_files", "embed_links"], True),
            _role(PARC, 0x1ABC9C, [], True),
            _role(PATRO, 0xF4D03F, [], True),
            _role(VIP, 0x9B59B6, [], True),

            _role("📢・Torcedor", 0x99AAB5, ["add_reactions"]),
            _role("👥・Membro", 0x99AAB5, ["add_reactions"]),
            _role("🆕・Novato", 0x7289DA, []),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],

        # ---------- CATEGORIAS ----------
        "categories": [

            _cat("📢・INFORMAÇÕES-OFICIAIS", [
                _txt("📜・regras"),
                _txt("📣・anúncios"),
                _txt("📅・calendário"),
                _txt("🏆・competições"),
                _txt("📖・história-do-clube"),
                _txt("🏛️・identidade-do-clube"),
                _txt("📋・estatuto"),
                _txt("❓・perguntas-frequentes"),
                _txt("🗳️・sugestões"),
                _txt("📌・avisos-importantes"),
            ], _readonly(*DIRECAO)),

            _cat("🏟️・CENTRAL-DO-CLUBE", [
                _txt("💬・chat-geral"),
                _txt("🎤・apresente-se"),
                _txt("📸・mídia-do-clube"),
                _txt("🎫・ingressos"),
                _txt("🎖️・planos-de-sócio"),
                _txt("🤝・parcerias"),
                _txt("👕・loja-oficial"),
                _txt("📍・localização-e-estádio"),
            ]),

            _cat("📰・IMPRENSA-E-MÍDIA", [
                _txt("🗞️・notícias-oficiais"),
                _txt("🎙️・entrevistas"),
                _txt("📸・fotografias"),
                _txt("🎬・bastidores"),
                _txt("📺・vídeos"),
                _txt("📊・estatísticas"),
                _txt("⭐・destaques-da-rodada"),
                _txt("🏅・premiações"),
            ], _readonly(*DIRECAO, MKT, IMPRENSA)),

            _cat("⚽・FUTEBOL-PROFISSIONAL", [
                _txt("👥・lista-de-jogadores"),
                _txt("📋・escalação"),
                _txt("🧠・táticas-e-estratégias"),
                _txt("🏋️・treinamentos"),
                _txt("📅・agenda-de-treinos"),
                _txt("📢・convocações"),
                _txt("📊・desempenho-individual"),
                _txt("🏆・metas-da-temporada"),
                _txt("🔄・substituições"),
                _txt("📝・relatório-de-partidas"),
                _vc("🧥・vestiário"),
                _vc("📋・sala-tática"),
                _vc("⚽・treinamento"),
            ], _lock(*DIRECAO, *STAFF_TEC, ELENCO, RESERVA)),

            _cat("🧤・GOLEIROS", [
                _txt("🧤・equipe-de-goleiros"),
                _txt("🏋️・treino-de-goleiros"),
                _txt("📊・estatísticas-de-goleiros"),
                _vc("🥅・treinamento-de-goleiros"),
            ], _lock(*DIRECAO, GOLEIRO, PREP, ELENCO, RESERVA)),

            _cat("🌱・CATEGORIAS-DE-BASE", [
                _txt("💬・chat-da-base"),
                _txt("⭐・sub-20"),
                _txt("🌟・sub-17"),
                _txt("⚡・sub-15"),
                _txt("🏋️・treinos-da-base"),
                _txt("📋・avaliação-de-atletas"),
                _txt("📢・convocações-da-base"),
                _txt("🔎・observação-de-jovens"),
                _vc("🧥・vestiário-da-base"),
                _vc("⚽・treinos-da-base"),
            ], _lock(*DIRECAO, *STAFF_TEC, BASE, SUB20, SUB17, SUB15)),

            _cat("🩺・DEPARTAMENTO-MÉDICO", [
                _txt("🩺・comunicados-médicos"),
                _txt("💉・fisioterapia"),
                _txt("🏥・recuperação"),
                _txt("📋・liberação-para-jogos"),
                _txt("🏋️・condicionamento-físico"),
                _vc("🏥・enfermaria"),
            ], _lock(*DIRECAO, MED, FISIO, PREP)),

            _cat("🔄・MERCADO-DA-BOLA", [
                _txt("📢・contratações-oficiais"),
                _txt("💱・negociações"),
                _txt("📄・contratos"),
                _txt("🔁・empréstimos"),
                _txt("🚪・saídas-do-clube"),
                _txt("🗣️・rumores"),
                _txt("🔎・jogadores-disponíveis"),
                _txt("📑・propostas-recebidas"),
            ], _lock(*DIRECAO, FIN, COORD, OLH, JUR)),

            _cat("🔍・SCOUTING-E-OBSERVAÇÃO", [
                _txt("🔎・relatórios-de-scouting"),
                _txt("🗺️・observação-de-jogadores"),
                _txt("📥・pedidos-de-análise"),
                _txt("📊・estatísticas-de-atletas"),
                _txt("⭐・talentos-promissores"),
            ], _lock(*DIRECAO, COORD, OLH, ANA)),

            _cat("💼・DIRETORIA-E-ADMINISTRAÇÃO", [
                _txt("🗂️・reuniões"),
                _txt("💰・finanças"),
                _txt("📈・planejamento"),
                _txt("📑・documentos"),
                _txt("⚖️・assuntos-jurídicos"),
                _txt("📨・denúncias-e-recursos"),
                _txt("🤝・negociações-comerciais"),
                _txt("📊・relatórios-administrativos"),
                _vc("💼・sala-da-diretoria"),
                _vc("🏛️・reunião-privada"),
            ], _lock(*DIRECAO, FIN, JUR, COM)),

            _cat("📣・MARKETING-E-PATROCÍNIOS", [
                _txt("📢・campanhas"),
                _txt("💎・patrocinadores"),
                _txt("🤝・parceiros-oficiais"),
                _txt("👕・uniformes"),
                _txt("📸・divulgação"),
                _txt("📈・resultados-de-campanhas"),
            ], _lock(*DIRECAO, MKT, COM)),

            _cat("🥁・TORCIDA-ORGANIZADA", [
                _txt("🥁・central-da-torcida"),
                _txt("🎶・cânticos-e-músicas"),
                _txt("🚩・caravanas"),
                _txt("🎉・dia-de-jogo"),
                _txt("📸・fotos-da-torcida"),
                _txt("💬・resenha-da-torcida"),
                _vc("🥁・arquibancada"),
                _vc("🎉・festa-da-torcida"),
            ]),

            _cat("🏆・COMPETIÇÕES-E-PARTIDAS", [
                _txt("📅・agenda-de-jogos"),
                _txt("⚽・próximas-partidas"),
                _txt("📋・resultados"),
                _txt("📊・classificação"),
                _txt("🥇・artilharia"),
                _txt("🧤・melhores-goleiros"),
                _txt("⭐・melhor-jogador"),
                _txt("🎯・palpites"),
                _txt("📸・melhores-momentos"),
            ]),

            _cat("🎙️・VOZ-DO-ESTÁDIO", [
                _vc("🎙️・palco-vip", limit=10),
                _vc("🎉・hall-do-clube"),
                _vc("🥁・torcida-organizada", limit=50),
                _vc("📺・transmissão-ao-vivo"),
                _vc("🎤・coletiva-de-imprensa"),
                _vc("💬・resenha-livre"),
            ]),

            _cat("🎫・ATENDIMENTO-E-SUPORTE", [
                _txt("🎫・abrir-atendimento"),
                _txt("❓・dúvidas"),
                _txt("📨・contato-com-a-diretoria"),
                _txt("📝・recrutamento"),
                _txt("⚽・inscrição-para-peneira"),
            ]),

            _cat("🤖・SISTEMA-E-BOTS", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
                _txt("🎮・diversão"),
                _txt("📌・registros"),
            ]),

            _cat("🎟️・SÓCIOS-E-ATENDIMENTO", [
                _txt("🎫・central-de-atendimento"),
                _txt("🪪・cadastro-de-sócios"),
                _txt("💳・pagamentos-de-sócios"),
                _txt("🎁・benefícios-e-vantagens"),
                _txt("📨・solicitações"),
            ]),
            _cat("📅・EVENTOS-DO-CLUBE", [
                _txt("📆・agenda-de-eventos"),
                _txt("🎉・eventos-exclusivos"),
                _txt("🗳️・votação-da-torcida"),
                _txt("🏅・reconhecimento-de-atletas"),
                _vc("🎙️・eventos-ao-vivo"),
            ]),
        ],
    }



# ---------- 🏘️ COMUNIDADE (completo) ----------
def comunidade(name="Central São Paulo 🏘️"):
    DONO = "👑・Dono"
    ADM = "⚙️・Administrador"
    MOD = "🛡️・Moderador"
    HELPER = "🎓・Ajudante"
    YOUTUBER = "🎬・Criador-de-Conteúdo"
    VERIF = "✅・Membro-Verificado"
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xD4AF37, ["administrator"], True),
            _role(ADM, 0xE74C3C, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log", "mention_everyone"], True),
            _role(MOD, 0x1ABC9C, ["manage_messages", "kick_members", "manage_channels", "view_audit_log"], True),
            _role(HELPER, 0x3498DB, ["manage_messages"], True),
            _role(YOUTUBER, 0xE91E63, ["attach_files", "embed_links", "mention_everyone"], True),
            _role("🎓・Veterano", 0x9B59B6, ["attach_files", "embed_links"], True),
            _role(VERIF, 0x2ECC71, ["attach_files", "add_reactions"], True),
            _role("👥・Membro", 0x99AAB5, ["add_reactions"]),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],
        "categories": [
            _cat("📢・INFORMAÇÕES", [
                _txt("📜・regras"),
                _txt("📣・anúncios"),
                _txt("❓・faq"),
                _txt("🗺️・guia-do-servidor"),
                _txt("🗳️・sugestões"),
                _txt("🔔・atualizações"),
            ], _readonly(DONO, ADM, MOD)),
            _cat("💬・COMUNIDADE", [
                _txt("💬・chat-geral"),
                _txt("🎤・apresente-se"),
                _txt("🎨・mídia-e-arte"),
                _txt("🧵・off-topic"),
                _txt("🎂・aniversários"),
                _txt("😴・bom-dia-e-boa-noite"),
            ]),
            _cat("🎮・DIVERSÃO", [
                _txt("🎲・jogos-e-desafios"),
                _txt("🎁・sorteios"),
                _txt("🏆・rankings-e-eventos"),
                _txt("🧩・quiz"),
                _txt("🎵・música"),
                _txt("🍜・comidas-e-receitas"),
                _txt("📺・filmes-e-séries"),
            ]),
            _cat("🎙️・VOZ", [
                _vc("🎙️・voz-geral"),
                _vc("🎧・música-voz"),
                _vc("🎮・squad-1"),
                _vc("🎮・squad-2"),
                _vc("🤫・consulta-privada"),
            ]),
            _cat("🎬・CRIADORES-DE-CONTEÚDO", [
                _txt("📢・divulgue-seu-canal"),
                _txt("🎥・vídeos-e-lives"),
                _txt("📸・clips-e-melhores-momentos"),
                _txt("🤝・colabs"),
            ], _readonly(DONO, ADM, MOD, YOUTUBER)),
            _cat("🛠️・EQUIPE", [
                _txt("🔧・staff-chat"),
                _txt("📋・mod-logs"),
                _txt("📨・denúncias"),
                _txt("🗂️・reuniões-da-equipe"),
                _vc("🛠️・sala-da-equipe"),
            ], _lock(DONO, ADM, MOD, HELPER)),
            _cat("🤖・BOT", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
            ]),

            _cat("🎫・CENTRAL-DE-ATENDIMENTO", [
                _txt("🎫・abrir-ticket"),
                _txt("❓・ajuda-e-dúvidas"),
                _txt("📨・denúncias-da-comunidade"),
                _txt("💡・ideias-para-o-servidor"),
            ]),
            _cat("🎉・EVENTOS-E-PROJETOS", [
                _txt("📅・agenda-de-eventos"),
                _txt("🏆・inscrições-e-competições"),
                _txt("🎁・resultados-de-sorteios"),
                _txt("📸・memórias-da-comunidade"),
                _vc("🎉・evento-da-comunidade"),
            ]),
        ],
    }


# ---------- 🎮 GAMING (completo) ----------
def gaming(name="Central SP Gaming 🎮"):
    DONO = "👑・Dono"
    ADM = "⚙️・Administrador"
    MOD = "🛡️・Moderador"
    COACH = "🎯・Coach"
    PRO = "🏆・Pro-Player"
    ESCR = "📋・Escritor-e-Narrador"
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xD4AF37, ["administrator"], True),
            _role(ADM, 0xE74C3C, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log", "mention_everyone"], True),
            _role(MOD, 0x1ABC9C, ["manage_messages", "kick_members", "manage_channels", "view_audit_log"], True),
            _role(COACH, 0x5B6DD1, ["manage_messages"], True),
            _role(PRO, 0x9B59B6, ["attach_files", "embed_links", "priority_speaker"], True),
            _role(ESCR, 0x3498DB, ["attach_files", "embed_links"], True),
            _role("🎮・Jogador", 0x3498DB, ["attach_files", "add_reactions"], True),
            _role("🕹️・Streamer", 0xE91E63, ["attach_files", "embed_links"], True),
            _role("👥・Membro", 0x99AAB5, ["add_reactions"]),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],
        "categories": [
            _cat("📢・INFORMAÇÕES", [
                _txt("📜・regras"),
                _txt("📣・anúncios"),
                _txt("🏆・ranking"),
                _txt("🗓️・calendário-de-torneios"),
                _txt("❓・faq"),
                _txt("🗳️・sugestões"),
            ], _readonly(DONO, ADM, MOD)),
            _cat("🎮・COMUNIDADE", [
                _txt("💬・chat-geral"),
                _txt("🎤・apresente-se"),
                _txt("🕹️・achar-squad"),
                _txt("📸・clips-e-plays"),
                _txt("🖥️・setup-e-periféricos"),
                _txt("🎁・giveaways"),
                _txt("😂・memes"),
            ]),
            _cat("🏆・COMPETITIVO", [
                _txt("⚔️・torneios-e-campeonatos"),
                _txt("📋・resultados"),
                _txt("🧠・meta-e-estratégias"),
                _txt("🎯・treinos-e-coach"),
                _txt("📊・estatísticas"),
            ], _readonly(DONO, ADM, MOD, COACH, PRO)),
            _cat("🎮・JOGOS-POPULARES", [
                _txt("🔫・fps"),
                _txt("⚔️・moba"),
                _txt("🌍・battle-royale"),
                _txt("🏎️・corrida"),
                _txt("🧟・survival"),
                _txt("⚽・esports-futebol"),
            ]),
            _cat("🎙️・VOZ", [
                _vc("🎮・squad-1"),
                _vc("🎮・squad-2"),
                _vc("🎮・squad-3"),
                _vc("🏆・treinamento-competitivo"),
                _vc("🎧・música"),
                _vc("🗣️・café-do-gamer"),
                _vc("📺・assistir-juntos"),
            ]),
            _cat("🎥・STREAMERS", [
                _txt("📺・lives-e-vídeos"),
                _txt("📣・divulgue-seu-canal"),
                _txt("🤝・colabs-e-equipes"),
            ], _readonly(DONO, ADM, MOD, "🕹️・Streamer", ESCR)),
            _cat("🛠️・EQUIPE", [
                _txt("🔧・staff-chat"),
                _txt("📋・mod-logs"),
                _txt("📨・denúncias"),
                _vc("🛠️・sala-da-equipe"),
            ], _lock(DONO, ADM, MOD)),
            _cat("🤖・BOT", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
            ]),

            _cat("🎫・SUPORTE-E-RECRUTAMENTO", [
                _txt("🎫・abrir-ticket"),
                _txt("🧩・problemas-técnicos"),
                _txt("📝・recrutamento-de-equipes"),
                _txt("🚨・reportar-jogador"),
            ]),
            _cat("🎉・EVENTOS-E-CAMPEONATOS", [
                _txt("📅・agenda-competitiva"),
                _txt("📝・inscrições"),
                _txt("📊・tabelas-e-chaves"),
                _txt("🏅・hall-da-fama"),
                _vc("🏆・transmissão-de-campeonato"),
            ]),
        ],
    }


# ---------- 🚗 FIVEM / RP (completo) ----------
def fivem(name="Central SP RP 🚔"):
    DONO = "👑・Dono"
    DEV = "🧑‍💻・Developer"
    ADM = "⚙️・Administrador"
    MOD = "🛡️・Moderador"
    SUP = "🎧・Suporte"
    WH = "📝・Whitelist"
    POL = "👮・Polícia"
    EMS = "🚑・EMS"
    ADV = "⚖️・Advogado"
    JUD = "👨‍⚖️・Juiz"
    JORN = "🎙️・Jornalista"
    MEC = "🔧・Mecânico"
    VEND = "💼・Vendedor"
    STAFF = (DONO, ADM, MOD, DEV)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xD4AF37, ["administrator"], True),
            _role(DEV, 0x1ABC9C, ["manage_webhooks", "manage_messages", "attach_files", "embed_links"], True),
            _role(ADM, 0xE74C3C, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log", "mention_everyone"], True),
            _role(MOD, 0x1ABC9C, ["manage_messages", "kick_members", "ban_members", "manage_channels", "view_audit_log"], True),
            _role(SUP, 0x3498DB, ["manage_messages"], True),
            _role(WH, 0x2ECC71, ["manage_messages", "view_audit_log"], True),
            _role(POL, 0x3498DB, [], True),
            _role(EMS, 0xE74C3C, [], True),
            _role(ADV, 0x9B59B6, [], True),
            _role(JUD, 0x8E44AD, [], True),
            _role(JORN, 0xE67E22, ["attach_files", "embed_links"], True),
            _role(MEC, 0x95A5A6, [], True),
            _role(VEND, 0xF1C40F, [], True),
            _role("👤・Civil", 0x99AAB5, ["attach_files", "add_reactions"]),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],
        "categories": [
            _cat("📢・INFORMAÇÕES", [
                _txt("📜・regras-da-cidade"),
                _txt("📣・anúncios"),
                _txt("🔗・conectar-e-requisitos"),
                _txt("❓・faq"),
                _txt("🗺️・mapa-da-cidade"),
                _txt("🆕・changelog-e-atualizações"),
                _txt("🗳️・sugestões"),
            ], _readonly(*STAFF)),
            _cat("📝・WHITELIST", [
                _txt("📝・aplique-aqui"),
                _txt("📋・resultados"),
                _txt("📕・apostila-do-cidadão"),
                _txt("🚔・normas-legais"),
            ], _readonly(*STAFF, WH)),
            _cat("🌍・CIDADE", [
                _txt("💬・chat-geral"),
                _txt("📸・prints-da-cidade"),
                _txt("🎬・clips-e-moments"),
                _txt("🚨・boletim-de-ocorrências"),
                _txt("📻・rádio-notícias"),
                _vc("🌍・voz-global"),
                _vc("🚗・garagem"),
            ]),
            _cat("💼・TRABALHOS-E-EMPRESAS", [
                _txt("🔧・mecânica"),
                _txt("💼・lojas-e-comércio"),
                _txt("⛽・postos-e-transporte"),
                _txt("🍔・restaurantes"),
                _txt("🚕・táxi-e-uber"),
                _txt("🌾・fazendas"),
                _txt("⛏️・garimpo"),
            ]),
            _cat("🏭・FACÇÕES-CRIMINOSAS", [
                _txt("🚬・chat-geral-facções"),
                _txt("⚰️・roubos-e-assaltos"),
                _txt("🔫・territórios"),
                _txt("🧺・lavagem-de-dinheiro"),
                _vc("🏭・base-1"),
                _vc("🏭・base-2"),
            ], _lock(*STAFF, "👤・Civil")),
            _cat("👮・POLÍCIA", [
                _txt("📋・batalhão"),
                _txt("🎯・operações"),
                _txt("🚨・procurados"),
                _txt("🔒・presos"),
                _vc("🚔・rádio-policia"),
                _vc("🏛️・delegacia"),
            ], _lock(*STAFF, POL)),
            _cat("🚑・EMS", [
                _txt("🏥・hospital"),
                _txt("💉・plantões"),
                _txt("🚁・resgate-aéreo"),
                _vc("🚑・rádio-ems"),
            ], _lock(*STAFF, EMS)),
            _cat("⚖️・JUSTIÇA", [
                _txt("🏛️・tribunal"),
                _txt("⚖️・advocacia"),
                _txt("🧾・processos-e-multas"),
                _vc("👨‍⚖️・sala-do-juiz"),
            ], _lock(*STAFF, ADV, JUD, POL)),
            _cat("🎙️・IMPRENSA", [
                _txt("🗞️・jornal-da-cidade"),
                _txt("📺・reportagens"),
                _txt("🎤・entrevistas"),
            ], _readonly(*STAFF, JORN)),
            _cat("💰・ECONOMIA", [
                _txt("💵・salários-e-bancos"),
                _txt("🏦・investimentos"),
                _txt("📊・mercado-imobiliário"),
                _txt("🚗・concessionárias"),
                _txt("🏠・corretagem"),
            ]),
            _cat("🛠️・STAFF", [
                _txt("🔧・staff-chat"),
                _txt("📋・logs"),
                _txt("📨・denúncias"),
                _txt("🐞・bugs-e-report"),
                _txt("💡・sugestões-da-equipe"),
                _vc("🛠️・sala-da-staff"),
            ], _lock(*STAFF)),
            _cat("🤖・BOT", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
            ]),

            _cat("🎫・ATENDIMENTO-DA-CIDADE", [
                _txt("🎫・abrir-ticket"),
                _txt("📝・revisão-de-whitelist"),
                _txt("🚨・denunciar-jogador"),
                _txt("🐞・reportar-bug"),
                _txt("📨・recorrer-de-punição"),
            ]),
            _cat("🎉・EVENTOS-DA-CIDADE", [
                _txt("📅・agenda-de-eventos"),
                _txt("🏁・corridas-e-encontros"),
                _txt("🎭・eventos-de-roleplay"),
                _txt("🏆・premiações"),
                _vc("🎉・evento-oficial"),
            ]),
        ],
    }


# ---------- 🛒 LOJA / E-COMMERCE (completo) ----------
def loja(name="Central SP Store 🛒"):
    DONO = "👑・Dono"
    ADM = "⚙️・Administrador"
    GER = "👔・Gerente"
    VEND = "💼・Vendedor"
    ESTQ = "📦・Estoquista"
    FIN = "💰・Financeiro"
    SUP = "🎧・Suporte"
    ENT = "🚚・Entregador"
    MKT = "📣・Marketing"
    STAFF = (DONO, ADM, GER, VEND, SUP)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xD4AF37, ["administrator"], True),
            _role(ADM, 0xE74C3C, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log", "mention_everyone"], True),
            _role(GER, 0x1ABC9C, ["manage_messages", "view_audit_log", "mention_everyone"], True),
            _role(VEND, 0x3498DB, ["manage_messages"], True),
            _role(ESTQ, 0x95A5A6, ["attach_files", "embed_links"], True),
            _role(FIN, 0x2ECC71, ["view_audit_log"], True),
            _role(SUP, 0x9B59B6, ["manage_messages"], True),
            _role(ENT, 0xE67E22, ["attach_files"], True),
            _role(MKT, 0xE91E63, ["manage_messages", "embed_links", "attach_files"], True),
            _role("💎・Cliente-VIP", 0xFFD700, ["attach_files", "add_reactions", "embed_links", "priority_speaker"], True),
            _role("✅・Cliente", 0x99AAB5, ["attach_files", "add_reactions"], True),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],
        "categories": [
            _cat("📢・INFORMAÇÕES", [
                _txt("📜・regras-da-loja"),
                _txt("📣・anúncios-e-novidades"),
                _txt("🕒・horário-de-funcionamento"),
                _txt("📍・localização-e-contato"),
                _txt("❓・faq"),
                _txt("🚚・política-de-entrega"),
                _txt("🔄・trocas-e-devoluções"),
            ], _readonly(*STAFF)),
            _cat("🛒・LOJA", [
                _txt("🛍️・catálogo"),
                _txt("🔥・promoções-do-dia"),
                _txt("⭐・lançamentos"),
                _txt("🏷️・cupons-e-descontos"),
                _txt("🎁・fidelidade-e-pontos"),
            ], _readonly(*STAFF, MKT)),
            _cat("🧾・PEDIDOS-ATENDIMENTO", [
                _txt("🛒・faça-seu-pedido"),
                _txt("🧾・acompanhe-seu-pedido"),
                _txt("💳・pagamentos-e-faturas"),
                _txt("🎧・suporte-ao-cliente"),
                _txt("⚠️・reclamações"),
                _txt("⭐・avaliações-e-feedback"),
            ]),
            _cat("📦・LOGÍSTICA", [
                _txt("📦・estoque-e-produtos"),
                _txt("🚚・entregas-em-andamento"),
                _txt("🗺️・rotas-e-zonas"),
                _txt("✅・entregas-concluídas"),
                _vc("🚚・central-de-entregas"),
            ], _lock(DONO, ADM, GER, ESTQ, ENT, VEND)),
            _cat("💼・GESTÃO", [
                _txt("🗂️・reunião-de-equipe"),
                _txt("💰・finanças-e-metas"),
                _txt("📊・relatórios-de-vendas"),
                _txt("🤝・fornecedores"),
                _txt("📈・estratégia-e-crescimento"),
                _vc("💼・sala-de-reuniões"),
            ], _lock(DONO, ADM, GER, FIN)),
            _cat("🤖・BOT", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
            ]),

            _cat("🎫・PÓS-VENDA-E-SUPORTE", [
                _txt("🎫・abrir-ticket"),
                _txt("📦・pedido-atrasado"),
                _txt("🔄・trocas-e-reembolsos"),
                _txt("🧾・comprovantes"),
                _txt("⭐・depoimentos-de-clientes"),
            ]),
            _cat("📣・CAMPANHAS", [
                _txt("🎉・campanhas-especiais"),
                _txt("🎁・sorteios-de-clientes"),
                _txt("📸・clientes-e-resultados"),
            ], _readonly(DONO, ADM, GER, MKT)),
        ],
    }


# ---------- 🏢 EMPRESA / CORPORAÇÃO (completo) ----------
def empresa(name="Central SP Enterprise 🏢"):
    DONO = "👑・CEO"
    DIRETOR = "👔・Diretor"
    GER = "⚙️・Gerente"
    RH = "🧑‍💼・Recursos-Humanos"
    TI = "🧑‍💻・Tecnologia"
    FIN = "💰・Financeiro"
    JUR = "⚖️・Jurídico"
    MKT = "📣・Marketing"
    VEND = "💼・Comercial"
    EST = "🎓・Estagiário"
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xD4AF37, ["administrator"], True),
            _role(DIRETOR, 0xF1C40F, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log", "mention_everyone"], True),
            _role(GER, 0x1ABC9C, ["manage_messages", "view_audit_log", "mention_everyone"], True),
            _role(RH, 0x9B59B6, ["manage_messages"], True),
            _role(TI, 0x3498DB, ["manage_messages", "manage_webhooks"], True),
            _role(FIN, 0x2ECC71, ["view_audit_log"], True),
            _role(JUR, 0x8E44AD, [], True),
            _role(MKT, 0xE91E63, ["manage_messages", "embed_links", "attach_files"], True),
            _role(VEND, 0xE67E22, ["attach_files", "embed_links"], True),
            _role("👨‍💼・Funcionário", 0x99AAB5, ["attach_files", "add_reactions"], True),
            _role(EST, 0xA3E4B0, ["add_reactions"], True),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],
        "categories": [
            _cat("📢・INFORMAÇÕES", [
                _txt("📜・código-de-conduta"),
                _txt("📣・avisos-da-diretoria"),
                _txt("📅・calendário-corporativo"),
                _txt("🏢・sobre-a-empresa"),
                _txt("🏆・metas-e-resultados"),
                _txt("🗳️・caixa-de-sugestões"),
            ], _readonly(DONO, DIRETOR, GER)),
            _cat("💬・INTERAÇÃO", [
                _txt("💬・chat-geral"),
                _txt("☕・pausa-para-o-café"),
                _txt("🎂・aniversariantes-do-mês"),
                _txt("📸・momentos-da-equipe"),
            ]),
            _cat("🧑‍💼・RECURSOS-HUMANOS", [
                _txt("📋・vagas-abertas"),
                _txt("📝・processo-seletivo"),
                _txt("🎓・treinamentos"),
                _txt("📄・documentos-e-políticas"),
                _txt("🏅・reconhecimentos-e-prêmios"),
            ], _readonly(DONO, DIRETOR, GER, RH)),
            _cat("💰・FINANCEIRO", [
                _txt("📊・orçamento-e-fluxo"),
                _txt("🧾・notas-fiscais"),
                _txt("🏦・bancos-e-contas"),
                _txt("📈・investimentos"),
            ], _lock(DONO, DIRETOR, GER, FIN)),
            _cat("🧑‍💻・TECNOLOGIA", [
                _txt("🐞・suporte-de-ti"),
                _txt("🖥️・infraestrutura-e-sistemas"),
                _txt("🔐・segurança-da-informação"),
                _txt("🚀・projetos-e-desenvolvimento"),
                _vc("🖥️・sala-de-ti"),
            ], _lock(DONO, DIRETOR, GER, TI)),
            _cat("⚖️・JURÍDICO", [
                _txt("📄・contratos"),
                _txt("🏛️・processos-e-compliance"),
                _txt("⚖️・consultas-internas"),
            ], _lock(DONO, DIRETOR, GER, JUR)),
            _cat("📣・MARKETING-E-COMERCIAL", [
                _txt("🎯・campanhas-e-estratégia"),
                _txt("📈・relatórios-de-vendas"),
                _txt("🤝・clientes-e-parceiros"),
                _txt("🖼️・materiais-e-criativos"),
                _vc("💼・sala-comercial"),
            ], _lock(DONO, DIRETOR, GER, MKT, VEND)),
            _cat("🎙️・VOZ", [
                _vc("🎙️・reunião-geral"),
                _vc("💼・sala-de-reuniões-1"),
                _vc("💼・sala-de-reuniões-2"),
                _vc("☕・sala-de-descanso"),
            ]),
            _cat("🤖・BOT", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
            ]),

            _cat("📌・PROJETOS-E-TAREFAS", [
                _txt("📋・projetos-em-andamento"),
                _txt("🎯・metas-da-equipe"),
                _txt("📅・prazos-e-entregas"),
                _txt("🧩・solicitações-internas"),
                _vc("🤝・reunião-de-projetos"),
            ]),
            _cat("🎫・SUPORTE-INTERNO", [
                _txt("🎫・solicitar-ajuda"),
                _txt("🖥️・problemas-de-sistema"),
                _txt("📨・solicitações-ao-rh"),
            ], _lock(DONO, DIRETOR, GER, RH, TI)),
        ],
    }


# ---------- 🎵 ESTÚDIO MUSICAL (completo) ----------
def studio(name="Central SP Records 🎵"):
    DONO = "👑・Produtor-Executivo"
    PROD = "🎛️・Produtor"
    ENG = "🎚️・Engenheiro-de-Som"
    ART = "🎤・Artista"
    SONG = "✍️・Compositor"
    DJ = "🎧・DJ"
    MKT = "📣・Marketing"
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xD4AF37, ["administrator"], True),
            _role(PROD, 0x1ABC9C, ["manage_messages", "manage_channels", "view_audit_log"], True),
            _role(ENG, 0x3498DB, ["attach_files", "embed_links", "priority_speaker"], True),
            _role(ART, 0xE91E63, ["attach_files", "embed_links"], True),
            _role(SONG, 0x9B59B6, ["attach_files"], True),
            _role(DJ, 0x2ECC71, ["attach_files", "priority_speaker"], True),
            _role(MKT, 0xE67E22, ["manage_messages", "embed_links"], True),
            _role("🎧・Ouvinte", 0x99AAB5, ["add_reactions"]),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],
        "categories": [
            _cat("📢・INFORMAÇÕES", [
                _txt("📜・regras-do-estúdio"),
                _txt("📣・lançamentos-e-novidades"),
                _txt("🎨・sobre-o-estúdio"),
                _txt("❓・faq"),
            ], _readonly(DONO, PROD, MKT)),
            _cat("🎵・MÚSICA", [
                _txt("🎵・lançamentos"),
                _txt("🆕・prévias-e-premieres"),
                _txt("🎧・playlists-e-recomendações"),
                _txt("📝・letras-e-composições"),
                _txt("🎤・covers-e-remixes"),
            ]),
            _cat("🎛️・PRODUÇÃO", [
                _txt("🎛️・chat-de-produção"),
                _txt("🎼・sessões-de-gravação"),
                _txt("🎚️・mixagem-e-masterização"),
                _txt("🥁・beats-e-instrumentais"),
                _vc("🎚️・sala-de-gravação"),
                _vc("🎧・cabine-de-voz"),
            ], _lock(DONO, PROD, ENG, ART, SONG)),
            _cat("🎬・DIVULGAÇÃO", [
                _txt("📺・clipes-e-vídeos"),
                _txt("📻・podcasts-e-entrevistas"),
                _txt("📣・campanhas-e-divulgação"),
                _txt("🤝・parceiros-e-selos"),
            ], _readonly(DONO, PROD, MKT)),
            _cat("🎉・EVENTOS", [
                _txt("📅・agenda-de-shows"),
                _txt("🎪・eventos-e-festivais"),
                _txt("🎫・ingressos-e-lotes"),
                _vc("🎪・evento-ao-vivo"),
            ]),
            _cat("🤖・BOT", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
            ]),

            _cat("📂・CLIENTES-E-PROJETOS", [
                _txt("📝・novos-projetos"),
                _txt("📆・cronograma-de-entregas"),
                _txt("🎧・feedback-de-clientes"),
                _txt("📦・arquivos-e-entregáveis"),
            ], _lock(DONO, PROD, ENG, ART, SONG, MKT)),
            _cat("🎫・CONTATO-E-SUPORTE", [
                _txt("🎫・solicitar-orçamento"),
                _txt("📨・falar-com-a-equipe"),
                _txt("❓・dúvidas-sobre-serviços"),
            ]),
        ],
    }


# ---------- 🏆 CLÃ DE E-SPORTS (completo) ----------
def clã(name="Central SP Esports 🏆"):
    DONO = "👑・Dono"
    COACH = "🎯・Head-Coach"
    AC = "📋・Assistente-Técnico"
    CAP = "🧢・Capitão"
    PRO = "🏆・Titular"
    SUB = "🔄・Reserva"
    ANAL = "📊・Analista"
    MANA = "💼・Manager"
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xD4AF37, ["administrator"], True),
            _role(COACH, 0x5B6DD1, ["manage_messages", "view_audit_log"], True),
            _role(AC, 0x3498DB, ["manage_messages"], True),
            _role(CAP, 0x2ECC71, ["manage_messages", "priority_speaker"], True),
            _role(PRO, 0x9B59B6, ["attach_files", "embed_links", "priority_speaker"], True),
            _role(SUB, 0x95A5A6, ["attach_files", "add_reactions"], True),
            _role(ANAL, 0xE67E22, ["attach_files", "embed_links"], True),
            _role(MANA, 0x1ABC9C, ["manage_messages", "embed_links"], True),
            _role("🥁・Torcedor", 0x99AAB5, ["add_reactions"]),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],
        "categories": [
            _cat("📢・INFORMAÇÕES", [
                _txt("📜・regras-do-clã"),
                _txt("📣・anúncios"),
                _txt("🏆・conquistas"),
                _txt("📅・calendário-de-jogos"),
                _txt("👤・elenco-atual"),
            ], _readonly(DONO, COACH, MANA)),
            _cat("⚔️・COMPETITIVO", [
                _txt("⚔️・campeonatos"),
                _txt("📋・resultados-e-mvp"),
                _txt("🎯・treinos-e-vods"),
                _txt("🧠・estudo-de-meta"),
                _txt("📊・estatísticas-do-time"),
            ], _lock(DONO, COACH, AC, CAP, PRO, SUB, ANAL)),
            _cat("🎮・JOGOS-DO-CLÃ", [
                _txt("🎮・chat-geral"),
                _txt("🏅・achar-scrim"),
                _txt("📸・clips-e-plays"),
                _txt("🎯・treinos-programados"),
                _vc("🎮・treino-oficial"),
                _vc("🎮・scrims-1"),
                _vc("🎮・scrims-2"),
                _vc("🎤・palestra-do-coach"),
            ]),
            _cat("💼・GESTÃO", [
                _txt("💼・contratos-e-salários"),
                _txt("🤝・patrocínios"),
                _txt("👕・uniformes-e-merch"),
                _txt("🧾・finanças-do-clã"),
            ], _lock(DONO, MANA, COACH)),
            _cat("🎉・COMUNIDADE", [
                _txt("💬・chat-da-torcida"),
                _txt("🎁・sorteios-e-giveaways"),
                _txt("📺・lives-e-streams"),
                _txt("🎪・eventos-com-a-comunidade"),
                _vc("🥁・bar-da-torcida"),
            ]),
            _cat("🤖・BOT", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
            ]),

            _cat("📝・RECRUTAMENTO", [
                _txt("📨・inscrições-para-o-clã"),
                _txt("🎯・testes-de-avaliação"),
                _txt("📋・requisitos-do-elenco"),
                _txt("📢・resultado-das-seletivas"),
            ], _readonly(DONO, COACH, AC, MANA)),
            _cat("📊・ANÁLISE-E-DESEMPENHO", [
                _txt("🎥・envio-de-vods"),
                _txt("📈・evolução-individual"),
                _txt("🧠・feedback-do-coach"),
                _txt("🗃️・biblioteca-de-estratégias"),
            ], _lock(DONO, COACH, AC, CAP, PRO, SUB, ANAL)),
        ],
    }


# ---------- 🚗 MTA SA (completo) ----------
def mta(name="Central SP MTA 🏙️"):
    FUND = "👑・Fundador"
    DONO = "💼・Owner"
    ADM = "⚙️・Administrador"
    MOD = "🛡️・Moderador"
    SUP = "🎧・Suporte"
    SCRIPT = "🧑‍💻・Scripter"
    ACL = "🔐・ACL-Master"
    WH = "📝・Aprovador"
    COP = "👮・Policial"
    ROT = "🚔・PM-Rotam"
    BOPE = "⚫・BOPE"
    FAR = "🚑・Farmer"
    MED = "🩺・Médico"
    REPO = "🔧・Repositor"
    GANGL = "🔫・Líder-de-Gangue"
    GANG = "🧢・Gangue"
    MAFIA = "🎩・Máfia"
    MILI = "🎖️・Militar"
    JUD = "⚖️・Juiz"
    NEWB = "🐣・Novato"
    STAFF = (FUND, DONO, ADM, MOD)
    return {
        "name": name,
        "roles": [
            _role(FUND, 0xD4AF37, ["administrator"], True),
            _role(DONO, 0xF1C40F, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log", "mention_everyone"], True),
            _role(ADM, 0xE74C3C, ["manage_guild", "manage_channels", "manage_messages", "kick_members", "ban_members", "view_audit_log", "mention_everyone"], True),
            _role(MOD, 0x1ABC9C, ["manage_messages", "kick_members", "manage_channels", "view_audit_log"], True),
            _role(SUP, 0x3498DB, ["manage_messages"], True),
            _role(SCRIPT, 0x1ABC9C, ["manage_messages", "manage_webhooks"], True),
            _role(ACL, 0x9B59B6, ["manage_messages"], True),
            _role(WH, 0x2ECC71, ["manage_messages", "view_audit_log"], True),
            _role(COP, 0x3498DB, [], True),
            _role(ROT, 0x8E44AD, [], True),
            _role(BOPE, 0x2C3E50, [], True),
            _role(MILI, 0x11806A, [], True),
            _role(FAR, 0x27AE60, [], True),
            _role(MED, 0xE74C3C, [], True),
            _role(REPO, 0x95A5A6, [], True),
            _role(GANGL, 0xC0392B, ["manage_messages"], True),
            _role(GANG, 0x992B2B, [], True),
            _role(MAFIA, 0x6C3483, [], True),
            _role(JUD, 0x8E44AD, [], True),
            _role("🚕・Taxista", 0xE67E22, [], True),
            _role("🚌・Motorista-de-Ônibus", 0xF39C12, [], True),
            _role("⛏️・Garimpeiro", 0x7F8C8D, [], True),
            _role(NEWB, 0x99AAB5, ["attach_files", "add_reactions"]),
            _role("🔇・Silenciado", 0x546E7A, []),
        ],
        "categories": [
            _cat("📢・INFORMAÇÕES", [
                _txt("📜・regras-do-servidor"),
                _txt("📣・anúncios"),
                _txt("🔗・ip-e-como-conectar"),
                _txt("🖥️・requisitos-e-download"),
                _txt("❓・faq"),
                _txt("🗺️・mapa-e-teleportes"),
                _txt("🆕・changelog"),
                _txt("🗳️・sugestões"),
            ], _readonly(*STAFF)),
            _cat("📝・WHITELIST", [
                _txt("📝・aplique-aqui"),
                _txt("📋・aprovados-e-reprovados"),
                _txt("📕・manual-do-cidadão"),
                _txt("🎥・tutorial-de-jogo"),
            ], _readonly(*STAFF, WH)),
            _cat("🌍・CIDADE", [
                _txt("💬・chat-geral"),
                _txt("📸・prints-da-cidade"),
                _txt("🎬・clips-e-moments"),
                _txt("📢・chat-in-game"),
                _txt("📻・rádio-cidade"),
                _vc("🌍・voz-global"),
            ]),
            _cat("👮・ORGÂNICOS-POLICIAIS", [
                _txt("🚔・polícia-civil"),
                _txt("⚫・bope"),
                _txt("🎖️・exército"),
                _txt("📋・delegacia-e-celas"),
                _txt("🚨・procurados"),
                _vc("🚔・rádio-da-pm"),
                _vc("⚫・rádio-do-bope"),
            ], _lock(*STAFF, COP, ROT, BOPE, MILI)),
            _cat("🚑・ORGÂNICOS-CIVIS", [
                _txt("🚑・médicos"),
                _txt("🔧・repositores"),
                _txt("🚕・taxistas"),
                _txt("🚌・transporte-público"),
                _txt("⛽・postos-e-mecânicos"),
                _vc("🚑・rádio-medico"),
            ], _lock(*STAFF, MED, REPO, FAR)),
            _cat("🔫・FACÇÕES-CRIMINOSAS", [
                _txt("🔫・gangues"),
                _txt("🎩・máfias"),
                _txt("☠️・territórios"),
                _txt("💰・roubos-e-assaltos"),
                _txt("🌿・drogas-e-armas"),
                _vc("🔫・base-das-gangues"),
            ], _lock(*STAFF, GANGL, GANG, MAFIA)),
            _cat("⚖️・JUSTIÇA", [
                _txt("🏛️・tribunal"),
                _txt("🧾・processos-e-multas"),
                _txt("⚖️・advocacia"),
                _vc("👨‍⚖️・sala-do-juiz"),
            ], _lock(*STAFF, JUD, COP)),
            _cat("💼・EMPREGOS", [
                _txt("⛏️・garimpo"),
                _txt("🌾・fazendeiro"),
                _txt("🎣・pescador"),
                _txt("🍕・entregador"),
                _txt("🚛・caminhoneiro"),
                _txt("🏦・banco-e-investimentos"),
                _txt("🏠・imobiliária"),
                _txt("🚗・concessionária"),
            ]),
            _cat("🧑‍💻・EQUIPE-DEVELOPMENT", [
                _txt("🧑‍💻・scripters"),
                _txt("🔐・acl-e-permissões"),
                _txt("🐞・bugs-e-report"),
                _txt("💡・ideias-e-projetos"),
                _vc("🧑‍💻・sala-de-dev"),
            ], _lock(FUND, DONO, SCRIPT, ACL)),
            _cat("🛠️・STAFF", [
                _txt("🔧・staff-chat"),
                _txt("📋・logs-e-punições"),
                _txt("📨・denúncias"),
                _txt("🎯・revisão-de-ban"),
                _vc("🛠️・sala-da-staff"),
            ], _lock(*STAFF)),
            _cat("🤖・BOT", [
                _txt("🤖・comandos"),
                _txt("📊・status"),
            ]),

            _cat("🎫・SUPORTE-E-RECURSOS", [
                _txt("🎫・abrir-ticket"),
                _txt("🚨・denunciar-jogador"),
                _txt("📨・recorrer-de-punição"),
                _txt("🐞・reportar-bugs"),
                _txt("📝・dúvidas-sobre-regras"),
            ]),
            _cat("🎉・EVENTOS-E-COMUNIDADE", [
                _txt("📅・agenda-de-eventos"),
                _txt("🏁・corridas-e-eventos"),
                _txt("📸・melhores-momentos"),
                _txt("🏆・hall-da-fama"),
                _vc("🎉・evento-da-cidade"),
            ]),
        ],
    }




# ---------- ⛏️ MINECRAFT ----------
def minecraft(name="Minecraft Community ⛏️"):
    DONO = "👑・Dono"
    ADMIN = "🛡️・Administrador"
    MOD = "🔨・Moderador"
    SUP = "🎫・Suporte"
    BUILDER = "🏗️・Builder"
    DEV = "💻・Desenvolvedor"
    YT = "🎥・Criador"
    VIP = "💎・VIP"
    MEMBRO = "⛏️・Membro"
    STAFF = (DONO, ADMIN, MOD, SUP)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xF1C40F, ["administrator"], True),
            _role(ADMIN, 0xE74C3C, ["manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members"], True),
            _role(MOD, 0xE67E22, ["manage_messages", "kick_members"], True),
            _role(SUP, 0x3498DB, ["manage_messages"], True),
            _role(BUILDER, 0x2ECC71, ["attach_files"], True),
            _role(DEV, 0x1ABC9C, ["manage_webhooks"], True),
            _role(YT, 0x9B59B6, ["attach_files", "embed_links"], True),
            _role(VIP, 0xF39C12, [], True),
            _role(MEMBRO, 0x95A5A6),
        ],
        "categories": [
            _cat("📌・INFORMAÇÕES", [
                _txt("📜・regras"), _txt("📢・anúncios"), _txt("📡・status-do-servidor"),
                _txt("🗺️・ip-e-versões"), _txt("❓・perguntas-frequentes", _readonly(DONO, ADMIN, MOD, SUP)),
            ]),
            _cat("💬・COMUNIDADE", [
                _txt("💬・chat-geral"), _txt("📸・prints-e-construções"), _txt("🎬・vídeos"),
                _txt("😂・memes"), _txt("🤝・procurar-amigos"), _vc("🔊・Bate-papo 1"), _vc("🔊・Bate-papo 2"),
            ]),
            _cat("🎮・MODOS-DE-JOGO", [
                _txt("⚔️・survival"), _txt("🛏️・bedwars"), _txt("🏹・skywars"),
                _txt("🏰・factions"), _txt("🎯・eventos-ingame"), _vc("🎮・Squad Minecraft"),
            ]),
            _cat("🏗️・CRIAÇÃO-E-DEV", [
                _txt("🏗️・projetos-de-build"), _txt("💻・sugestões-de-plugins"),
                _txt("🐞・bugs"), _txt("🧩・mods-e-texturas"), _vc("🛠️・Sala dos Builders"),
            ]),
            _cat("🎫・SUPORTE", [
                _txt("🎫・abrir-ticket"), _txt("🚨・denúncias"), _txt("⚖️・revisão-de-punição"),
            ]),
            _cat("🔒・EQUIPE", [
                _txt("🔒・staff-chat"), _txt("📋・logs"), _txt("📝・reuniões"),
                _vc("🔒・Call da Staff"),
            ], _lock(*STAFF)),
        ],
    }


# ---------- 📺 CRIADORES DE CONTEÚDO ----------
def youtube(name="Creator Hub 📺"):
    DONO = "👑・Fundador"
    ADMIN = "🛡️・Administração"
    MOD = "🔨・Moderação"
    DESIGN = "🎨・Designer"
    EDITOR = "🎬・Editor"
    CREATOR = "🌟・Criador"
    PARCEIRO = "🤝・Parceiro"
    MEMBRO = "👤・Membro"
    STAFF = (DONO, ADMIN, MOD)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xF1C40F, ["administrator"], True),
            _role(ADMIN, 0xE74C3C, ["manage_channels", "manage_roles", "manage_messages"], True),
            _role(MOD, 0xE67E22, ["manage_messages", "kick_members"], True),
            _role(DESIGN, 0x9B59B6, ["attach_files", "embed_links"], True),
            _role(EDITOR, 0x3498DB, ["attach_files", "embed_links"], True),
            _role(CREATOR, 0xE91E63, ["attach_files", "embed_links"], True),
            _role(PARCEIRO, 0x1ABC9C, [], True),
            _role(MEMBRO, 0x95A5A6),
        ],
        "categories": [
            _cat("📌・INÍCIO", [
                _txt("📜・regras"), _txt("👋・boas-vindas", _readonly(DONO, ADMIN, MOD)),
                _txt("📢・avisos", _readonly(DONO, ADMIN)), _txt("🎭・cargos"),
            ]),
            _cat("💬・COMUNIDADE", [
                _txt("💬・chat-geral"), _txt("📸・divulgue-seu-canal"), _txt("🔴・lives"),
                _txt("🎞️・vídeos-novos"), _txt("💡・ideias-de-conteúdo"),
                _vc("🎙️・Resenha"), _vc("🎮・Gravação"),
            ]),
            _cat("🧰・PRODUÇÃO", [
                _txt("🎨・pedidos-de-artes"), _txt("🎬・edição-de-vídeos"),
                _txt("🖼️・thumbnails"), _txt("📝・roteiros"), _txt("📅・calendário-de-postagens"),
            ]),
            _cat("🤝・PARCERIAS", [
                _txt("📨・propostas"), _txt("📣・divulgação-de-parceiros"),
                _txt("🏆・colaborações"),
            ]),
            _cat("🔒・EQUIPE", [
                _txt("🔒・staff-chat"), _txt("📋・planejamento"), _txt("📊・resultados"),
                _vc("🔒・Reunião da Equipe"),
            ], _lock(*STAFF)),
        ],
    }


# ---------- 🍥 ANIME / OTAKU ----------
def anime(name="Anime World 🍥"):
    DONO = "👑・Dono"
    ADMIN = "🛡️・Admin"
    MOD = "🔨・Moderador"
    EVENT = "🎉・Organizador"
    VIP = "💎・VIP"
    MEMBRO = "🌸・Membro"
    STAFF = (DONO, ADMIN, MOD)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xF1C40F, ["administrator"], True),
            _role(ADMIN, 0xE74C3C, ["manage_channels", "manage_roles", "manage_messages"], True),
            _role(MOD, 0xE67E22, ["manage_messages", "kick_members"], True),
            _role(EVENT, 0x9B59B6, ["manage_messages"], True),
            _role(VIP, 0xF39C12, [], True),
            _role(MEMBRO, 0xE91E63),
        ],
        "categories": [
            _cat("📌・INFORMAÇÕES", [
                _txt("📜・regras"), _txt("📢・anúncios", _readonly(DONO, ADMIN)),
                _txt("👋・apresentações"), _txt("🎭・escolher-cargos"),
            ]),
            _cat("🌸・COMUNIDADE", [
                _txt("💬・chat-geral"), _txt("😂・memes-anime"), _txt("🎨・fanarts"),
                _txt("📸・cosplay"), _txt("🎵・músicas-e-aberturas"),
                _vc("🍡・Bate-papo"), _vc("🎧・Sala de Música"),
            ]),
            _cat("🍿・ANIMES-E-MANGÁS", [
                _txt("🍿・recomendações"), _txt("📖・mangás"), _txt("🔥・episódios-da-semana"),
                _txt("💬・debates-sem-spoiler"), _txt("⚠️・spoilers"),
            ]),
            _cat("🎉・EVENTOS", [
                _txt("📅・agenda"), _txt("🗳️・enquetes"), _txt("🏆・concursos"),
                _txt("🎲・quiz-anime"), _vc("🎉・Evento ao vivo"),
            ]),
            _cat("🔒・MODERAÇÃO", [
                _txt("🔒・staff-chat"), _txt("📋・logs"), _txt("🚨・casos"),
            ], _lock(*STAFF)),
        ],
    }


# ---------- 📚 ESTUDOS / ESCOLA ----------
def estudos(name="Central de Estudos 📚"):
    DONO = "👑・Coordenação"
    ADMIN = "🛡️・Admin"
    MOD = "🔨・Monitor"
    PROF = "🍎・Professor"
    ALUNO = "📚・Estudante"
    STAFF = (DONO, ADMIN, MOD, PROF)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xF1C40F, ["administrator"], True),
            _role(ADMIN, 0xE74C3C, ["manage_channels", "manage_roles", "manage_messages"], True),
            _role(MOD, 0xE67E22, ["manage_messages"], True),
            _role(PROF, 0x3498DB, ["manage_messages", "attach_files"], True),
            _role(ALUNO, 0x2ECC71),
        ],
        "categories": [
            _cat("📌・CENTRAL", [
                _txt("📜・regras"), _txt("📢・comunicados", _readonly(DONO, ADMIN, PROF)),
                _txt("📅・calendário"), _txt("👋・apresentações"),
            ]),
            _cat("📖・MATÉRIAS", [
                _txt("🧮・matemática"), _txt("🧪・ciências"), _txt("🌎・geografia"),
                _txt("📜・história"), _txt("✍️・português"), _txt("🇬🇧・inglês"),
            ]),
            _cat("📝・ATIVIDADES", [
                _txt("📚・materiais"), _txt("📝・tarefas"), _txt("❓・dúvidas"),
                _txt("🏆・conquistas"), _vc("📚・Estudo em grupo"),
            ]),
            _cat("💬・CONVIVÊNCIA", [
                _txt("💬・chat-geral"), _txt("🤝・grupo-de-estudos"),
                _txt("🎯・metas-da-semana"), _vc("☕・Intervalo"),
            ]),
            _cat("🔒・EQUIPE", [
                _txt("🔒・coordenação"), _txt("📋・planejamento"), _txt("🧾・registros"),
                _vc("🔒・Reunião"),
            ], _lock(*STAFF)),
        ],
    }


# ---------- 🧑‍💻 SUPORTE TÉCNICO ----------
def suporte(name="Central de Suporte 🧑‍💻"):
    DONO = "👑・Proprietário"
    ADMIN = "🛡️・Administrador"
    AGENTE = "🎧・Atendente"
    TEC = "🧑‍💻・Técnico"
    CLIENTE = "👤・Cliente"
    STAFF = (DONO, ADMIN, AGENTE, TEC)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xF1C40F, ["administrator"], True),
            _role(ADMIN, 0xE74C3C, ["manage_channels", "manage_roles", "manage_messages"], True),
            _role(AGENTE, 0x3498DB, ["manage_messages"], True),
            _role(TEC, 0x1ABC9C, ["manage_messages", "attach_files"], True),
            _role(CLIENTE, 0x95A5A6),
        ],
        "categories": [
            _cat("📌・CENTRAL-DE-AJUDA", [
                _txt("📜・regras"), _txt("📢・status-do-serviço", _readonly(DONO, ADMIN)),
                _txt("📚・base-de-conhecimento"), _txt("🧭・como-funciona"),
            ]),
            _cat("🎫・ATENDIMENTO", [
                _txt("🎫・abrir-ticket"), _txt("💳・financeiro"),
                _txt("🧰・problemas-técnicos"), _txt("📦・pedidos-e-entregas"),
                _txt("⭐・avaliações"),
            ]),
            _cat("💬・COMUNIDADE", [
                _txt("💬・chat-geral"), _txt("💡・sugestões"), _txt("🐞・relatar-problema"),
                _vc("🎧・Atendimento por voz"),
            ]),
            _cat("🔒・PAINEL-INTERNO", [
                _txt("🔒・equipe-chat"), _txt("📋・tickets-em-andamento"),
                _txt("📊・relatórios"), _txt("🧾・logs"),
                _vc("🔒・Reunião da equipe"),
            ], _lock(*STAFF)),
        ],
    }


# ---------- 🎨 AGÊNCIA DE DESIGN ----------
def design(name="Creative Studio 🎨"):
    DONO = "👑・Diretor"
    ADMIN = "🛡️・Gerente"
    DESIGNER = "🎨・Designer"
    EDITOR = "🎬・Editor"
    CLIENTE = "👤・Cliente"
    STAFF = (DONO, ADMIN, DESIGNER, EDITOR)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xF1C40F, ["administrator"], True),
            _role(ADMIN, 0xE74C3C, ["manage_channels", "manage_roles", "manage_messages"], True),
            _role(DESIGNER, 0x9B59B6, ["attach_files", "embed_links"], True),
            _role(EDITOR, 0x3498DB, ["attach_files", "embed_links"], True),
            _role(CLIENTE, 0x95A5A6),
        ],
        "categories": [
            _cat("📌・INFORMAÇÕES", [
                _txt("📜・regras"), _txt("📢・avisos", _readonly(DONO, ADMIN)),
                _txt("🧾・serviços-e-valores"), _txt("📁・portfólio"),
            ]),
            _cat("🛍️・CLIENTES", [
                _txt("🎫・solicitar-orçamento"), _txt("📨・enviar-referências"),
                _txt("📦・entregas"), _txt("🔁・revisões"), _txt("⭐・feedback"),
            ]),
            _cat("🖌️・PRODUÇÃO", [
                _txt("🎨・identidade-visual"), _txt("🖼️・thumbnails-e-banners"),
                _txt("🎬・edição"), _txt("📋・fila-de-projetos"),
                _vc("🎙️・Call com cliente"),
            ]),
            _cat("🔒・EQUIPE", [
                _txt("🔒・equipe-chat"), _txt("📊・gestão-de-projetos"),
                _txt("💡・referências-e-ideias"), _txt("🧾・financeiro"),
                _vc("🔒・Reunião interna"),
            ], _lock(*STAFF)),
        ],
    }


# ---------- 🎙️ PODCAST ----------
def podcast(name="Podcast Network 🎙️"):
    DONO = "👑・Produtor Executivo"
    ADMIN = "🛡️・Admin"
    HOST = "🎙️・Apresentador"
    EDITOR = "🎬・Editor"
    CONVIDADO = "⭐・Convidado"
    OUVINTE = "🎧・Ouvinte"
    STAFF = (DONO, ADMIN, HOST, EDITOR)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xF1C40F, ["administrator"], True),
            _role(ADMIN, 0xE74C3C, ["manage_channels", "manage_roles", "manage_messages"], True),
            _role(HOST, 0x9B59B6, ["attach_files"], True),
            _role(EDITOR, 0x3498DB, ["attach_files", "embed_links"], True),
            _role(CONVIDADO, 0x1ABC9C),
            _role(OUVINTE, 0x95A5A6),
        ],
        "categories": [
            _cat("📌・PROGRAMA", [
                _txt("📜・regras"), _txt("📢・episódios-novos", _readonly(DONO, ADMIN)),
                _txt("🗓️・agenda-de-gravações"), _txt("🎧・onde-ouvir"),
            ]),
            _cat("💬・COMUNIDADE", [
                _txt("💬・chat-geral"), _txt("💡・sugestões-de-temas"),
                _txt("❓・perguntas-para-o-programa"), _txt("⭐・feedback"),
                _vc("🎧・Conversa com ouvintes"),
            ]),
            _cat("🎙️・BASTIDORES", [
                _txt("📝・pautas-e-roteiros"), _txt("📨・convidados"),
                _txt("🎬・cortes-e-clipes"), _txt("📁・materiais"),
                _vc("🎙️・Estúdio de gravação"),
            ]),
            _cat("🔒・PRODUÇÃO", [
                _txt("🔒・produção-chat"), _txt("📋・cronograma"),
                _txt("🧾・parcerias"), _txt("📊・métricas"),
            ], _lock(*STAFF)),
        ],
    }


# ---------- 🎪 EVENTOS / COMUNIDADE ----------
def eventos(name="Central de Eventos 🎪"):
    DONO = "👑・Organizador Geral"
    ADMIN = "🛡️・Administrador"
    STAFF_ROLE = "🎟️・Organizador"
    DIVULGADOR = "📣・Divulgação"
    PARTICIPANTE = "🎉・Participante"
    STAFF = (DONO, ADMIN, STAFF_ROLE, DIVULGADOR)
    return {
        "name": name,
        "roles": [
            _role(DONO, 0xF1C40F, ["administrator"], True),
            _role(ADMIN, 0xE74C3C, ["manage_channels", "manage_roles", "manage_messages"], True),
            _role(STAFF_ROLE, 0x3498DB, ["manage_messages"], True),
            _role(DIVULGADOR, 0x9B59B6, ["manage_messages", "embed_links"], True),
            _role(PARTICIPANTE, 0x2ECC71),
        ],
        "categories": [
            _cat("📌・INFORMAÇÕES", [
                _txt("📜・regras"), _txt("📢・avisos", _readonly(DONO, ADMIN)),
                _txt("📅・calendário-de-eventos"), _txt("🎟️・inscrições"),
            ]),
            _cat("🎉・EVENTOS-ATIVOS", [
                _txt("🎊・evento-atual"), _txt("🗳️・votações"),
                _txt("📸・fotos-e-registros"), _txt("🏆・resultados"),
                _vc("🎤・Palco do evento"),
            ]),
            _cat("💬・COMUNIDADE", [
                _txt("💬・chat-geral"), _txt("🤝・networking"),
                _txt("💡・ideias-para-eventos"), _txt("📣・divulgações"),
                _vc("🎉・Convivência"),
            ]),
            _cat("🔒・ORGANIZAÇÃO", [
                _txt("🔒・equipe-chat"), _txt("📋・planejamento"),
                _txt("📨・fornecedores-e-parcerias"), _txt("🧾・orçamento"),
                _vc("🔒・Reunião dos organizadores"),
            ], _lock(*STAFF)),
        ],
    }

# ---------- 🌆 COMUNIDADE GIGANTE ----------
def comunidade_pro(name="Metrópole Central 🌆"):
    DONO = "👑・Fundador"
    CEO = "⚜️・CEO"
    DIR = "💼・Diretor-Geral"
    ADMIN = "🧭・Administrador"
    MODCHEFE = "🛡️・Moderador-Chefe"
    MOD = "🛠️・Moderador"
    TRIAL = "🧪・Mod-em-Teste"
    HELPER = "🎓・Helper"
    SEG = "🕵️・Anti-Raid"
    JURI = "⚖️・Jurídico"
    FIN = "💰・Financeiro"
    MARK = "📣・Marketing"
    DESIGN = "🎨・Designer"
    EDITOR = "📹・Editor"
    PARC = "🤝・Parcerias"
    SORTEIO = "🎁・Sorteios"
    EVENTOS = "🎉・Eventos"
    DEV = "🧠・Bot-Developer"
    WEB = "🌐・Web-Developer"

    STAFF = (DONO, CEO, DIR, ADMIN, MODCHEFE, MOD, TRIAL, HELPER, SEG, JURI)
    EQUIPE = STAFF + (FIN, MARK, DESIGN, EDITOR, PARC, SORTEIO, EVENTOS, DEV, WEB)

    return {
        "name": name,
        "roles": [
            _role(DONO, 0xFFD700, ["administrator"], True),
            _role(CEO, 0xE74C3C, ["administrator"], True),
            _role(DIR, 0xF1C40F, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log", "moderate_members"], True),
            _role(ADMIN, 0xE67E22, ["manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "view_audit_log", "moderate_members"], True),
            _role(MODCHEFE, 0x9B59B6, ["manage_messages", "kick_members", "moderate_members", "view_audit_log"], True),
            _role(MOD, 0x3498DB, ["manage_messages", "moderate_members", "kick_members"], True),
            _role(TRIAL, 0x5DADE2, ["manage_messages", "moderate_members"], True),
            _role(HELPER, 0x48C9B0, ["manage_messages"], True),
            _role(SEG, 0xC0392B, ["ban_members", "kick_members", "manage_messages", "moderate_members"], True),
            _role(JURI, 0x34495E, ["manage_messages"], True),
            _role(FIN, 0x2ECC71, [], True),
            _role(MARK, 0xE91E63, ["manage_messages", "embed_links", "attach_files", "mention_everyone"], True),
            _role(DESIGN, 0xF5B041, ["attach_files", "embed_links"], True),
            _role(EDITOR, 0xAF7AC5, ["attach_files", "embed_links"], True),
            _role(PARC, 0x1ABC9C, ["embed_links", "manage_messages"], True),
            _role(SORTEIO, 0x2ECC71, ["embed_links", "add_reactions", "mention_everyone"], True),
            _role(EVENTOS, 0x8E44AD, ["embed_links", "manage_messages", "mention_everyone"], True),
            _role(DEV, 0x11806A, ["manage_messages", "manage_webhooks", "embed_links"], True),
            _role(WEB, 0x21618C, ["embed_links", "attach_files"], True),

            _role("🎥・Streamer", 0x9B59B6, ["attach_files", "embed_links"], True),
            _role("📺・YouTuber", 0xC0392B, ["attach_files", "embed_links"], True),
            _role("🎼・Músico", 0x1ABC9C, ["attach_files", "embed_links"], True),
            _role("✍️・Escritor", 0xD4AC0D, ["attach_files", "embed_links"], True),
            _role("📸・Fotógrafo", 0x5499C7, ["attach_files", "embed_links"], True),

            _role("💎・Lenda", 0xF1C40F, ["attach_files", "add_reactions", "embed_links"], True),
            _role("🏆・Veterano", 0x2ECC71, ["attach_files", "add_reactions"], True),
            _role("⭐・Membro-Ativo", 0x3498DB, ["add_reactions"], True),
            _role("👤・Membro", 0x99AAB5, ["add_reactions"]),
            _role("🆕・Novato", 0x7289DA),

            _role("💜・Booster", 0x9B59B6, ["attach_files", "embed_links", "add_reactions"], True),
            _role("👑・VIP-Ouro", 0xFFD700, ["attach_files", "embed_links", "add_reactions"], True),
            _role("🥈・VIP-Prata", 0xB2BABB, ["attach_files", "embed_links"], True),
            _role("🥉・VIP-Bronze", 0x935116, ["attach_files"], True),
            _role("🎫・Sortudo", 0x2ECC71, ["add_reactions"], True),
            _role("🏅・Campeão", 0xF39C12, ["add_reactions"], True),
            _role("🔊・DJ", 0x8E44AD, ["connect", "speak", "priority_speaker"], True),

            _role("🤖・Robô", 0x747F8D, []),
            _role("🔇・Silenciado", 0x546E7A),
        ],
        "categories": [
            _cat("📌・INÍCIO", [
                _txt("👋・boas-vindas", _readonly(*EQUIPE)),
                _txt("📜・regras", _readonly(*EQUIPE)),
                _txt("🎭・cargos-e-medalhas", _readonly(*EQUIPE)),
                _txt("❓・faq", _readonly(*EQUIPE)),
                _txt("🚪・verifique-se", _readonly(*EQUIPE)),
                _txt("📰・novidades", _readonly(*EQUIPE)),
            ]),
            _cat("📢・COMUNICADOS", [
                _txt("📣・anúncios", _readonly(*EQUIPE)),
                _txt("🎉・eventos-oficiais", _readonly(*EQUIPE)),
                _txt("🎁・sorteios-oficiais", _readonly(*EQUIPE)),
                _txt("🗳️・enquetes", _readonly(*EQUIPE)),
                _txt("📊・resultados", _readonly(*EQUIPE)),
                _txt("🏆・ranking-semanal", _readonly(*EQUIPE)),
            ]),
            _cat("💬・INTERAÇÃO", [
                _txt("💬・chat-geral"), _txt("🐸・memes"), _txt("📸・mídia"),
                _txt("🎤・apresentações"), _txt("💭・off-topic"),
                _txt("🏆・conquistas"), _txt("💡・dicas"),
            ]),
            _cat("🎨・CONTEÚDO-CRIADOR", [
                _txt("🖌️・fanart"), _txt("🎬・clipes"), _txt("🎵・músicas"),
                _txt("📺・vídeos"), _txt("🔴・avisos-de-live"), _txt("💼・portfólio"),
            ]),
            _cat("🎮・JOGOS", [
                _txt("🎲・chat-games"), _txt("🤝・matchmaking"),
                _vc("🎮・Sala-1"), _vc("🎮・Sala-2"), _vc("🎮・Sala-3"),
            ]),
            _cat("🎉・EVENTOS", [
                _txt("🎪・evento-atual"), _txt("📝・inscrições"),
                _txt("🏅・resultados-do-evento"), _txt("📷・fotos-do-evento"),
                _vc("🎤・Palco-do-Evento"),
            ]),
            _cat("🎁・SORTEIOS", [
                _txt("🎫・sorteio-atual", _readonly(*EQUIPE)),
                _txt("🏆・ganhadores", _readonly(*EQUIPE)),
                _txt("📜・regras-dos-sorteios", _readonly(*EQUIPE)),
            ]),
            _cat("💡・COMUNIDADE", [
                _txt("💡・sugestões"), _txt("🗳️・votações"),
                _txt("🤝・indique-um-amigo"), _txt("📈・feedback-da-staff"),
            ]),
            _cat("🛒・LOJA-DA-COMUNIDADE", [
                _txt("🛍️・catálogo", _readonly(*EQUIPE)),
                _txt("💳・fazer-pedido"),
                _txt("👑・benefícios-vip", _readonly(*EQUIPE)),
                _txt("💜・apoiar-a-comunidade", _readonly(*EQUIPE)),
            ]),
            _cat("🤝・PARCERIAS", [
                _txt("📣・divulgação-de-parceiros", _readonly(PARC, *STAFF)),
                _txt("💬・chat-parceiros", _lock(PARC, *STAFF)),
                _txt("📋・requisitos-de-parceria", _readonly(PARC, *STAFF)),
            ]),
            _cat("🎫・ATENDIMENTO", [
                _txt("❓・central-de-ajuda"), _txt("🚨・denúncias"),
                _txt("⚠️・reportar-bug"),
            ]),
            _cat("📊・ESTATÍSTICAS", [
                _txt("📈・contador-de-membros", _readonly(*EQUIPE)),
                _txt("🏅・hall-da-fama", _readonly(*EQUIPE)),
            ]),
            _cat("🔊・VOZ", [
                _vc("🎙️・Palco-Principal"), _vc("🎧・Música"),
                _vc("🎮・Gaming-1"), _vc("🎮・Gaming-2"),
                _vc("☕・Café"), _vc("💤・AFK"),
            ]),
            _cat("🔒・STAFF", [
                _txt("🔒・staff-chat"), _txt("📋・mod-log"), _txt("🧾・logs"),
                _txt("📅・planejamento"), _txt("📥・candidaturas"),
                _txt("📢・avisos-staff"),
            ], _lock(*STAFF)),
            _cat("🧰・FERRAMENTAS", [
                _txt("🤖・comandos"), _txt("🧪・testes"),
            ]),
        ],
    }


# ---------- 🏬 LOJA GIGANTE (E-COMMERCE PRO) ----------
def loja_pro(name="Central Prime Store 🏬"):
    CEO = "👑・CEO"
    DIRETOR = "💼・Diretor"
    GERENTE = "📊・Gerente-Geral"
    GERVEN = "🛒・Gerente-de-Vendas"
    COORD = "🔍・Coordenador"
    SUP = "🧾・Supervisor"
    VEND = "🤝・Vendedor"
    CAIXA = "💳・Financeiro"
    FAT = "🧮・Faturamento"
    LOG = "📦・Logística"
    ENTREGA = "🚚・Entregador"
    ESTOQUE = "🏪・Estoque"
    COMPRAS = "🛍️・Compras"
    JURI = "⚖️・Jurídico"
    MARK = "📣・Marketing"
    DESIGN = "🎨・Design-da-Loja"
    TI = "💻・TI"
    N1 = "📞・Atendimento-N1"
    N2 = "🧑‍💻・Atendimento-N2"
    POS = "🔄・Pós-Venda"
    QUALI = "🧪・Qualidade"
    SEG = "🛡️・Segurança"

    STAFF = (CEO, DIRETOR, GERENTE, GERVEN, COORD, SUP, JURI, SEG)
    EQUIPE = STAFF + (VEND, CAIXA, FAT, LOG, ENTREGA, ESTOQUE, COMPRAS, MARK, DESIGN, TI, N1, N2, POS, QUALI)

    return {
        "name": name,
        "roles": [
            _role(CEO, 0xFFD700, ["administrator"], True),
            _role(DIRETOR, 0xE74C3C, ["manage_guild", "manage_channels", "manage_roles", "manage_messages", "view_audit_log", "moderate_members"], True),
            _role(GERENTE, 0xF1C40F, ["manage_channels", "manage_messages", "view_audit_log", "moderate_members"], True),
            _role(GERVEN, 0xE67E22, ["manage_messages", "moderate_members"], True),
            _role(COORD, 0x9B59B6, ["manage_messages", "moderate_members"], True),
            _role(SUP, 0x3498DB, ["manage_messages"], True),
            _role(VEND, 0x1ABC9C, ["manage_messages", "embed_links"], True),
            _role(CAIXA, 0x2ECC71, [], True),
            _role(FAT, 0x27AE60, [], True),
            _role(LOG, 0x5D6D7E, [], True),
            _role(ENTREGA, 0x85C1E9, [], True),
            _role(ESTOQUE, 0x7F8C8D, [], True),
            _role(COMPRAS, 0x16A085, [], True),
            _role(JURI, 0x34495E, [], True),
            _role(MARK, 0xE91E63, ["manage_messages", "embed_links", "attach_files", "mention_everyone"], True),
            _role(DESIGN, 0xF5B041, ["attach_files", "embed_links"], True),
            _role(TI, 0x11806A, ["manage_messages", "manage_webhooks"], True),
            _role(N1, 0x48C9B0, ["manage_messages"], True),
            _role(N2, 0x2874A6, ["manage_messages"], True),
            _role(POS, 0x22A6B3, [], True),
            _role(QUALI, 0x99A3A4, [], True),
            _role(SEG, 0xC0392B, ["manage_messages", "kick_members", "ban_members", "moderate_members"], True),

            _role("🏭・Fornecedor", 0x5D6D7E),
            _role("🤝・Revendedor", 0x1ABC9C),
            _role("🌐・Afiliado", 0x9B59B6, ["embed_links"]),

            _role("💎・Cliente-Diamante", 0x7FB3D5, ["attach_files", "embed_links"], True),
            _role("🥇・Cliente-Ouro", 0xFFD700, ["attach_files"], True),
            _role("🥈・Cliente-Prata", 0xB2BABB, [], True),
            _role("🥉・Cliente-Bronze", 0x935116, [], True),
            _role("🛍️・Cliente", 0x99AAB5, ["add_reactions"]),
            _role("🆕・Compra-Primeira", 0x7289DA),
            _role("👑・VIP", 0x9B59B6, ["attach_files", "embed_links"], True),

            _role("🔇・Silenciado", 0x546E7A),
            _role("🤖・Robô", 0x747F8D),
        ],
        "categories": [
            _cat("🏬・INÍCIO", [
                _txt("👋・boas-vindas", _readonly(*EQUIPE)),
                _txt("📜・regras", _readonly(*EQUIPE)),
                _txt("🏢・sobre-a-loja", _readonly(*EQUIPE)),
                _txt("🕐・horário-de-atendimento", _readonly(*EQUIPE)),
                _txt("❓・perguntas-frequentes", _readonly(*EQUIPE)),
                _txt("⭐・avaliações-da-loja", _readonly(*EQUIPE)),
            ]),
            _cat("📢・COMUNICADOS", [
                _txt("📣・anúncios", _readonly(*EQUIPE)),
                _txt("🔥・promoções", _readonly(*EQUIPE)),
                _txt("🆕・novidades", _readonly(*EQUIPE)),
                _txt("⚡・oferta-relâmpago", _readonly(*EQUIPE)),
                _txt("🗓️・promoções-da-semana", _readonly(*EQUIPE)),
            ]),
            _cat("🛒・VITRINE", [
                _txt("📋・catálogo", _readonly(*EQUIPE)),
                _txt("🆕・lançamentos", _readonly(*EQUIPE)),
                _txt("🏆・mais-vendidos", _readonly(*EQUIPE)),
                _txt("👑・catálogo-vip", _readonly(*EQUIPE)),
                _txt("📦・encomendas-sob-demanda"),
                _txt("🏷️・cupons-e-descontos", _readonly(*EQUIPE)),
            ]),
            _cat("📝・PEDIDOS", [
                _txt("🛒・fazer-pedido"),
                _txt("📦・acompanhar-pedido"),
                _txt("✅・pedidos-finalizados", _readonly(N1, N2, *STAFF)),
                _txt("⭐・avaliações-de-clientes"),
                _txt("↩️・trocas-e-devoluções"),
                _txt("❌・cancelamentos", _lock(N1, N2, POS, *STAFF)),
            ]),
            _cat("💬・ATENDIMENTO", [
                _txt("📞・chat-de-atendimento"),
                _txt("🚨・reclamações"),
                _txt("🔄・pós-venda", _lock(POS, N1, N2, *STAFF)),
                _txt("👑・suporte-vip", _lock(N2, *STAFF)),
            ]),
            _cat("💰・FINANCEIRO", [
                _txt("💳・pagamentos", _lock(CAIXA, FAT, *STAFF)),
                _txt("🧮・faturamento", _lock(CAIXA, FAT, *STAFF)),
                _txt("📊・relatórios-diários", _lock(CAIXA, FAT, *STAFF)),
                _txt("🧾・notas-fiscais", _lock(CAIXA, FAT, JURI, *STAFF)),
            ], _lock(CAIXA, FAT, JURI, *STAFF)),
            _cat("📦・LOGÍSTICA", [
                _txt("🚚・entregas-do-dia", _lock(LOG, ENTREGA, *STAFF)),
                _txt("🗺️・rotas", _lock(LOG, ENTREGA, *STAFF)),
                _txt("🏪・controle-de-estoque", _lock(LOG, ESTOQUE, COMPRAS, *STAFF)),
                _txt("🏭・fornecedores", _lock(COMPRAS, LOG, *STAFF)),
                _txt("🧾・conferência-de-pedidos", _lock(SUP, LOG, *STAFF)),
            ], _lock(LOG, ENTREGA, ESTOQUE, COMPRAS, SUP, *STAFF)),
            _cat("📣•MARKETING", [
                _txt("🎨・campanhas", _lock(MARK, DESIGN, *STAFF)),
                _txt("🖼️・criativos", _lock(MARK, DESIGN, *STAFF)),
                _txt("📱・redes-sociais", _lock(MARK, *STAFF)),
                _txt("🌐・afiliados", _lock(MARK, *STAFF)),
                _txt("🤝・parcerias-e-revendas", _lock(MARK, JURI, *STAFF)),
            ], _lock(MARK, DESIGN, JURI, *STAFF)),
            _cat("🧪・QUALIDADE", [
                _txt("🧾・controle-de-qualidade", _lock(QUALI, SUP, *STAFF)),
                _txt("⚠️・problemas-reportados", _lock(QUALI, N2, *STAFF)),
                _txt("📈・melhorias", _lock(QUALI, *STAFF)),
            ], _lock(QUALI, SUP, *STAFF)),
            _cat("🔒・DIRETORIA", [
                _txt("🔒・diretoria-chat"),
                _txt("📅・planejamento"),
                _txt("🎯・metas-do-mês"),
                _txt("📊・resultados"),
                _txt("⚖️・assuntos-jurídicos", _lock(JURI, *STAFF)),
            ], _lock(*STAFF)),
            _cat("🔊・VOZ", [
                _vc("📞・Atendimento-1"), _vc("📞・Atendimento-2"),
                _vc("🏢・Reunião-da-Equipe"), _vc("🚚・Coordenação-de-Entregas"),
            ]),
            _cat("🧰・FERRAMENTAS", [
                _txt("🤖・comandos"), _txt("🧾・logs"),
            ]),
        ],
    }


# ---------- 🏛️ CORPORAÇÃO GIGANTE ----------
def empresa_pro(name="Global Corporation 🏛️"):
    CEO = "👑・CEO"
    VICE = "⚜️・Vice-CEO"
    CONSELHO = "🏛️・Conselho"
    CFO = "📊・CFO-Financeiro"
    COO = "🧠・COO-Operacional"
    CTO = "💻・CTO-Tecnologia"
    CMO = "📣・CMO-Marketing"
    CHRO = "👥・CHRO-RH"
    DIRJUR = "⚖️・Diretor-Jurídico"
    DIRIND = "🏭・Diretor-Industrial"
    GER = "💼・Gerente"
    SUP = "🧾・Supervisor"
    COORD = "🔍・Coordenador"
    ANA = "👔・Analista"
    FIN = "💰•Financeiro"
    CONT = "🧮・Contabilidade"
    TI = "💻・TI"
    SUTI = "🛠️・Suporte-TI"
    INFOSEC = "🔐・Info-Segurança"
    RH = "👥・RH"
    TREINA = "🎓・Treinamento"
    JURI = "⚖️・Jurídico"
    MARK = "📣・Marketing"
    DESIGN = "🎨・Design"
    COMERCIAL = "🤝・Comercial"
    PROD = "🏭・Produção"
    LOGI = "🚚・Logística"
    QUALI = "🧪・Qualidade"
    PD = "🔬・P&D"
    ATEND = "📞・Atendimento"

    ALTA = (CEO, VICE, CONSELHO)
    GESTAO = ALTA + (CFO, COO, CTO, CMO, CHRO, DIRJUR, DIRIND, GER, SUP, COORD)
    EQUIPE = GESTAO + (ANA, FIN, CONT, TI, SUTI, INFOSEC, RH, TREINA, JURI, MARK,
                       DESIGN, COMERCIAL, PROD, LOGI, QUALI, PD, ATEND)

    return {
        "name": name,
        "roles": [
            _role(CEO, 0xFFD700, ["administrator"], True),
            _role(VICE, 0xE74C3C, ["administrator"], True),
            _role(CONSELHO, 0x9B59B6, ["manage_guild", "manage_channels", "manage_messages", "view_audit_log"], True),
            _role(CFO, 0xF1C40F, ["manage_channels", "manage_messages", "view_audit_log"], True),
            _role(COO, 0xE67E22, ["manage_channels", "manage_messages", "moderate_members", "view_audit_log"], True),
            _role(CTO, 0x11806A, ["manage_channels", "manage_messages", "manage_webhooks"], True),
            _role(CMO, 0xE91E63, ["manage_messages", "embed_links", "attach_files", "mention_everyone"], True),
            _role(CHRO, 0x2ECC71, ["manage_messages", "moderate_members"], True),
            _role(DIRJUR, 0x34495E, ["manage_messages"], True),
            _role(DIRIND, 0x5D6D7E, ["manage_messages"], True),
            _role(GER, 0x3498DB, ["manage_messages", "moderate_members"], True),
            _role(SUP, 0x5DADE2, ["manage_messages"], True),
            _role(COORD, 0x48C9B0, ["manage_messages"], True),
            _role(ANA, 0x99AAB5, ["embed_links", "attach_files"], True),
            _role(FIN, 0x2ECC71, [], True),
            _role(CONT, 0x27AE60, [], True),
            _role(TI, 0x1ABC9C, ["manage_messages", "manage_webhooks"], True),
            _role(SUTI, 0x16A085, ["manage_messages"], True),
            _role(INFOSEC, 0x17202A, [], True),
            _role(RH, 0xF5B041, ["manage_messages"], True),
            _role(TREINA, 0xAF7AC5, ["manage_messages"], True),
            _role(JURI, 0x707B7C, [], True),
            _role(MARK, 0xE91E63, ["embed_links", "attach_files", "mention_everyone"], True),
            _role(DESIGN, 0xF5B041, ["attach_files", "embed_links"], True),
            _role(COMERCIAL, 0x1ABC9C, ["manage_messages", "embed_links"], True),
            _role(PROD, 0x7F8C8D, [], True),
            _role(LOGI, 0x85C1E9, [], True),
            _role(QUALI, 0x99A3A4, [], True),
            _role(PD, 0x9B59B6, [], True),
            _role(ATEND, 0x48C9B0, ["manage_messages"], True),

            _role("🌱・Estagiário", 0x7289DA),
            _role("👤・Colaborador", 0x99AAB5, ["add_reactions"]),
            _role("🏅・Destaque-do-Mês", 0xFFD700, ["attach_files"], True),
            _role("🤝・Parceiro", 0x1ABC9C, ["embed_links"]),
            _role("🔇・Silenciado", 0x546E7A),
            _role("🤖・Robô", 0x747F8D),
        ],
        "categories": [
            _cat("🏛️・INSTITUCIONAL", [
                _txt("📜・código-de-conduta", _readonly(*EQUIPE)),
                _txt("🏢・sobre-a-empresa", _readonly(*EQUIPE)),
                _txt("🎯・missão-e-valores", _readonly(*EQUIPE)),
                _txt("📊・organograma", _readonly(*GESTAO)),
                _txt("📋・políticas-internas", _readonly(*GESTAO)),
                _txt("📢・comunicados-gerais", _readonly(*GESTAO)),
            ]),
            _cat("🚪・RECEPÇÃO", [
                _txt("👋・boas-vindas", _readonly(*EQUIPE)),
                _txt("🎤・apresentações"),
                _txt("❓・dúvidas-gerais"),
            ]),
            _cat("🧑‍💼・SETORES", [
                _txt("💰・chat-financeiro", _lock(FIN, CONT, CFO, SUP, *ALTA)),
                _txt("💻・chat-ti", _lock(TI, SUTI, INFOSEC, CTO, *ALTA)),
                _txt("👥・chat-rh", _lock(RH, TREINA, CHRO, *ALTA)),
                _txt("📣・chat-marketing", _lock(MARK, DESIGN, CMO, *ALTA)),
                _txt("🤝・chat-comercial", _lock(COMERCIAL, ATEND, *ALTA)),
                _txt("🏭・chat-produção", _lock(PROD, LOGI, QUALI, DIRIND, *ALTA)),
                _txt("⚖️・chat-jurídico", _lock(JURI, DIRJUR, *ALTA)),
            ]),
            _cat("💼・GESTÃO", [
                _txt("🔒・diretoria-chat"),
                _txt("📅・planejamento-estratégico"),
                _txt("🎯・metas-e-kpis"),
                _txt("📊・relatórios-mensais"),
                _txt("🕵️・auditoria", _lock(*ALTA)),
            ], _lock(*GESTAO)),
            _cat("👥・RECURSOS-HUMANOS", [
                _txt("📋・vagas-abertas", _readonly(RH, CHRO, *ALTA)),
                _txt("📥・candidaturas", _lock(RH, CHRO, TREINA, *ALTA)),
                _txt("🎓・onboarding", _lock(RH, TREINA, *ALTA)),
                _txt("🗓️・folgas-e-escala", _lock(RH, SUP, *ALTA)),
                _txt("⭐・avaliações", _lock(RH, SUP, *GESTAO)),
            ]),
            _cat("🎓・CAPACITAÇÃO", [
                _txt("📚・materiais-de-estudo", _lock(*EQUIPE)),
                _txt("📜・certificações", _lock(TREINA, RH, *ALTA)),
                _txt("💡・treinamentos", _lock(TREINA, *ALTA)),
            ]),
            _cat("💻・TECNOLOGIA", [
                _txt("🛠️・suporte-ti", _lock(SUTI, TI, *ALTA)),
                _txt("🚨・incidentes", _lock(SUTI, TI, INFOSEC, *ALTA)),
                _txt("🖥️・infraestrutura", _lock(TI, INFOSEC, CTO, *ALTA)),
                _txt("🐛・bugs-e-correções", _lock(TI, PD, *ALTA)),
                _txt("📝・changelog-de-sistemas", _lock(TI, *ALTA)),
            ]),
            _cat("📣•MARKETING", [
                _txt("🎨・campanhas", _lock(MARK, DESIGN, CMO, *ALTA)),
                _txt("📱・redes-sociais", _lock(MARK, *ALTA)),
                _txt("🎬・conteúdo", _lock(MARK, DESIGN, *ALTA)),
            ]),
            _cat("🏭・OPERAÇÃO", [
                _txt("⚙️・produção-diária", _lock(PROD, SUP, DIRIND, *ALTA)),
                _txt("🧪・controle-de-qualidade", _lock(QUALI, DIRIND, *ALTA)),
                _txt("🔬・pesquisa-e-desenvolvimento", _lock(PD, DIRIND, *ALTA)),
                _txt("🚚・expedição", _lock(LOGI, DIRIND, *ALTA)),
            ]),
            _cat("📞・ATENDIMENTO", [
                _txt("💬・atendimento-a-clientes"),
                _txt("⚠️・reclamações", _lock(ATEND, COMERCIAL, *ALTA)),
                _txt("⭐・satisfação", _lock(ATEND, CMO, *ALTA)),
            ]),
            _cat("🎉・BEM-ESTAR", [
                _txt("☕・coffee-break"),
                _txt("🎂・aniversariantes"),
                _txt("🎊・festas-da-empresa"),
                _txt("💬・feedback-da-equipe"),
            ]),
            _cat("🔊・VOZ", [
                _vc("🏢・Reunião-Geral"), _vc("🔒・Sala-da-Diretoria"),
                _vc("💻・Suporte"), _vc("🏭・Chão-de-Fábrica"),
                _vc("☕・Call-Livre"),
            ]),
            _cat("🧰・FERRAMENTAS", [
                _txt("🤖・comandos"), _txt("🧾・logs"),
            ]),
        ],
    }


# ---------- 🌐 REDE DE SERVIDORES ----------
def rede(name="Slayer Network 🌐"):
    DONO = "👑・Dono-da-Rede"
    COOWNER = "⚜️・Co-Owner"
    ADGLOBAL = "🧭・Admin-Global"
    DEV = "🧠・Developer"
    MODGLOBAL = "🛡️・Staff-Global"
    SUPORTE = "🎫・Suporte-da-Rede"
    MIDIA = "📣・Mídia-da-Rede"
    PARCEIRO = "🤝・Parceiro-da-Rede"
    GER5M = "🚗・Gerente-FiveM"
    GERMC = "⛏️・Gerente-Minecraft"
    GERGAME = "🎮・Gerente-Gaming"
    MOD = "🛠️・Moderador"

    ALTA = (DONO, COOWNER)
    STAFF = ALTA + (ADGLOBAL, DEV, MODGLOBAL, SUPORTE, MIDIA, MOD)
    EQUIPE = STAFF + (PARCEIRO, GER5M, GERMC, GERGAME)

    return {
        "name": name,
        "roles": [
            _role(DONO, 0xFFD700, ["administrator"], True),
            _role(COOWNER, 0xE74C3C, ["administrator"], True),
            _role(ADGLOBAL, 0xE67E22, ["manage_channels", "manage_roles", "manage_messages", "kick_members", "ban_members", "moderate_members", "view_audit_log"], True),
            _role(DEV, 0x11806A, ["manage_messages", "manage_webhooks", "manage_guild"], True),
            _role(MODGLOBAL, 0x9B59B6, ["manage_messages", "kick_members", "moderate_members"], True),
            _role(SUPORTE, 0x48C9B0, ["manage_messages"], True),
            _role(MIDIA, 0xE91E63, ["manage_messages", "embed_links", "mention_everyone"], True),
            _role(PARCEIRO, 0x1ABC9C, ["embed_links"], True),
            _role(GER5M, 0x5DADE2, ["manage_messages", "manage_channels", "moderate_members"], True),
            _role(GERMC, 0x27AE60, ["manage_messages", "manage_channels", "moderate_members"], True),
            _role(GERGAME, 0x9B59B6, ["manage_messages", "manage_channels", "moderate_members"], True),
            _role(MOD, 0x3498DB, ["manage_messages", "moderate_members"], True),

            _role("💎・VIP-Global", 0xF1C40F, ["attach_files", "embed_links"], True),
            _role("🚗・VIP-FiveM", 0x5DADE2, [], True),
            _role("⛏️・VIP-Minecraft", 0x27AE60, [], True),
            _role("🎮・VIP-Gaming", 0x9B59B6, [], True),

            _role("🗺️・Turista", 0x7289DA),
            _role("👤・Membro-da-Rede", 0x99AAB5, ["add_reactions"]),
            _role("🔇・Silenciado", 0x546E7A),
            _role("🤖・Robô", 0x747F8D),
        ],
        "categories": [
            _cat("🌐・REDE", [
                _txt("👋・boas-vindas", _readonly(*EQUIPE)),
                _txt("📜・regras-da-rede", _readonly(*EQUIPE)),
                _txt("🏢・sobre-a-rede", _readonly(*EQUIPE)),
                _txt("📊・status-dos-servidores", _readonly(*EQUIPE)),
                _txt("🗺️・como-entrar-nos-servidores", _readonly(*EQUIPE)),
                _txt("📰・novidades-da-rede", _readonly(*EQUIPE)),
            ]),
            _cat("📢・COMUNICADOS", [
                _txt("📣・anúncios", _readonly(*EQUIPE)),
                _txt("🔄・atualizações", _readonly(*EQUIPE)),
                _txt("🎉・eventos-da-rede", _readonly(*EQUIPE)),
                _txt("🧑‍💼・vagas-de-staff", _readonly(*EQUIPE)),
            ]),
            _cat("💬・HUB-DA-REDE", [
                _txt("💬・chat-geral"), _txt("🎤・apresentações"),
                _txt("📸・mídia"), _txt("🐸・memes"),
                _txt("💡・sugestões"), _txt("🏆・conquistas"),
            ]),
            _cat("🚗・FIVEM", [
                _txt("📌・info-fiveM", _readonly(GER5M, *STAFF)),
                _txt("💬・chat-fivem"),
                _txt("🚦・whitelist"),
                _txt("🎫・suporte-fivem"),
                _vc("🚗・Cidade-1"), _vc("🚗・Cidade-2"),
            ]),
            _cat("⛏️・MINECRAFT", [
                _txt("📌・info-minecraft", _readonly(GERMC, *STAFF)),
                _txt("💬・chat-minecraft"),
                _txt("🚦・whitelist-minecraft"),
                _txt("🎫・suporte-minecraft"),
                _vc("⛏️・Survival"), _vc("⛏️・Creative"),
            ]),
            _cat("🎮・GAMING", [
                _txt("📌・info-gaming", _readonly(GERGAME, *STAFF)),
                _txt("💬・chat-gaming"),
                _txt("🤝・matchmaking"),
                _vc("🎮・Squad-1"), _vc("🎮・Squad-2"), _vc("🎮・Squad-3"),
            ]),
            _cat("🎫・SUPORTE-DA-REDE", [
                _txt("❓・central-de-ajuda"),
                _txt("🚨・denúncias"),
                _txt("⚖️・apelacoes", _lock(SUPORTE, *STAFF)),
            ]),
            _cat("🤝•PARCERIAS", [
                _txt("📋・requisitos", _readonly(PARCEIRO, MIDIA, *STAFF)),
                _txt("📣・divulgação-de-parceiros", _readonly(PARCEIRO, MIDIA, *STAFF)),
                _txt("💬・chat-parceiros", _lock(PARCEIRO, MIDIA, *STAFF)),
            ]),
            _cat("🔒・DIRETORIA", [
                _txt("🔒・dono-chat", _lock(*ALTA)),
                _txt("🧠・dev-chat", _lock(DEV, ADGLOBAL, *ALTA)),
                _txt("🧾・logs-da-rede", _lock(*STAFF)),
                _txt("📅・planejamento", _lock(*STAFF)),
                _txt("💰・finanças-da-rede", _lock(*ALTA)),
            ], _lock(*STAFF)),
            _cat("🔊・VOZ", [
                _vc("🎙️・Palco-da-Rede"), _vc("🏢・Reunião-Global"),
                _vc("🎧・Música"), _vc("☕・Lounge"),
            ]),
            _cat("🧰・FERRAMENTAS", [
                _txt("🤖・comandos"),
            ]),
        ],
    }



# registro dos templates
TEMPLATES = {
    "futebol": {"label": "Futebol Profissional", "emoji": "⚽", "desc": "Clube profissional completo: diretoria, comissão técnica, médico, scouting, mercado, mídia e 60+ canais", "fn": futebol},
    "comunidade": {"label": "Comunidade", "emoji": "🏘️", "desc": "Comunidade premium: diversão, criadores de conteúdo, sorteios, eventos, voz e equipe completa", "fn": comunidade},
    "gaming": {"label": "Gaming", "emoji": "🎮", "desc": "Servidor de gaming competitivo: torneios, coach, ranking, streamers e squads de voz", "fn": gaming},
    "fivem": {"label": "FiveM / RP", "emoji": "🚗", "desc": "Cidade RP completa: whitelist, departamentos (polícia, EMS, justiça), facções, economia e imprensa", "fn": fivem},
    "mta": {"label": "MTA SA (GTA)", "emoji": "🏙️", "desc": "Servidor MTA completo: orgânicos, gangues e máfias, empregos, whitelist, scripters, ACL e justiça", "fn": mta},
    "loja": {"label": "Loja / E-commerce", "emoji": "🛒", "desc": "Loja completa: catálogo, pedidos, entregas, logística, financeiro e suporte ao cliente", "fn": loja},
    "empresa": {"label": "Empresa / Corporação", "emoji": "🏢", "desc": "Empresa completa: RH, TI, financeiro, jurídico, marketing e comercial", "fn": empresa},
    "studio": {"label": "Estúdio Musical", "emoji": "🎵", "desc": "Estúdio completo: gravação, produção, mixagem, lançamentos, divulgação e eventos", "fn": studio},
    "cla": {"label": "Clã de E-sports", "emoji": "🏆", "desc": "Clã competitivo: elenco titular e reserva, coach, analista, scrims e comunidade de torcedores", "fn": clã},
    "minecraft": {"label": "Minecraft", "emoji": "⛏️", "desc": "Servidor Minecraft com modos de jogo, comunidade, builders, desenvolvedores e suporte", "fn": minecraft},
    "youtube": {"label": "Criadores de Conteúdo", "emoji": "📺", "desc": "Comunidade para YouTubers, streamers, editores, designers, divulgação e parcerias", "fn": youtube},
    "anime": {"label": "Anime / Otaku", "emoji": "🍥", "desc": "Comunidade otaku com animes, mangás, fanarts, debates, eventos e cargos", "fn": anime},
    "estudos": {"label": "Estudos / Escola", "emoji": "📚", "desc": "Organização de estudos com matérias, tarefas, materiais, professores e grupos", "fn": estudos},
    "suporte": {"label": "Suporte Técnico", "emoji": "🧑‍💻", "desc": "Central de atendimento com tickets, equipe técnica, clientes e relatórios", "fn": suporte},
    "design": {"label": "Agência de Design", "emoji": "🎨", "desc": "Agência criativa com clientes, orçamentos, portfólio, entregas e equipe", "fn": design},
    "podcast": {"label": "Podcast", "emoji": "🎙️", "desc": "Servidor de podcast com episódios, pautas, gravações, convidados e ouvintes", "fn": podcast},
    "eventos": {"label": "Eventos", "emoji": "🎪", "desc": "Gestão de eventos com inscrições, calendário, divulgação, participantes e organização", "fn": eventos},
}


def get_template(key):
    t = TEMPLATES.get(key)
    return t["fn"]() if t else None


# ---------- VALIDAÇÃO DOS TEMPLATES ----------
def validar_templates():
    """Verifica nomes duplicados e categorias acima do limite de canais."""
    avisos = []
    for chave, item in TEMPLATES.items():
        dados = item["fn"]()
        nomes_cargos = [r["name"] for r in dados.get("roles", [])]
        if len(nomes_cargos) != len(set(nomes_cargos)):
            avisos.append(f"{chave}: existem cargos com nomes duplicados.")
        nomes_categorias = [c["name"] for c in dados.get("categories", [])]
        if len(nomes_categorias) != len(set(nomes_categorias)):
            avisos.append(f"{chave}: existem categorias com nomes duplicados.")
        canais = []
        for categoria in dados.get("categories", []):
            if len(categoria.get("channels", [])) > 50:
                avisos.append(f"{chave}: a categoria {categoria['name']} ultrapassa 50 canais.")
            canais.extend(c["name"] for c in categoria.get("channels", []))
        if len(canais) != len(set(canais)):
            avisos.append(f"{chave}: existem canais com nomes duplicados.")
    return avisos
