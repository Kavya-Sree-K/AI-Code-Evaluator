import streamlit as st
import subprocess
import tempfile
import os
import re
import time
import json

from app import evaluate_code

# =========================================================
# HISTORY FILE
# =========================================================

HISTORY_FILE = "history.json"

# =========================================================
# LOAD HISTORY
# =========================================================

def load_history():

    if not os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "w") as file:
            json.dump([], file)

    with open(HISTORY_FILE, "r") as file:

        return json.load(file)

# =========================================================
# SAVE HISTORY
# =========================================================

def save_history(question, result):

    history = load_history()

    # =====================================
    # REMOVE DUPLICATE QUESTIONS
    # =====================================

    history = [
        item for item in history
        if item["question"] != question
    ]

    # =====================================
    # ADD NEW QUESTION
    # =====================================

    history.insert(0, {
        "question": question,
        "generated_code": result["generated_code"],
        "score": result["score"],
        "feedback": result["feedback"],
        "suggestions": result["suggestions"]
    })

    # =====================================
    # LIMIT HISTORY
    # =====================================

    history = history[:20]

    # =====================================
    # SAVE TO FILE
    # =====================================

    with open(HISTORY_FILE, "w") as file:

        json.dump(history, file, indent=4)


# =========================================================
# DELETE HISTORY
# =========================================================

def delete_history(question):

    history = load_history()

    history = [
        item for item in history
        if item["question"] != question
    ]

    with open(HISTORY_FILE, "w") as file:

        json.dump(history, file, indent=4)



# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Code Evaluator",
    page_icon="💻",
    layout="wide"
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚡ AI Code Evaluator")

    st.markdown("---")

    # =====================================================
    # NEW QUERY BUTTON
    # =====================================================

    if st.button("➕ New Query"):

        st.session_state.show_history = False

        st.session_state.generated_code = None

        st.session_state.result = None

        st.session_state.execution_output = ""

        st.session_state.execution_error = ""

    st.markdown("---")

    # =====================================================
    # HISTORY SECTION
    # =====================================================

    st.subheader("🕘 Previous Questions")

    history = load_history()

    if len(history) == 0:

        st.info("No previous questions found.")

    else:

        for index, item in enumerate(history):

            col1, col2 = st.columns([5, 1])

            # =========================================
            # QUESTION BUTTON
            # =========================================

            with col1:

                if st.button(
                    item["question"],
                    key=f"history_{index}",
                    use_container_width=True
                ):

                    st.session_state.show_history = True

                    st.session_state.generated_code = (
                        item["generated_code"]
                    )

                    st.session_state.result = item

                    st.session_state.execution_output = ""

                    st.session_state.execution_error = ""

            # =========================================
            # DELETE BUTTON
            # =========================================

            with col2:

                if st.button(
                    "🗑",
                    key=f"delete_{index}"
                ):

                    delete_history(item["question"])

                    st.rerun()

    st.markdown("---")

    st.caption(
        "Built with Streamlit • Ollama • Gemini AI"
    )
# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

html, body, [class*="css"] {
    color: white !important;
}

textarea {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
}

textarea::placeholder {
    color: #94a3b8 !important;
}

.stTextInput input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
}

.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    border: none;
    background: linear-gradient(to right, #2563eb, #1d4ed8);
    color: white;
    font-size: 16px;
    font-weight: bold;
}

pre {
    background-color: #020617 !important;
    border-radius: 12px !important;
}

.output-box {
    background: #020617;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
}

.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

