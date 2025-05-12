# -*- coding: utf-8 -*-
import fitz  # PyMuPDF
from typing import Dict, List

class ProcessadorPDF:
    """Classe principal para extração estruturada de textos PDF"""

    def __init__(self):
        self.blocos_texto = []
        self.metadados = {}

    def processar_arquivo(self, caminho_arquivo: str) -> Dict:
        """Processa PDF mantendo contexto visual e estrutural"""
        try:
            with fitz.open(caminho_arquivo) as doc:
                self.metadados = doc.metadata
                for num_pagina, pagina in enumerate(doc):
                    self._extrair_blocos(pagina, num_pagina + 1)
            return {"status": "sucesso", "blocos": len(self.blocos_texto)}
        except Exception as e:
            return {"erro": f"Falha no processamento: {str(e)}"}

    def _extrair_blocos(self, pagina, num_pagina: int):
        """Extrai blocos de texto com metadados visuais"""
        blocos = pagina.get_text("dict")["blocks"]
        for bloco in blocos:
            if bloco['type'] == 0:  # Bloco de texto
                span = bloco['lines'][0]['spans'][0]
                self.blocos_texto.append({
                    "pagina": num_pagina,
                    "texto": span['text'],
                    "fonte": span['font'],
                    "tamanho": span['size'],
                    "coordenadas": bloco['bbox']
                })
