from flask import Flask, render_template, request
import stanza
import spacy
from comma_and_separated_nouns import get_noun_phrases

# download the English language model
stanza.download('en')

# initialize the pipeline
nlp = stanza.Pipeline('en')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    input_text = ""
    pronouns = []
    sentence = ""
    noun_phrases = []
    if request.method == 'POST':
        input_text = request.form['sentence']
        pronouns = extract_pronouns(input_text)
        sentence = request.form['sentence']
        noun_phrases = get_noun_phrases(sentence)
    return render_template('index.html', input_text=input_text, pronouns=pronouns, sentence=sentence, noun_phrases=noun_phrases)

def extract_pronouns(text):
    # process the input text
    doc = nlp(text)

    # extract the pronouns from the processed text
    pronouns = []
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.upos == 'PRON':
                pronouns.append(word.text)

    # return the identified pronouns as a list
    return pronouns

def get_noun_phrases(text):
    # process the input text
    doc = nlp(text)

    # extract the noun phrases from the processed text
    noun_phrases = []
    for sentence in doc.sentences:
        phrase = []
        for token in sentence.tokens:
            # check if the current token is a noun
            if token.upos.startswith('N'):
                phrase.append(token.text)
            # if the current token is not a noun, add the current phrase to the list of phrases
            elif phrase:
                noun_phrases.append(' '.join(phrase))
                phrase = []
        # if the sentence ends with a noun phrase, add it to the list of phrases
        if phrase:
            noun_phrases.append(' '.join(phrase))

    # return the identified noun phrases as a list
    return noun_phrases




if __name__ == '__main__':
    app.run(debug=True)
