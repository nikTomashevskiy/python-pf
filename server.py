import csv,sqlite3
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
print(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page>')
def html_page(page):
    return render_template(f'{page}.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        # write_to_csv(data)
        write_to_db(data)
        return redirect('/thank_you')
    else:
        return redirect('/something_went_wrong')


def write_to_csv(data):
    with open('database.csv', 'a') as db:
        writer = csv.DictWriter(db, data.keys())
        writer.writerow(data)


def write_to_db(data):
    con = sqlite3.connect('messages.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
       email TEXT,
       subject TEXT,
       message TEXT);
    """)
    data_to_insert=(data['email'],data['subject'],data['message'])
    cur.execute("INSERT INTO messages VALUES(?, ?, ?);", data_to_insert)
    con.commit()
    con.close()