from reportlab.pdfgen import canvas
from flask import send_file
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask App
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Expense Table Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# Home Page
@app.route('/')
def index():

    expenses = Expense.query.all()

    total = sum(exp.amount for exp in expenses)

    category_data = {}

    for exp in expenses:

        if exp.category in category_data:
            category_data[exp.category] += exp.amount
        else:
            category_data[exp.category] = exp.amount

    labels = list(category_data.keys())
    amounts = list(category_data.values())

    return render_template(
        'index.html',
        expenses=expenses,
        total=total,
        labels=labels,
        amounts=amounts
    )
# Add Expense
@app.route('/add', methods=['GET', 'POST'])
def add_expense():

    if request.method == 'POST':

        title = request.form['title']
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']

        new_expense = Expense(
            title=title,
            amount=float(amount),
            category=category,
            date=datetime.strptime(date, "%Y-%m-%d")
        )

        db.session.add(new_expense)
        db.session.commit()

        return redirect('/')

    return render_template('add_expense.html')

# Delete Expense
@app.route('/delete/<int:id>')
def delete_expense(id):

    expense = Expense.query.get_or_404(id)

    db.session.delete(expense)
    db.session.commit()

    return redirect('/')

# Edit Expense
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):

    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':

        expense.title = request.form['title']
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']

        db.session.commit()

        return redirect('/')

    return render_template('edit_expense.html', expense=expense)
@app.route('/monthly-summary')
def monthly_summary():

    expenses = Expense.query.all()

    monthly_data = {}

    for expense in expenses:

        month = expense.date.strftime("%B %Y")

        if month not in monthly_data:
            monthly_data[month] = 0

        monthly_data[month] += expense.amount

    return render_template(
        'monthly_summary.html',
        monthly_data=monthly_data
    )
@app.route('/export-pdf')
def export_pdf():

    filename = "expense_report.pdf"

    pdf = canvas.Canvas(filename)

    pdf.drawString(
        100,
        800,
        "Expense Report"
    )

    expenses = Expense.query.all()

    y = 760

    for expense in expenses:

        pdf.drawString(

            100,
            y,

            f"{expense.title} | ₹{expense.amount} | {expense.category}"

        )

        y -= 20

    pdf.save()

    return send_file(
        filename,
        as_attachment=True
    )
# Run Application
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)