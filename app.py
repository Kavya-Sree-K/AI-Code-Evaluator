import requests
import json
import os

from dotenv import load_dotenv
from google import genai

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

GEMINI_API_KEY = os.getenv("Google_Api_Key")

# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# MAIN FUNCTION
# ==========================================

def evaluate_code(user_query):

    # ==========================================
    # OLLAMA PROMPT
    # ==========================================

    ollama_prompt = f"""
You are an expert AI coding assistant.

Accept only programming and coding related questions.

Questions may belong to any programming language.

If the question is not coding related respond exactly:
ONLY CODING RELATED QUESTIONS ARE ALLOWED


Do not provide explanations.
Do not use markdown formatting.
Do not use triple backticks.
Do not use comments.

Return only raw executable code.

IMPORTANT:
Always generate complete runnable programs.
Always print the final output.
Always include execution logic.
If input is needed use input() function.
Strictly do not give any explanations like here is the program
strictly give only code 

Examples:

Question: sum of two numbers

Correct Output:
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

sum_value = a + b

print("Sum:", sum_value)

User Question:
{user_query}
"""

    # ==========================================
    # OLLAMA API CALL
    # ==========================================

    ollama_response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": ollama_prompt,
            "stream": False
        },
        #  timeout=300
    )

    ollama_json = ollama_response.json()

    generated_code = ollama_json.get(
        "response",
        "Error generating code."
    )

    # ==========================================
    # CLEAN CODE
    # ==========================================

    generated_code = generated_code.replace(
        "```python",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    # ==========================================
    # INVALID QUESTION CHECK
    # ==========================================

    if (
        "ONLY CODING RELATED QUESTIONS ARE ALLOWED"
        in generated_code.upper()
    ):

        return {
            "invalid_question": True,
            "message": "Only coding related questions are allowed."
        }

    # ==========================================
    # GEMINI PROMPT
    # ==========================================

    gemini_prompt = f"""
You are an expert AI code reviewer.

Analyze the generated code professionally.

Check:
- correctness
- syntax
- optimization
- readability
- logic

Feedback must contain 4 to 5 meaningful lines.

If score is below 100 provide improvement suggestions.

Return only valid JSON.

JSON format:
{{
  "score": number,
  "feedback": "text",
  "suggestions": "text"
}}

Generated Code:
{generated_code}
"""

    # ==========================================
    # GEMINI API CALL
    # ==========================================

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=gemini_prompt
    )

    review_text = response.text

    # ==========================================
    # CLEAN JSON
    # ==========================================

    review_text = review_text.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    # ==========================================
    # PARSE JSON
    # ==========================================

    review_json = json.loads(review_text)

    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {
        "invalid_question": False,
        "generated_code": generated_code,
        "score": review_json.get("score"),
        "feedback": review_json.get("feedback"),
        "suggestions": review_json.get("suggestions")
    }