import os
import traceback

# ___ LOAD ALL WORDS
word_file = open("words.txt", "r")
words = word_file.readlines()

# ___ LOAD THE FREQUENCY LIST
frequeny_dict = {}
def load_frequencies(file_name="freq.csv"):
    with open(file_name, "r") as f:
        all_lines = f.readlines()
    for line in all_lines:
        line = line.lower().strip("\n").strip(" ")
        if "," in line:
            try:
                word_freq = line.split(",")
                frequeny_dict[word_freq[0]] = int(word_freq[1])
                #print(line, word_freq, "\n")
            except:
                #print(line)
                pass
        else:
            pass    
        
# ___ MERGE SORT
def frequency_comparator(a, b):
    word_a_frequency = a[1]
    word_b_frequency = b[1]
    
    if word_a_frequency >= word_b_frequency:
        return a
    else:
        return b

def merge_sort(lst, comparator=min):

    if len(lst) == 1:
        return lst
        
    mid_way = len(lst) // 2
    a = lst[:mid_way]
    b = lst[mid_way:]
    
    a_sorted = merge_sort(a, comparator)
    b_sorted = merge_sort(b, comparator)
    
    merge_sorted = merger(a_sorted, b_sorted, comparator)
    
    return merge_sorted
    
def merger(a, b, comparator):
    sorted_ = []
    
    while a and b:
        element_1 = a[0]
        element_2 = b[0]
        
        result = comparator(element_1, element_2)
        sorted_.append(result)
        if result == element_1:
            del a[0]
        else:
            del b[0]
    
    while a:
        sorted_.append(a[0])
        del a[0]
        
    while b:
        sorted_.append(b[0])
        del b[0]
        
    return sorted_
    
# ___ FILTER UNNECESSARY WORDS
digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
def has_digit(word):
    for character in word:
        if character in digits:
            return True
    return False    
    
def filterer(word):
    if "." in word:
        return False
    
    if "-" in word:
        return False
        
    if has_digit(word):
        return False
        
    return True
    
filtered_wordlist = list(filter(filterer, words))

# ___ MAP WORDS TO A NEW DICTIONARY
def change_words(word):
    word = word.strip("\n").strip(" ")
    word = word.lower()
    return word
    
new_wordlist = list(map(change_words, filtered_wordlist))

# __ CREATE RULES
def contains_all_letters(word, letters=[]):
    for c in letters:
        if c not in word:
            return False
    return True

def doesnt_contain(word, excluded_letters=[]):
    for c in excluded_letters:
        if c in word:
            return False
    return True

def matches_position(word, position_hints=[]):
    for c in position_hints:
        letter = c[0]
        index = c[1]
        if word[index] != letter:
            return False
    return True

def cancel_position(word, cancel_letters=[]):
    for c in cancel_letters:
        letter = c[0]
        index = c[1]
        if word[index] == letter:
            return False
    return True

def find_words(min_length, max_length, letter_hints=[], positional_hints=[], positional_cancels=[], excluded_letters=[]):
    possible_words = []
    for word in new_wordlist:
        if len(word) >= min_length and len(word) <= max_length:
            if contains_all_letters(word, letter_hints):
                if matches_position(word, positional_hints):
                    if cancel_position(word, positional_cancels):
                        if doesnt_contain(word, excluded_letters):
                            possible_words.append(word)
                    
    return possible_words

# ___ FIND FREQUENCY OF EACH WORD
def sort_by_frequency(wordlist):
    word_frequency_list = []
    for word in wordlist:
        try:
            frequency = frequeny_dict[word]
            word_frequency_list.append((word, frequency))
        except KeyError:
            word_frequency_list.append((word, 0))
    
    sorted_list = merge_sort(word_frequency_list, frequency_comparator)
    return sorted_list


# __ UI
def ask_input(prompt, ask_list=False, delimeter=",", ask_bool=False, ask_number=False, reject_empty=True, min_=None, max_=None, add_newline=False):
    while True:
        inp = input(prompt + ">>> ")
        if reject_empty and len(inp) == 0:
            print("Cannot accept empty values. Please input something. \n")
            continue
        if ask_list:
            if delimeter in inp:
                return inp.split(delimeter)
            else:
                return [inp]
        if ask_bool:
            if "y" in inp.lower() or "t" in inp.lower():
                return True
            else:
                return False
        if ask_number:
            try:
                n = int(inp)
                if min_ and n < min_:
                    raise ValueError
                if max_ and n > max_:
                    raise ValueError
                return n
            except ValueError:
                print(inp + " is not a valid input. Please try again. \n") 
                continue
        
        if add_newline:
            print("\n")
        
        return inp
def gather_info():
    # __ LENGTH OF THE WORD
    length = ask_input("Please input the length of the word you're looking for", ask_number=True, min_=1, add_newline=True)
    
    # ___ LETTERS IN THE WORD
    confirmation = ask_input("Do you know some letters in the word? (y/n)", ask_bool=True, add_newline=True)
    letter_hints_ = []
    if confirmation:
        letter_hints_ = ask_input("Type the letters (separate them using comma ',') eg. a, b, c", ask_list=True, add_newline=True)
    
    # ___ POSITION OF THE LETTERS    
    confirmation = ask_input("Do you know the position of some letters? (y/n)", ask_bool=True, add_newline=True)
    positions = []
    if confirmation:
        print("\n")
        print("""  
            Type the letter and position of letter, separated by comma, one by one, pressing enter
            eg. a,3
                b, 7
            Type "end" when you're done.
            """)
        while True:
            try:
                inp = ask_input("")
                print(inp)
                if inp == "end":
                    break
                if "," in inp:
                    word_pos = inp.split(",")
                    positions.append((word_pos[0], int(word_pos[1])))
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input: ", inp, ". Type correctly or press end.\n")               
    
    
    # ___ POSITION OF THE CANCEL POINTS
    cancel_points = []
    confirmation = ask_input("Do you know some letters that dont belong to a position? (y/n)", ask_bool=True, add_newline=True)
    if confirmation:
        print("\n")
        print("""  
            Type the letter and position of letter where it does not belong, separated by comma, one by one, pressing enter
            eg. a,3
                b, 7
            Type "end" when you're done.
            """)
        while True:
            try:
                inp = ask_input("")
                if inp == "end":
                    break
                if "," in inp:
                    word_pos = inp.split(",")
                    cancel_points.append((word_pos[0], int(word_pos[1])))
                else:
                    raise ValueError
            except ValueError:
                print("Invalid input: ", inp, ". Type correctly or press end.\n")
    
    # ___ EXCLUDED LETTERS
    excluded_letters_ = []
    confirmation = ask_input("Do you know some letters that ARE NOT in the word? (y/n)", ask_bool=True)
    if confirmation:
        excluded_letters = ask_input("Type the letters (separate them using comma ',') eg. a, b, c", ask_list=True)
    
    return length, letter_hints_, positions, cancel_points, excluded_letters
    
def main():
    load_frequencies()
    l, h, p, c, e = gather_info()
    possible_words = find_words(l, l, h, p, c, e)
    sorted_by_frequency = sort_by_frequency(possible_words)
    count = 1
    o_file = open("out.txt", "wb")
    for tuple_ in sorted_by_frequency:
        out = str(count) + ". " + str(tuple_[0])
        o_file.write((out+"\n").encode())
        count += 1
    o_file.close()
    print("\n\n\tThe answers have been saved to file out.txt. ENJOY.")
        
main()
