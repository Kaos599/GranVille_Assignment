import os
from groq import Groq
from duckduckgo_search import DDGS
import google.generativeai as genai
import json
import textstat
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY environment variable not set. Please set your Groq API key.")
    exit()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set. Please set your Gemini API key.")
    exit()
genai.configure(api_key=GEMINI_API_KEY)

def call_groq_llm(prompt, system_message=None, model="llama-3.3-70b-versatile", temperature=0.7):
    """
    Function to call the Groq LLM API using the groq Python library.
    Corrected parameter name: using 'max_tokens' instead of 'max_completion_tokens'
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
            max_tokens=6024,
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

def call_gemini_llm_structured(prompt, model_name="gemini-2.0-flash-exp", temperature=1.0):
    """
    Function to call the Google Gemini LLM API and request structured JSON output.
    """
    print(f"\n--- Calling Gemini LLM (Model: {model_name}) for Structured JSON Output ---")
    print(f"Prompt: {prompt}")

    try:
        generation_config = {
          "temperature": temperature,
          "top_p": 0.95,
          "top_k": 40,
          "max_output_tokens": 8192,
          "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
          model_name=model_name,
          generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])

        response = chat_session.send_message(prompt)

        try:
            structured_data = json.loads(response.text)
            print(f"Generated Structured JSON Data from Gemini:\n{json.dumps(structured_data, indent=2)}\n")
            return structured_data

        except json.JSONDecodeError:
            print(f"Warning: Gemini did not return valid JSON. Raw text response:\n{response.text}\n")
            return {"text_response": response.text, "json_parse_error": "true"}

    except Exception as e:
        print(f"Error calling Gemini API for JSON output: {e}")
        return {"error": "Gemini API Error", "details": str(e)}

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

def analyze_educational_content_json(json_filepath):
    """
    Analyzes a single educational content JSON file for quality metrics,
    including multiple readability scores from textstat, and handles file/json errors.

    Args:
        json_filepath (str): Path to the JSON file.

    Returns:
        dict: Dictionary of analysis metrics for the content, including readability scores or error details.
    """
    analysis_metrics = {}

    try:
        with open(json_filepath, 'r') as f:
            content_data = json.load(f)

        analysis_metrics['filename'] = os.path.basename(json_filepath)

        # --- Extract Text Content for Analysis ---
        full_text_content = ""
        if "title" in content_data:
            full_text_content += content_data.get("title", "") + ". "
        if "summary" in content_data:
            full_text_content += content_data.get("summary", "") + ". "
        if "sections" in content_data and isinstance(content_data["sections"], list):
            for section in content_data["sections"]:
                if "content" in section:
                    full_text_content += section.get("content", "") + ". "

        analysis_metrics['extracted_text_length'] = len(full_text_content)

        # --- Linguistic Clarity (Readability) - Multiple Metrics from textstat ---
        try:
            analysis_metrics['readability_flesch_kincaid_grade'] = textstat.flesch_kincaid_grade(full_text_content)
            analysis_metrics['readability_smog_index'] = textstat.smog_index(full_text_content)
            analysis_metrics['readability_coleman_liau_index'] = textstat.coleman_liau_index(full_text_content)
            analysis_metrics['readability_automated_readability_index'] = textstat.automated_readability_index(full_text_content)
            analysis_metrics['readability_linsear_write_formula'] = textstat.linsear_write_formula(full_text_content)
            analysis_metrics['readability_dale_chall_readability_score'] = textstat.dale_chall_readability_score(full_text_content)

        except Exception as e:
            analysis_metrics['readability_error'] = "Error calculating readability metrics"
            print(f"  Warning: Error calculating readability for {json_filepath}: {e}")

    except FileNotFoundError:
        analysis_metrics['error'] = "FileNotFoundError"
        print(f"Error: JSON file not found: {json_filepath}")
    except json.JSONDecodeError:
        analysis_metrics['error'] = "JSONDecodeError"
        print(f"Error: Could not decode JSON from file: {json_filepath}")
    except Exception as e:
        analysis_metrics['error'] = "AnalysisError"
        analysis_metrics['details'] = str(e)
        print(f"Error during analysis of {json_filepath}: {e}")

    return analysis_metrics


def generate_educational_content_workflow(grade_level, subject, topic, topic_details=""):
    """
    Main function to run the educational content generation workflow.
    Mimics the Langflow workflow but in Python code.
    Using Gemini to generate structured JSON for the simplification step.
    Saves the output to a JSON file AND calls the analysis function.
    """
    print("\n--- Starting Educational Content Generation Workflow ---")
    print(f"Input: Grade Level: {grade_level}, Subject: {subject}, Topic: {topic}, Details: {topic_details}")

    content_gen_prompt_template = """
    Generate educational content for {subject} at a {grade_level} level, focusing on the topic of {topic}.

    Please ensure the content is:
    - Informative and accurate for a {grade_level} level understanding.
    - Engaging and easy to understand for students.
    - Structured logically with headings and bullet points where appropriate.
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
    Simplify the following educational content to be easily understandable and engaging for {grade_level} grade students. Focus on using clear, concise language and appropriate vocabulary for their age group. Incorporate relevant information and context from the provided DuckDuckGo search results to enhance the content and ensure accuracy.

    Structure the simplified content into a JSON object with the following format:

    {{
      "title": "Concise title for the topic",
      "grade_level_appropriateness_assessment": "A brief assessment of how well the content is simplified for the target grade level (e.g., 'Excellent', 'Good', 'Needs further simplification')",
      "sections": [
        {{
          "heading": "Section 1 Heading (e.g., Introduction)",
          "content": "Simplified content for section 1, using bullet points or short paragraphs for readability"
        }},
        {{
          "heading": "Section 2 Heading (e.g., Key Concepts)",
          "content": "Simplified content for section 2..."
        }},
        ... (more sections as needed)
      ],
      "summary": "A short summary of the key learning points in the simplified content."
    }}

    Original Content: {generated_content}

    DuckDuckGo Search Results: {search_results}

    Ensure the ENTIRE response is valid JSON and nothing else.
    """
    simplification_prompt = simplification_prompt_template.format(
        grade_level=grade_level, generated_content=generated_content, search_results=search_results
    )

    simplified_content_json = call_gemini_llm_structured(prompt=simplification_prompt, model_name="gemini-2.0-flash-exp", temperature=0.7)

    # --- Save to JSON File ---
    output_dir = "output_json"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{subject.replace(' ', '_')}_{grade_level.replace(' ', '_')}_{topic.replace(' ', '_')}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(simplified_content_json, f, indent=4)

    print(f"\n--- Final Educational Content (Simplified JSON - Bias Mitigation Removed) ---\n")
    print(json.dumps(simplified_content_json, indent=2))
    print(f"\n--- JSON output saved to: {filepath} ---\n")

    # --- Call Analysis Function ---
    print("\n--- Calling Content Analysis Function ---")
    print("\n--- Content Analysis Metrics ---")
    print(json.dumps(analysis_metrics, indent=2))  # Add this line to print the metrics
    print("\n--- Content Analysis Complete ---")


    return simplified_content_json


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