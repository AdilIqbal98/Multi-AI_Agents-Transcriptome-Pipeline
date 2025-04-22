import logging
from orchestrator import TranscriptomicAnalysisAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("pipeline_trace.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def main():
    logging.info("[PIPELINE_MAP]")
    logging.info("- Step 1: literature_mining(query)")
    logging.info("- Step 2: identify_biomarkers(sequencing_data)")
    logging.info("- Step 3: pathway_drug_analysis(biomarkers)")
    logging.info("- Step 4: generate_report(literature, biomarkers, analysis)")

    query = "Identify transcriptomic biomarkers for aggressive breast cancer."
    sequencing_data = "DEGs/counts.csv"

    agent = TranscriptomicAnalysisAgent()
    report = agent.run_pipeline(query, sequencing_data)

    logging.info("\n\n[FINAL REPORT]\n" + report)

if __name__ == "__main__":
    main()
