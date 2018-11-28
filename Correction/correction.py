# from correction_lib import Find_Possible_Candidates
import difflib
# print(Reverse_Dic)
#
# print(Find_Possible_Candidates("attened"))

# def fname(arg):
#     pass

a = "continues"
b = "continues"


def find_sub_rev_letters(ground_truth_word, tesseract_word):

    SequenceList = difflib.SequenceMatcher(None, ground_truth_word, tesseract_word).get_opcodes()

    pre_letter = ""

    changed_letter = ""

    tag = ""

    if len(SequenceList) == 3 or len(SequenceList) == 2:
        tag = "sub"
        for tag, a1, a2, b1, b2 in SequenceList:
            if tag == 'replace':
                pre_letter = ground_truth_word[a1]
                changed_letter = tesseract_word[a1]
    else:

        Differ_Index = [index for index in range(len(ground_truth_word)) if ground_truth_word[index] != tesseract_word[index]]
        ground_truth_pre_letter = ground_truth_word[Differ_Index[0]]
        tesseract_pre_letter = tesseract_word[Differ_Index[0]]
        ground_truth_pos_letter = ground_truth_word[Differ_Index[1]]
        tesseract_pos_letter = tesseract_word[Differ_Index[1]]

        if len(Differ_Index) == 2 and ground_truth_pre_letter == tesseract_pos_letter and ground_truth_pos_letter == tesseract_pre_letter:
            tag = "rev"
            pre_letter = ground_truth_word[Differ_Index[0]]
            changed_letter = tesseract_word[Differ_Index[0]]

    return({"tag": tag, "pre_letter" : pre_letter, "changed_letter": changed_letter})


print(find_sub_rev_letters(a,b))
