from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    first_term = int(request.form['num1'])
    common_difference_ratio = int(request.form['num2'])
    operation = request.form['operation']
    num_terms = 10  # Set default number of terms to 10

    # Check if number of terms is provided
    if 'terms' in request.form:
        num_terms = int(request.form['terms'])

    # Calculate the sequence based on the selected operation
    if operation == 'AP':
        sequence = [first_term + i * common_difference_ratio for i in range(num_terms)]
        result = {'sequence': sequence, 'type': 'AP'}
    elif operation == 'GP':
        sequence = [first_term * common_difference_ratio ** i for i in range(num_terms)]
        result = {'sequence': sequence, 'type': 'GP'}
    else:
        result = {'error': 'Invalid operation selected'}

    return result

if __name__ == '__main__':
    app.run(debug=True)