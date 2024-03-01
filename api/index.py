from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

# New route for the grid
@app.route('/grid')
def grid():
    return render_template('grid.html')  # This will render the grid.html template

if __name__ == '__main__':
    app.run(debug=True)
