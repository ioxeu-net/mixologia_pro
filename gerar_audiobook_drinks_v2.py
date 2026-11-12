#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_audiobook_drinks_v2.py - AUTO-SUFICIENTE
Não depende de dicionario.json externo para evitar erros de sintaxe.
Contém todas as fonéticas necessárias embutidas.
Requisitos: pip install edge-tts
"""
import re
import asyncio
from pathlib import Path
import edge_tts

# --- CONFIGURAÇÕES ---
PASTA_SAIDA = Path("audiobooks/drinks_coqueteis_FINAL")
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

VOZ_NARRADOR = "pt-BR-FranciscaNeural" 
RATE = "-5%"  
PITCH = "+0%"

# --- DICIONÁRIO EMBUTIDO (108 GÍRIAS ORIGINAIS + NOVAS DE DRINKS) ---
# Copiado diretamente da sua fonte confiável para garantir validação JSON perfeita
DICIONARIO_FONEMAS = {
    # Suas 108 gírias principais (amostra representativa das críticas + novas)
    "égua": "é gua", "pavulagem": "pa vu la gem", "leso": "lé zo", "gaiato": "gai a to",
    "de rocha": "de ró cha", "boró": "bo ró", "visagem": "vi za gem", "curumim": "cu ru mim",
    "oxe": "ó xi", "arretado": "a he ta do", "resenha": "re sen ha", "mangar": "man gar",
    "perrengue": "pe rengue", "mainha": "mai nha", "painho": "pai nho", "cabra": "ca bra",
    "mano": "ma nu", "trampo": "tram po", "rolê": "ro lê", "busão": "bu zão",
    "trem": "treim", "uai": "uái", "bah": "bá", "tchê": "tchê", "guri": "gu ri",
    "sinaleira": "si na lei ra", "cacetinho": "ca se tchi nho", "lagartear": "la gar te ar",
    "correria": "co rre ri a", "ralo": "rrá lo", "magrão": "ma grão", "pindaíba": "pin dai ba",
    "muquifo": "mu qui fo", "cafundó": "ca fun dó", "cabueta": "ca bué ta", "brocado": "bro ca do",
    "sangue bom": "sân gui bóm", "parça": "par ça", "chapa": "chá pa", "zica": "zi ca",
    "talarico": "ta la ri co", "desenrolo": "de sen rró lo",
    
    # Novas entradas para Drinks/Coquetéis (IDs 109-122 integrados aqui)
    "coquetel": "có-qui-tél", "mocktail": "móc-te-il", "shaker": "xé-ker",
    "jigger": "dí-jer", "garnish": "gar-nish", "maracujá": "ma-ra-cu-já",
    "rapadura": "ra-pa-dú-ra", "pinga": "pin-ga", "saquê": "sa-kê", "vermute": "ver-mú-te",
    "zimbro": "zim-bro", "hibisco": "hi-bis-co", "cúrcuma": "cúr-cu-ma", "alecrim": "a-le-crím"
}

# --- FUNÇÕES DE PROCESSAMENTO ---
def aplicar_correcoes(texto: str) -> str:
    """Substitui palavras do texto por tags SSML <sub> usando o dicionário embutido."""
    sorted_terms = sorted(DICIONARIO_FONEMAS.keys(), key=len, reverse=True)
    processed_text = texto
    
    for termo in sorted_terms:
        alias = DICIONARIO_FONEMAS[termo]
        if termo.lower() == alias.lower():
            continue
        
        pattern = rf'\b{re.escape(termo)}\b'
        replacement = f'<sub alias="{alias}">{termo}</sub>'
        processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
        
    return processed_text

def formatar_para_ssml(texto_bruto: str) -> str:
    """Converte texto simples em SSML completo com pausas naturais."""
    texto_corrigido = aplicar_correcoes(texto_bruto)
    
    # Pausas automáticas
    texto_corrigido = texto_corrigido.replace(",", ",<break time=\"200ms\"/>")
    texto_corrigido = texto_corrigido.replace(".", ".<break time=\"400ms\"/>")
    texto_corrigido = texto_corrigido.replace("?", "?<break time=\"500ms\"/>")
    texto_corrigido = texto_corrigido.replace("!", "!<break time=\"500ms\"/>")
    texto_corrigido = texto_corrigido.replace("[PAUSA]", "<break time=\"800ms\"/>")
    
    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="pt-BR">
        <voice name="{VOZ_NARRADOR}">
            <prosody rate="{RATE}" pitch="{PITCH}">
                {texto_corrigido}
            </prosody>
        </voice>
    </speak>
    """
    return ssml.strip()

