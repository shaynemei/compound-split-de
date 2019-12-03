# Find possible segmentations using a translation lexicon table from euparl de-en giza result

import re
import sys
import collections
import pickle

# Find all possible morphological segmentation pairs of up to three morphemes per word
# Morphemes are at least 2 chars
def morph_seg(words, exception_list):
    splits = []
    for word in words:
        splits_1 = [[word]]
        
        # Find 2-morpheme splits
        splits_2 = []
        freedom_2 = len(word) - 4
        for i in range(freedom_2 + 1):
            first_split = word[:2+i]
            second_split = word[2+i:]
            splits_2.append([first_split, second_split])

            # Check for connectors from exception_list and generate new splits
            if len(first_split) == 3:
                if first_split[-1] in exception_list:
                    splits_2.append([first_split[:-1], second_split])
            elif len(first_split) > 3:
                if first_split[-1] in exception_list:
                    splits_2.append([first_split[:-1], second_split])
                if first_split[-2:] in exception_list:
                    splits_2.append([first_split[:-2], second_split])
                    
        # Find 3-morpheme splits
        splits_3 = []
        freedom_3 = freedom_2 - 2
        for i in range(freedom_3 + 1):
            for j in range(i+1):
                first_split = word[:2+freedom_3-i]
                second_split = word[2+freedom_3-i:2+freedom_3-i+i+2-j]
                third_split = word[2+freedom_3-i+i+2-j:]
    
                splits_3.append([first_split, second_split, third_split])
        
                # Check for connectors from exception_list and generate new splits
                # Also check for connectors between second and third morpheme
                if len(first_split) < 3: 
                    if len(second_split) == 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                    elif len(second_split) > 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                            if second_split[-2:] in exception_list:
                                splits_3.append([first_split, second_split[:-2], third_split])
                elif len(first_split) == 3:
                    if first_split[-1] in exception_list:
                        splits_3.append([first_split[:-1], second_split, third_split])
                        if len(second_split) == 3:
                            if second_split[-1] in exception_list:
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                                splits_3.append([first_split, second_split[:-1], third_split])
                        elif len(second_split) > 3:
                            if second_split[-1] in exception_list:
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                                splits_3.append([first_split, second_split[:-1], third_split])
                                if second_split[-2:] in exception_list:
                                    splits_3.append([first_split[:-1], second_split[:-2], third_split])
                                    splits_3.append([first_split, second_split[:-2], third_split])
                    elif len(second_split) == 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                    elif len(second_split) > 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                            if second_split[-2:] in exception_list:
                                splits_3.append([first_split, second_split[:-2], third_split])

                elif len(first_split) > 3:
                    if first_split[-1] in exception_list:
                        splits_3.append([first_split[:-1], second_split, third_split])
                        if len(second_split) == 3:
                            if second_split[-1] in exception_list:
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                                splits_3.append([first_split, second_split[:-1], third_split])
                        elif len(second_split) > 3:
                            if second_split[-1] in exception_list:
                                splits_3.append([first_split[:-1], second_split[:-1], third_split])
                                splits_3.append([first_split, second_split[:-1], third_split])
                                if second_split[-2:] in exception_list:
                                    splits_3.append([first_split[:-1], second_split[:-2], third_split])
                                    splits_3.append([first_split, second_split[:-2], third_split])

                        if first_split[-2:] in exception_list:
                            splits_3.append([first_split[:-2], second_split, third_split])
                            if len(second_split) == 3:
                                if second_split[-1] in exception_list:
                                    splits_3.append([first_split[:-2], second_split[:-1], third_split])
                                    splits_3.append([first_split, second_split[:-1], third_split])
                            elif len(second_split) > 3:
                                if second_split[-1] in exception_list:
                                    splits_3.append([first_split[:-2], second_split[:-1], third_split])
                                    splits_3.append([first_split, second_split[:-1], third_split])
                                    if second_split[-2:] in exception_list:
                                        splits_3.append([first_split[:-2], second_split[:-2], third_split])
                                        splits_3.append([first_split, second_split[:-2], third_split])
                    elif len(second_split) == 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                    elif len(second_split) > 3:
                        if second_split[-1] in exception_list:
                            splits_3.append([first_split, second_split[:-1], third_split])
                            if second_split[-2:] in exception_list:
                                splits_3.append([first_split, second_split[:-2], third_split])
        splits_2.extend(splits_3)
        splits_1.extend(splits_2)
        splits.append(splits_1)
    return splits

def main():
    exception_list = ['n', 'en', 's', 'es', 'e', '-']
    words = sys.stdin.readlines()
    words = [word.lower().replace("\n","") for word in words]
    splits = morph_seg(words, exception_list)
    with open("freq_dict", "rb") as f:
        freq_dict = pickle.load(f)
    no_translation_pairs = []
    for i, word in enumerate(splits):
        for j, morph_pairs in enumerate(word):
            used_translation = []
            for morph in morph_pairs:
                max_splits = 0
                max_freq = 0
                selected_translation = ""
                if morph not in freq_dict:
                    no_translation_pairs.append((i,j))
                    break
                for translation in freq_dict[morph]:
                    if translation in used_translation:
                        continue
                    num_translation_splits = len(re.findall(" \.{3} | ", translation)) + 1
                    freq_translation = freq_dict[morph][translation]
                    if num_translation_splits > max_splits:
                        max_splits = num_translation_splits
                        max_freq = freq_translation
                        selected_translation = translation
                    if (num_translation_splits == max_splits) and (freq_translation > max_freq):
                        max_freq = freq_translation
                        selected_translation = translation
                if selected_translation == "":
                    no_translation_pairs.append((i,j))
                    break
                used_translation.append(selected_translation)

    for i, word in enumerate(splits):
        for j, morph_pairs in enumerate(word):
            if (i,j) in no_translation_pairs:
                continue
            print(" ".join(morph_pairs) + " = ", end = "")
            for k, morph in enumerate(morph_pairs):
                max_splits = 0
                max_freq = 0
                selected_translation = ""
                for translation in freq_dict[morph]:
                    if translation in used_translation:
                        continue
                    num_translation_splits = len(re.findall(" \.{3} | ", translation)) + 1
                    freq_translation = freq_dict[morph][translation]
                    if num_translation_splits > max_splits:
                        max_splits = num_translation_splits
                        max_freq = freq_translation
                        selected_translation = translation
                    if (num_translation_splits == max_splits) and (freq_translation > max_freq):
                        max_freq = freq_translation
                        selected_translation = translation
                print(morph + " (" + selected_translation + ") ", end = "")
            print()

if __name__ == "__main__":
    main()