import logging
import time
from datetime import datetime

def log_retry_attempt(agent_name, attempt, error):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] ❌ {agent_name} failed on attempt {attempt}: {error}"
    logging.warning(msg)
    with open("pipeline_retry_log.txt", "a") as f:
        f.write(msg + "\n")

def validate_and_retry(agent_func, validator_func=None, input_data=None, agent_name="Agent", max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            result = agent_func(input_data)
            if validator_func:
                if not validator_func(result.dict()):
                    raise ValueError("Validation failed")
            return result
        except Exception as e:
            log_retry_attempt(agent_name, attempt, e)
            time.sleep(1)  # Small delay before retry

    raise RuntimeError(f"{agent_name} failed after {max_retries} attempts.")
