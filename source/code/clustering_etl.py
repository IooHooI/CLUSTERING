from tqdm import tqdm
import requests
import os
import logging
import zipfile
import string
from nltk import word_tokenize
from nltk.corpus import stopwords


class CLUSTERINGETL:

    _contractions = {
        "ain't": "am not / are not / is not / has not / have not",
        "aren't": "are not / am not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he had / he would",
        "he'd've": "he would have",
        "he'll": "he shall / he will",
        "he'll've": "he shall have / he will have",
        "he's": "he has / he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how has / how is / how does",
        "I'd": "I had / I would",
        "I'd've": "I would have",
        "I'll": "I shall / I will",
        "I'll've": "I shall have / I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it had / it would",
        "it'd've": "it would have",
        "it'll": "it shall / it will",
        "it'll've": "it shall have / it will have",
        "it's": "it has / it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she had / she would",
        "she'd've": "she would have",
        "she'll": "she shall / she will",
        "she'll've": "she shall have / she will have",
        "she's": "she has / she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so as / so is",
        "that'd": "that would / that had",
        "that'd've": "that would have",
        "that's": "that has / that is",
        "there'd": "there had / there would",
        "there'd've": "there would have",
        "there's": "there has / there is",
        "they'd": "they had / they would",
        "they'd've": "they would have",
        "they'll": "they shall / they will",
        "they'll've": "they shall have / they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we had / we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what shall / what will",
        "what'll've": "what shall have / what will have",
        "what're": "what are",
        "what's": "what has / what is",
        "what've": "what have",
        "when's": "when has / when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where has / where is",
        "where've": "where have",
        "who'll": "who shall / who will",
        "who'll've": "who shall have / who will have",
        "who's": "who has / who is",
        "who've": "who have",
        "why's": "why has / why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you had / you would",
        "you'd've": "you would have",
        "you'll": "you shall / you will",
        "you'll've": "you shall have / you will have",
        "you're": "you are",
        "you've": "you have"
    }

    _stop_w = stopwords.words('english')
    _the_trash = frozenset(
        _stop_w +
        list(string.punctuation) +
        list(string.digits)
    )

    def __init__(self, local_path):
        self.logger = logging.getLogger(CLUSTERINGETL.__name__)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)
        self.logger.info('\nINITIALIZING...')
        self.local_path = local_path
        self.logger.info('INITIALIZATION HAS BEEN COMPLETED')

    def get_raw_data(self, url):
        file_name = url.split('/')[-1]
        if not os.path.exists(os.path.join(self.local_path, file_name)):
            self.logger.info('ARCHIVE FILE HAS NOT BEEN DOWNLOADED YET')
            if not os.path.exists(self.local_path):
                self.logger.info('CREATE LOCAL DIRECTORY')
                os.mkdir(self.local_path)
            self.logger.info('START DOWNLOADING ARCHIVE FILE')
            response = requests.get(url, stream=True)
            with open(os.path.join(self.local_path, file_name), "wb") as handle:
                for data in tqdm(response.iter_content()):
                    handle.write(data)
            self.logger.info('ARCHIVE FILE DOWNLOADING HAS BEEN COMPLETED')
            # ==========================================================================================================
            if not os.path.exists(os.path.join(self.local_path, 'unzipped')):
                self.logger.info('ARCHIVE FILE HAS NOT BEEN UNZIPPED YET')
                self.logger.info('UNZIP ARCHIVE FILE')
                zip_ref = zipfile.ZipFile(os.path.join(self.local_path, file_name), 'r')
                zip_ref.extractall(self.local_path)
                zip_ref.close()
                self.logger.info('ARCHIVE FILE HAS BEEN UNZIPPED')
                open(os.path.join(self.local_path, 'unzipped'), 'a').close()
            # ==========================================================================================================
        else:
            self.logger.info('ARCHIVE FILE HAS BEEN ALREADY DOWNLOADED')
            # ==========================================================================================================
            if not os.path.exists(os.path.join(self.local_path, 'unzipped')):
                self.logger.info('ARCHIVE FILE HAS NOT BEEN UNZIPPED YET')
                self.logger.info('UNZIP ARCHIVE FILE')
                zip_ref = zipfile.ZipFile(os.path.join(self.local_path, file_name), 'r')
                zip_ref.extractall(self.local_path)
                zip_ref.close()
                self.logger.info('ARCHIVE FILE HAS BEEN UNZIPPED')
                open(os.path.join(self.local_path, 'unzipped'), 'a').close()
            # ==========================================================================================================
            else:
                self.logger.info('ARCHIVE FILE HAS BEEN ALREADY UNZIPPED')

    def extract_documents(self):
        files = [f for f in os.listdir(self.local_path) if os.path.isfile(os.path.join(self.local_path, f))]
        files = [f for f in files if '.txt' in f]
        topic_labels = dict(zip(list(map(lambda x: x[:-4], files)), range(len(files))))
        file_paths = [os.path.join(self.local_path, f) for f in files]
        labelled_documents = []
        labels = []
        for file_path in tqdm(file_paths, desc='Files reading and documents extraction'):
            with open(file_path, 'r', encoding='utf8', errors='ignore') as documents_source:
                lines = documents_source.readlines()
                lines = list(map(str.strip, lines))
                full_text = ' '.join(lines)
                label = file_path.split('/')[-1][:-4]
                documents = full_text.split('Newsgroup: {}'.format(label))
                labelled_documents.extend(documents)
                labels.extend([topic_labels[label]] * len(documents))
        for i in tqdm(range(len(labelled_documents)), desc='Documents tokenization'):
            labelled_documents[i] = self._transf(labelled_documents[i])
        return labelled_documents, labels

    def _transf(self, raw_text):
        from nltk.stem import WordNetLemmatizer
        # WordNet lemmatizer
        w_n_l = WordNetLemmatizer()
        # Raw text without contractions
        r_t_w_c = self._expand_contractions(raw_text, self._contractions)
        # Tokenized raw text without contractions
        t_r_t_w_c = word_tokenize(r_t_w_c.lower())
        # Tokenized raw text without contractions and stop words
        t_r_t_w_c_a_s_w = [word for word in t_r_t_w_c if not self._filter(word)]
        # Lemmatized tokenized document
        l_t_d = self._lemmatize(t_r_t_w_c_a_s_w, w_n_l, 'v')
        l_t_d = self._lemmatize(l_t_d, w_n_l, 'n')
        # Shrinked lemmatized tokenized document
        s_l_t_d = [token for token in l_t_d if len(token) > 2 and not self._filter(token)]
        return ' '.join(s_l_t_d)

    def _filter(self, word):
        return any(not letter.isalpha() for letter in word) or word in self._the_trash

    @staticmethod
    def _expand_contractions(text, dic):
        """
        This method runs through text and replaces all contracted phrases with their full forms.
        For example: don't --> do not, shouldn't've --> should not have etc.
        :param text: original text with contractions.
        :param dic: a dictionary of type:
                            {
                                contraction1: full form1,
                                contraction2: full form2,
                                ...
                                contraction_N: full form_N
                            }
        :return: the text with full phrase forms.
        """
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    @staticmethod
    def _lemmatize(tokens, lemmatizer, pos):
        return list(map(lambda x: lemmatizer.lemmatize(x, pos=pos), tokens))
