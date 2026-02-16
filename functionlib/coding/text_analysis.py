"""
Text Analysis Functions

Text processing, analysis, and natural language processing utilities.
"""

import re
import math
from typing import List, Dict, Set, Tuple
from collections import Counter


def word_frequency(text: str) -> Dict[str, int]:
    """
    Calculate word frequency
    
    Args:
        text: Input text
        
    Returns:
        Dictionary of word counts
        
    Example:
        >>> word_frequency("hello world hello")
        {'hello': 2, 'world': 1}
    """
    words = re.findall(r'\b\w+\b', text.lower())
    return dict(Counter(words))


def most_common_words(text: str, n: int = 10) -> List[Tuple[str, int]]:
    """
    Get n most common words
    
    Args:
        text: Input text
        n: Number of words
        
    Returns:
        List of (word, count) tuples
        
    Example:
        >>> most_common_words("a a b b b c", 2)
        [('b', 3), ('a', 2)]
    """
    freq = word_frequency(text)
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]


def character_frequency(text: str) -> Dict[str, int]:
    """
    Calculate character frequency
    
    Args:
        text: Input text
        
    Returns:
        Dictionary of character counts
        
    Example:
        >>> character_frequency("hello")
        {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    """
    return dict(Counter(text))


def remove_stopwords(text: str, stopwords: Set[str] = None) -> str:
    """
    Remove common stopwords from text
    
    Args:
        text: Input text
        stopwords: Set of stopwords (default common English words)
        
    Returns:
        Text without stopwords
        
    Example:
        >>> remove_stopwords("the quick brown fox")
        'quick brown fox'
    """
    if stopwords is None:
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                    'to', 'for', 'of', 'with', 'by', 'from', 'is', 'was', 'are'}
    
    words = text.split()
    filtered = [w for w in words if w.lower() not in stopwords]
    return ' '.join(filtered)


def ngrams(text: str, n: int) -> List[Tuple[str, ...]]:
    """
    Generate n-grams from text
    
    Args:
        text: Input text
        n: N-gram size
        
    Returns:
        List of n-grams
        
    Example:
        >>> ngrams("hello world", 2)
        [('hello', 'world')]
    """
    words = text.split()
    return [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]


def sentence_count(text: str) -> int:
    """
    Count sentences in text
    
    Args:
        text: Input text
        
    Returns:
        Number of sentences
        
    Example:
        >>> sentence_count("Hello. How are you? I'm fine.")
        3
    """
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])


def average_word_length(text: str) -> float:
    """
    Calculate average word length
    
    Args:
        text: Input text
        
    Returns:
        Average word length
        
    Example:
        >>> average_word_length("hello world")
        5.0
    """
    words = re.findall(r'\b\w+\b', text)
    if not words:
        return 0
    
    return sum(len(w) for w in words) / len(words)


def lexical_diversity(text: str) -> float:
    """
    Calculate lexical diversity (unique words / total words)
    
    Args:
        text: Input text
        
    Returns:
        Lexical diversity ratio
        
    Example:
        >>> lexical_diversity("hello world hello")
        0.666...
    """
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    
    return len(set(words)) / len(words)


def flesch_reading_ease(text: str) -> float:
    """
    Calculate Flesch Reading Ease score
    
    Args:
        text: Input text
        
    Returns:
        Reading ease score (0-100, higher is easier)
        
    Example:
        >>> score = flesch_reading_ease("The cat sat on the mat.")
        >>> 80 < score < 100
        True
    """
    sentences = sentence_count(text)
    words = len(re.findall(r'\b\w+\b', text))
    syllables = sum(count_syllables(w) for w in re.findall(r'\b\w+\b', text))
    
    if sentences == 0 or words == 0:
        return 0
    
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)


