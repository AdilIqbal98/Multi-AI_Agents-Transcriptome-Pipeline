import logging
from schemas import LiteratureOutput, BiomarkerOutput, PathwayOutput
from pydantic import ValidationError

class ValidationAgent:

    @staticmethod
    def validate_literature(data):
        try:
            LiteratureOutput(**data)
            logging.info("[VALIDATOR] ✅ Literature passed")
            return True
        except ValidationError as e:
            logging.warning(f"[VALIDATOR] ❌ Literature failed: {e}")
            return False

    @staticmethod
    def validate_biomarkers(data):
        try:
            BiomarkerOutput(**data)
            logging.info("[VALIDATOR] ✅ Biomarkers passed")
            return True
        except ValidationError as e:
            logging.warning(f"[VALIDATOR] ❌ Biomarkers failed: {e}")
            return False

    @staticmethod
    def validate_pathway(data):
        try:
            PathwayOutput(**data)
            logging.info("[VALIDATOR] ✅ Pathway passed")
            return True
        except ValidationError as e:
            logging.warning(f"[VALIDATOR] ❌ Pathway failed: {e}")
            return False
