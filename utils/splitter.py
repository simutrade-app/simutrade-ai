from langchain.text_splitter import CharacterTextSplitter

def split_text(text, chunk_size=800, chunk_overlap=100):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True)
    return splitter.split_text(text)