.feedback-box {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #38bdf8;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

# st.title("💻 AI Code Evaluator")

# st.write(
#     "Generate, Execute and Evaluate Code using Ollama and Gemini AI"
# )

# =========================================================
# SESSION STATE
# =========================================================

if "generated_code" not in st.session_state:
    st.session_state.generated_code = None

if "execution_output" not in st.session_state:
    st.session_state.execution_output = ""

if "execution_error" not in st.session_state:
    st.session_state.execution_error = ""

if "result" not in st.session_state:
    st.session_state.result = None

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# if "show_home" not in st.session_state:
#     st.session_state.show_home = True

if "show_history" not in st.session_state:
    st.session_state.show_history = False

# =========================================================
# HOME SCREEN
# =========================================================

generate_button = False

user_query = ""

if not st.session_state.show_history:

    st.title("💻 AI Code Evaluator")

    st.write(
        "Generate, Execute and Evaluate Code using Ollama and Gemini AI"
    )

    st.subheader("✍ Enter Coding Question")

    user_query = st.text_area(
        "",
        height=180,
        placeholder="""
Generate Python code for palindrome number

Generate Python calculator

Generate Python code for factorial
"""
    )

    generate_button = st.button("🚀 Generate Code")

# =========================================================
# GENERATE LOGIC
# =========================================================

if generate_button:

    if user_query.strip() == "":

        st.warning("Please enter coding related question.")

    else:

        try:

            progress = st.progress(0)

            status = st.empty()

            status.info("Connecting to Ollama...")
            progress.progress(20)

            time.sleep(1)

            status.info("Generating Code...")
            progress.progress(60)

            result = evaluate_code(user_query)

            status.info("Evaluating Code...")
            progress.progress(100)

            time.sleep(1)

            progress.empty()
            status.empty()

            if result["invalid_question"]:

                st.error(result["message"])

            else:

                st.session_state.generated_code = (
                    result["generated_code"]
                )

                st.session_state.result = result

                st.session_state.execution_output = ""

                st.session_state.execution_error = ""

                # =====================================
                # SAVE HISTORY
                # =====================================

                save_history(user_query, result)

        except Exception as e:

            st.error(str(e))

# =========================================================
# CODE DISPLAY
# =========================================================

if st.session_state.generated_code:

    generated_code = st.session_state.generated_code

    result = st.session_state.result

    st.markdown("---")

    st.subheader("🧠 Generated Code")

    st.code(generated_code)

    # =====================================================
    # DETECT INPUT PROMPTS
    # =====================================================

    input_prompts = re.findall(
        r'input\(["\'](.*?)["\']\)',
        generated_code
    )

    requires_input = len(input_prompts) > 0

    # =====================================================
    # RUN SECTION
    # =====================================================

    st.markdown("---")

    st.subheader("▶ Run Program")

    user_inputs = []

    # =====================================================
    # DYNAMIC INPUT BOXES
    # =====================================================

    if requires_input:

        st.write("### ⌨ Enter Program Inputs")

        for i, prompt in enumerate(input_prompts):

            value = st.text_input(
                prompt,
                key=f"user_input_{i}"
            )

            user_inputs.append(value)

    # =====================================================
    # RUN BUTTON
    # =====================================================

    run_button = st.button("⚡ Run Code")

    # =====================================================
    # EXECUTE CODE
    # =====================================================

    if run_button:

        try:

            # =============================================
            # CONVERT INPUTS TO MULTILINE STRING
            # =============================================

            final_input = "\n".join(user_inputs)

            # =============================================
            # CREATE TEMP FILE
            # =============================================

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False
            ) as temp_file:

                temp_file.write(generated_code)

                temp_path = temp_file.name

            # =============================================
            # EXECUTE CODE
            # =============================================

            process = subprocess.run(
                ["python", temp_path],
                input=final_input,
                capture_output=True,
                text=True,
                timeout=15
            )

            clean_output = process.stdout.strip()

            # =============================================
            # REMOVE INPUT PROMPTS FROM OUTPUT
            # =============================================

            for prompt in input_prompts:

                clean_output = clean_output.replace(
                    prompt,
                    ""
                )

            st.session_state.execution_output = (
                clean_output.strip()
            )

            st.session_state.execution_error = (
                process.stderr.strip()
            )

            os.remove(temp_path)

        except Exception as e:

            st.session_state.execution_error = str(e)

    # =====================================================
    # OUTPUT SECTION
    # =====================================================

    st.markdown("---")

    st.subheader("📦 Expected Output")

    if st.session_state.execution_output:

        st.markdown(
            f"""
            <div class="output-box">
            <pre>{st.session_state.execution_output}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif st.session_state.execution_error:

        st.markdown(
            f"""
            <div class="output-box">
            <pre>{st.session_state.execution_error}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Run the generated code to see output."
        )

    # =====================================================
    # METRICS
    # =====================================================

    st.markdown("---")

    st.subheader("📊 Gemini Evaluation")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <h3>⭐ Score</h3>
                <h1>{result['score']}/100</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        lines = len(
            generated_code.splitlines()
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <h3>📄 Lines of Code</h3>
                <h1>{lines}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # FEEDBACK
    # =====================================================

    st.markdown("---")

    st.subheader("📝 Gemini Feedback")

    st.markdown(
        f"""
        <div class="feedback-box">
        {result["feedback"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # SUGGESTIONS
    # =====================================================

    st.markdown("---")

    st.subheader("🚀 Suggestions")

    suggestions = result.get("suggestions", "")

    if suggestions and suggestions.strip() != "":

        st.markdown(
            f"""
            <div class="feedback-box">
            {suggestions}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No suggestions. Code quality is excellent."
        )