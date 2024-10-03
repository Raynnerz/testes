import pandas as pd
import numpy as np
df = pd.read_csv('registro_cancer.csv')  # Substitua pelo caminho correto do arquivo

# 1. Selecionar pacientes com Topografia de pulmão (TOPOGRUP = C34)
df = df[df['TOPOGRUP'] == 'C34']

# 2. Selecionar pacientes com estado de Residência de São Paulo (UFRESID = 'SP')
df = df[df['UFRESID'] == 'SP']

# 3. Selecionar pacientes com Base do Diagnóstico com Confirmação Microscópica (BASEDIAG = 3)
df = df[df['BASEDIAG'] == 3]

# 4. Retirar categorias 0, X e Y da coluna ECGRUP
df = df[~df['ECGRUP'].isin([0, 'X', 'Y'])]

# 5. Retirar pacientes que fizeram Hormonioterapia e TMO (HORMONIO = 1 e TMO = 1)
df = df[~((df['HORMONIO'] == 1) & (df['TMO'] == 1))]

# 6. Selecionar pacientes com Ano de Diagnóstico até 2019 (ANODIAG <= 2019)
df = df[df['ANODIAG'] <= 2019]

# 7. Retirar pacientes com IDADE menor do que 20 anos
df = df[df['IDADE'] >= 20]

# 8. Calcular a diferença em dias entre as datas (DTCONSULT, DTDIAG, DTTRAT)
df['DTCONSULT'] = pd.to_datetime(df['DTCONSULT'], errors='coerce')
df['DTDIAG'] = pd.to_datetime(df['DTDIAG'], errors='coerce')
df['DTTRAT'] = pd.to_datetime(df['DTTRAT'], errors='coerce')

# Cálculo das diferenças em dias
df['CONSDIAG'] = (df['DTCONSULT'] - df['DTDIAG']).dt.days
df['DIAGTRAT'] = (df['DTTRAT'] - df['DTDIAG']).dt.days
df['TRATCONS'] = (df['DTTRAT'] - df['DTCONSULT']).dt.days

# Codificação das colunas
df['CONSDIAG'] = pd.cut(df['CONSDIAG'], bins=[-np.inf, 30, 60, np.inf], labels=[0, 1, 2])
df['DIAGTRAT'] = pd.cut(df['DIAGTRAT'], bins=[-np.inf, 60, 90, np.inf], labels=[0, 1, 2], right=False)
df['TRATCONS'] = pd.cut(df['TRATCONS'], bins=[-np.inf, 60, 90, np.inf], labels=[0, 1, 2], right=False)

# 9. Criar a coluna binária de óbito, a partir da coluna ULTINFO
df['OBITO'] = df['ULTINFO'].apply(lambda x: 1 if x in [3, 4] else 0)

# 10. Remover colunas irrelevantes
colunas_para_remover = [
    'UFNASC', 'UFRESID', 'CIDADE', 'DTCONSULT', 'CLINICA', 'DTDIAG', 'BASEDIAG', 
    'TOPOGRUP', 'DESCTOPO', 'DESCMORFO', 'T', 'N', 'M', 'PT', 'PN', 'PM', 'S', 'G',
    'LOCALTNM', 'IDMITOTIC', 'PSA', 'GLEASON', 'OUTRACLA', 'META01', 'META02', 
    'META03', 'META04', 'DTTRAT', 'NAOTRAT', 'TRATAMENTO', 'TRATHOSP', 'TRATFANTES',
    'TRATFAPOS', 'HORMONIO', 'TMO', 'NENHUMANT', 'CIRURANT', 'RADIOANT', 
    'QUIMIOANT', 'HORMOANT', 'TMOANT', 'IMUNOANT', 'OUTROANT', 'HORMOAPOS', 
    'TMOAPOS', 'DTULTINFO', 'CICI', 'CICIGRUP', 'CICISUBGRU', 'FAIXAETAR', 'LATERALI', 
    'INSTORIG', 'RRAS', 'ERRO', 'DTRECIDIVA', 'RECNENHUM', 'RECLOCAL', 'RECREGIO', 
    'RECDIST', 'REC01', 'REC02', 'REC03', 'REC04', 'CIDO', 'DSCCIDO', 'HABILIT', 
    'HABIT11', 'HABILIT1', 'CIDADEH', 'PERDASEG'
]

df = df.drop(columns=colunas_para_remover)
print(df.head())
