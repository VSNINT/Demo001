import azure.functions as func
import json

app = func.FunctionApp()

@app.function_name(name="CheckLoanEligibility")
@app.route(route="CheckLoanEligibility", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def check_loan_eligibility(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"isEligible": False, "reason": "Invalid request data."}),
            mimetype="application/json"
        )

    name = data.get("name", "")
    age = data.get("age", 0)
    credit_score = data.get("creditScore", 0)
    salary = data.get("salary", 0.0)
    existing_emi = data.get("existingEmi", 0.0)
    amount = data.get("amount", 0.0)

    # Eligibility Logic (same as C#)
    if not name or age == 0 or credit_score == 0:
        return func.HttpResponse(
            json.dumps({"isEligible": False, "reason": "All fields are required."}),
            mimetype="application/json"
        )
    if age < 21:
        return func.HttpResponse(
            json.dumps({"isEligible": False, "reason": "Applicant must be at least 21 years old."}),
            mimetype="application/json"
        )
    if credit_score < 650:
        return func.HttpResponse(
            json.dumps({"isEligible": False, "reason": "Credit score must be at least 650."}),
            mimetype="application/json"
        )
    if salary < 20000:
        return func.HttpResponse(
            json.dumps({"isEligible": False, "reason": "Monthly salary must be at least ₹20,000."}),
            mimetype="application/json"
        )
    if existing_emi > 0.5 * salary:
        return func.HttpResponse(
            json.dumps({"isEligible": False, "reason": "Existing EMI exceeds 50% of salary."}),
            mimetype="application/json"
        )
    if amount > (salary - existing_emi) * 20:
        return func.HttpResponse(
            json.dumps({"isEligible": False, "reason": "Loan amount too high compared to your disposable income."}),
            mimetype="application/json"
        )

    # Eligible
    return func.HttpResponse(
        json.dumps({"isEligible": True, "reason": "Congratulations! You are eligible for the loan."}),
        mimetype="application/json"
    )

@app.function_name(name="Frontend")
@app.route(route="frontend", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def frontend(req: func.HttpRequest) -> func.HttpResponse:
    try:
        html_path = "wwwroot/LoanEligibilityChecker.html"
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return func.HttpResponse(html_content, mimetype="text/html")
    except Exception as e:
        return func.HttpResponse("HTML file not found or error: " + str(e), status_code=404)
