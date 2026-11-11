# 🤖 Central São Paulo Bot

Bot do Discord que **faz tudo por menção**: conversa com IA e **monta servidores completos**
(cargos, categorias, canais e permissões) automaticamente — com painel interativo dentro do Discord.

## ✨ O que ele faz

- **Respostas com IA** quando você menciona `@bot`
- **Reset total + criação por menção**: quando você pede pra criar, ele **apaga TODOS os canais,
  categorias e cargos** do servidor e monta tudo **do zero**. Ex.:
  > `@bot crie um servidor profissional de futebol`
- **4 modelos prontos**: ⚽ Futebol Profissional, 🏘️ Comunidade, 🎮 Gaming, 🚗 FiveM/RP
- **Painel (dashboard) dentro do Discord**: comando `/painel` ou `@bot painel` → botões clicáveis
- **IA opcional**: se você colocar uma chave de IA, ele entende pedidos de forma natural e
  conversa sobre qualquer assunto. Sem chave, ele funciona por palavras-chave.

## ☁️ Deixar online 24/7 de graça (Render + GitHub)

Sem instalar nada — tudo pelo navegador:

### 1. Subir o código pro GitHub
1. Crie uma conta em **https://github.com** (se não tiver)
2. Clique em **New repository** → nome `central-sp-bot` → escolha **Private** → **Create**
3. Na página do repositório, clique em **"uploading an existing file"**
4. Abra a pasta `central-sp-bot` no seu computador e **arraste todos os arquivos** EXCETO:
   - ❌ `.env` (nunca subir — tem o token!)
   - ❌ pasta `__pycache__`
   - ❌ `ligar-bot.bat`, `testar_templates.py`
   - ✅ Suba: `bot.py`, `ai.py`, `builder.py`, `templates.py`, `config.py`, `requirements.txt`, `render.yaml`, `.gitignore`, `README.md`
5. Clique em **Commit changes**

### 2. Criar o serviço no Render
1. Acesse **https://render.com** → cadastre-se com o **GitHub**
2. **New +** → **Web Service** → conecte sua conta GitHub → escolha o repo `central-sp-bot`
3. Se o `render.yaml` for detectado, ele preenche tudo sozinho. Se não:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** **Free**
4. Em **Environment Variables**, adicione:
   - `DISCORD_TOKEN` → o token do seu bot
   - `OWNER_ID` → sua ID do Discord
5. **Deploy Web Service** → aguarde ~2 min → status **Live** = bot online 24/7! 🎉

### 3. Impedir de dormir (plano gratuito)
O plano free do Render adormece o serviço após 15 min sem visitas. Solução de graça:
1. Crie conta em **https://uptimerobot.com** (grátis)
2. **Add New Monitor** → tipo **HTTP(s)** → URL: a URL do seu serviço no Render (aparece no topo, ex: `https://central-sp-bot.onrender.com`) → intervalo: **10 minutos**
3. Salvar. O UptimeRobot "visita" o bot a cada 10 min e ele nunca dorme.

### ⚠️ Dicas importantes
- **Feche o bot no seu PC** antes de ligar no Render (dois bots com o mesmo token se conflitam)
- Se mudar algo no código, é só editar no GitHub (ou subir de novo) que o Render atualiza sozinho
- O `.env` continua só no seu computador — no Render você usou as variáveis de ambiente

## 🚀 Instalação (passo a passo)

1. **Crie o bot no Discord**
   - Acesse https://discord.com/developers/applications → **New Application** → dê o nome `Central SP Bot`
   - Aba **Bot** → **Reset Token** → copie o token
   - Aba **Bot** → ative **MESSAGE CONTENT INTENT** (e os 3 Privileged Intents)

2. **Convide o bot para seu servidor** (precisa de permissão de Administrador para montar tudo)
   - Aba **OAuth2 → URL Generator** → marque `bot` + `applications.commands`
   - Em *Bot Permissions*, marque **Administrator**
   - Abra o link gerado e escolha seu servidor **Central São Paulo**

3. **Configure**
   ```
   cd central-sp-bot
   copy .env.example .env
   ```
   Abra o `.env` com o Bloco de Notas e preencha `DISCORD_TOKEN=` e `OWNER_ID=` (sua ID: no
   Discord, atione Modo Desenvolvedor, clique com botão direito no seu perfil → *Copiar ID do usuário*).

4. **Instale e rode**
   ```
   pip install -r requirements.txt
   python bot.py
   ```

## 💡 Como usar

Digite **`/`** no chat para ver todos os comandos do bot (com autocomplete):

| Comando | O que faz |
|---|---|
| `/painel` | 🧩 Abre o painel com botões de criação |
| `/criar` | 🏗️ Monta servidor (menu: ⚽ Futebol, 🏘️ Comunidade, 🎮 Gaming, 🚗 RP) |
| `/ajuda` | ❓ Mostra tudo o que o bot faz |
| `/ping` | 🏓 Latência do bot |
| `/servidor` | 📊 Informações do servidor |
| `/avatar` | 🖼️ Avatar de um usuário |
| `/limpar` | 🧹 Apaga mensagens (moderação) |

Ou **mencione** e peça por texto:

| Ação | Como pedir |
|---|---|
| Abrir o painel | `@bot painel` |
| Criar servidor de futebol | `@bot crie um servidor profissional de futebol` |
| Criar comunidade | `@bot monte uma comunidade` |
| Criar servidor de jogos | `@bot cria um servidor de gaming` |
| Conversar | `@bot qual o melhor jogador do mundo?` |

### ⚠️ Sobre "criar servidores"
O Discord **não permite que bots criem servidores** (contas de bot não podem criar guildas —
só contas humanas). O fluxo é: você cria um servidor vazio (ou usa um que já tenha), convida o
bot com Administrador, e ele monta **tudo** dentro dele: cargos com permissões, categorias,
canais de texto e voz — exatamente como no seu pedido "servidor profissional de futebol".

## 🔑 IA (opcional, recomendado)

Funciona com qualquer API compatível com OpenAI. Exemplo grátis (Groq):
1. Crie uma chave em https://console.groq.com
2. No `.env`:
   ```
   AI_API_KEY=sua-chave
   AI_BASE_URL=https://api.groq.com/openai/v1
   AI_MODEL=llama-3.3-70b-versatile
   ```

Com IA ligada, o bot entende pedidos como *"faz um servidor de e-sports com cargos de manager"*
e monta um modelo personalizado — além de conversar sobre qualquer assunto.
