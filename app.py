from flask import Flask, render_template, request, redirect
from services.db_service import save_report, get_recent_reports

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    reports = get_recent_reports()
    return render_template("index.html", reports=reports, get_reason_class=get_reason_class)

@app.route("/submit", methods=["POST"])
def submit():
    bus_number = request.form["busNumber"]
    stop_name = request.form["stopName"]
    date = request.form["date"]
    time = request.form["time"]
    email = request.form["email"]
    additional_info = request.form["additionalInfo"]

    reason = request.form["reason"]
    
    # If "Other" is selected, get the user-inputted reason
    if reason == "Other":
        reason = request.form.get("otherReason", "").strip()

    save_report(bus_number, stop_name, date, time, email, additional_info, reason)

    return redirect("/")

def get_reason_class(reason):
    reason_classes = {
        "Bus did not show": "list-group-item-danger",  
        "Bus was late": "list-group-item-warning",  
        "Bus drove past without stopping": "list-group-item-info",  
        "Other": "list-group-item-secondary",  
    }
    return reason_classes.get(reason, "list-group-item-light")  # Default colour

if __name__ == "__main__":
    app.run(debug=True)