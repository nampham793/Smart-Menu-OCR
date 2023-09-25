import re
from symspellpy import SymSpell, Verbosity

class SpellChecker(object):
    def __init__(self, vovabulary_path:  str, vocabulary_big_gram_path: str=None, edit_distance=3, prefix_length = 7):
        self.spell = SymSpell(
            max_dictionary_edit_distance=edit_distance,
            prefix_length=prefix_length
        )

        self.ed = edit_distance

        self.spell.load_dictionary(
            vovabulary_path, 0, 1, separator="$", encoding='utf-8'
        )

        if vocabulary_big_gram_path:
            self.spell.load_bigram_dictionary(
                vocabulary_big_gram_path, 0, 1, separator = '$', encoding='utf-8'
            )

    def correct_spell(self, text, lookup_only = True, include_unknown = False):
        """
        Input: text
        """
        if not text:
            return text
            
        text =  text.lower()

        if lookup_only:
            suggestion = self.spell.lookup(
                text,
                Verbosity.CLOSEST,
                include_unknown=include_unknown
            )
        else:
            suggestion = self.spell.lookup_compound(
                text,
                max_edit_distance=self.ed,
                ignore_non_words=True,
                ignore_term_with_digits=True
                )
        suggestion_list = []

        if not suggestion:
            return ""

        return suggestion[0]._term

if __name__ == "__main__":
    FOODVOCAB_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/Food Vocab/food_vocabulary_tokenize.txt"
    BIGGRAMS_PATH = "/Users/nampham/OneDrive - Đại học FPT- FPT University/Intern/Menu 1.2/Food Vocab/big_grams.txt" 

    spellcheck = SpellChecker(
        FOODVOCAB_PATH,
        BIGGRAMS_PATH
    )
    print(spellcheck.correct_spell("IẮC"))