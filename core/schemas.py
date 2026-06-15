# core/schemas.py

# --- CHUVAS (Mensal 01-31) ---
CHUVA_CONFIG = {
    'table': 'dbo.Chuvas',
    'key_cols': ['EstacaoCodigo', 'NivelConsistencia', 'Data', 'TipoMedicaoChuvas'],
    'value_cols': ['Maxima', 'Total', 'TotalAnual'] + [f'Chuva{i:02d}' for i in range(1, 32)],
    'status_cols': ['MaximaStatus', 'TotalStatus', 'TotalAnualStatus', 'NumDiasDeChuvaStatus'] + [f'Chuva{i:02d}Status' for i in range(1, 32)],
    'extra_exact_cols': ['DiaMaxima', 'NumDiasDeChuva']
}

# --- CHUVAS2 (Mensal 01-31 com sufixo _1) ---
CHUVA2_CONFIG = {
    'table': 'dbo.Chuvas2',
    'key_cols': ['EstacaoCodigo', 'NivelConsistencia', 'Data', 'Hora1', 'TipoMedicaoChuvas'],
    'value_cols': ['Maxima', 'Total', 'TotalAnual'] + [f'Chuva{i:02d}_1' for i in range(1, 32)],
    'status_cols': ['MaximaStatus', 'TotalStatus', 'TotalAnualStatus', 'NumDiasDeChuvaStatus'] + [f'Chuva{i:02d}_1Status' for i in range(1, 32)],
    'extra_exact_cols': ['DiaMaxima', 'NumDiasDeChuva']
}

# --- CHUVAS24 (Horário 00-23) ---
CHUVA24_CONFIG = {
    'table': 'dbo.Chuvas24',
    'key_cols': ['EstacaoCodigo', 'NivelConsistencia', 'Data', 'TipoMedicaoChuvas'],
    'value_cols': ['Maxima', 'Total'] + [f'Chuva{i:02d}' for i in range(24)],
    'status_cols': ['MaximaStatus', 'TotalStatus'] + [f'Chuva{i:02d}Status' for i in range(24)],
    'extra_exact_cols': ['HoraMaxima']
}

# --- COTAS (Mensal 01-31) ---
COTAS_CONFIG = {
    'table': 'dbo.Cotas',
    'key_cols': ['EstacaoCodigo', 'NivelConsistencia', 'Data', 'Hora', 'TipoMedicaoCotas'],
    'value_cols': ['Maxima', 'Minima', 'Media', 'MediaAnual'] + [f'Cota{i:02d}' for i in range(1, 32)],
    'status_cols': ['MaximaStatus', 'MinimaStatus', 'MediaStatus', 'MediaAnualStatus'] + [f'Cota{i:02d}Status' for i in range(1, 32)],
    'extra_exact_cols': ['DiaMaxima', 'DiaMinima']
}

# --- COTAS24 (Horário 00-23) ---
COTAS24_CONFIG = {
    'table': 'dbo.Cotas24',
    'key_cols': ['EstacaoCodigo', 'NivelConsistencia', 'Data', 'TipoMedicaoCotas'],
    'value_cols': ['Maxima', 'Minima', 'Media'] + [f'Cota{i:02d}' for i in range(24)],
    'status_cols': ['MaximaStatus', 'MinimaStatus', 'MediaStatus'] + [f'Cota{i:02d}Status' for i in range(24)],
    'extra_exact_cols': ['HoraMaxima', 'HoraMinima']
}

# --- VAZÕES (Mensal 01-31) ---
VAZOES_CONFIG = {
    'table': 'dbo.Vazoes',
    'key_cols': ['EstacaoCodigo', 'NivelConsistencia', 'Data', 'Hora', 'MetodoObtencaoVazoes'],
    'value_cols': ['Maxima', 'Minima', 'Media', 'MediaAnual', 'MediaDiaria'] + [f'Vazao{i:02d}' for i in range(1, 32)],
    'status_cols': ['MaximaStatus', 'MinimaStatus', 'MediaStatus', 'MediaAnualStatus'] + [f'Vazao{i:02d}Status' for i in range(1, 32)],
    'extra_exact_cols': ['DiaMaxima', 'DiaMinima']
}

# --- VAZÕES24 (Horário 00-23) ---
VAZOES24_CONFIG = {
    'table': 'dbo.Vazoes24',
    'key_cols': ['EstacaoCodigo', 'NivelConsistencia', 'Data', 'Hora', 'MetodoObtencaoVazoes'],
    'value_cols': ['Maxima', 'Minima', 'Media', 'MediaDiaria'] + [f'Vazao{i:02d}' for i in range(24)],
    'status_cols': ['MaximaStatus', 'MinimaStatus', 'MediaStatus'] + [f'Vazao{i:02d}Status' for i in range(24)],
    'extra_exact_cols': ['HoraMaxima', 'DiaMinima']
}
