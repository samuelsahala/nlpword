# data cleaning process (clean and format)
# 	corpus - collection of texts - pandas use dataframe
# 	clean - remove numbers, lowercase , remove punctuation(?-,) use regular expressions
# 	tokenization - split by word (remove stop words?)
#	format
import os
import pathlib
import pickle
import re
import string
from urllib.parse import urlparse
import pandas as pd
import requests
from bs4.element import Comment
from collections import Counter, defaultdict


class Trie:
	def __init__(self):
		# if empty string return true
		self.root = {"*": "*"}
		self.counter = 0
	
	def add_word(self, word, data_set):
		self.root = data_set if data_set else self.root
		current_node = self.root
		for letter in word:
			if letter not in current_node:
				# if not children - create a new dict to move the pointer one level "down"
				current_node[letter] = dict()
			current_node = current_node[letter]
		# end of the word
		if "*" in current_node:
			current_node["*"] = current_node.get("*", 0) + 1
		else:
			current_node["*"] = 1
		return {"status": True, "data": self.root}
	
	def word_exist(self, word, data_set):
		current_node = data_set if data_set else self.root
		for letter in word:
			if letter not in current_node:
				return False
			current_node = current_node[letter]
		return current_node["*"]


m_trie = Trie()


def trie_word_save(clean_text_bag):
	data_set = load_obj("trie-words")
	for word in clean_text_bag.split():
		res = m_trie.add_word(word, data_set if data_set else None)
		save_obj(res["data"], "trie-words")
	return res["status"]


def trie_search_word(word):
	data_set = load_obj("trie-words")
	res = m_trie.word_exist(word, data_set)
	if res:
		return {"word": word, "count": res}
	else:
		return False


def save_obj(obj, name):
	with open(name+'.pkl', 'wb') as f:
		pickle.dump(obj, f, protocol=2)


def load_obj(name):
	try:
		with open(name+'.pkl', 'rb') as f:
			obj = pickle.load(f)
			return obj
	except (OSError, IOError) as e:
		return False


def read_dataframe():
	cwd = os.getcwd()
	data = pd.read_pickle(cwd + '/app/static/uploads/' + "cleandfword.pkl")
	return data


def re_clean_text_bag(text):
	# lower case
	text = text.lower()
	# remove .*?
	text = re.sub('\[.*?\]', '', text)
	# remove any punctuation
	text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
	# digits, a-z, w* contain numbers
	text = re.sub('\w*\d\w*', '', text)
	# remove '''""'
	text = re.sub('[‘’“”…]', '', text)
	# remove \n
	text = re.sub('\n', '', text)
	return text


# html handler
def lxml_tag_visible(element):
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	# \s white space \r row string \n one char new line
	if re.match(r"[\s\r\n]+", str(element)):
		return False
	if isinstance(element, Comment):
		return False
	return True


def url_reachable(url):
	rex_url = re.compile(
		r'^(?:http|ftp)s?://'  # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
		r'localhost|'  # localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
		r'(?::\d+)?'  # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	if re.match(rex_url, url) is not None:
		try:
			url_parts = urlparse(url)
			request = requests.head("://".join([url_parts.scheme, url_parts.netloc]))
			return request.status_code
			# return request.status_code == HTTPStatus.OK
		except:
			return False
	else:
		return False
