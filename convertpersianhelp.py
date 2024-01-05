import arabic_reshaper
from bidi.algorithm import get_display

def convert(text):
    reshaped_text = arabic_reshaper.reshape(text)
    converted = get_display(reshaped_text)
    return converted


# pip install arabic-reshaper
# pip install python-bidi