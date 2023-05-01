from flask import Flask, render_template, request
import stanza

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
        sentence = request.form['sentence']
        pronouns = extract_pronouns(sentence)
        noun_phrases = get_noun_phrases(sentence)
    return render_template('index.html', pronouns=pronouns, sentence=sentence, noun_phrases=noun_phrases)

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
    noun_phrases = []
    # process the sentence
    doc = nlp(text)

    # start the reverse traversal from the end of the sentence
    i = len(doc.sentences[0].words) - 1
    while i >= 0:
        # if a word has deprel "conj", start a second pointer j to find the subject deprel
        if doc.sentences[0].words[i].deprel == "conj":
            j = i - 1
            while j >= 0:
                # if a subject deprel is found, print the words from j to i
                if doc.sentences[0].words[j].deprel.startswith("obl") or doc.sentences[0].words[j].deprel.startswith("nsubj") or doc.sentences[0].words[j].deprel.startswith("obj"):
                    words = [word.text for word in doc.sentences[0].words[j:i+1]]
                    noun_phrases.append(" ".join(words))
                    print("hit4")
                    print(noun_phrases)
                    break
                j -= 1
            # start the next traversal from the position before the subject deprel word
            i = j - 1
        else:
            i -= 1
    print("return:",noun_phrases)
    return noun_phrases

if __name__ == '__main__':
    app.run(debug=True)
