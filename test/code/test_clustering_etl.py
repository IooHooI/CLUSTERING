import unittest
from source.code.data_downloader import DataDownloader
from collections import Counter


class TestCLUSTERINGETL(unittest.TestCase):

    def setUp(self):
        self.clustering_etl = DataDownloader('../../data/datasets/')

    def test_get_raw_data(self):
        self.clustering_etl.get_raw_data('https://www.kaggle.com/crawford/20-newsgroups/downloads/20-newsgroups.zip')

    def test_extract_documents(self):
        documents, labels = self.clustering_etl.extract_documents()
        self.assertEqual(len(documents), len(labels), 'All documents should have a label!!!')
        self.assertEqual(20, len(Counter(labels).keys()), 'The topics count should be equal 20!!!')

    def test_counter(self):
        list_ = [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 1, 4, 2, 1, 4, 2]
        print(list_ == 1)


if __name__ == '__main__':
    unittest.main()
