import logging
from pydantic import ValidationError
from schemas import LiteratureOutput, BiomarkerOutput, PathwayOutput

class ValidationAgent:

    @staticmethod
    def validate_literature(data):
        try:
            if isinstance(data, LiteratureOutput):
                return True
            LiteratureOutput(**data)
            logging.info("[VALIDATOR] ✅ Literature passed")
            return True
        except ValidationError as e:
            logging.warning(f"[VALIDATOR] ❌ Literature failed: {e}")
            return False

    @staticmethod
    def validate_biomarkers(data):
        try:
            if isinstance(data, BiomarkerOutput):
                return True
            BiomarkerOutput(**data)
            logging.info("[VALIDATOR] ✅ Biomarkers passed")
            return True
        except ValidationError as e:
            logging.warning(f"[VALIDATOR] ❌ Biomarkers failed: {e}")
            return False

    @staticmethod
    def validate_pathway(data):
        try:
            if isinstance(data, PathwayOutput):
                return True
            PathwayOutput(**data)
            logging.info("[VALIDATOR] ✅ Pathway passed")
            return True
        except ValidationError as e:
            logging.warning(f"[VALIDATOR] ❌ Pathway failed: {e}")
            return False
