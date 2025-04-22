# schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class LiteratureResult(BaseModel):
    title: str
    id: str

class LiteratureOutput(BaseModel):
    papers: List[LiteratureResult]
    source_databases: List[str]

class DEGResult(BaseModel):
    gene: str
    log2FoldChange: float
    pvalue: float
    padj: float

class BiomarkerOutput(BaseModel):
    known_biomarkers: List[str]
    novel_predictions: List[str]
    deg_results: List[DEGResult]

class PathwayOutput(BaseModel):
    pathways: List[str]
    drug_targets: List[str]
