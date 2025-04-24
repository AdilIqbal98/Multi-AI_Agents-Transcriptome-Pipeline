from orchestrator import run_pipeline
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='pipeline_retry_log.txt', level=logging.WARNING, format='%(asctime)s - %(message)s')
    count_file = "DEGs/counts.csv"
    report = run_pipeline(count_file)
    print("\n📘 Final Report:\n")
    print(report)
