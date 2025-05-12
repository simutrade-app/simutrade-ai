
def make_prompt(query, relevant_passage):
    escaped = relevant_passage.replace("'", "").replace('"', "")
    
    banned_words = [
        "kill",
        "bomb",
        "murder",
        "destroy",
        "death",
    ]
    
    prompt = f"""You are an expert in international trade and exports.

    Answer the following question using your expertise, the information provided, and optionally Google Search if it strengthens your answer.

    Avoid answering if the question contains malicious words like {banned_words} or their synonyms—just say: "Sorry, I can't help due to harmful content."

    If the topic is outside the provided info, say: "Good question! This is out of scope, but here's my best answer based on what I know."

    Refer to the supplementary info as "my augmented trade knowledge", not by name.

    Question: {query}

    Supplementary Info: {escaped}

    Your response:
    """
    
    return prompt

def convert_passages_to_string(passages):
    context = ""
    
    for passage in passages:
        context += passage + "\n"
        
    return context