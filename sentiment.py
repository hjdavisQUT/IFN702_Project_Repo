#Script Start

#requires vaderSentiment package.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import os.path

#initialize the analyser.
analyser = SentimentIntensityAnalyzer()

#parameters parsed to the script from Cherwell.
input_comment = sys.argv[1]
qs_id = sys.argv[2]

#calculating the sentiment score.
vs_score = analyser.polarity_scores(input_comment)
vs_comp = float(vs_score['compound'])

#Saving the result to a txt file with the name of the quick survey public ID.
file_dest = "C:\\Temp\\Quick Survey\\output\\"
file_name = str(qs_id) + '.txt'
file_path = os.path.join(file_dest, file_name)
f = open(file_path, 'w')
f.write(str(vs_comp))
f.close()

#Script End
