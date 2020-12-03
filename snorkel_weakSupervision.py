from preprocessing import fetch_and_preprocess_snorkel, tfidf_vectorizer
from weak_supervision import weak_supervisor
from Training import train, get_test_accuracy
import pandas as pd

classification_accuracies = []
unlabeled_df, train_df, test_df = fetch_and_preprocess_snorkel("./imdb/train", "./imdb/test")
print("unlabeled_df shape: ", unlabeled_df.shape)
print("test_df shape: ", test_df.shape)

# generating weak labels for the unlabeled data
validation_df = weak_supervisor(pd.DataFrame(train_df), "label_model")

# construct train and test sets
X_train = tfidf_vectorizer(validation_df['data'], max_df=0.4, ngram_range=(1,2), max_features=15000)
Y_train = validation_df['weak_labels'].values
X_test = tfidf_vectorizer(test_df['data'], max_df=0.4, ngram_range=(1,2), max_features=15000)
Y_test = test_df['target'].values

# Training
classifier, Y_test_predicted = train(X_train, Y_train, X_test, "SVC")
get_test_accuracy(1, Y_test, Y_test_predicted, classification_accuracies)
