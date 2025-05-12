
def make_prompt(query, relevant_passage):
    escaped = relevant_passage.replace("'", "").replace('"', "")
    
    prompt = f"""Question: {query}.\n
    Supplementary Information: {escaped}\n
    Answer the question according to your knowledge and supplemented with the supplementary information provided. If the question is not within the scope of the supplementary information, you should say "Good Question! But regretfully, this is out of my scope. I will still answer to the best of my knowledge" and then proceed answering only with your knowledge.\n
    If you refer to the supplementary information, you don't need to say "according to the supplementary information", instead say "according to my augmented knowledge on trade and exports".\n
    Your response:
    """
    
    return prompt

def convert_passages_to_string(passages):
    context = ""
    
    for passage in passages:
        context += passage + "\n"
        
    return context