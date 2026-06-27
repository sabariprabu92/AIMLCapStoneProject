def verify_output(answer: str, source_chunks: list):
    if not answer or not answer.strip():
        return {
            "agent": "verification",
            "is_valid": False,
            "reason": "Answer is empty"
        }

    unsafe_phrases = [
        "ignore previous instructions",
        "system prompt",
        "developer message",
        "secret key",
        "api key",
        "password"
    ]

    lowered_answer = answer.lower()

    for phrase in unsafe_phrases:
        if phrase in lowered_answer:
            return {
                "agent": "verification",
                "is_valid": False,
                "reason": f"Unsafe phrase detected: {phrase}"
            }

    if "I could not find this information" in answer:
        return {
            "agent": "verification",
            "is_valid": True,
            "reason": "Answer correctly refused unsupported information"
        }

    if not source_chunks:
        return {
            "agent": "verification",
            "is_valid": False,
            "reason": "No source chunks available for verification"
        }

    return {
        "agent": "verification",
        "is_valid": True,
        "reason": "Answer passed basic safety and grounding checks"
    }