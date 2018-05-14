import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import pickle

from nltk.corpus import stopwords
stopwords_list = stopwords.words("english")


def loadCSV(file="the-office-lines - scripts.csv"):
	return pd.read_csv(file, sep=",")

def GroupFilmedColumns(dt,column_name):
	return dt.groupby([column_name])

def GetFilmedLines():
	dt = GroupFilmedColumns(loadCSV(),'deleted')
	keys = dt.groups.keys()
	return dt.get_group(keys[0])

def GetLines_noStopWords():
	dt = GetFilmedLines()
	df = dt.values
	lines_spoken = df[:,4]
	for i in range(lines_spoken.shape[0]):
		tokenized_sentence = lines_spoken[i].lower().split(" ")
		tmp_lst = [word.strip('.').strip(',').strip(':').strip(',').strip('?').strip(';') for word in tokenized_sentence if word not in stopwords_list]
		tmp_str = ' '.join(tmp_lst)
		lines_spoken[i] = tmp_str
	df[:,4] = lines_spoken

	dt_changed = pd.DataFrame(df)
	dt_changed.to_csv("FilmedLinesWithoutStopWords_28thApril.csv",sep=",",header=None,index=False)

def FilterShowRegulars():
	dt = GroupFilmedColumns(loadCSV("FilmedLinesWithoutStopWords_28thApril.csv"),'speaker')
	keys = dt.groups.keys()
	all_character_lines = [len(dt.get_group(key)) for key in keys]
	threshold_filter = sum(all_character_lines)*2/100
	filtered_keys = [key for key in keys if len(dt.get_group(key))>=threshold_filter]
	filtered_keys.append('Jan')
	return dt, filtered_keys


def MostTalkedbyaCharacter():
	dt, keys = FilterShowRegulars()
	keys_lower = [key.lower() for key in keys]
	my_dict = {}
	for key in keys:
		temp_dict = {}
		character_info = dt.get_group(key)
		character_info['line_text'].replace('', np.nan, inplace=True)
		character_info.dropna(subset=['line_text'], inplace=True)
		character_lines = character_info.values[:,4]
		for line in character_lines:
			for key_lw in keys_lower:
				if key_lw in line:
					if key_lw not in temp_dict:
						temp_dict[key_lw] = 1
					else:
						temp_dict[key_lw] = temp_dict[key_lw] + 1
		my_dict[key] = temp_dict
	with open('Chartalkchar_dict','wb') as fp:
		pickle.dump(my_dict, fp)

def PlotTalkedCharacterHistogram():
	with open("Chartalkchar_dict","rb") as fp:
		CharactertalkCharacter = pickle.load(fp)
	for character in CharactertalkCharacter:
		print character, CharactertalkCharacter[character]

PlotTalkedCharacterHistogram()