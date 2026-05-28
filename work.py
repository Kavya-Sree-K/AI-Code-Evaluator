from flask import Flask, request, jsonify

import subprocess
import tempfile
import os

from app import evaluate_code

# ======================================================
# FLASK APP
# ======================================================

app = Flask(__name__)

# ======================================================
# GENERATE API
# ======================================================

@app.route("/generate", methods=["POST"])

def generate_code():

    try:

        # ==============================================
        # GET DATA FROM FRONTEND
        # ==============================================

        data = request.json

        user_query = data.get("question")

        # ==============================================
        # CALL app.py FUNCTION
        # ==============================================

        result = evaluate_code(user_query)

        # ==============================================
        # RETURN RESPONSE
        # ==============================================

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "error": str(e)

        })

# ======================================================
# RUN API
# ======================================================

@app.route("/run", methods=["POST"])

def run_code():

    try:

        # ==============================================
        # GET DATA
        # ==============================================

        data = request.json

        code = data.get("code")

        user_input = data.get(
            "user_input",
            ""
        )

        # ==============================================
        # CREATE TEMP FILE
        # ==============================================

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as temp_file:

            temp_file.write(code)

            temp_path = temp_file.name

        # ==============================================
        # EXECUTE CODE
        # ==============================================

        process = subprocess.run(
            ["python", temp_path],
            input=user_input,
            capture_output=True,
            text=True,
            timeout=20
        )

        # ==============================================
        # DELETE TEMP FILE
        # ==============================================

        os.remove(temp_path)

        # ==============================================
        # RETURN OUTPUT
        # ==============================================

        return jsonify({

            "output": process.stdout,

            "error": process.stderr
        })

    except Exception as e:

        return jsonify({

            "output": "",

            "error": str(e)
        })

# ======================================================
# HEALTH API
# ======================================================

@app.route("/health")

def health():

    return jsonify({

        "status": "API Working"
    })

# ======================================================
# RUN FLASK SERVER
# ======================================================

if __name__ == "__main__":

    app.run(debug=True)