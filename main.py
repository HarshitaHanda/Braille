# main.py
import streamlit as st
import re
from symspellpy import SymSpell, Verbosity
import pkg_resources

# Braille-Text Mappings (Unicode Braille characters)
braille_to_text = {
    '⠁': 'a', '⠃': 'b', '⠉': 'c', '⠙': 'd', '⠑': 'e',
    '⠋': 'f', '⠛': 'g', '⠓': 'h', '⠊': 'i', '⠚': 'j',
    '⠅': 'k', '⠇': 'l', '⠍': 'm', '⠝': 'n', '⠕': 'o',
    '⠏': 'p', '⠟': 'q', '⠗': 'r', '⠎': 's', '⠞': 't',
    '⠥': 'u', '⠧': 'v', '⠺': 'w', '⠭': 'x', '⠽': 'y',
    '⠵': 'z', ' ': ' ', '⠀': ' '  # Braille space
}

text_to_braille = {v: k for k, v in braille_to_text.items()}

# Initialize SymSpell for spell correction
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# Auto-Correction Function
def auto_correct_sentence(text):
    words = re.findall(r'\w+|\s+|[^\w\s]', text)
    corrected_words = []
    
    for word in words:
        if word.strip():
            suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
            corrected_word = suggestions[0].term if suggestions else word
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)
    
    return ''.join(corrected_words)

# Conversion Functions
def braille_to_text_conversion(braille_str):
    text = ''.join([braille_to_text.get(c, '?') for c in braille_str])
    return auto_correct_sentence(text)

def text_to_braille_conversion(text_str):
    return ''.join([text_to_braille.get(c.lower(), '?') for c in text_str])

# Streamlit UI
st.title("Braille Converter")

conversion_mode = st.sidebar.radio(
    "Select conversion mode:", 
    ["Text to Braille", "Braille to Text"]
)

input_text = st.text_area("Input Text/Braille", "Enter text or Braille here...")

if conversion_mode == "Text to Braille":
    if st.button("Convert to Braille"):
        output = text_to_braille_conversion(input_text)
        st.text_area("Converted Braille", output)

elif conversion_mode == "Braille to Text":
    if st.button("Convert to Text"):
        output = braille_to_text_conversion(input_text)
        st.text_area("Converted Text", output)

# Styling
st.markdown("""
    <style>
        .stTextArea textarea { background-color: #f0f8ff; }
        .stButton button { width: 100%; transition: all 0.3s ease; }
        .stButton button:hover { transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)
