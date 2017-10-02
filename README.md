# Dataset

The dataset is divided into three files:

1. **Sarcasm_tweets.txt**: This file contains all the tweet ids and their corresponding tweet text. Each tweet id is followed by the text and a blank line and so on. 

1. **Sarcasm_tweets_with_language.txt**: This file contains tweet id followed by the corresponding tweet that tokenized and each token is tagged with a language tag (en/hi/rest). 


1. **Sarcasm_tweet_truth.txt**: This file contains tweet id followed by a label (YES/NO) that indicates presence of sarcasm and then a blank line.


# Classification system

We use three machine learning techniques and 10-fold cross validation for sarcasm detection on the provided dataset. Run the script 'classification.py' with one of the following arguments: 

1. rbfsvm
1. linearsvm
1. randomforest

where rbfsvm stands for support vector machine with radial basis function kernel, linearsvm stands for linear support vector machine and randomforest stands for random forest classifier. For example use the following command:

`python classification.py randomforest`
