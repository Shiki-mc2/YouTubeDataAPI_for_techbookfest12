import sys
import re
import random
import warnings
warnings.simplefilter('ignore', FutureWarning)

from wordcloud import WordCloud
import MeCab
import treetaggerwrapper as ttw

def get_word_str_jp(text):
    mecab = MeCab.Tagger("-d C:\MeCab\dic\ipadic-neologd")
    token = mecab.parse(text)
    
    word_list = []
    for line in token.split("\n"):
        tag = re.split('\t|,', str(line))
        if (len(tag) > 2 and
            tag[1] in ["名詞"] and
            tag[2] in ["一般", "固有名詞"] and
            not re.search(r"[a-zA-Z']", tag[0])):
                word_list.append(tag[0])
                
    return " A " . join(word_list)

def get_word_str_eng(text):
    tags_tabseparated = ttw.TreeTagger(TAGLANG='en').tag_text(text)
    tags_tuple = ttw.make_tags(tags_tabseparated)

    word_list = []
    for tag in tags_tuple:
        if (len(tag) == 3 and
            tag[1] in ["NN","NNS","NP","NPS"] and
            not re.search(r"[^a-zA-Z']", tag[0]) and
            len(tag[0]) > 1):
            word_list.append(tag[0])
            
    return " A " . join(word_list)

def plot_word_Cloud(fname, word_str):
    font_path = "C:/WINDOWS/Fonts/BIZ-UDGOTHICR.TTC"
    
    wordcloud = WordCloud(colormap='Dark2',
                          background_color='white',
                          prefer_horizontal=1.0,
                          font_path=font_path,
                          random_state = random,
                          width=800,height=600).generate(word_str)
    wordcloud.to_file(fname)

def main():
    if len(sys.argv) == 1:
        return
    
    fname = sys.argv[1]
    seed = None
    
    if len(sys.argv) > 2:
        seed = int(sys.argv[2])
    random.seed(seed)
    
    with open(fname, "r", encoding="utf-8") as r:
        text = r.read()
        
        word_str_jp  = get_word_str_jp(text)
        word_str_eng = get_word_str_eng(text)
        
        wname = fname[:fname.rfind(".")]
        plot_word_Cloud(wname + "_jp.png", word_str_jp)
        plot_word_Cloud(wname + "_eng.png", word_str_eng)
        plot_word_Cloud(wname + "_jp_and_eng.png", word_str_jp + " " + word_str_eng)

if __name__ == "__main__":
    main()
