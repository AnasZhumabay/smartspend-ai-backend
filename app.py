from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)
client = genai.Client()

MODEL_NAME = "gemini-2.5-flash-lite"

def build_prompt(question, total_balance, total_income, total_expense, top_category, recent_transactions):
    lines = []

    for tx in recent_transactions:
        name = tx.get("name", "Unknown")
        amount = tx.get("amount", 0)
        category = tx.get("category", "Other")
        lines.append(f"- {name}: {amount} ({category})")

    tx_block = "\n".join(lines) if lines else "No recent transactions."

    return f"""
You are SmartSpend AI, a premium financial adviser inside a personal finance app.

User question:
{question}

Finance summary:
- Total balance: {total_balance}
- Total income: {total_income}
- Total expense: {total_expense}
- Top expense category: {top_category}

Recent transactions:
{tx_block}

Rules:
- Be practical, concise, and personalized.
- Focus on budgeting, savings, and spending habits.
- Do not claim to be a licensed financial advisor.
- Use only the provided data.
- Reply in 3-6 sentences.
""".strip()

@app.route("/")
def home():
    return {"message": "SmartSpend Gemini backend is running"}

@app.route("/ai/advice", methods=["POST"])
def ai_advice():
    try:
        data = request.get_json() or {}

        question = data.get("question", "").strip()
        total_balance = data.get("total_balance", 0)
        total_income = data.get("total_income", 0)
        total_expense = data.get("total_expense", 0)
        top_category = data.get("top_category", "Unknown")
        recent_transactions = data.get("recent_transactions", [])

        if not question:
            return jsonify({"error": "Question is required"}), 400

        prompt = build_prompt(
            question=question,
            total_balance=total_balance,
            total_income=total_income,
            total_expense=total_expense,
            top_category=top_category,
            recent_transactions=recent_transactions,
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)