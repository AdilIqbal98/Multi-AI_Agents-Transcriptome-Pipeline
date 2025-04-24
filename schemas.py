from pydantic import BaseModel
from typing import List, Dict

class Paper(BaseModel):
    title: str
    id: str

class LiteratureOutput(BaseModel):
    papers: List[Paper]
    source_databases: List[str]

class GeneEntry(BaseModel):
    gene: str
    condition: str

class DEGStat(BaseModel):
    gene: str
    log2FoldChange: float
    pvalue: float
    padj: float

class BiomarkerOutput(BaseModel):
    known_biomarkers: List[GeneEntry]
    novel_predictions: List[GeneEntry]
    deg_results: List[DEGStat]

class PathwayOutput(BaseModel):
    pathways: List[str]
    drug_targets: List[str]
