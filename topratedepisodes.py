import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize.treebank import TreebankWordTokenizer

#mport nltk.tokenizer
# The formula for calculating the Top Rated 250 Titles gives a true Bayesian estimate:
# weighted rating (WR) = (v / (v+m)) * R + (m / (v+m)) * C
# Where:
# R = average for the movie (mean) = (Rating)
# v = number of votes for the movie = (votes)
# m = minimum votes required to be listed in the Top 250 (currently 25000)
# C = the mean vote across the whole report (currently 7.0)

df= pd.read_csv("EpisodeWiseRating.csv",names=['season','episode','rating','votes'])

sorted_df= df.sort_values('rating',ascending=False)

#### Plot for Number of Votes vs IMDb Ratings 
# plt.plot(np.array(sorted_df['rating']),np.array(sorted_df['votes'])) 
# plt.xlabel('Ratings')
# plt.ylabel('Number of Votes')
# plt.title('Number of Votes vs IMDb Ratings')
# plt.show()

top_ten_df= sorted_df.iloc[:10]

lines_df = pd.read_csv("FilmedLinesWithoutStopWords_28thApril.csv")
#### To calculate which character has the most dialogues in the best episodes
# for i in range(len(top_ten_df)):
# 	chosen_lines_df = lines_df.loc[(lines_df['season']==top_ten_df.iloc[i]['season']) & (lines_df['episode']==top_ten_df.iloc[i]['episode']) ]
# 	print chosen_lines_df['speaker'].value_counts().keys()[0]

t = TreebankWordTokenizer()
characters = ['erin','darryl','oscar','jim','michael','angela','pam','andy','ryan','dwight','kevin','kelly','toby','jan','stanley','meredith']
mentions=[]
central_charac_df=pd.DataFrame(columns=['season','episode','central_character','mentions'])
for i in range(len(top_ten_df)):
	ment_dict={}
	temp_dict={}			#For appending final output
	chosen_lines_df = lines_df.loc[(lines_df['season']==top_ten_df.iloc[i]['season']) & (lines_df['episode']==top_ten_df.iloc[i]['episode']) ]
	for line in chosen_lines_df['line_text']:
		try:
			lower_text = t.tokenize(line)
		except TypeError:
			continue
		
		for word in lower_text:
			if word in characters:
				if ment_dict.has_key(word):
					ment_dict[word] = ment_dict[word] + 1
				else:
					ment_dict[word] = 1
	temp_dict['season'] = top_ten_df.iloc[i]['season']
	temp_dict['episode'] = top_ten_df.iloc[i]['episode']
	temp_dict['central_character'] = max(ment_dict, key=ment_dict.get)
	temp_dict['mentions'] = ment_dict[temp_dict['central_character']]
	print temp_dict
	central_charac_df = central_charac_df.append(temp_dict, ignore_index=True)

central_charac_df.to_csv("Central Characters.csv")

