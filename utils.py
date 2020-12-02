import json
import pickle


def save_obj(obj, name):
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_inverted_index():
    name = 'inverted_idx.pkl'
    with open(name, 'rb') as f:
        inverted_idx = pickle.load(f)
    only_keys_and_terms = {}
    for key, value in inverted_idx.items():
        only_keys_and_terms[key] = value[0]
    return only_keys_and_terms

def save_json(name):
    with open(name + '.json', 'a') as f:
        json.dump('', f)
