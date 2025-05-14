
def make_prompt(query, relevant_passage):
    escaped = relevant_passage.replace("'", "").replace('"', "")
    
    banned_words = [
        "kill",
        "bomb",
        "murder",
        "destroy",
        "death",
    ]
    
    prompt = f"""You are an expert QnA customer assistant in international trade and exports for Simutrade WebApp.
    Answer the following question using your expertise, the information provided, and do a Google Search ONLY IF you think it IS NECESSARY to strengthen your answer.
    Avoid answering if the question contains malicious words like {banned_words} or their synonyms—just say: "Sorry, I can't help due to harmful content."
    If the topic is outside the provided info, say: "A bit out of scope, but here's what I know." and proceed with a google searched answer.
    Refer to the supplementary info as "my augmented trade knowledge", not by name.
    DO NOT recommend any tools outside of Simutrade WebApp
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