import stanza
import spacy
def load_stanza_model():
    try:
        # try to load the English model
        nlp = stanza.Pipeline('en')
    except:
        # if it's not available, download it
        stanza.download('en')
        nlp = stanza.Pipeline('en')
    return nlp

# load the English model
nlp = load_stanza_model()

def get_pronouns(text):
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
