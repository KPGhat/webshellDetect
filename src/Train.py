import os
import numpy as np
import pickle
import random
import string
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer


def NLP_By_BoW(history_model = ''):
	webshelldir = './webshellBoW'
	whitecodedir = './whitecodeBoW'
	webshellBoWs = os.listdir(webshelldir)
	whitecodeBoWs = os.listdir(whitecodedir)
	
	BoWs = []
	Yarr = []
	# process bow files' path
	# mark webshell with 1
	# mark whitecode with 0
	for webshellBoW in webshellBoWs:
		BoWs.append(os.path.join(webshelldir, webshellBoW))
		Yarr.append([1])
	for whitecodeBoW in whitecodeBoWs:
		BoWs.append(os.path.join(whitecodedir, whitecodeBoW))
		Yarr.append([0])

	# choose whether to use built BoWs
	model_path = './TF_IDF_model'
	if history_model:
		vectorizer = pickle.load(open(os.path.join(model_path, history_model), 'rb'))
		print('[*]Using history model')
	else:
		vectorizer = TfidfVectorizer(input='filename', token_pattern=r'(\S*)\b')
		vectorizer.fit(BoWs)
		store_model(vectorizer, model_path)
		print('[+]Using new trained model')

	X = vectorizer.transform(BoWs)
	Y = np.array(Yarr)
	return (X , Y)


def MPL(X, y, history_model = '', activation = 'relu', solver = 'lbfgs'):
	feature_train, feature_test, target_train, target_test = train_test_split(X, y, random_state=3)

	model_path = './MLP_model'
	if history_model:
		clf = pickle.load(open(os.path.join(model_path, history_model), 'rb'))
	else:
		# 神经网络输入为2层，第一隐藏层神经元个数为30，第二隐藏层神经元个数为20，输出结果为2分类。
		# solver='lbfgs',  MLP的求解方法：L-BFGS 在小数据上表现较好，Adam 较为鲁棒，
		# SGD在参数调整较优时会有最佳表现（分类效果与迭代次数）,SGD标识随机梯度下降。
		clf =  MLPClassifier(activation=activation, solver=solver, hidden_layer_sizes=(30,20), random_state=1, max_iter=1000)
		clf.fit(feature_train, np.ravel(target_train))
		store_model(clf, model_path, '-'.join([activation, solver]))

	predict_results = clf.predict(feature_test)
	print(f"[*]Using {activation} activation and {solver} solver...")
	print("[+]result:", accuracy_score(predict_results, target_test))
	# print(classification_report(target_test, predict_results))

def KNN(X, y, history_model = '', K = 5):
	feature_train, feature_test, target_train, target_test = train_test_split(X, y, random_state=3)

	model_path = './KNN_model'
	if history_model:
		knn = pickle.load(open(os.path.join(model_path, history_model), 'rb'))
	else:
		knn = KNeighborsClassifier(n_neighbors=K)
		knn.fit(feature_train, np.ravel(target_train))
		store_model(knn, model_path, str(K))
	
	predict_results = knn.predict(feature_test)
	print(f'K={K}:',accuracy_score(predict_results, target_test))
	# print(classification_report(target_test, predict_results))

def store_model(model, model_path, model_name = ''):
	if not os.path.exists(model_path):
		os.mkdir(model_path)

	if model_name == '':
		model_name = ''.join(random.choices(string.ascii_letters, k=15))
		while os.path.exists(os.path.join(model_path, model_name)):
			model_name = ''.join(random.choices(string.ascii_letters, k=15))

	pickle.dump(model, open(os.path.join(model_path, model_name), 'wb'))


if __name__ == '__main__':
	X, y = NLP_By_BoW()
	print('[+]Bag of Words model transform finish')
	MPL(X, y, activation='relu', solver='adam')
	for i in range(3, 10):
		KNN(X, y, K=i)
