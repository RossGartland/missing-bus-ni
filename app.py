from flask import Flask, render_template, request, redirect
from services.db_service import save_report, get_recent_reports, generate_graph_data  

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    reports = get_recent_reports(6)

    reason_counts, date_counts, bus_numbers = generate_graph_data()

    return render_template("index.html", 
                           reports=reports, get_reason_class=get_reason_class, 
                           reason_counts=reason_counts, date_counts=date_counts,  bus_numbers=bus_numbers)

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
        "Bus did not show": "bg-danger",  
        "Bus was late": "bg-warning",  
        "Bus drove past without stopping": "bg-info",  
        "Other": "bg-secondary",  
    }
    return reason_classes.get(reason, "bg-light")  # Default colour

@app.route('/reports')
def view_all_reports():
    reports = get_recent_reports(100)
    return render_template("reports.html", reports=reports)


if __name__ == "__main__":
    app.run(debug=True)