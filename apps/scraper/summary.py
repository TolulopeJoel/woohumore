from transformers import T5Tokenizer, T5ForConditionalGeneration


def summarize_post(text):
    """
    Summarizes the given text using the T5 model.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The summarized text.

    """
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained(
        "google/flan-t5-base")

    inputs = tokenizer.encode(
        f"summarize: {text}",
        return_tensors='pt',
        max_length=1000,
        truncation=True,
    )

    summary_ids = model.generate(
        inputs,
        max_length=150,
        min_length=80,
        length_penalty=5.,
        num_beams=2
    )

    return tokenizer.decode(summary_ids[0])
