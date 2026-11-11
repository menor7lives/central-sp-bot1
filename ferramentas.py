"""Ferramentas visuais: gerador de logos e banners (funciona com Pillow)."""
import io

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CORES = {
    "roxo": (88, 101, 242),
    "roxo escuro": (100, 63, 168),
    "azul": (52, 152, 219),
    "azul escuro": (31, 97, 141),
    "vermelho": (231, 76, 60),
    "vermelho escuro": (146, 43, 33),
    "dourado": (241, 196, 15),
    "verde": (46, 204, 113),
    "verde escuro": (24, 130, 82),
    "rosa": (232, 118, 165),
    "ciano": (26, 188, 156),
    "laranja": (230, 126, 34),
    "branco": (233, 236, 244),
    "preto": (35, 37, 42),
}


def cor_rgb(nome, padrao=(88, 101, 242)):
    return CORES.get((nome or "").strip().lower(), padrao)


def cor_hex_ou_nome(texto, padrao=0x5865F2) -> int:
    t = (texto or "").strip().lower()
    if not t:
        return padrao
    if t.startswith("#"):
        try:
            return int(t[1:], 16)
        except ValueError:
            return padrao
    if t in CORES:
        r, g, b = CORES[t]
        return (r << 16) + (g << 8) + b
    return padrao


def _fonte(tam):
    # Windows → Linux (Render) → fonte padrão escalável do Pillow
    for caminho in ("arialbd.ttf",
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(caminho, tam)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size=tam)
    except TypeError:
        return ImageFont.load_default()


def _claro(rgb, fator=0.35):
    return tuple(min(255, int(v + (255 - v) * fator)) for v in rgb)


def _escuro(rgb, fator=0.35):
    return tuple(max(0, int(v * (1 - fator))) for v in rgb)


def _texto_ajustado(desenhista, texto, largura, tam_ini):
    tam = tam_ini
    fonte = _fonte(tam)
    while tam > 14 and desenhista.textlength(texto, font=fonte) > largura:
        tam = int(tam * 0.92)
        fonte = _fonte(tam)
    return fonte


def _gradiente(W, H, c1, c2, caixa):
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    x0, y0, x1, y1 = caixa
    altura = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / altura
        cor = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)
        gd.line([(x0, y), (x1, y)], fill=cor)
    return grad


def gerar_logo_bytes(texto, cor="roxo") -> bytes:
    """Logo quadrada com inicial + nome (1024x1024 PNG)."""
    texto = (texto or "S").strip() or "S"
    c1 = cor_rgb(cor)
    c2 = _escuro(c1, 0.45)
    W = H = 1024
    img = Image.new("RGBA", (W, H), (0,  0, 0, 0))
    caixa = (64, 64, W - 64, H - 64)

    mascara = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mascara).rounded_rectangle(caixa, radius=190, fill=255)
    img.paste(_gradiente(W, H, c1, c2, caixa), (0, 0), mascara)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle(caixa, radius=190, outline=_claro(c1, 0.55), width=10)

    letra = texto[0].upper()
    d.text((W // 2, H // 2 - 70), letra, font=_fonte(560), anchor="mm",
           fill=(255, 255, 255, 255))
    nome = texto[:24]
    d.text((W // 2, H - 155), nome, font=_texto_ajustado(d, nome, W - 220, 110),
           anchor="mm", fill=_claro(c1, 0.8))

    glow = img.filter(ImageFilter.GaussianBlur(16))
    ga = glow.getchannel("A").point(lambda v: int(v * 0.45))
    glow.putalpha(ga)
    final = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    final.alpha_composite(glow)
    final.alpha_composite(img)

    buf = io.BytesIO()
    final.convert("RGB").save(buf, "PNG")
    return buf.getvalue()


def gerar_banner_bytes(nome, membros, subtitulo="") -> bytes:
    """Banner 1500x500 com nome do servidor e contagem de membros."""
    W, H = 1500, 500
    c1, c2 = (88, 101, 242), (100, 63, 168)
    img = Image.new("RGBA", (W, H), (18, 18, 22, 255))
    img.paste(_gradiente(W, H, c1, c2, (0, 0, W, H)), (0, 0))

    d = ImageDraw.Draw(img)
    # círculos decorativos translúcidos
    d.ellipse([W - 260, -160, W + 160, 260], fill=(255, 255, 255, 18))
    d.ellipse([-200, H - 220, 220, H + 180], fill=(255, 255, 255, 14))
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=28,
                        outline=(255, 255, 255, 60), width=3)

    titulo = (nome or "Seu Servidor")[:40]
    d.text((W // 2, 195), titulo, font=_texto_ajustado(d, titulo, W - 200, 150),
           anchor="mm", fill=(255, 255, 255, 255))

    linha2 = f"• {membros} membros" + (f"  •  {subtitulo}" if subtitulo else "")
    d.text((W // 2, 330), linha2[:80], font=_texto_ajustado(d, linha2[:80], W - 320, 70),
           anchor="mm", fill=(235, 236, 244, 255))

    d.text((W // 2, 430), "SLAYER BOT", font=_fonte(48), anchor="mm",
           fill=(241, 196, 15, 235))

    buf = io.BytesIO()
    img.convert("RGB").save(buf, "PNG")
    return buf.getvalue()
