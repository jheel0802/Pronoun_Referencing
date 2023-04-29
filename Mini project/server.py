from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home page with form for user input
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get user input
        text = request.form.get('text')

        # Call Google Colab notebook to identify pronouns
        colab_url = 'https://colab.research.google.com/drive/1SZ3xIJv0H-LjTxDq7imZsMS88bsdnd5d#scrollTo=RULwu8fjYehV'
        colab_payload = {'text': text}
        colab_response = requests.post(colab_url, data=colab_payload)

        # Parse output to extract identified pronouns
        pronouns = colab_response.json()['identify_pronouns']

        # Render output in HTML template
        return render_template('output.html', pronouns=pronouns)

    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
