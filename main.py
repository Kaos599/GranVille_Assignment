import os
from groq import Groq  
from duckduckgo_search import DuckDuckGo as ddg  


GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  
if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY environment variable not set. Please set your Groq API key.")
    exit()



def call_groq_llm(prompt, system_message=None, model="llama-3-8b-instant", temperature=0.1):
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
            max_completion_tokens=1024, 
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
    Function for DuckDuckGo search using the duckduckgo-search library.
    """
    print(f"\n--- DuckDuckGo Search ---")
    print(f"Query: {query}")

    try:
        results = ddg(query, max_results=5) 
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

    

    return simplified_content
    # bias_report = detect_bias_basic_keywords(simplified_content)
    # print(f"\n--- Bias Detection Report (Basic Keyword Check) ---\n{bias_report}\n")

    
    # bias_mitigation_prompt_template = """
    # The following educational content has been flagged for potential biases (see bias report). Revise the content to remove or rephrase any biased language and ensure it is inclusive, fair, and neutral.

    # Bias Report: {bias_report}

    # Potentially Biased Content: {potentially_biased_content}
    # """
    # bias_mitigation_prompt = bias_mitigation_prompt_template.format(
    #     bias_report=bias_report, potentially_biased_content=simplified_content
    # )

    
    # bias_mitigated_content = call_groq_llm(prompt=bias_mitigation_prompt, system_message="You are an AI assistant specialized in removing biases from text and ensuring inclusivity and fairness in language. You will revise the content based on the provided bias report.")

    
    # print("\n--- Final Educational Content (Bias Mitigated) ---\n")
    # print(bias_mitigated_content)
    # return bias_mitigated_content


if __name__ == "__main__":
    test_inputs = [
        {"grade_level": "3rd Grade", "subject": "Science", "topic": "The Water Cycle", "topic_details": "Explain the stages of the water cycle: evaporation, condensation, precipitation, and collection. Use simple terms and examples that a 3rd grader can understand. Mention the importance of the water cycle for life on Earth."},
        {"grade_level": "7th Grade", "subject": "History", "topic": "Ancient Egypt", "topic_details": "Focus on the pyramids of Giza, the pharaohs (like Tutankhamun), and the importance of the Nile River to ancient Egyptian civilization. Keep it engaging for 7th graders and mention some interesting facts or stories."},
        {"grade_level": "10th Grade", "subject": "Math", "topic": "Quadratic Equations", "topic_details": "Explain what a quadratic equation is, the standard form (ax^2 + bx + c = 0), and methods to solve them (factoring, quadratic formula). Include a simple example and explain the concept of roots or solutions."},
        {"grade_level": "8th Grade", "subject": "Literature", "topic": "Theme in Literature", "topic_details": "Explain what 'theme' means in a story or poem. Use examples of common themes like 'friendship,' 'courage,' 'good vs. evil,' and 'overcoming challenges.' Keep the explanation clear and relatable for 8th graders."}
    ]

    for input_data in test_inputs:
        generate_educational_content_workflow(
            grade_level=input_data["grade_level"],
            subject=input_data["subject"],
            topic=input_data["topic"],
            topic_details=input_data["topic_details"]
        )
        print("\n" + "="*50 + "\n") 