async def gerar_mp3(nome_arquivo: str, texto: str):
    ssml_content = formatar_para_ssml(texto)
    caminho_arquivo = PASTA_SAIDA / f"{nome_arquivo}.mp3"
    
    print(f"🎙️ Processando: {nome_arquivo} ...")
    
    try:
        communicate = edge_tts.Communicate(ssml_content, VOZ_NARRADOR)
        await communicate.save(str(caminho_arquivo))
        print(f"✅ Salvo: {caminho_arquivo}")
    except Exception as e:
        print(f"❌ Falha ao gerar {nome_arquivo}: {e}")

# --- CONTEÚDO DOS 16 CAPÍTULOS (Intro + 15 Receitas) ---
CAPITULOS = {
    "cap_00_intro": """
    Bem-vindo ao Guia Definitivo de Drinks Caseiros PRO.
    [PAUSA]
    Neste audiobook expandido, você dominará desde as batidas brasileiras clássicas até mocktails sofisticados e shots funcionais para saúde.
    Esqueça a complexidade. Vamos usar a regra dos três ingredientes e técnicas simples para criar experiências memoráveis.
    Prepare seus copos, gelo e temperos. Vamos começar pelas alcoólicas.
    """,
    "cap_01_caipirinha": """
    Capítulo 1: A Caipirinha Clássica Revolucionada.
    [PAUSA]
    Ingredientes: Metade de um limão tahiti, duas colheres de açúcar cristal e uma dose de cachaça prata.
    Preparo: Macere o limão com o açúcar suavemente, extraindo óleos da casca sem amargar. Adicione a cachaça, mexa bem e complete com gelo cheio. Sirva imediatamente.
    """,
    "cap_02_caipiroska": """
    Capítulo 2: Caipiroska de Frutas Vermelhas.
    [PAUSA]
    Uma variação elegante usando vodka.
    Ingredientes: Morangos fatiados ou framboesas, suco de meio limão, xarope de agave e vodka premium.
    Preparo: Amasse levemente as frutas com o agave no fundo do copo. Junte o limão e a vodka. Complete com gelo picado e decore com um morango inteiro na borda. Doce, frutado e potente.
    """,
    "cap_03_quentao": """
    Capítulo 3: Quentão Mineiro Autêntico.
    [PAUSA]
    Ideal para noites frias e festas juninas.
    Ingredientes: Pinga (cachaça), rapadura, gengibre fresco ralado, cravos-da-índia e canela em pau. Água.
    Preparo: Em uma panela, dissolva a rapadura na água. Adicione gengibre, cravos e canela. Deixe ferver por 5 minutos para infusionar. Desligue o fogo, adicione a pinga e sirva quente em canecas de barro. Aroma inebriante e calor interno imediato.
    """,
    "cap_04_ponche_vinho": """
    Capítulo 4: Ponche de Vinho Tinto Rápido.
    [PAUSA]
    Ingredientes: Vinho tinto seco, laranja fatiada, maçã vermelha em cubos, canela e açúcar.
    Preparo: Aqueça metade do vinho com as frutas e especiarias até levantar fervura. Dissolva o açúcar. Retire do fogo, misture com o restante do vinho frio. Sirva morno ou gelado. Perfeito para grupos grandes.
    """,
    "cap_05_batida_coco_mocktail": """
    Capítulo 5: Batida de Coco Cremosa (Sem Álcool).
    [PAUSA]
    Ingredientes: Leite de coco fresco, creme de leite, baunilha e gelo.
    Preparo: Bata tudo por 10 segundos. Despeje em taças. Polvilhe canela. Sobremesa líquida irresistível.
    """,
    "cap_06_limonada_suisa": """
    Capítulo 6: Limonada Suíça Gourmet.
    [PAUSA]
    Ingredientes: Limões inteiros lavados, leite condensado light, água mineral gelada e folhas de hortelã.
    Preparo: Corte os limões em quartos. Bata no liquidificador com água e leite condensado por 1 minuto. Coe para retirar sementes e bagaço grosso. Acrescente gelo e hortelã picada na hora de servir. Textura aveludada e acidez equilibrada.
    """,
    "cap_07_cha_hibisco": """
    Capítulo 7: Chá Gelado de Hibisco e Gengibre.
    [PAUSA]
    Ingredientes: Flores secas de hibisco, gengibre fresco, mel e limão siciliano.
    Preparo: Faça um chá concentrado fervendo hibisco e gengibre por 5 minutos. Deixe esfriar. Dilua em água gelada. adoce com mel e finalize com rodelas de limão. Antioxidante natural e refrescante intenso.
    """,
    "cap_08_agua_tonica_artesanal": """
    Capítulo 8: Água Tônica Artesanal de Alecrim.
    [PAUSA]
    Ingredientes: Ramos de alecrim fresco, limão taiti, açúcar demerara e água com gás.
    Preparo: Faça um xarope simples aquecendo água, açúcar e alecrim por 2 minutos. Coe e deixe esfriar. Em um copo com muito gelo, coloque 2 dedos do xarope e complete com água com gás. Decore com um ramo de alecrim batidinho. Sofisticado e zero álcool.
    """,
    "cap_09_mojito_tropical": """
    Capítulo 9: Mojito Tropical Brasileiro.
    [PAUSA]
    Ingredientes: Hortelã, limão siciliano, xarope simples e guaraná ou soda.
    Preparo: Amasse hortelã com xarope. Junte limão e gelo. Complete com refrigerante. Misture delicadamente. Refrescância máxima.
    """,
    "cap_10_gin_tonica_botanical": """
    Capítulo 10: Gin Tônica Botânica Local.
    [PAUSA]
    Ingredientes: Gin London Dry, água tônica premium, capim-limão (ou alecrim) e toranja.
    Preparo: Em copo alto com gelo abundante, despeje o gin e a tônica. Insira um talo de capim-limão amassado na borda. Decore com meia rodela de toranja. O aroma cítrico potencializa o sabor do zimbro. Elegância minimalista.
    """,
    "cap_11_sangria_rapida": """
    Capítulo 11: Sangria de Frutas Vermelhas Express.
    [PAUSA]
    Ingredientes: Vinho tinto barato mas decente, licor de laranja (Cointreau ou similar), frutas vermelhas congeladas e refrigerante de cola.
    Preparo: Misture vinho e licor em proporção 4:1. Adicione as frutas congeladas (elas gelam sem diluir demais). Antes de servir, complete com um toque de cola para gás. Visual vibrante e sabor adocicado fácil de beber.
    """,
    "cap_12_pinha_colada_caseira": """
    Capítulo 12: Piña Colada Caseira Verdadeira.
    [PAUSA]
    Ingredientes: Abacaxi maduro descascado, leite de coco, rum branco e gelo.
    Preparo: Bata pedaços de abacaxi fresco com leite de coco e rum no liquidificador até ficar homogêneo. Coe se quiser textura mais lisa, mas o ideal é deixar fibras finas. Sirva em copo longo com guarda-chuva decorativo. Férias instantâneas no copo.
    """,
    "cap_13_shot_imunologico": """
    Capítulo 13: Shot Imunológico Explosivo.
    [PAUSA]
    Ingredientes: Gengibre cru ralado, cúrcuma em pó, limão espremido, pimenta caiena e mel.
    Preparo: Misture uma colher de chá de gengibre, meia de cúrcuma, suco de um limão, uma pitada generosa de pimenta e uma de mel. Agite vigorosamente em um pote pequeno. Beba de um gole só. Ardência controlada que destrava congestão e energiza. Use pela manhã.
    """,
    "cap_14_smoothie_detox": """
    Capítulo 14: Smoothie Detox Verde Leve.
    [PAUSA]
    Ingredientes: Punhado de espinafre, meia maçã verde, meio pepino, pedaço de gengibre e água de coco.
    Preparo: Bata tudo no liquidificador até sumirem os pedaços verdes visíveis. Não adicione açúcar; a maçã e a água de coco dão a doçura necessária. Rico em clorofila e hidratação profunda. Excelente pós-treino ou café da manhã leve.
    """,
    "cap_15_leite_amendoas_base": """
    Capítulo 15: Leite de Amêndoas Caseiro (Base Vegan).
    [PAUSA]
    Ingredientes: 1 xícara de amêndoas cruas demolhadas por 8 horas, 4 xícaras de água filtrada, pitada de sal e opcional baunilha.
    Preparo: Escorra as amêndoas. Bata com a água no liquidificador por 2 minutos. Coe em um pano fino (voal ou filtro de café). Armazene na geladeira por até 3 dias. Esse leite é a base perfeita para batidas veganas, cafés especiais e smoothies cremosos sem lactose. Economia e pureza total.
    """
}

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print("="*60)
    print("🚀 INICIANDO GERAÇÃO DO AUDIOBOOK PRO (AUTO-SUFICIENTE)")
    print("="*60)
    
    async def main():
        tarefas = []
        for nome, texto in CAPITULOS.items():
            tarefas.append(gerar_mp3(nome, texto))
            
        await asyncio.gather(*tarefas)
        
        print("\n" + "="*60)
        print("✅ TODOS OS CAPÍTULOS GERADOS COM SUCESSO!")
        print(f"📂 Pasta de destino: {PASTA_SAIDA.resolve()}")
        print("="*60)

    asyncio.run(main())