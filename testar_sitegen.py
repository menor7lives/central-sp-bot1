"""Testa o gerador de sites — valida HTML de todos os tipos e o reconhecimento de pedidos."""
import sitegen

print("Tipos de site disponiveis:", len(sitegen.TIPOS))

for tipo in sitegen.TIPOS:
    html = sitegen.gerar_html(tipo)
    ok = all(x in html for x in ["<!DOCTYPE html>", "</html>", "charset", "viewport"])
    status = "VALIDO" if ok else "ERRO!"
    print(f"{tipo:12s} | {status} | {len(html)} bytes")

pedidos = [
    "cria um site de loja",
    "faz um site portfolio",
    "quero um site para barbearia",
    "site de restaurante",
    "me faz um site",
    "cria um site pra mim de fotografia",
]
print()
for p in pedidos:
    print("pedido:", p, "->", sitegen.match_tipo(p))
