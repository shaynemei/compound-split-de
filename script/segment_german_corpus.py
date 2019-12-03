import re
import sys
import os
import collections

def in_vocab(split1, split2, split3):
    if (split1 in count_data) and (split2 in count_data) and (split3 in count_data):
        return True
    else:
        return False

def morph_seg(word, exception_list, vocab):
    splits_1 = [[word]]
    
    # Find 2-morpheme splits
    splits_2 = []
    freedom_2 = len(word) - 4
    for i in range(freedom_2 + 1):
        first_split = word[:2+i]
        second_split = word[2+i:]
        if (first_split in vocab) and (second_split in vocab):
            splits_2.append([first_split, second_split])

        # Check for connectors from exception_list and generate new splits
        if len(first_split) == 3:
            if (first_split[-1] in exception_list) and (first_split[-1] in vocab):
                splits_2.append([first_split[:-1], second_split])
        elif len(first_split) > 3:
            if (first_split[-1] in exception_list) and (first_split[-1] in vocab):
                splits_2.append([first_split[:-1], second_split])
            if (first_split[-2] in exception_list) and (first_split[-2] in vocab):
                splits_2.append([first_split[:-2], second_split])
                
    # Find 3-morpheme splits
    splits_3 = []
    freedom_3 = freedom_2 - 2
    for i in range(freedom_3 + 1):
        for j in range(i+1):
            first_split = word[:2+freedom_3-i]
            second_split = word[2+freedom_3-i:2+freedom_3-i+i+2-j]
            third_split = word[2+freedom_3-i+i+2-j:]
            
            if in_vocab(first_split, second_split, third_split):
                splits_3.append([first_split, second_split, third_split])
    
            # Check for connectors from exception_list and generate new splits
            # Also check for connectors between second and third morpheme
            if len(first_split) < 3: 
                if len(second_split) == 3:
                    if second_split[-1] in exception_list:
                        if in_vocab(first_split, second_split[:-1], third_split):
                            splits_3.append([first_split, second_split[:-1], third_split])
                elif len(second_split) > 3:
                    if second_split[-1] in exception_list:
                        if in_vocab(first_split, second_split[:-1], third_split):
                            splits_3.append([first_split, second_split[:-1], third_split])
                        if second_split[-2:] in exception_list:
                            if in_vocab(first_split, second_split[:-2], third_split):
                                splits_3.append([first_split, second_split[:-2], third_split])
            elif len(first_split) == 3:
                if first_split[-1] in exception_list:
                    if in_vocab(first_split[:-1], second_split, third_split):
                        splits_3.append([first_split[:-1], second_split, third_split])
                    if len(second_split) == 3:
                        if second_split[-1] in exception_list:
                            if in_vocab(first_split[:-1], second_split[:-1], third_split):
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                            if in_vocab(first_split, second_split[:-1], third_split):
                                splits_3.append([first_split, second_split[:-1], third_split])
                    elif len(second_split) > 3:
                        if second_split[-1] in exception_list:
                            if in_vocab(first_split[:-1], second_split[:-1], third_split):
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                            if in_vocab(first_split, second_split[:-1], third_split):
                                splits_3.append([first_split, second_split[:-1], third_split])
                            if second_split[-2:] in exception_list:
                                if in_vocab(first_split[:-1], second_split[:-2], third_split):
                                    splits_3.append([first_split[:-1], second_split[:-2], third_split])
                                if in_vocab(first_split, second_split[:-2], third_split):
                                    splits_3.append([first_split, second_split[:-2], third_split])
                elif len(second_split) == 3:
                    if second_split[-1] in exception_list:
                        if in_vocab(first_split, second_split[:-1], third_split):
                            splits_3.append([first_split, second_split[:-1], third_split])
                elif len(second_split) > 3:
                    if second_split[-1] in exception_list:
                        if in_vocab(first_split, second_split[:-1], third_split):
                            splits_3.append([first_split, second_split[:-1], third_split])
                        if second_split[-2:] in exception_list:
                            if in_vocab(first_split, second_split[:-2], third_split):
                                splits_3.append([first_split, second_split[:-2], third_split])

            elif len(first_split) > 3:
                if first_split[-1] in exception_list:
                    if in_vocab(first_split[:-1], second_split, third_split):
                        splits_3.append([first_split[:-1], second_split, third_split])
                    if len(second_split) == 3:
                        if second_split[-1] in exception_list:
                            if in_vocab(first_split[:-1], second_split[:-1], third_split):
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                            if in_vocab(first_split, second_split[:-1], third_split):
                                splits_3.append([first_split, second_split[:-1], third_split])
                    elif len(second_split) > 3:
                        if second_split[-1] in exception_list:
                            if in_vocab(first_split[:-1], second_split[:-1], third_split):
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                            if in_vocab(first_split, second_split[:-1], third_split):
                                splits_3.append([first_split, second_split[:-1], third_split])
                            if second_split[-2:] in exception_list:
                                if in_vocab(first_split[:-1], second_split[:-2], third_split):
                                    splits_3.append([first_split[:-1], second_split[:-2], third_split])
                                if in_vocab(first_split, second_split[:-2], third_split):
                                    splits_3.append([first_split, second_split[:-2], third_split])

                    if first_split[-2:] in exception_list:
                        if in_vocab(first_split[:-2], second_split, third_split):
                            splits_3.append([first_split[:-2], second_split, third_split])
                        if len(second_split) == 3:
                            if second_split[-1] in exception_list:
                                if in_vocab(first_split[:-2], second_split[:-1], third_split):
                                    splits_3.append([first_split[:-2], second_split[:-1], third_split])
                                if in_vocab(first_split, second_split[:-1], third_split):
                                    splits_3.append([first_split, second_split[:-1], third_split])
                        elif len(second_split) > 3:
                            if second_split[-1] in exception_list:
                                if in_vocab(first_split[:-2], second_split[:-1], third_split):
                                    splits_3.append([first_split[:-2], second_split[:-1], third_split])
                                if in_vocab(first_split, second_split[:-1], third_split):
                                    splits_3.append([first_split, second_split[:-1], third_split])
                                if second_split[-2:] in exception_list:
                                    if in_vocab(first_split[:-2], second_split[:-2], third_split):
                                        splits_3.append([first_split[:-2], second_split[:-2], third_split])
                                    if in_vocab(first_split, second_split[:-2], third_split):
                                        splits_3.append([first_split, second_split[:-2], third_split])
                elif len(second_split) == 3:
                    if second_split[-1] in exception_list:
                        if in_vocab(first_split, second_split[:-1], third_split):
                            splits_3.append([first_split, second_split[:-1], third_split])
                elif len(second_split) > 3:
                    if second_split[-1] in exception_list:
                        if in_vocab(first_split, second_split[:-1], third_split):
                            splits_3.append([first_split, second_split[:-1], third_split])
                        if second_split[-2:] in exception_list:
                            if in_vocab(first_split, second_split[:-2], third_split):
                                splits_3.append([first_split, second_split[:-2], third_split])
        splits_2.extend(splits_3)
        splits_1.extend(splits_2)

    return splits_1

