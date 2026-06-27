from app.agents.planner_agent import plan_task
from app.agents.retriever_agent import retrieve_information
from app.agents.reasoning_agent import reason_over_chunks
from app.agents.response_agent import generate_final_response
from app.agents.verification_agent import verify_output


def run_agentic_workflow(question: str):
    planner_result = plan_task(question)

    retriever_result = retrieve_information(question)

    reasoning_result = reason_over_chunks(
        question,
        retriever_result["retrieved_chunks"]
    )

    response_result = generate_final_response(
        question,
        reasoning_result["grounded_context"]
    )

    verification_result = verify_output(
        response_result["answer"],
        retriever_result["retrieved_chunks"]
    )

    final_answer = response_result["answer"]

    if not verification_result["is_valid"]:
        final_answer = "The generated response did not pass verification. Please rephrase the question or upload a clearer document."

    return {
        "planner": planner_result,
        "retriever": retriever_result,
        "reasoning": reasoning_result,
        "response": response_result,
        "verification": verification_result,
        "final_answer": final_answer
    }