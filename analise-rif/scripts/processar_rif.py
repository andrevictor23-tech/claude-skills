#!/usr/bin/env python3
"""Processador de dados RIF/COAF.

Carrega, valida, limpa, deduplica e resume os 3 CSVs do RIF (Envolvidos,
Comunicacoes, Ocorrencias). Substitui o bloco de codigo que antes vivia colado
no SKILL.md: aqui e um arquivo executavel e testavel, nao um exemplo para
reproduzir a mao.

Uso:
    python processar_rif.py --entrada DIR_COM_OS_CSVS
    python processar_rif.py --entrada . --saida resumo.json
    python processar_rif.py --entrada . --exportar-limpos ./limpos

Requisito: pandas.
"""

import argparse
import json
import os
import re
import sys

import pandas as pd

CAMPOS_VALOR = ["CampoA", "CampoB", "CampoC", "CampoD", "CampoE"]


class ProcessadorRIF:
    def __init__(self, dir_entrada="."):
        self.dir = dir_entrada
        self.df_env = None
        self.df_com = None
        self.df_oco = None
        self.legendas_campos = {}
        self.log_processamento = []
        self.metricas = {}

    def log(self, msg):
        self.log_processamento.append(msg)
        print(msg)

    def carregar_csv(self, filepath):
        """Carrega CSV do COAF com deteccao automatica de encoding e separador."""
        for enc in ["latin-1", "utf-8", "cp1252"]:
            for sep in [";", ","]:
                try:
                    df = pd.read_csv(filepath, encoding=enc, sep=sep, dtype=str)
                except Exception:
                    continue
                if len(df.columns) > 1 and "Indexador" in df.columns:
                    self.log(
                        f"OK  Carregado: {os.path.basename(filepath)} "
                        f"({enc}, sep='{sep}', {len(df)} linhas)"
                    )
                    return df
        raise ValueError(f"Falha ao ler: {filepath}")

    def encontrar_arquivos(self):
        """Encontra os 3 CSVs do RIF no diretorio de entrada."""
        arquivos = os.listdir(self.dir)
        csv_files = [f for f in arquivos if f.lower().endswith(".csv") and "RIF" in f.upper()]

        env = [f for f in csv_files if "envolvido" in f.lower()]
        com = [f for f in csv_files if "comunicac" in f.lower()]
        oco = [f for f in csv_files if "ocorrencia" in f.lower()]

        return env, com, oco

    def extrair_legendas(self, df_com_raw):
        """Extrai legendas dos campos de valores das linhas nao-indexadoras.

        A legenda do proprio arquivo prevalece sobre references/legenda_campos_segmento.md.
        """
        legendas = {}
        for _, row in df_com_raw.iterrows():
            idx = str(row.get("Indexador", "")).strip()
            if not idx.isdigit() and idx and re.match(r"^\d+\s*-", idx):
                # Linha de legenda: "42 - SFN - Especie: CampoA = Total..."
                match = re.match(r"^(\d+)\s*-\s*(.+)", idx)
                if match:
                    legendas[match.group(1)] = match.group(2)
        self.legendas_campos = legendas
        return legendas

    def filtrar_indexadores(self, df):
        """Mantem apenas as linhas com indexador numerico valido."""
        df_clean = df.copy()
        df_clean["Indexador"] = df_clean["Indexador"].astype(str).str.strip()
        mask = df_clean["Indexador"].str.match(r"^\d+$", na=False)
        removidos = int((~mask).sum())
        df_clean = df_clean[mask].copy()
        df_clean["Indexador"] = df_clean["Indexador"].astype(int)
        return df_clean, removidos

    def deduplicar(self, df_com):
        """Deduplica por idComunicacao (nivel-caso; ids vazios sao unicos — ver FASE 3).

        Entre duplicatas, mantem a linha com informacoesAdicionais mais longa.
        """
        if "idComunicacao" not in df_com.columns:
            return df_com, 0

        antes = len(df_com)
        ids = df_com["idComunicacao"].fillna("").astype(str).str.strip()
        sem_id = df_com[ids == ""]
        com_id = df_com[ids != ""].copy()
        com_id["_info_len"] = (
            com_id.get("informacoesAdicionais", pd.Series(dtype=str)).fillna("").str.len()
        )
        com_id = (
            com_id.sort_values("_info_len", ascending=False)
            .drop_duplicates(subset=["idComunicacao"], keep="first")
            .drop(columns=["_info_len"])
        )
        df_dedup = pd.concat([com_id, sem_id]).sort_index()
        return df_dedup, antes - len(df_dedup)

    def converter_valor(self, val):
        """Converte valor monetario brasileiro para float (regras da FASE 4.3)."""
        if pd.isna(val) or str(val).strip() in ["", "0", "-"]:
            return 0.0
        s = re.sub(r"\s|R\$", "", str(val), flags=re.IGNORECASE)
        if not s:
            return 0.0
        tem_ponto, tem_virgula = "." in s, "," in s
        if tem_ponto and tem_virgula:
            s = s.replace(".", "").replace(",", ".")
        elif tem_virgula:
            s = s.replace(",", ".")
        elif tem_ponto and re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s):
            s = s.replace(".", "")
        try:
            return float(s)
        except ValueError:
            return 0.0

    def processar(self):
        """Pipeline completo. Devolve True se processou os 3 arquivos."""
        env_files, com_files, oco_files = self.encontrar_arquivos()

        faltando = [
            nome
            for nome, lista in (("Envolvidos", env_files), ("Comunicacoes", com_files), ("Ocorrencias", oco_files))
            if not lista
        ]
        if faltando:
            self.log(f"ERRO  CSV do RIF nao encontrado: {', '.join(faltando)} (em {self.dir})")
            return False

        self.df_env = self.carregar_csv(os.path.join(self.dir, env_files[0]))
        self.df_com = self.carregar_csv(os.path.join(self.dir, com_files[0]))
        self.df_oco = self.carregar_csv(os.path.join(self.dir, oco_files[0]))

        # Legendas saem das linhas nao-indexadoras — extrair ANTES de filtrar.
        self.extrair_legendas(self.df_com)

        self.df_env, rem_env = self.filtrar_indexadores(self.df_env)
        self.df_com, rem_com = self.filtrar_indexadores(self.df_com)
        self.df_oco, rem_oco = self.filtrar_indexadores(self.df_oco)
        self.log(
            f"Indexadores filtrados - Env: {rem_env} removidos, "
            f"Com: {rem_com} removidos, Oco: {rem_oco} removidos"
        )

        self.df_com, dedup = self.deduplicar(self.df_com)
        self.log(f"Deduplicacao: {dedup} comunicacoes duplicadas eliminadas")

        for campo in CAMPOS_VALOR:
            if campo in self.df_com.columns:
                self.df_com[f"{campo}_float"] = self.df_com[campo].apply(self.converter_valor)

        titulares = self.df_env[self.df_env["tipoEnvolvido"].str.strip().str.lower() == "titular"]
        self.metricas = {
            "comunicacoes_validas": len(self.df_com),
            "comunicacoes_removidas_dedup": dedup,
            "indexadores_unicos": int(self.df_com["Indexador"].nunique()),
            "titulares": int(titulares["cpfCnpjEnvolvido"].nunique()),
            "envolvidos": int(self.df_env["cpfCnpjEnvolvido"].nunique()),
            "ocorrencias": len(self.df_oco),
            "valor_total_campoA": float(self.df_com["CampoA_float"].sum())
            if "CampoA_float" in self.df_com.columns
            else 0.0,
            "periodo_inicio": str(self.df_com["Data_da_operacao"].min())
            if "Data_da_operacao" in self.df_com.columns
            else "N/I",
            "periodo_fim": str(self.df_com["Data_da_operacao"].max())
            if "Data_da_operacao" in self.df_com.columns
            else "N/I",
            "legendas_do_arquivo": self.legendas_campos,
        }

        m = self.metricas
        valor = f"{m['valor_total_campoA']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.log("")
        self.log("RESUMO DO RIF:")
        self.log(f"   Comunicacoes validas: {m['comunicacoes_validas']}")
        self.log(f"   Indexadores unicos:   {m['indexadores_unicos']}")
        self.log(f"   Titulares:            {m['titulares']}")
        self.log(f"   Total de envolvidos:  {m['envolvidos']}")
        self.log(f"   Valor total (CampoA): R$ {valor}")
        self.log(f"   Periodo:              {m['periodo_inicio']} a {m['periodo_fim']}")

        return True

    def exportar_limpos(self, destino):
        """Grava os 3 dataframes ja limpos em CSV UTF-8, para as fases seguintes."""
        os.makedirs(destino, exist_ok=True)
        for nome, df in (("envolvidos", self.df_env), ("comunicacoes", self.df_com), ("ocorrencias", self.df_oco)):
            caminho = os.path.join(destino, f"limpo_{nome}.csv")
            df.to_csv(caminho, index=False, encoding="utf-8", sep=";")
            self.log(f"Gravado: {caminho}")


def main():
    ap = argparse.ArgumentParser(description="Processa os CSVs do RIF/COAF (validacao, limpeza, deduplicacao, resumo).")
    ap.add_argument("--entrada", default=".", help="diretorio com os 3 CSVs do RIF (padrao: diretorio atual)")
    ap.add_argument("--saida", help="grava o resumo em JSON neste arquivo")
    ap.add_argument("--exportar-limpos", metavar="DIR", help="grava os CSVs ja limpos neste diretorio")
    args = ap.parse_args()

    proc = ProcessadorRIF(args.entrada)
    if not proc.processar():
        return 1

    if args.exportar_limpos:
        proc.exportar_limpos(args.exportar_limpos)

    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as fh:
            json.dump(proc.metricas, fh, ensure_ascii=False, indent=2)
        print(f"\nResumo gravado em {args.saida}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
