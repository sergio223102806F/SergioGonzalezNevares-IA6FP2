# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:14:49 2025

@author: elvin
"""

# Import required libraries
from collections import defaultdict  # For dictionary with default values
import numpy as np  # For probability calculations and random sampling
import math  # For logarithmic operations

class LanguageModel:
    def __init__(self, n_gram=2):
        """
        Initialize the language model with n-gram structure.
        
        Args:
            n_gram (int): The context window size (2 for bigrams, 3 for trigrams, etc.)
        """
        self.n_gram = n_gram  # Store the n-gram size
        # Dictionary to store counts of each n-gram (e.g., ('el', 'gato') -> 2)
        self.counts = defaultdict(int)
        # Dictionary to store counts of each context (n-1 words)
        self.context_counts = defaultdict(int)
        # Set to store unique vocabulary words
        self.vocab = set()
        # Counter for total words processed (including start/end markers)
        self.total_words = 0

    def preprocess(self, text):
        """
        Process raw text into tokens with start/end markers.
        
        Args:
            text (str): Input sentence/phrase
            
        Returns:
            list: Processed tokens with markers
        """
        # Convert to lowercase and split into words
        tokens = text.lower().split()
        # Add start markers (<s>) at beginning and end marker (</s>) at end
        # Number of start markers depends on n-gram size (n-1 markers needed)
        return ['<s>']*(self.n_gram-1) + tokens + ['</s>']

    def train(self, corpus):
        """
        Train the model on a text corpus by counting n-gram frequencies.
        
        Args:
            corpus (list): List of sentences/phrases
        """
        for text in corpus:  # Process each text in corpus
            tokens = self.preprocess(text)  # Tokenize with markers
            self.total_words += len(tokens)  # Update total word count
            
            # Add all words to vocabulary
            self.vocab.update(tokens)
            
            # Slide n-gram window through text
            for i in range(len(tokens) - self.n_gram + 1):
                # Extract n-word sequence
                n_gram = tuple(tokens[i:i+self.n_gram])
                # Context is first n-1 words of n-gram
                context = tuple(n_gram[:-1])
                
                # Increment count for this specific n-gram
                self.counts[n_gram] += 1
                # Increment count for this context
                self.context_counts[context] += 1

    def probability(self, word, context):
        """
        Calculate P(word|context) with Laplace (add-1) smoothing.
        
        Args:
            word (str): Word to predict
            context (tuple): Context words (n-1 words)
            
        Returns:
            float: Probability estimate
        """
        context = tuple(context)  # Ensure context is tuple
        # Numerator: count of (context + word) + 1 for smoothing
        numerator = self.counts[context + (word,)] + 1
        # Denominator: count of context + vocabulary size
        denominator = self.context_counts[context] + len(self.vocab)
        return numerator / denominator

    def perplexity(self, test_corpus):
        """
        Evaluate model on test corpus using perplexity metric.
        Lower perplexity = better model performance.
        
        Args:
            test_corpus (list): List of test sentences
            
        Returns:
            float: Perplexity score
        """
        total_log_prob = 0  # Accumulator for log probabilities
        test_word_count = 0  # Counter for words in test set
        
        for text in test_corpus:
            tokens = self.preprocess(text)
            test_word_count += len(tokens)
            
            # Start predicting from nth word (after context)
            for i in range(self.n_gram-1, len(tokens)):
                context = tokens[i-self.n_gram+1:i]  # Get context
                word = tokens[i]  # Current word to predict
                # Add log probability to accumulator
                total_log_prob += math.log(self.probability(word, context))
        
        # Calculate perplexity: e^(-average log probability)
        return math.exp(-total_log_prob / test_word_count)

    def generate_text(self, max_length=20):
        """
        Generate new text by sampling from the model's probability distribution.
        
        Args:
            max_length (int): Maximum words to generate
            
        Returns:
            str: Generated text
        """
        # Initialize with start markers
        text = ['<s>']*(self.n_gram-1)
        
        while len(text) < max_length + self.n_gram - 1:
            # Get last n-1 words as current context
            context = tuple(text[-(self.n_gram-1):])
            
            # Collect possible next words and their probabilities
            candidates = []
            for word in self.vocab:
                if context + (word,) in self.counts:
                    prob = self.probability(word, context)
                    candidates.append((word, prob))
            
            # If no candidates, stop generation
            if not candidates:
                break
                
            # Separate words and probabilities
            words, probs = zip(*candidates)
            # Normalize probabilities to sum to 1
            probs = np.array(probs) / sum(probs)
            # Randomly select word based on probabilities
            word = np.random.choice(words, p=probs)
            
            text.append(word)
            # Stop if end marker is generated
            if word == '</s>':
                break
                
        # Return generated text without markers
        if text[-1] == '</s>':
            return ' '.join(text[self.n_gram-1:-1])
        else:
            return ' '.join(text[self.n_gram-1:])

# Demonstration
if __name__ == "__main__":
    # Example training data (Spanish phrases about pets)
    corpus = [
        "el gato come pescado",
        "el perro come carne",
        "el gato bebe leche",
        "el perro bebe agua"
    ]
    
    # Create and train bigram model
    print("Training bigram model...")
    lm = LanguageModel(n_gram=2)
    lm.train(corpus)
    
    # Evaluate on test sentence
    test_text = ["el gato bebe agua"]
    print(f"Perplexity on test text: {lm.perplexity(test_text):.2f}")
    
    # Generate new text
    print("Generated example:", lm.generate_text())