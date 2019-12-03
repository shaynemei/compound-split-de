import sys
import re
import collections
import pickle

def main():
    data = sys.stdin.readlines()
    data = [(data[i].split(), data[i+1]) for i in range(1, len(data), 3)]
    result = []
    word_list = []
    for sent_pair in data:
        found = re.findall("(\w+) \(\{ ((?:\d )+)\}\)",sent_pair[1])
        for item in found:
            word_de = item[0] + " "
            try:
                indices = [int(idx)-1 for idx in item[1].split()]
                word_list.append(item[0])
            except:
                result.append(item[0])
                continue
            for i, idx in enumerate(indices):
                if (i==len(indices)-1):
                    word_de += sent_pair[0][idx]
                elif (idx != indices[i+1]-1):
                    word_de += sent_pair[0][idx] + " ... "
                else:
                    word_de += sent_pair[0][idx] + " "
            result.append(word_de)
            
    counts = collections.Counter(result)
    count_word = collections.Counter(word_list)

    final = {}
    for entry in counts:
        find = re.search("\w+", entry)
        word = find.group(0)
        translation = entry[find.end(0)+1:]
        freq_word = count_word[word]
        freq_translation = counts[entry]
        freq = freq_translation / freq_word
        if freq < 0.01:
            continue
        else:
            if word in final:
                final[word][translation] = freq_translation / freq_word
            else:
                final[word] = {translation: freq_translation / freq_word}

    for word in final:
        print(word, end='\t')
        for i, translation in enumerate(final[word]):
            if(i==0):
                print(translation + " " + "(" + str(final[word][translation]) + ")", end='')
            else:
                print("||| " + translation + " " + "(" + str(final[word][translation]) + ")", end='')
        print()


    with open("freq_dict", "wb") as f:
        pickle.dump(final,f)


if __name__ == "__main__":
	main()