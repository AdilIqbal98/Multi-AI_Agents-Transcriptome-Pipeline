from query_agent import generate_bioinformatics_style_query
from literature_mining import run_literature_agent
from biomarker_identification import run_biomarker_agent
from pathway_drug_analysis import run_pathway_agent
from report_generation import generate_final_report


def run_pipeline(count_file_path):
    # Step 0: Generate scientific query
    query = generate_bioinformatics_style_query()
    print(f"\n🧪 Generated Scientific Query: {query}\n")

    # Step 1: Literature mining
    print("🔍 Step 1: Literature Mining")
    literature = run_literature_agent(query)
    print("✅ Literature Output Received\n")

    # Step 2: Biomarker identification
    print("🧬 Step 2: Biomarker Identification")
    biomarkers = run_biomarker_agent(count_file_path)
    print("✅ Biomarker Output Received\n")

    # Step 3: Pathway and drug mapping
    print("🧪 Step 3: Pathway & Drug Mapping")
    gene_list = [entry["gene"] if isinstance(entry, dict) else entry.gene
                 for entry in biomarkers.known_biomarkers + biomarkers.novel_predictions]
    pathways = run_pathway_agent(gene_list)
    print("✅ Pathway Output Received\n")

    # Step 4: Report generation
    print("📄 Step 4: Report Generation")
    report = generate_final_report(
        literature.dict(), biomarkers.dict(), pathways.dict())
    print("\n✅ Final Report Generated\n")
    return report
