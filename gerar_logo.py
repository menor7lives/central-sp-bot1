"""Logo Slayer Bot — S dentro do SL (monograma)."""

from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
d = ImageDraw.Draw(img)

# paleta
ROXO1 = (88, 101, 242)    # #5865F2
ROXO2 = (142, 68, 173)    # #8E44AD
VERMELHO = (231, 76, 60) # #E74C3C
BRANCO = (255, 255, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ============ S e L do "SL" de fundo (roxo, grandes) ============
sl_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sl_layer)

# ---- L de fundo (à direita) ----
# haste vertical
sd.rounded_rectangle([700, 180, 790, 840], radius=45, fill=ROXO2)
# pé do L
sd.rounded_rectangle([700, 750, 960, 840], radius=45, fill=ROXO2)

# ---- S de fundo (à esquerda) ----
# curva de cima (abre pra direita)
sd.arc([180, 200, 620, 560], start=-60, end=180, fill=ROXO1, width=90)
# curva de baixo (abre pra esquerda)
sd.arc([140, 460, 580, 820], start=120, end=360, fill=ROXO1, width=90)

img.alpha_composite(sl_layer)

# ============ S da frente (vermelho, dentro/encaixado) ============
f_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(f_layer)

# S central menor, encaixado no miolo do SL
# curva de cima
fd.arc([330, 300, 700, 620], start=-60, end=180, fill=VERMELHO, width=75)
# curva de baixo
fd.arc([300, 540, 670, 860], start=120, end=360, fill=VERMELHO, width=75)

img.alpha_composite(f_layer)

# ============ glow ============
glow = img.filter(ImageFilter.GaussianBlur(22))
ga = glow.copy()
a = ga.getchannel("A").point(lambda v: int(v * 0.5))
ga.putalpha(a)
final = Image.new("RGBA", (W, H), (255, 255, 255, 255))
final.alpha_composite(ga)
final.alpha_composite(img)

final.convert("RGB").save("slayer-logo.png", "PNG")
print("PNG salvo: slayer-logo.png — S dentro do SL")
