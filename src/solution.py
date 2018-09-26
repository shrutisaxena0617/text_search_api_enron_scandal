import email
import os
import string
from glob import iglob

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class UserEmails:
    """Class to encapsulate each email as a unique document
       userID is the unique ID of the person receiving email
       emailPath is the unique path of the email in the dataset directory
       emailContent is the email content"""

    def __init__(self, userID, emailPath, emailContent):
        self.userID = userID
        self.emailPath = emailPath
        self.emailContent = emailContent


class TokenMap:
    """lass to build master_dict, an inverted document index dictionary
        for all unique tokens in the email corpus as keys
        and list of UserEmails class objects containing these tokens in their emails as values"""

    def __init__(self):
        # self.path = '../dataset/**/*' # Uncomment this line to try testing the search api on all users
        self.path = '../dataset/allen-p/*/*'
        self.master_dict = {}

    def parseText(self):
        file_list = [f for f in iglob(self.path, recursive=True) if os.path.isfile(f)]
        self.master_dict = {}
        for f in file_list:
            with open(f, 'r') as file:
                emailContent = file.read()
                file.close()

            emailPath = str(f)
            userID = emailPath.split('/')[2]
            userEmailObj = UserEmails(userID, emailPath, emailContent)

            emailBodyContent = email.message_from_string(emailContent)
            if emailBodyContent.is_multipart():
                for payload in emailBodyContent.get_payload():
                    # if payload.is_multipart(): ...
                    finalEmailBodyContent = payload.get_payload()
            else:
                finalEmailBodyContent = emailBodyContent.get_payload()

            lemmatizedTokens = self.getTokens(finalEmailBodyContent)

            for e in lemmatizedTokens:
                x = self.master_dict.get(e, [])
                x.append(userEmailObj)
                self.master_dict[e] = x
        print('Parsing complete.')

    def getTokens(self, emailContent):
        tokens = word_tokenize(emailContent)
        tokens = [token.lower() for token in tokens]
        table = str.maketrans('', '', string.punctuation)
        stripped_tokens = [token.translate(table) for token in tokens]
        stripped_tokens_alpha = [word for word in stripped_tokens if word.isalpha()]
        stopword_list = set(stopwords.words('english'))
        tokens_without_stopwords = [token for token in stripped_tokens_alpha if not token in stopword_list]
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens_without_stopwords]
        return set(lemmatized_tokens)
