import argparse
from src.processador_pdf import ProcessadorPDF
from src.modelo_ia import AnalisadorPTBR

def executar_fluxo(caminho_pdf: str, pergunta: str):
    # Processamento do PDF
    pdf_processor = ProcessadorPDF()
    resultado = pdf_processor.processar_arquivo(caminho_pdf)
    
    if "erro" in resultado:
        print(f"Erro: {resultado['erro']}")
        return

    # Análise com IA
    ia = AnalisadorPTBR()
    resposta = ia.responder_pergunta(
        contexto=" ".join([b['texto'] for b in pdf_processor.blocos_texto]),
        pergunta=pergunta
    )
    
    print(f"\nResposta:\n{resposta['answer']}\n\nConfiança: {resposta['score']:.2%}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assistente de PDF em Português")
    parser.add_argument("--arquivo", required=True, help="Caminho do PDF")
    parser.add_argument("--pergunta", required=True, help="Pergunta sobre o conteúdo")
    
    args = parser.parse_args()
    executar_fluxo(args.arquivo, args.pergunta)
