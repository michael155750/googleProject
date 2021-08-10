from dataclasses import dataclass
import json
from Levenshtein import distance
from operator import itemgetter
CHAR_IGNORE = ('$','!' ,'#', '%', '^', '&', '*', '(',')',',',' ', '.', '/', '\\')

@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


def get_best_k_completions(prefix: str) -> list:
    results_lst = []
    f = True
    prefix = ''.join(e for e in prefix if e.isalnum())
    with open('sample.json') as jsonData:
        dataBase = json.load(jsonData)
    local_prefix = prefix[0] + prefix[1]
    for result in dataBase[local_prefix]:
        f2 = True
        replace = 0
        differ = 0
        j = len(prefix)
        if result == "":
            continue
        string_sentence = ''.join(e for e in result[3] if e.isalnum())
        if string_sentence.find(prefix) != -1:
            for it in results_lst:
                if it[0].completed_sentence == result[3]:
                    f = False
        else:
            i = result[0]
            j = 0
            while j < len(prefix) and i < len(string_sentence) -1 and f2: # and i - result[0] < len(prefix):
                if string_sentence[i] != prefix[j]:
                    if differ != 0 or replace != 0:
                        f2 = False
                        break
                    if string_sentence[i + 1] == prefix[j]: # check less letter from line
                        i += 1
                        differ = j + 1
                    elif j < len(prefix) - 1:
                        if string_sentence[i + 1] == prefix[j + 1]: # check replacement of one letter prefix and line
                            j += 1
                            i += 1
                            replace = j + 1
                        elif string_sentence[i] == prefix[j + 1]: # check more letter from line
                            j += 1
                            differ = j + 1
                        else:
                            f2 = False
                    if j == len(prefix) - 1:
                        if string_sentence[i + 1] != prefix[j]:
                            differ = j + 1
                        j += 1

                else:
                    i += 1
                    j += 1

        for it in results_lst:
            if it[0].completed_sentence == result[3]:
                f = False
        if f and f2 and j == len(prefix):

            score = len(prefix) * 2
            if replace != 0:
                if replace == 1:
                    score -= 5
                elif replace == 2:
                    score -= 4
                elif replace == 3:
                    score -= 3
                elif replace == 4:
                    score -= 2
                else:
                    score -= 1
            if differ != 0:
                if differ == 1:
                    score -= 10
                elif differ == 2:
                    score -= 8
                elif differ == 3:
                    score -= 6
                elif differ == 4:
                    score -= 4
                else:
                    score -= 2

            results_lst.append([AutoCompleteData(result[3], result[2], result[1], score), score])
            if len(results_lst) > 5:
                     results_lst.remove(min(results_lst, key=lambda x: x[1]))

        f = True
    return sorted(results_lst, key=itemgetter(1),reverse=True)


def print_top_5(results_list):
    for result in results_list:
        print(result[0].completed_sentence + "( " + str(result[0].offset) + " " + result[0].source_text + " )")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_top_5(get_best_k_completions("apt"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