def count_syllables(word: str) -> int:
    """
    Estimate syllable count in a word
    
    Args:
        word: Word
        
    Returns:
        Estimated syllable count
        
    Example:
        >>> count_syllables("hello")
        2
    """
    word = word.lower()
    vowels = 'aeiouy'
    syllables = 0
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllables += 1
        previous_was_vowel = is_vowel
    
    # Adjust for silent e
    if word.endswith('e'):
        syllables -= 1
    
    return max(1, syllables)


def tf_idf(documents: List[str], document_index: int, term: str) -> float:
    """
    Calculate TF-IDF score
    
    Args:
        documents: List of documents
        document_index: Index of document to analyze
        term: Term to score
        
    Returns:
        TF-IDF score
        
    Example:
        >>> docs = ["hello world", "hello there", "world peace"]
        >>> tf_idf(docs, 0, "hello")
        0.0
    """
    # Term frequency
    words = documents[document_index].lower().split()
    tf = words.count(term.lower()) / len(words) if words else 0
    
    # Inverse document frequency
    df = sum(1 for doc in documents if term.lower() in doc.lower().split())
    idf = math.log(len(documents) / df) if df > 0 else 0
    
    return tf * idf


def cosine_similarity_text(text1: str, text2: str) -> float:
    """
    Calculate cosine similarity between two texts
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Cosine similarity (0-1)
        
    Example:
        >>> cosine_similarity_text("hello world", "hello there")
        0.5
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    all_words = words1 | words2
    
    vec1 = [1 if w in words1 else 0 for w in all_words]
    vec2 = [1 if w in words2 else 0 for w in all_words]
    
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))
    
    return dot / (mag1 * mag2) if mag1 * mag2 > 0 else 0


def jaccard_similarity_text(text1: str, text2: str) -> float:
    """
    Calculate Jaccard similarity between two texts
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Jaccard similarity (0-1)
        
    Example:
        >>> jaccard_similarity_text("hello world", "hello there")
        0.333...
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union if union > 0 else 0


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate Levenshtein (edit) distance
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Edit distance
        
    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def hamming_distance(s1: str, s2: str) -> int:
    """
    Calculate Hamming distance (must be same length)
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Hamming distance
        
    Example:
        >>> hamming_distance("karolin", "kathrin")
        3
    """
    if len(s1) != len(s2):
        raise ValueError("Strings must be same length")
    
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text
    
    Args:
        text: Input text
        
    Returns:
        List of email addresses
        
    Example:
        >>> extract_emails("Contact: user@example.com")
        ['user@example.com']
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text
    
    Args:
        text: Input text
        
    Returns:
        List of URLs
        
    Example:
        >>> extract_urls("Visit https://example.com")
        ['https://example.com']
    """
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(pattern, text)


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extract phone numbers from text
    
    Args:
        text: Input text
        
    Returns:
        List of phone numbers
        
    Example:
        >>> extract_phone_numbers("Call 123-456-7890")
        ['123-456-7890']
    """
    pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    return re.findall(pattern, text)


def extract_hashtags(text: str) -> List[str]:
    """
    Extract hashtags from text
    
    Args:
        text: Input text
        
    Returns:
        List of hashtags
        
    Example:
        >>> extract_hashtags("Love #python and #coding")
        ['#python', '#coding']
    """
    return re.findall(r'#\w+', text)


def extract_mentions(text: str) -> List[str]:
    """
    Extract @mentions from text
    
    Args:
        text: Input text
        
    Returns:
        List of mentions
        
    Example:
        >>> extract_mentions("Hey @user1 and @user2")
        ['@user1', '@user2']
    """
    return re.findall(r'@\w+', text)