def save_to_temp_file(text, temp_file_name):
    cleanup_temp_file(temp_file_name)
    f = open(temp_file_name, 'w')
    f.write(text)
    f.close()

def cleanup_temp_file(temp_file_name):
    try:
        os.remove(temp_file_name)
    except OSError:
        pass  

def find_best_seg(word, exception_list, count_data):
    
    splits = morph_seg(word, exception_list, count_data)
    
    max_score = 0
    best = ""
    
    for j, morph_pairs in enumerate(splits):
        product = 1
        morph_pair_str = ""
        for k, morph in enumerate(morph_pairs):
            freq = count_data[morph]
            product *= freq
            morph_pair_str += morph + " "
        score = round(product**(1/(k+1)), 1)
        if score > max_score:
            max_score = score
            best = morph_pair_str.strip()
        
    return best

def segment_corpus(path, count_data, exception_list):

    SPACE = ' '
    NEWLINE = '\n'
    cache = {}
    with open(path, 'r') as f:
        for line in f:
            tokens = []
            for tok in line.split():
                if tok in cache:
                    tok = cache[tok]
                elif len(tok) > 3:
                    cache[tok] = find_best_seg(tok, exception_list, count_data)
                    tok = cache[tok]
                tokens.append(tok)
            sys.stdout.write(SPACE.join(tokens) + NEWLINE)

if __name__ == "__main__":
    exception_list = ['n', 'en', 's', 'es', 'e', '-']
    temp_file_name = os.getcwd() + '/__temp__.txt'
    data = sys.stdin.read()
    save_to_temp_file(data, temp_file_name)
    data = data.replace("\n"," ").split()
    count_data = collections.Counter(data)
    data = None
    
    segment_corpus(temp_file_name, count_data, exception_list)
    cleanup_temp_file(temp_file_name)


