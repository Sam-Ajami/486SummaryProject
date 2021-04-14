============
summarization.py
============
To run summarization.py you must have all your articles in folder in the directory the python file is in. You must also have a second empty folder titled "ourSummaries". From there, you run it like so:

python3 summarization.py [name of folder of articles]

This will populate the ourSummaries folder with text files corresponding to the input articles.

NOTE: summarization.py makes some assumptions about the files its processing. Articles must follow standard english grammar and quotation marks cannot be allowed to hand unclosed. If you don't use periods, question marks, or exclaimation to end sentences, then the whole article will be considered one sentence. Check the provided dataset to see examples of proper articles
============
evaluation.py
============
To run evaluation.py, you must have all the summarization.py summaries in a folder and their corresponding "correct" summaries in another folder in the same directory the python file is in. From there, you run it like so:

python3 evaluation.py [name of folder of "correct" summaries] [name of folder of evaluation.py summaries]

This will print in the terminal the Recall and Precision of each of the summarization.py summaries along with the macro-averaged Recall and Precision

NOTE: the folder containing the "correct" summaries must have at least as many summaries as the summarization.py summary folder. Summaries will be matched 1-to-1 based on their natural alphabetical sorting. Check the provided dataset to see examples of proper formatting.