def sentiment_score_simple(text: str) -> float:
    """
    Simple sentiment analysis (-1 to 1)
    
    Args:
        text: Input text
        
    Returns:
        Sentiment score
        
    Example:
        >>> sentiment_score_simple("I love this!")
        1.0
    """
    positive_words = {'good', 'great', 'excellent', 'love', 'wonderful', 
                      'amazing', 'fantastic', 'best', 'happy', 'joy'}
    negative_words = {'bad', 'terrible', 'awful', 'hate', 'worst', 
                      'horrible', 'poor', 'sad', 'angry', 'disappointing'}
    
    words = set(text.lower().split())
    
    positive_count = len(words & positive_words)
    negative_count = len(words & negative_words)
    total = positive_count + negative_count
    
    if total == 0:
        return 0
    
    return (positive_count - negative_count) / total


def text_summary_extract(text: str, num_sentences: int = 3) -> str:
    """
    Extract summary sentences (simple extractive summarization)
    
    Args:
        text: Input text
        num_sentences: Number of sentences to extract
        
    Returns:
        Summary text
        
    Example:
        >>> text = "First sentence. Second sentence. Third sentence."
        >>> len(text_summary_extract(text, 2).split('.'))
        3
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= num_sentences:
        return text
    
    # Score sentences by word frequency
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(words)
    
    sentence_scores = []
    for sentence in sentences:
        words_in_sentence = re.findall(r'\b\w+\b', sentence.lower())
        score = sum(word_freq[w] for w in words_in_sentence)
        sentence_scores.append((sentence, score))
    
    # Select top sentences
    top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:num_sentences]
    
    # Return in original order
    result = []
    for sentence in sentences:
        if any(sentence == s[0] for s in top_sentences):
            result.append(sentence)
        if len(result) == num_sentences:
            break
    
    return '. '.join(result) + '.'


def keyword_extraction(text: str, n: int = 5) -> List[str]:
    """
    Extract keywords from text
    
    Args:
        text: Input text
        n: Number of keywords
        
    Returns:
        List of keywords
        
    Example:
        >>> keywords = keyword_extraction("python is great python coding")
        >>> 'python' in keywords
        True
    """
    # Remove stopwords
    text_clean = remove_stopwords(text)
    
    # Get word frequency
    freq = word_frequency(text_clean)
    
    # Return top n
    return [word for word, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]]


def acronym_detection(text: str) -> List[str]:
    """
    Detect acronyms in text (all caps words)
    
    Args:
        text: Input text
        
    Returns:
        List of acronyms
        
    Example:
        >>> acronym_detection("NASA and FBI are agencies")
        ['NASA', 'FBI']
    """
    return re.findall(r'\b[A-Z]{2,}\b', text)


def camel_case_split(text: str) -> List[str]:
    """
    Split camelCase text into words
    
    Args:
        text: camelCase text
        
    Returns:
        List of words
        
    Example:
        >>> camel_case_split("helloWorldExample")
        ['hello', 'World', 'Example']
    """
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+', text)


def capitalize_sentences(text: str) -> str:
    """
    Capitalize first letter of each sentence
    
    Args:
        text: Input text
        
    Returns:
        Capitalized text
        
    Example:
        >>> capitalize_sentences("hello. world.")
        'Hello. World.'
    """
    sentences = re.split(r'([.!?]\s+)', text)
    result = []
    
    for i, part in enumerate(sentences):
        if i % 2 == 0 and part:  # Sentence part, not delimiter
            result.append(part[0].upper() + part[1:] if part else '')
        else:
            result.append(part)
    
    return ''.join(result)


# Export all functions
__all__ = [
    'word_frequency', 'most_common_words', 'character_frequency',
    'remove_stopwords', 'ngrams', 'sentence_count', 'average_word_length',
    'lexical_diversity', 'flesch_reading_ease', 'count_syllables',
    'tf_idf', 'cosine_similarity_text', 'jaccard_similarity_text',
    'levenshtein_distance', 'hamming_distance',
    'extract_emails', 'extract_urls', 'extract_phone_numbers',
    'extract_hashtags', 'extract_mentions',
    'sentiment_score_simple', 'text_summary_extract', 'keyword_extraction',
    'acronym_detection', 'camel_case_split', 'capitalize_sentences',
]
