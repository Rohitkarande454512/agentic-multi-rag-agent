from langchain.prompts import PromptTemplates

def query_agent(query):
    return f"Understanding query: {query}"

def retrieval_agent(query):
    return f"Retrieving documents for: {query}"

def summarization_agent(text):
    return f"Summary: {text[:200]}"

def validation_agent(answer):
    return{
        "validated_answer" : answer,
        "status": "validated"
    }