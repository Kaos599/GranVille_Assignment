import os
import json
import textstat  

def analyze_educational_content_json(json_filepath):
    """
    Analyzes a single educational content JSON file for quality metrics,
    including multiple readability scores from textstat.

    Args:
        json_filepath (str): Path to the JSON file.

    Returns:
        dict: Dictionary of analysis metrics for the content, including readability scores.
    """
    analysis_metrics = {}

    try:
        with open(json_filepath, 'r') as f:
            content_data = json.load(f)

        analysis_metrics['filename'] = os.path.basename(json_filepath)

        
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
        print(full_text_content) 
        print("--- End of Text Content ---") 

        
        try:
            analysis_metrics['readability_flesch_kincaid_grade'] = textstat.flesch_kincaid_grade(full_text_content)
            analysis_metrics['readability_smog_grade'] = textstat.smog_index(full_text_content)
            analysis_metrics['readability_coleman_liau_index'] = textstat.coleman_liau_index(full_text_content)
            analysis_metrics['readability_automated_readability_index'] = textstat.automated_readability_index(full_text_content)
            analysis_metrics['readability_linsear_write_formula'] = textstat.linsear_write_formula(full_text_content)
            analysis_metrics['readability_dale_chall_readability_score'] = textstat.dale_chall_readability_score(full_text_content)
            

        except Exception as e:
            analysis_metrics['readability_error'] = "Error calculating readability metrics"
            print(f"  Warning: Error calculating readability for {json_filepath}: {e}")

        
        analysis_metrics['coherence_assessment'] = "Placeholder - Needs Advanced NLP or Human Evaluation"
        analysis_metrics['contextual_alignment_assessment'] = "Placeholder - Needs Curriculum/Knowledge Base Integration & Evaluation"

        print(f"\n--- Analysis Metrics for: {json_filepath} ---")
        print(json.dumps(analysis_metrics, indent=4)) 

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


def analyze_json_files_in_directory(directory_path="output_json"):
    """
    Analyzes all JSON files in the specified directory and generates a summary report,
    including multiple readability metrics in the report.

    Args:
        directory_path (str): Path to the directory containing JSON files (default: "output_json").
    """
    print(f"\n--- Starting JSON File Analysis in Directory: {directory_path} ---")

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found: {directory_path}")
        return

    json_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f.endswith(".json")]

    if not json_files:
        print(f"No JSON files found in directory: {directory_path}")
        return

    all_files_metrics = []
    for json_file in json_files:
        json_filepath = os.path.join(directory_path, json_file)
        file_metrics = analyze_educational_content_json(json_filepath) 
        all_files_metrics.append(file_metrics) 

    
    print("\n--- Summary Report: Analysis of Educational Content JSON Files ---")
    for metrics in all_files_metrics:
        print(f"\nFile: {metrics.get('filename', 'N/A')}")
        print(f"  Readability (Flesch-Kincaid Grade Level): {metrics.get('readability_flesch_kincaid_grade', 'N/A')}")
        print(f"  Readability (SMOG Grade): {metrics.get('readability_smog_grade', 'N/A')}")
        print(f"  Readability (Coleman-Liau Index): {metrics.get('readability_coleman_liau_index', 'N/A')}")
        print(f"  Readability (ARI): {metrics.get('readability_automated_readability_index', 'N/A')}")
        print(f"  Readability (Linsear Write Formula): {metrics.get('readability_linsear_write_formula', 'N/A')}")
        print(f"  Readability (Dale-Chall Score): {metrics.get('readability_dale_chall_readability_score', 'N/A')}")
        print(f"  Coherence Assessment: {metrics.get('coherence_assessment', 'N/A')}")
        print(f"  Contextual Alignment Assessment: {metrics.get('contextual_alignment_assessment', 'N/A')}")
        if "readability_error" in metrics:
            print(f"  Readability Calculation Error: {metrics['readability_error']}")
        if "error" in metrics:
            print(f"  Error: {metrics['error']}")
            if "details" in metrics:
                print(f"    Details: {metrics['details']}")

    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    analyze_json_files_in_directory() 