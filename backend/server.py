# backend/server.py - Servidor Flask completo com tratamento de erros
import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from io import StringIO
import csv
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configurações
BASE_DIR = Path(__file__).parent
CSV_FILE = os.path.join(BASE_DIR, 'operadoras.csv')
MAX_RESULTS = 20

def load_csv_safely(file_path):
    """Função robusta para carregar CSV com tratamento de erros"""
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'windows-1252']  # Tentar diferentes encodings
    
    for encoding in encodings:
        try:
            # Tenta ler com pandas primeiro
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                delimiter=';',
                dtype={'CNPJ': 'str'},
                on_bad_lines='warn'
            )
            
            # Verifica se há caracteres malformados nas primeiras linhas
            sample_text = df.head(5).to_string()
            if 'Ã' in sample_text and 'ã' not in sample_text:
                continue  # Provavelmente encoding errado, tentar próximo
                
            return df
            
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    
    # Se nenhum encoding funcionou, tentar fallback manual
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            
        for encoding in encodings:
            try:
                text = content.decode(encoding)
                if 'Ã' in text and 'ã' not in text:
                    continue
                    
                # Processamento manual se necessário
                lines = text.splitlines()
                reader = csv.DictReader(lines, delimiter=';')
                df = pd.DataFrame(list(reader))
                return df
            except:
                continue
                
    except Exception as e:
        print(f"Erro crítico ao ler CSV: {str(e)}")
    
    return pd.DataFrame()

# Carrega os dados ao iniciar o servidor
try:
    df = load_csv_safely(CSV_FILE)
    if not df.empty:
        print("Dados carregados com sucesso!")
        print(f"Total de registros: {len(df)}")
        # Padroniza nomes de colunas
        df.columns = df.columns.str.strip()
    else:
        print("DataFrame vazio - verifique o arquivo CSV")
except Exception as e:
    print(f"Falha ao carregar dados: {str(e)}")
    df = pd.DataFrame()

@app.route('/')
def home():
    return """
    <h1>Servidor Operadoras ANS</h1>
    <p>Endpoints disponíveis:</p>
    <ul>
        <li><a href="/api/buscar?q=saude">/api/buscar?q=termo</a> - Busca operadoras</li>
        <li><a href="/api/health">/api/health</a> - Verificar status do servidor</li>
    </ul>
    """

@app.route('/api/buscar', methods=['GET'])
def buscar_operadoras():
    try:
        termo = request.args.get('q', '').lower().strip()
        
        if df.empty:
            return jsonify({
                'success': False,
                'error': 'Dados não carregados',
                'results': []
            }), 503  # Service Unavailable
        
        if not termo:
            return jsonify({
                'success': True,
                'count': 0,
                'results': []
            })
        
        # Filtra os dados
        mask = (
            df['Razao_Social'].str.lower().str.contains(termo, na=False) |
            df['Nome_Fantasia'].str.lower().str.contains(termo, na=False) |
            df['CNPJ'].astype(str).str.contains(termo, na=False) |
            df['Cidade'].str.lower().str.contains(termo, na=False) |
            df['UF'].str.lower().str.contains(termo, na=False)
        )
        
        resultados = df[mask]
        
        return jsonify({
            'success': True,
            'count': len(resultados),
            'results': resultados.head(MAX_RESULTS).fillna('').to_dict('records')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'results': []
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy' if not df.empty else 'no_data',
        'data_loaded': not df.empty,
        'columns': list(df.columns) if not df.empty else [],
        'row_count': len(df) if not df.empty else 0
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')