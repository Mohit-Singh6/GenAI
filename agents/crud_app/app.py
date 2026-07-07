from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Message('{self.text}')"
    

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = Message(text=request.form['text'])
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('index'))
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        message = Message(text=request.form['text'])
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    message = Message.query.get_or_404(id)
    if request.method == 'POST':
        message.text = request.form['text']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', message=message)

@app.route('/delete/<int:id>')
def delete(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)