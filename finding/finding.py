from dataclasses import dataclass
import json
from Levenshtein import distance


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


def get_best_k_completions(prefix: str) -> list:
    results_lst = []
    f = True

    with open('sample.json') as jsonData:
        dataBase = json.load(jsonData)
    local_prefix = prefix[0] + prefix[1]
    for result in dataBase[local_prefix]:
        f2 = True
        replace = 0
        differ = 0
        j = len(prefix) - 1
        if result == "":
            continue
        if result[2].find(prefix) != -1:
            for it in results_lst:
                if it[0].completed_sentence == result[2]:
                    f = False
        else:
            i = result[0]
            j = 0

            while j < len(prefix) - 1 and i < len(result[2]) - 1 and f2: # and i - result[0] < len(prefix):
                if result[2][i] != prefix[j]:
                    if differ != 0 or replace != 0:
                        f2 = False
                        break

                    if result[2][i + 1] == prefix[j]: # check less letter from line
                        i += 1
                        differ = j
                    elif result[2][i + 1] == prefix[j + 1]: #check replacement of one letter prefix and line
                        j += 1
                        i += 1
                        replace = j
                    elif result[2][i] == prefix[j + 1]: # check more letter from line
                        j += 1
                        differ = j
                    else:
                        f2 = False
                i += 1
                j += 1

        if f and f2 and j == len(prefix) - 1:
            score = len(prefix) * 2 - 2
            results_lst.append([AutoCompleteData(result[2], result[1], result[0], score), score])
            if len(results_lst) > 5:
                results_lst.remove(min(results_lst, key=lambda x: x[1]))
        f = True
    return results_lst


def print_top_5(results_list):
    for result in results_list:
        print(result[0].completed_sentence + "( " + str(result[0].offset) + " " + result[0].source_text + " )")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_top_5(get_best_k_completions("chaer"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
