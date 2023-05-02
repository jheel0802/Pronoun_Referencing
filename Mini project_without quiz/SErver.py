from flask import Flask, render_template, request
import spacy
import stanza

# download the English language model
stanza.download('en')

# initialize the pipeline
nlp = stanza.Pipeline('en')

app = Flask(__name__)
nlp_spacy = spacy.load("en_core_web_lg")
nlp_stanza = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma')

@app.route('/', methods=['GET', 'POST'])
def index():
    input_text = ""
    pronouns = []
    sentence = ""
    noun_phrases = []
    nouns = []
    proper_nouns = []
    noun_chunks = []
    adjectives = []
    articles = []
    verbs = []
    prepositions = []
    conjunctions = []
    if request.method == 'POST':
        sentence = request.form['sentence']
        doc_spacy = nlp_spacy(sentence)
        doc_stanza = nlp_stanza(sentence)
        pronouns = extract_pronouns(sentence)
        noun_phrases = get_noun_phrases(sentence)

        for token in doc_spacy:
            if token.pos_ == 'NOUN':
                if token.text[0].isupper():
                    proper_nouns.append(token.text)
                else:
                    nouns.append(token.text)
            elif token.pos_ == 'ADJ':
                adjectives.append(token.text)
            elif token.pos_ == 'DET' and token.text.lower() in ['a', 'an', 'the']:
                articles.append(token.text)
            elif token.pos_ == 'VERB':
                verbs.append(token.text)
            elif token.pos_ == 'ADP':
                prepositions.append(token.text)
            elif token.pos_ == 'CCONJ' or token.pos_ == 'SCONJ':
                conjunctions.append(token.text)
        for sentence in doc_spacy.sents:
            for chunk in sentence.noun_chunks:
                noun_chunks.append(chunk.text)

    return render_template('Index.html', pronouns=pronouns, sentence=sentence, noun_phrases=noun_phrases , nouns=nouns, proper_nouns=proper_nouns, noun_chunks=noun_chunks, adjectives=adjectives, articles=articles, verbs=verbs, prepositions=prepositions, conjunctions=conjunctions)

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
