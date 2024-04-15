from django.shortcuts   import render
from django.conf        import settings

from keras.saving       import load_model, save_model
from pickle             import load, dump

from tensorflow.keras.preprocessing.sequence  import pad_sequences

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


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
    'relevance_score' : 100,
    'irrelevance_score' : 100,
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
            print(handle)
            settings.TOKENIZER = load(handle)
        
        print(f"Loaded tokenizer from file {settings.TOKENIZER}")
    except Exception as e:
        from .model_backend import train_from_dataset

        print(f"Got exception, trying to load tokenizer ", e)
        try:
            settings.TOKENIZER = train_from_dataset()
            print("trained tokenizer from dataset")

        except Exception as ex:
            print("Got exception, trying to train tokenizer from file ", ex)


    
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
    print(meta_infos, liked_keywords, "\n" * 3)
    model = load_nn_model()
    meta_pads = tokenize_data(meta_infos)
    liked_pad = tokenize_data(liked_keywords)

    print(liked_keywords, liked_pad.shape, meta_pads.shape, "\n" * 3)
    liked_pads = np.repeat(liked_pad, meta_pads.shape[0], axis=0)
    # liked_pad = np.expand_dims(liked_pad, axis=0)
    
    print("meta_pads", meta_pads.shape, "liked_pads", liked_pads.shape, "\n" * 3)
    print(meta_pads, liked_pads, "\n" * 3)
    scores = model.predict([meta_pads, liked_pads])
    return scores

def retrain_model(meta_info, liked_keywords, score):
    """
    Retrain the model using the given meta_info, liked_keywords, and score.

    Args:
        meta_info (str): the meta information of the record
        liked_keywords (str): the liked keywords of the record
        score (float): the score of the record

    Returns:
        None
    """
    print("retrain_model", meta_info, liked_keywords, score, "\n" * 3)
    model = load_nn_model()
    meta_pad = tokenize_data(meta_info)
    liked_pad = tokenize_data(liked_keywords)
    liked_pads = np.repeat(liked_pad, meta_pad.shape[0], axis=0)
    print(meta_pad.shape, liked_pad.shape, "liked_pads", liked_pads.shape, "\n" * 3)
    print(meta_pad, liked_pads, "\n" * 3)
    model.fit([meta_pad, liked_pads], [score], epochs=10, verbose=1)
    save_nn_model(model)

    return model

def get_relevance_score(meta_infos, liked_keywords, rev = False):
    #Compute embedding for both lists
    liked_keys = model.encode(' '.join(liked_keywords), convert_to_tensor=True)
    metas = model.encode(meta_infos, convert_to_tensor=True)

    res = [
        util.pytorch_cos_sim(meta, liked_keys).tolist()[0][0]
        for meta in metas
    ]
    if rev:
        res.reverse()

    print("=======================", res)
    return res

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
    return list([word for word, perc in set(get_extract_keywords(s))])

def prioritize_results_order(items, order):
    """
        used to prioritize the search results with order

        Args:
            items: list of search results
            order: list of priorities
        
        Returns:
            list: list of search results with priority scores
    """
    print(order)
    for i in range(0, len(items)):
        print(order[i], items[i]['title'])
        items[i]['priority_score'] = order[i]
    
    items.sort(key = lambda item: -item['priority_score'])
    return items

def generate_order(orders, n):

    types_of_orders = orders.keys()
    total_sum_of_priorities = sum([priority_score[key] for key in types_of_orders])
    result_order = [0] * n

    for i in range(0, n):
        for key in types_of_orders:
            result_order[i] += priority_score[key] * (orders[key][i] / total_sum_of_priorities)
    
    return result_order

