#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organizar_blocos.py - Separação Final: Alcoólicos vs Zero Álcool
Numeração independente para cada bloco (A-01... e B-01...).
Requisitos: Nenhuma dependência externa além da stdlib.
"""
import shutil
from pathlib import Path

# --- CONFIGURAÇÕES ---
PASTA_ORIGEM = Path("audiobooks/drinks_coqueteis_FINAL")
PASTA_DESTINO_A = Path("produto_final/Bloco_A_Clasicos_Alcoolicos")
PASTA_DESTINO_B = Path("produto_final/Bloco_B_Zero_Alcool_Funcionais")
ARQ_INTRO = "cap_00_intro.mp3" # Tratamento especial da introdução

# Mapeamento de Origem -> Novo Nome (Bloco A)
MAPA_BLOCO_A = {
    "cap_01_caipirinha": "A-01_Caipirinha_Classica",
    "cap_02_caipiroska": "A-02_Caipiroska_Frutas",
    "cap_03_quentao": "A-03_Quentao_Mineiro",
    "cap_04_ponche_vinho": "A-04_Ponche_Vinho_Tinto",
    "cap_09_mojito_tropical": "A-05_Mojito_Tropical_BR",
    "cap_10_gin_tonica_botanical": "A-06_Gin_Tonica_Botanica",
    "cap_11_sangria_rapida": "A-07_Sangria_Expressa",
    "cap_12_pinha_colada_caseira": "A-08_Pinha_Colada_Caseira"
}

# Mapeamento de Origem -> Novo Nome (Bloco B)
MAPA_BLOCO_B = {
    "cap_05_batida_coco_mocktail": "B-01_Batida_Coco_Sem_Alcool",
    "cap_06_limonada_suisa": "B-02_Limonada_Suisa_Gourmet",
    "cap_07_cha_hibisco": "B-03_Cha_Hibisco_Gelado",
    "cap_08_agua_tonica_artesanal": "B-04_Agua_Tonica_Alecrim",
    "cap_13_shot_imunologico": "B-05_Shot_Imunologico",
    "cap_14_smoothie_detox": "B-06_Smoothie_Detox_Verde",
    "cap_15_leite_amendoas_base": "B-07_Leite_Amendoas_Base"
}

def organizar_produtos():
    print("="*60)
    print("🚀 INICIANDO ORGANIZAÇÃO DOS PRODUTOS FINAIS")
    print("="*60)

    # Criar pastas de destino
    PASTA_DESTINO_A.mkdir(parents=True, exist_ok=True)
    PASTA_DESTINO_B.mkdir(parents=True, exist_ok=True)
    
    if not PASTA_ORIGEM.exists():
        print(f"❌ Erro: Pasta de origem não encontrada: {PASTA_ORIGEM}")
        return

    arquivos_origem = list(PASTA_ORIGEM.glob("*.mp3"))
    print(f"📂 Encontrados {len(arquivos_origem)} arquivos MP3 na origem.")

    sucesso_a = 0
    sucesso_b = 0
    erros = []

    for arquivo in arquivos_origem:
        nome_sem_ext = arquivo.stem # Remove .mp3
        
        # Verificar Bloco A
        if nome_sem_ext in MAPA_BLOCO_A:
            novo_nome = MAPA_BLOCO_A[nome_sem_ext] + ".mp3"
            destino = PASTA_DESTINO_A / novo_nome
            try:
                shutil.copy2(arquivo, destino)
                print(f"✅ [A] Copiado: {nome_sem_ext} -> {novo_nome}")
                sucesso_a += 1
            except Exception as e:
                erros.append(f"A: {nome_sem_ext} ({e})")
        
        # Verificar Bloco B
        elif nome_sem_ext in MAPA_BLOCO_B:
            novo_nome = MAPA_BLOCO_B[nome_sem_ext] + ".mp3"
            destino = PASTA_DESTINO_B / novo_nome
            try:
                shutil.copy2(arquivo, destino)
                print(f"✅ [B] Copiado: {nome_sem_ext} -> {novo_nome}")
                sucesso_b += 1
            except Exception as e:
                erros.append(f"B: {nome_sem_ext} ({e})")
                
        # Ignorar outros (como intro ou duplicados não mapeados explicitamente neste script)
        else:
            print(f"ℹ️  Ignorado (não mapeado): {nome_sem_ext}")

    # Relatório Final
    print("\n" + "="*60)
    print("📊 RESUMO DA ORGANIZAÇÃO:")
    print(f"   Bloco A (Alcoólicos): {sucesso_a} arquivos organizados.")
    print(f"   Bloco B (Zero Álcool): {sucesso_b} arquivos organizados.")
    
    if erros:
        print(f"   ⚠️  Erros encontrados: {len(erros)}")
        for err in erros:
            print(f"      - {err}")
    else:
        print("   ✅ Nenhum erro detectado.")
        
    print(f"\n📂 Pastas criadas em: {Path('produto_final').resolve()}")
    print("="*60)

if __name__ == "__main__":
    organizar_produtos()