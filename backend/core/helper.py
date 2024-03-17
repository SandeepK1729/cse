from django.shortcuts   import render
from django.conf        import settings

from keras.saving       import load_model, save_model
from pickle             import load, dump

from tensorflow.keras.preprocessing.sequence  import pad_sequences

# import nltk    #need to download necessary dictionaries 
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

from collections import Counter
from string import punctuation
import numpy as np

nlp = None
kw_extractor = None

if settings.TOKENIZING_APPROACH == 'nlp':
    import spacy
    nlp = spacy.load("en_core_web_sm")

elif settings.TOKENIZING_APPROACH == 'yake':
    from yake import KeywordExtractor
    kw_extractor = KeywordExtractor()

elif settings.TOKENIZING_APPROACH == 'keybert':
    from keybert import keyBERT

    kw_extractor = keyBERT()

priority_score = {
    'predictive_score': 100,
    'relevance_score' : 0
}

templates = {
    "search": {
        True: "components/search_results_component.html",
        False: "search.html"
    }
}
def get_template(template_name, is_htmx):
    return templates[template_name][is_htmx]
    
def custom_render(request, template_name, context = {}):
    is_htmx = request.META.get("HTTP_HX_REQUEST", 'false') == 'true'

    return render(request, get_template(template_name, is_htmx), context)

def load_nn_model():
    if settings.MODEL is None:
        try:
            settings.MODEL = load_model(f"../models/model_{settings.MODEL_VERSION}.keras")
            print(f"Loaded model from {settings.MODEL}")
        except Exception as e:
            print(f"Got exception, trying to load model from model_version: {settings.MODEL_VERSION} ", e)
            return None
        
    return settings.MODEL

def save_nn_model():
    try:
        save_model(settings.MODEL, f"../models/model_{settings.MODEL_VERSION}.keras", overwrite=True)
    except Exception as e:
        print(f"Got exception, trying to save model to model_version: {settings.MODEL_VERSION} ", e)
    finally:
        return settings.MODEL

def load_tokenizer():
    if settings.TOKENIZER is not None:
        return settings.TOKENIZER
    
    try:
        with open('../models/tokenizer.pickle', 'rb') as handle:
            settings.TOKENIZER = load(handle)
        print(f"Loaded tokenizer from {settings.TOKENIZER}")
    except Exception as e:
        print(f"Got exception, trying to load tokenizer ", e)
    
    return settings.TOKENIZER

def save_tokenizer():
    try:
        dump(settings.TOKENIZER, open("../models/tokenizer.pickle", "wb"))
    except Exception as e:
        print(f"Got exception, trying to save tokenizer ", e)
    finally:
        return settings.TOKENIZER

def tokenize_data(records):
    tokenizer = load_tokenizer()
    seq = tokenizer.texts_to_sequences(records)
    pad = pad_sequences(seq, padding='post', maxlen = settings.PARAMS)
    return pad

def predict_priority_scores(meta_infos, liked_keywords):
    model = load_nn_model()
    meta_pads = tokenize_data(meta_infos)
    liked_pad = tokenize_data(liked_keywords)

    liked_pads = np.repeat(liked_pad, meta_pads.shape[0], axis=0)
    # liked_pad = np.expand_dims(liked_pad, axis=0)

    scores = model.predict([meta_pads, liked_pads])
    return scores

def get_extract_keywords(s, approach = settings.TOKENIZING_APPROACH):
    """
        used to retrieve keywords from a string

        Args:
            s: string containing keywords
        
        Returns:
            list: list of keywords
    """
    if approach == 'nlp':
        result = []
        pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
        doc = nlp(s.lower()) 
        for token in doc:
            if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
                continue
            if(token.pos_ in pos_tag):
                result.append(token.text)
        return result
    
    elif approach in ('yake', 'keybert'):
        keywords = kw_extractor.extract_keywords(s)
        return keywords
    
    return []

def extract_keywords(s):
    return set(get_extract_keywords(s))

def prioritize_results_order(items, order):
    """
        used to prioritize the search results with order

        Args:
            items: list of search results
            order: list of priorities
        
        Returns:
            list: list of search results with priority scores
    """
    for i in range(0, len(items)):
        items[i]['priority_score'] = order[i]
    
    items.sort(key = lambda item: item['priority_score'])
    return items

def generate_order(orders, n):

    types_of_orders = orders.keys()
    total_sum_of_priorities = sum([priority_score[key] for key in types_of_orders])
    result_order = [0] * n

    for i in range(0, n):
        for key in types_of_orders:
            result_order[i] += priority_score[key] * (orders[key][i] / total_sum_of_priorities)
    
    return result_order

