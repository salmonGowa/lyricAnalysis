import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download
from matplotlib.sankey import Sankey
import nltk
import seaborn as sns

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw')



class Lyricscompare:
    def __init__(self):
        self.data = {}

    def load_text(self, filename, label=""):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
                self.data[filename] = {'text': text, 'label': label}
                print(f"File '{filename}' loaded successfully.")
        except Exception as e:
            print(f"Error loading '{filename}': {e}")

    def load_stop_words(self, stopfile):
        download('stopwords')
        with open(stopfile, 'r') as f:
            stop_words = f.read().splitlines()
        self.data['stopwords'] = stop_words
        print("Stopwords loaded successfully.")

    def preprocess_text(self, text):
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Remove stop words
        stop_words = set(self.data.get('stopwords', stopwords.words('english')))
        tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        
        return tokens

    def wordcount_sankey(self, word_list=None, k=5):
        sankey_data = {}
        for filename, content in self.data.items():
            if filename != 'stopwords':
                text = content['text']
                tokens = self.preprocess_text(text)
                word_counts = Counter(tokens)
                if word_list:
                    selected_words = [word for word in word_list if word in word_counts]
                else:
                    selected_words = [word for word, _ in word_counts.most_common(k)]
                sankey_data[filename] = {word: word_counts[word] for word in selected_words}

        # Plot Sankey diagram
        sankey = Sankey()
        for filename, word_counts in sankey_data.items():
            for word, count in word_counts.items():
                sankey.add(flows=[1, -1], labels=[filename, word], orientations=[0, 1], trunklength=10, color='b', alpha=0.3)
        sankey.finish()

    def wordcloud_subplot(self):
        # Exclude stopwords
        num_files = len(self.data) - 1  
        ncols = min(3, num_files)
         # Ceiling division
        nrows = -(-num_files // ncols) 

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows))
        if num_files==1:
            axes=axes.reshape(1)

        for idx, (filename, content) in enumerate(self.data.items()):
            if filename != 'stopwords':
                text = content['text']
                tokens = self.preprocess_text(text)
                word_counts = Counter(tokens)
                ax = axes[idx // ncols, idx % ncols] if num_files > 1 else axes
                wordcloud = WordCloud(width=800, height=800, background_color='white').generate_from_frequencies(word_counts)
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(content['label'])
    

        #ploting the graph using matplotlib
        plt.tight_layout()
        plt.figure(figsize=(12, 6))
        sns.barplot(x='song', y='artist', palette='viridis')
        plt.xlabel('Number of Songs')
        plt.ylabel('Artist(s) Name')
        plt.title('Top 10 Artists with Most Songs')
        

        plt.show()

    def comparative_visualization(self):
        fig, ax = plt.subplots(figsize=(10, 6))

        for filename, content in self.data.items():
            if filename != 'stopwords':
                text = content['text']
                tokens = self.preprocess_text(text)
                word_counts = Counter(tokens)
                ax.plot(sorted(word_counts.values()), label=content['label'])

        ax.legend()
        ax.set_xlabel('word_rank')
        ax.set_ylabel('word_frequency')
        ax.set_title('compared_Frequencies')
        plt.show()


compare = Lyricscompare()
# Load stopwords ,also create a list of stopwors
compare.load_stop_words('stopwords.txt')  
#top 10 songs on spotify 2023
# Load text files
compare.load_text('flowers.txt', 'flowers')  
compare.load_text('killBill.txt', 'killBill')
compare.load_text('AsItWas.txt', 'AsItWas')
compare.load_text('Seven.txt', 'Seven')
compare.load_text('EllaBailasola.txt', 'EllaBailaSola')
compare.load_text('CruelSummer.txt', 'CruelSummer')
compare.load_text('Creepin.txt', 'Creepin')
compare.load_text('CalmDown.txt', 'CalmDown')
compare.load_text('Shakira_Bzrp_Music_Session.txt', 'Shakira_Bzrp_Music_Session')
compare.load_text('Anti_Hero.txt', 'Anti_Hero')
# Generate Sankey diagram
compare.wordcount_sankey(k=10)  
# Generate wordcloud subplot
compare.wordcloud_subplot()      
# Generate comparative visualization
compare.comparative_visualization()  

#spotify 2023 top 10 list
'''
1'Flowers' by Miley Cyrus
2'Kill Bill' by SZA
3'As It Was' by Harry Styles
4'Seven (feat. Latto)' by Jung Kook
5'Ella Baila Sola' by Eslabon Armado, Peso Pluma
6'Cruel Summer' by Taylor Swift
7'Creepin’ (with The Weeknd & 21 Savage)' by Metro Boomin, The Weeknd, 21 Savage
8'Calm Down (with Selena Gomez)' by Rema, Selena Gomez
9'Shakira: Bzrp Music Sessions, Vol. 53' by Bizarrap, Shakira
10'Anti-Hero' by Taylor Swift
'''