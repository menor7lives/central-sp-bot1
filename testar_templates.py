"""Valida os templates: permissões existem e cargos referenciados existem."""
import discord
import templates

valid = {f for f in dir(discord.Permissions()) if not f.startswith("_")}
ok = True

for key in templates.TEMPLATES:
    spec = templates.TEMPLATES[key]["fn"]()
    rolenames = {r["name"] for r in spec["roles"]}

    for r in spec["roles"]:
        for p in r["permissions"]:
            if p not in valid:
                print("PERM INVALIDA em", key, ":", p)
                ok = False

    for c in spec["categories"]:
        ow = dict(c.get("overwrites") or {})
        for ch in c["channels"]:
            ow.update(ch.get("overwrites") or {})
        for name in ow:
            if name != "@everyone" and name not in rolenames:
                print("CARGO INEXISTENTE em", key, ":", name)
                ok = False
        for rules in ow.values():
            for p in rules.get("allow", []) + rules.get("deny", []):
                if p not in valid:
                    print("PERM INVALIDA em", key, ":", p)
                    ok = False

    total_ch = sum(len(c["channels"]) for c in spec["categories"])
    print(f"{key}: {len(spec['roles'])} cargos, {len(spec['categories'])} categorias, {total_ch} canais")

print("TUDO VALIDO!" if ok else "ERROS ACIMA")
