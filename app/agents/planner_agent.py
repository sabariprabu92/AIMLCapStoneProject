def plan_task(question: str):
    return {
        "agent": "planner",
        "task": "Understand the user question and plan retrieval",
        "question": question,
        "plan": [
            "Validate the user question",
            "Retrieve relevant chunks from the uploaded document",
            "Reason over retrieved content",
            "Generate grounded final response"
        ]
    }