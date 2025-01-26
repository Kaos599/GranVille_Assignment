import os
from groq import Groq  
from duckduckgo_search import DDGS  


GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  
if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY environment variable not set. Please set your Groq API key.")
    exit()



def call_groq_llm(prompt, system_message=None, model="llama-3.1-70b-versatile", temperature=0.8):
    """
    Function to call the Groq LLM API using the groq Python library.
    """
    print(f"\n--- Calling Groq LLM (Model: {model}) ---")
    if system_message:
        print(f"System Message: {system_message}")
    print(f"Prompt: {prompt}")

    try:
        client = Groq(api_key=GROQ_API_KEY) 
        messages_list = []
        if system_message:
            messages_list.append({"role": "system", "content": system_message})
        messages_list.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=model,
            messages=messages_list,
            temperature=temperature,
            max_completion_tokens=6024, 
            top_p=1,
            stream=False, 
            stop=None,
        )

        generated_text = completion.choices[0].message.content

        print(f"Generated Text:\n{generated_text}\n")
        return generated_text

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Error generating content from Groq LLM." 

def duckduckgo_search_func(query): 
    """
    Function for DuckDuckGo text search using the duckduckgo-search library DDGS class.
    """
    print(f"\n--- DuckDuckGo Search ---")
    print(f"Query: {query}")

    try:
        ddgs = DDGS() 
        results = ddgs.text(keywords=query, max_results=5) 
        search_results_text = "\n".join([f"Title: {res['title']}\nSnippet: {res['body']}\nURL: {res['href']}" for res in results]) if results else "No search results found."
        print(f"Search Results:\n{search_results_text}\n")
        return search_results_text

    except Exception as e:
        print(f"Error during DuckDuckGo search: {e}")
        return "Error fetching DuckDuckGo search results."



def generate_educational_content_workflow(grade_level, subject, topic, topic_details=""):
    """
    Main function to run the educational content generation workflow.
    Mimics the Langflow workflow but in Python code.
    Bias mitigation steps are removed in this version.
    """
    print("\n--- Starting Educational Content Generation Workflow ---")
    print(f"Input: Grade Level: {grade_level}, Subject: {subject}, Topic: {topic}, Details: {topic_details}")

    
    content_gen_prompt_template = """
    Generate educational content for {subject} at a {grade_level} level, focusing on the topic of {topic}.

    Please ensure the content is:
    - Informative and accurate for a {grade_level} level understanding.
    - Engaging and easy to understand for students.
    - Structured logically.
    - Written in a neutral, inclusive, and unbiased manner, avoiding stereotypes and promoting diversity.
    - Use clear and simple language appropriate for {grade_level}.

    Topic details: {topic_details} (Optional: Add specific details or learning objectives).
    """
    content_gen_prompt = content_gen_prompt_template.format(
        subject=subject, grade_level=grade_level, topic=topic, topic_details=topic_details
    )

    
    generated_content = call_groq_llm(prompt=content_gen_prompt)

    
    ddg_query_prompt_template = "Formulate a DuckDuckGo search query to fact-check and find additional context for the following educational content about {topic} for {grade_level} students: {generated_content}"
    ddg_query_prompt = ddg_query_prompt_template.format(
        topic=topic, grade_level=grade_level, generated_content=generated_content
    )

    
    search_results = duckduckgo_search_func(query=ddg_query_prompt) 

    
    simplification_prompt_template = """
    Simplify the following educational content to be easily understandable and engaging for {grade_level} grade students. Focus on using clear, concise language and appropriate vocabulary for their age group.

    Also, please incorporate relevant information and context from the provided DuckDuckGo search results to enhance the content and ensure accuracy.

    Original Content: {generated_content}

    DuckDuckGo Search Results: {search_results}
    """
    simplification_prompt = simplification_prompt_template.format(
        grade_level=grade_level, generated_content=generated_content, search_results=search_results
    )

    
    simplified_content = call_groq_llm(prompt=simplification_prompt, system_message="You are an AI assistant skilled in simplifying complex text for educational purposes and ensuring clarity for students of different grade levels. You also incorporate relevant information from search results to enhance and fact-check the content.")

    

    

    
    print("\n--- Final Educational Content (Simplified - Bias Mitigation Removed) ---\n")
    print(simplified_content) 
    return simplified_content 


if __name__ == "__main__":
    test_inputs = [
        {"grade_level": "3rd Grade", "subject": "Science", "topic": "The Water Cycle", "topic_details": "Explain the stages of the water cycle: evaporation, condensation, precipitation, and collection. Use simple terms and examples that a 3rd grader can understand. Mention the importance of the water cycle for life on Earth."},
        {"grade_level": "7th Grade", "subject": "History", "topic": "Ancient Egypt", "topic_details": "Focus on the pyramids of Giza, the pharaohs (like Tutankhamun), and the importance of the Nile River to ancient Egyptian civilization. Keep it engaging for 7th graders and mention some interesting facts or stories."}
    ]

    for input_data in test_inputs:
        generate_educational_content_workflow(
            grade_level=input_data["grade_level"],
            subject=input_data["subject"],
            topic=input_data["topic"],
            topic_details=input_data["topic_details"]
        )
        print("\n" + "="*50 + "\n") 