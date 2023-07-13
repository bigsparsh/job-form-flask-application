from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = "sparshsinghpythonprojectflask"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "pythonsample4@gmail.com"
app.config["MAIL_PASSWORD"] = "nvruknpagdzshqun"

mail = Mail(app)

db = SQLAlchemy(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    start_date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        start_date = request.form["start_date"]
        date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name, email=email, start_date=date_obj,
                    occupation=occupation)
        db.session.add(form)
        db.session.commit()

        text_message = f"Hey, {first_name} your job application has been submitted successfully.\n" \
                       f"We hope we can consider you for the job, after enquiry we will be contacting" \
                       f"you if you are the one for the job." \
                       f"The data you have submitted is below:\n" \
                       f"Name: {first_name} {last_name}\n" \
                       f"Email: {email}\n" \
                       f"Starting Date: {start_date}\n" \
                       f"Occupation: {occupation}.\n" \
                       f"- Our team"
        message = Message(subject="Job Application form Submitted",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=text_message)
        mail.send(message)

        flash(f"{first_name}, your form was submitted successfully.", "sucess")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
