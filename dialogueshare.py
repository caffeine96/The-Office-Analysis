import pandas as pd
import matplotlib.pyplot as plt
import os

from matplotlib.transforms import TransformedBbox
from matplotlib.image import BboxImage
from matplotlib.legend_handler import HandlerBase
from matplotlib._png import read_png

df = pd.read_csv("FilmedLinesWithoutStopWords_28thApril.csv")



def dialogueshare(character):
	characters = df['speaker']
	characters = set(characters)
	#print characters

	###clean
	remove_charac=[]
	for i in characters:
		if len(i)>20:
			remove_charac.append(i)
	for i in remove_charac:
		characters.remove(i)

	print len(characters)


	dialogue_stat={}

	#### Counter per character per season
	for i in characters:
		dialogue_stat[i]=[0]*9
		df_char =  df.loc[(df['speaker'] == i)]
		for j in range(0,len(df_char)):
			dialogue_stat[i][(df_char.iloc[j]['season'])-1] += 1

	print dialogue_stat[character]		
	charac_dialogue = dialogue_stat[character]

	total_dialogue=[0]*9
	### Dialogues per season
	for i in range(9):
		df_dial= df.loc[(df['season'] == i+1)]
		total_dialogue[i] = len(df_dial)

	print total_dialogue

	dialogue_share_norm=[]
	for i in range(9):
		dialogue_share_norm.append(float(charac_dialogue[i])/float(total_dialogue[i]))

	print dialogue_share_norm 
	print "\n\n"

	return dialogue_share_norm

def dialogueplot(dialogue_share_norm,characters):
	season=[i for i in xrange(1,10)]
	subplots= [221,222,223,224]
	plt.figure(1)

	for i in range(4):
		plt.subplot(subplots[i])
		plt.bar(season,dialogue_share_norm[characters[i]])
		plt.xlabel('Season')
		plt.ylabel('Dialogue Share')
		plt.ylim((0,0.5))
		plt.title('Dialogue Share of '+ str(characters[i])+ ' over seasons')
	plt.show()


if __name__=="__main__":
	dialogue_share_norm={}
	characters=["Michael","Jim","Dwight","Pam"]
	for i in characters:
		dialogue_share_norm[i] = dialogueshare(i)
	dialogueplot(dialogue_share_norm,characters)


