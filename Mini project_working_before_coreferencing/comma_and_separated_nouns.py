import stanza

# download the English language model
stanza.download('en')

# initialize the pipeline
nlp = stanza.Pipeline('en')

def get_noun_phrases(text):
    # """
    # Given a text, extract all noun phrases using both dependency parsing and part-of-speech tagging.
    # Return as a list.
    # """
    # # process the input text
    # doc = nlp(text)
    
    # # list to store noun phrases
    # noun_phrases = []
    
    # # iterate over all sentences in the text
    # for sentence in doc.sentences:
        
    #     # iterate over all words in the sentence
    #     for i, word in enumerate(sentence.words):
            
    #         # if the word is a noun or pronoun, start a new noun phrase
    #         if word.upos in ['NOUN', 'PRON']:
    #             noun_phrase = [word.text]
    #             head_id = word.head
            
    #             # iterate over the children of the noun or pronoun
    #             for child in sentence.words:
    #                 if child.head == head_id and child.id != word.id:
    #                     # if the child is an adjective, include it in the noun phrase
    #                     if child.upos == 'ADJ':
    #                         noun_phrase.append(child.text)
                
    #             # add the completed noun phrase to the list
    #             noun_phrases.append(" ".join(noun_phrase))
                
    #         # if the word is a verb, find its children that are noun phrases and add them to the list
    #         elif word.upos == 'VERB':
    #             for child in sentence.words:
    #                 if child.head == word.id and child.upos in ['NOUN', 'PRON']:
    #                     noun_phrase = [child.text]
    #                     head_id = child.head
    #                     for grandchild in sentence.words:
    #                         if grandchild.head == head_id and grandchild.id != child.id:
    #                             if grandchild.upos == 'ADJ':
    #                                 noun_phrase.append(grandchild.text)
    #                     noun_phrases.append(" ".join(noun_phrase))
    
    # # return the identified noun phrases as a list
    # return noun_phrases
    x = []
    # process the sentence
    doc = nlp(text)

    # start the reverse traversal from the end of the sentence
    i = len(doc.sentences[0].words) - 1
    print(i)
    while i >= 0:
        # if a word has deprel "conj", start a second pointer j to find the subject deprel
        if doc.sentences[0].words[i].deprel == "conj":
            # print("hit:",i)
            j = i - 1
            while j >= 0:
                # if a subject deprel is found, print the words from j to i
                if doc.sentences[0].words[j].deprel.startswith("obl") or doc.sentences[0].words[j].deprel.startswith("nsubj") or doc.sentences[0].words[j].deprel.startswith("obj"):
                    words = [word.text for word in doc.sentences[0].words[j:i+1]]
                    x.append(" ".join(words))
                    break
                j -= 1
            # start the next traversal from the position before the subject deprel word
            i = j - 1
        else:
            # print("else hit:",i)
            i -= 1
    return x