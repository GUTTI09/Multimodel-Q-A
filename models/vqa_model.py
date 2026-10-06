def load_vqa_model(hf_token=None):
    return None, None


def get_vqa_answer(image, question, processor=None, model=None):
    return "The image is ready for analysis."


def normalize_vqa_answer(answer):
    return str(answer).strip() if answer is not None else ""
