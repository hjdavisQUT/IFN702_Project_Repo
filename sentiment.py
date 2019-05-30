from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import os.path

analyser = SentimentIntensityAnalyzer()

input_comment = sys.argv[1]
qs_id = sys.argv[2]

vs_score = analyser.polarity_scores(input_comment)
vs_comp = float(vs_score['compound'])
file_dest = "C:\\Temp\\Quick Survey\\output\\"
file_name = str(qs_id) + '.txt'
file_path = os.path.join(file_dest, file_name)

f = open(file_path, 'w')
f.write(str(vs_comp))
f.close()
