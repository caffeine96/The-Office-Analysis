import pandas as pd
import matplotlib.pyplot as plt

df= pd.read_csv("EpisodeWiseRating.csv",names=['season','episode','rating','votes'])

mean = df['rating'].mean()
var = df['rating'].var()

print mean
print var

rating_dixt={}
for i in range(len(df)):
	if rating_dixt.has_key(df.iloc[i]['rating']):
		rating_dixt[df.iloc[i]['rating']] = rating_dixt[df.iloc[i]['rating']] + 1
	else:	
		rating_dixt[df.iloc[i]['rating']]=1

lists = sorted(rating_dixt.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.plot(x, y)
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.title('Frequency of Ratings ')
plt.show()