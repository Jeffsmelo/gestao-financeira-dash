from services.despesas_service import get_despesas
df = get_despesas(usuario="1207", ano=2025)
print(df.columns.tolist())