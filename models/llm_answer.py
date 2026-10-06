def load_llm_chain(api_key=None):
    return {"api_key": api_key}


def get_final_answer(chain, caption, question, normalized_vqa_answer):
    return (
        f"Caption: {caption}\n"
        f"Question: {question}\n"
        f"Visual answer: {normalized_vqa_answer or 'No specific answer was generated.'}"
    )
