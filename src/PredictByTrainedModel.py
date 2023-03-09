import os
import random
import pickle
import subprocess
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

def get_phpfile_vector(filepath, model_to_use = ''):
    model_path = './TF_IDF_model'

    if model_to_use == '':
        models = os.listdir(model_path)
        model_to_use = random.choice(models)
    vectorizer = pickle.load(open(os.path.join(model_path, model_to_use), 'rb'))

    vectorizer.set_params(input='content')
    file_BoW = subprocess.check_output(["php", "GenASTBoW.php", filepath])
    X = vectorizer.transform([file_BoW.decode()])
    # print(vectorizer.idf_)
    return X

def predict(filepath, model_path = './MLP_model', model_to_use = ''):
    X = get_phpfile_vector(filepath)

    if model_to_use == '':
        models = os.listdir(model_path)
        model_to_use = random.choice(models)
    clf = pickle.load(open(os.path.join(model_path, model_to_use), 'rb'))
    
    predict_results = clf.predict(X)
    if predict_results.tolist()[0] == 1:
        print(f"[+]{filepath} is likely webshell!!!")
    else:
        print(f"[-]{filepath} is normal")

if __name__ == '__main__':
    predict('./test.php')
