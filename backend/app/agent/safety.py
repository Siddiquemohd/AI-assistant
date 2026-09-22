import hashlib
import json
from typing import Any, Dict

MAX_TOOL_CALLS_PER_RUN = 5

def generate_confirmation_token_digest(run_id: str, tool_name: str, params: Dict[str, Any]) -> str:
    serialized_params = json.dumps(params, sort_keys=True)
    raw_payload = f"{run_id}:{tool_name}:{serialized_params}"
    return hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

def validate_confirmation_token_digest(run_id: str, tool_name: str, params: Dict[str, Any], provided_digest: str) -> bool:
    expected_digest = generate_confirmation_token_digest(run_id, tool_name, params)
    return hashlib.sha256(expected_digest.encode('utf-8')).hexdigest() == hashlib.sha256(provided_digest.encode('utf-8')).hexdigest()

class AgentLoopDetectedException(Exception):
    pass

class MaxToolCallsExceededException(Exception):
    pass
