import pandas as pd

# leer datos crudos
df = pd.read_csv("data/raw_crypto.csv")

# seleccionar columnas importantes
df = df[['name', 'current_price', 'market_cap', 'price_change_percentage_24h']]

# renombrar
df = df.rename(columns={
    'name': 'crypto',
    'current_price': 'precio',
    'market_cap': 'capitalizacion',
    'price_change_percentage_24h': 'cambio_24h'
})

# limpiar
df = df.dropna()

# Después de limpiar los datos
df['cambio_24h'] = df['cambio_24h'].round(2)
df['cambio_24h'] = df['cambio_24h'].replace(-0.00, 0.00)

# guardar limpio
df.to_csv("data/crypto.csv", index=False)

print(df.head())