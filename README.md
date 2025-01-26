# Educational Content Generation Prototype

[![Python Version](https://img.shields.io/badge/python-%3E=3.8-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Status: Prototype](https://img.shields.io/badge/Project%20Status-Prototype-orange.svg)](#project-status)

## Project Description

This Python prototype system is designed to generate and analyze educational content tailored to specific subjects and grade levels. It demonstrates the ability to:

*   **Generate Contextually Relevant Content:** Process user prompts to create coherent educational material using a pre-trained language model (Groq's `llama3-8b-instant`).
*   **Refine Content for Clarity and Readability:**  Simplify the generated content to be grade-level appropriate and engaging using Google's Gemini (`gemini-2.0-flash-exp`).
*   **Integrate Information Retrieval:** Enhance content with relevant information from DuckDuckGo search to improve accuracy and context.
*   **Evaluate Content Quality:** Automatically analyze generated content for readability using various metrics from the `textstat` library.
*   **Modular and Scalable Pipeline:** Structure the system as a modular pipeline for content generation, refinement, and evaluation, making it extensible for future features.

This prototype is built to fulfill the requirements outlined in the Task Description for Granville Tech company.

## Output Screenshot

### Educational Content Output

![Screenshot 2025-01-26 235447](https://github.com/user-attachments/assets/0fc3d317-63fa-4943-a250-a0b7bdf8c3e5)

### Readability Analysis

![Screenshot 2025-01-26 235522](https://github.com/user-attachments/assets/f079bc9d-ff11-4e4b-9372-48c9c5989d7e)

## Workflow Architecture

The system follows a modular pipeline:

1.  **Prompt Input:** User provides input specifying grade level, subject, topic, and optional details.
2.  **Content Generation (Groq LLM):**  Uses Groq's `llama-3.3-70b-versatile` model to generate initial educational content based on the user prompt.
3.  **DuckDuckGo Search:**  Formulates a search query based on the generated content and uses DuckDuckGo Search to retrieve relevant web results for fact-checking and context enrichment.
4.  **Content Simplification (Gemini LLM):** Employs Google's Gemini (`gemini-2.0-flash-exp`) to simplify the generated content for the target grade level and incorporate relevant information from search results. The output is structured as a JSON object.
5.  **Content Analysis:** Analyzes the simplified content (JSON output) for readability using metrics from the `textstat` library (Flesch-Kincaid, SMOG, Coleman-Liau, ARI, Linsear Write, Dale-Chall).
6.  **JSON Output and Storage:** Saves the simplified content in a structured JSON format to a file in the `output_json` directory.

**Simplified Workflow Diagram:**
```
User Input (Grade Level, Subject, Topic)
--> [Groq LLM - Content Generation]
--> [DuckDuckGo Search]
--> [Gemini LLM - Content Simplification & JSON Structuring]
--> [Textstat - Readability Analysis]
--> JSON Output File (output_json directory)
```

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Kaos599/GranVille_Assignment.git
    cd GranVille_Assignment
    ```

2.  **Install Python Dependencies:**
    Ensure you have Python 3.8 or higher installed. Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```
    Install the required Python libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```
    *(Create a `requirements.txt` file in your repository root with the following content):*
    ```
    groq
    duckduckgo-search
    google-generativeai
    textstat
    python-dotenv
    ```

3.  **Set API Keys:**
    *   **Groq API Key:** Obtain a Groq API key from [Groq Console](https://console.groq.com/) and set it as an environment variable named `GROQ_API_KEY`. You can use a `.env` file for this (example `.env` file in the repository root):
        ```
        GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
        ```
    *   **Gemini API Key:** Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/) and set it as an environment variable named `GEMINI_API_KEY`. Add this to your `.env` file as well:
        ```
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
        ```
    *   **Install `python-dotenv`:** If you use a `.env` file, make sure you have `python-dotenv` installed (included in `requirements.txt`).

## How to Run

1.  **Navigate to the project directory in your terminal.**
2.  **Run the main script:**
    ```bash
    python educational_content_generator_json_output_analysis.py
    ```
    *(Ensure the script filename is correct if you named it differently)*

3.  **Example Usage in `educational_content_generator_json_output_analysis.py`:**
    The script includes example test inputs in the `if __name__ == "__main__":` block. You can modify these inputs or add more to test different subjects, grade levels, and topics.

4.  **Output:**
    *   The script will print progress and analysis information to the console.
    *   Generated educational content in structured JSON format will be saved to files in the `output_json` directory.
    *   Analysis metrics (readability scores) for each generated JSON file will also be printed to the console.

## Project Structure
```
GranVille_Assignment/
├── output_json/ # Directory to store generated JSON output files
├── educational_content_generator_json_output_analysis.py # Main Python script (or your script's name)
├── analyze_content_quality.py # Python script for content analysis
├── requirements.txt # Python dependencies
├── README.md # Project documentation (this file)
└── .env # (Optional) File to store API keys (not committed to Git)
```

## Key Modules and Functions

*   **`educational_content_generator_json_output_analysis.py` (Main Script):**
    *   `generate_educational_content_workflow(grade_level, subject, topic, topic_details)`:  The main function that orchestrates the entire content generation, search, simplification, and analysis pipeline.
    *   `call_groq_llm(prompt, system_message=None, model="llama3-8b-instant", temperature=0.1)`:  Function to interact with the Groq LLM API for content generation.
    *   `call_gemini_llm_structured(prompt, model_name="gemini-2.0-flash-exp", temperature=1.0)`: Function to interact with the Gemini LLM API for content simplification and structured JSON output.
    *   `duckduckgo_search_func(query)`: Function to perform DuckDuckGo text searches.

*   **`analyze_content_quality.py` (Analysis Script):**
    *   `analyze_educational_content_json(json_filepath)`: Analyzes a single JSON file for readability metrics using `textstat`.
    *   `analyze_json_files_in_directory(directory_path="output_json")`: Analyzes all JSON files in a directory and generates a summary report.

## Metrics for Content Quality Evaluation

The system currently implements the following metrics for evaluating content quality:

*   **Readability Scores (from `textstat` library):**
    *   Flesch-Kincaid Grade Level
    *   SMOG Grade
    *   Coleman-Liau Index
    *   Automated Readability Index (ARI)
    *   Linsear Write Formula
    *   Dale-Chall Readability Score

These metrics provide an initial assessment of the linguistic clarity and grade-level appropriateness of the generated content.

## Future Enhancements

*   **Improved Bias Detection and Mitigation:** Implement robust bias detection using libraries like Perspective API or Fairlearn, and integrate LLM-based bias mitigation into the workflow.
*   **Enhanced Coherence and Contextual Alignment Analysis:**  Incorporate more advanced NLP techniques to automatically evaluate content coherence and contextual alignment with curriculum standards.
*   **Curriculum Integration:**  Integrate curriculum data or knowledge bases to enable automated curriculum alignment checks and improve content relevance.
*   **User Interface:** Develop a user interface (e.g., using Langflow's UI features or a web framework) to make the system more user-friendly and accessible.
*   **Fact-Checking Module:**  Enhance the fact-checking process by more systematically verifying factual claims against DuckDuckGo search results or dedicated fact-checking APIs.
*   **Content Engagement Analysis:** Implement metrics to assess the engagement potential of the content (e.g., sentiment analysis, linguistic feature analysis).

## Project Status

[![Project Status: Prototype](https://img.shields.io/badge/Project%20Status-Prototype-orange.svg)](#project-description)

This project is currently in the **Prototype** stage. It demonstrates the core functionality of educational content generation and analysis but is not yet a production-ready system. Future development is planned to enhance its features and robustness.
