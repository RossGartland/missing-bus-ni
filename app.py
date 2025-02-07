from flask import Flask, render_template, request, redirect
from services.db_service import save_report, get_recent_reports

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    reports = get_recent_reports()
    return render_template("index.html", reports=reports)

@app.route("/submit", methods=["POST"])
def submit():
    bus_number = request.form["busNumber"]
    stop_name = request.form["stopName"]
    date = request.form["date"]
    time = request.form["time"]
    email = request.form["email"]
    additional_info = request.form["additionalInfo"]

    save_report(bus_number, stop_name, date, time, email, additional_info)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)