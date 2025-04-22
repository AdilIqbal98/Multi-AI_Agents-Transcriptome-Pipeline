import logging
from literature_mining import literature_mining
from biomarker_identification import identify_biomarkers
from pathway_drug_analysis import pathway_drug_analysis
from report_generation import generate_report
from validation_agent import ValidationAgent

class TranscriptomicAnalysisAgent:
    def run_pipeline(self, query, sequencing_data):
        logging.info("[ORCHESTRATOR] Starting Pipeline")

        for attempt in range(2):
            literature = literature_mining(query)
            if ValidationAgent.validate_literature(literature):
                break
        else:
            return "[ORCHESTRATOR] ❌ Literature validation failed."

        for attempt in range(2):
            biomarkers = identify_biomarkers(sequencing_data)
            if ValidationAgent.validate_biomarkers(biomarkers):
                break
        else:
            return "[ORCHESTRATOR] ❌ Biomarker validation failed."

        for attempt in range(2):
            analysis = pathway_drug_analysis(biomarkers)
            if ValidationAgent.validate_pathway(analysis):
                break
        else:
            return "[ORCHESTRATOR] ❌ Pathway validation failed."

        return generate_report(literature, biomarkers, analysis)
