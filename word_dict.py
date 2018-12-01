from correction_lib import All_Ground_Truth_Words, Ground_Truth_Words, File_Names, Ground_Truth_Path, Tesseract_Path
from correction_lib import clean_word, clean_word2, Delete_Non_Letter
import sys

def abc():
    pass

def Create_Words_Dictionary():
    Ground_Truth_Word_Dict = dict()

    Total_Files = len(File_Names)

    Searched_File = 0

    Progress_Bar_Length = 30

    for FileName in File_Names:
        File_Dir = Ground_Truth_Path + FileName + ".txt"
        with open(File_Dir, 'r') as file:
            Ground_Truth_file_Content = file.read()

            uncleaned_word = Ground_Truth_file_Content.split()
            # print(uncleaned_word)
            cleaned_word = list(map(clean_word,uncleaned_word))
            cleaned_word = list(filter(clean_word2, cleaned_word))
            # print(cleaned_word)
            while "" in cleaned_word:
                cleaned_word.remove("")

            for index in range(len(cleaned_word)):
                current_word = cleaned_word[index]
                if current_word not in Ground_Truth_Word_Dict:
                    Ground_Truth_Word_Dict[current_word] = dict()
                    Ground_Truth_Word_Dict[current_word]["left"] = dict()
                    Ground_Truth_Word_Dict[current_word]["right"] = dict()

                if index-1 >= 0 and index + 1 < len(cleaned_word):
                    left_index = index-1
                    right_index = index+1
                    left_word = cleaned_word[left_index]
                    right_word = cleaned_word[right_index]
                    if left_word not in Ground_Truth_Word_Dict[current_word]["left"]:
                        Ground_Truth_Word_Dict[current_word]["left"][left_word] = 0
                    if right_word not in Ground_Truth_Word_Dict[current_word]["right"]:
                        Ground_Truth_Word_Dict[current_word]["right"][right_word] = 0

                    Ground_Truth_Word_Dict[current_word]["left"][left_word] += 1
                    Ground_Truth_Word_Dict[current_word]["right"][right_word] += 1


                elif index-1 >= 0 and index + 1 >= len(cleaned_word):
                    left_index = index-1
                    left_word = cleaned_word[left_index]
                    if left_word not in Ground_Truth_Word_Dict[current_word]["left"]:
                        Ground_Truth_Word_Dict[current_word]["left"][left_word] = 0
                    Ground_Truth_Word_Dict[current_word]["left"][left_word] += 1

                elif index-1 < 0 and index + 1 < len(cleaned_word):
                    right_index = index+1
                    right_word = cleaned_word[right_index]
                    if right_word not in Ground_Truth_Word_Dict[current_word]["right"]:
                        Ground_Truth_Word_Dict[current_word]["right"][right_word] = 0
                    Ground_Truth_Word_Dict[current_word]["right"][right_word] += 1

    return(Ground_Truth_Word_Dict)


def Create_Word_Pair():

    Word_Pair = list()

    Word_Dict = dict()

    for FileName in File_Names:
        Word_Dict[FileName] = dict()
        Ground_Truth_File_Dir = Ground_Truth_Path + FileName + ".txt"
        Tesseract_File_Dir = Tesseract_Path + FileName + ".txt"
        with open(Ground_Truth_File_Dir, 'r') as file:
            Ground_Truth_file_Content = file.readlines()
            Word_Dict[FileName]["ground_truth"] = Ground_Truth_file_Content

        with open(Tesseract_File_Dir, 'r') as file:
            Tesseract_file_Content = file.readlines()
            Word_Dict[FileName]["tesseract"] = Tesseract_file_Content

    for Each_File in Word_Dict:
        Ground_Truth = Word_Dict[Each_File]["ground_truth"]
        Tesseract = Word_Dict[Each_File]["tesseract"]
        for Line_Index in range(min(len(Ground_Truth), len(Tesseract))):
            # remove \n and \r
            Ground_Truth_Line = Ground_Truth[Line_Index].rstrip()
            Tesseract_Line = Tesseract[Line_Index].rstrip()
            # next we need to split the lines by spaces
            Ground_Truth_Line_Words = Delete_Non_Letter(Ground_Truth_Line.split())
            Tesseract_Line_Words = Delete_Non_Letter(Tesseract_Line.split())
            Min_Length = min(len(Ground_Truth_Line_Words), len(Tesseract_Line_Words))
            for word_index in range(Min_Length):
                # first remove all non alphabet letter including ; , . / 0-9
                Ground_Truth_Line_Word = clean_word(Ground_Truth_Line_Words[word_index])
                Tesseract_Line_Word = clean_word(Tesseract_Line_Words[word_index])
                if Ground_Truth_Line_Word != Tesseract_Line_Word and max(len(Ground_Truth_Line_Word), len(Tesseract_Line_Word))-min(len(Ground_Truth_Line_Word), len(Tesseract_Line_Word)) <= 1:
                    Word_Pair.append((Ground_Truth_Line_Word, Tesseract_Line_Word))
    return(Word_Pair)

#
# Total_Words = len(Ground_Truth_Words)
#
# Searched_Word = 0
#
# for word in Ground_Truth_Words:
#
#     Progress_Bar_Length = 30
#
#     if word not in Ground_Truth_Word_Dict:
#         Ground_Truth_Word_Dict[word] = dict()
#         Ground_Truth_Word_Dict[word]["left"] = dict()
#         Ground_Truth_Word_Dict[word]["right"] = dict()
#     for FileName in File_Names:
#         File_Dir = Ground_Truth_Path + FileName + ".txt"
#         with open(File_Dir, 'r') as file:
#             Ground_Truth_file_Content = file.read()
#
#             uncleaned_word = Ground_Truth_file_Content.split()
#             # print(uncleaned_word)
#             cleaned_word = list(map(clean_word,uncleaned_word))
#             cleaned_word = list(map(clean_word2, cleaned_word))
#             while "" in cleaned_word:
#                 cleaned_word.remove("")
#             word_match_index = [index for index in range(len(cleaned_word)) if cleaned_word[index] == word]
#             if len(word_match_index) >= 1:
#                 for index in word_match_index:
#                     if index-1 >= 0 and index + 1 < len(cleaned_word):
#                         left_index = index-1
#                         right_index = index+1
#                         left_word = cleaned_word[left_index]
#                         right_word = cleaned_word[right_index]
#                         if left_word not in Ground_Truth_Word_Dict[word]["left"]:
#                             Ground_Truth_Word_Dict[word]["left"][left_word] = 0
#                         if right_word not in Ground_Truth_Word_Dict[word]["right"]:
#                             Ground_Truth_Word_Dict[word]["right"][right_word] = 0
#
#                         Ground_Truth_Word_Dict[word]["left"][left_word] += 1
#                         Ground_Truth_Word_Dict[word]["right"][right_word] += 1
#
#                     elif index-1 >= 0 and index + 1 >= len(cleaned_word):
#                         left_index = index-1
#                         left_word = cleaned_word[left_index]
#                         if left_word not in Ground_Truth_Word_Dict[word]["left"]:
#                             Ground_Truth_Word_Dict[word]["left"][left_word] = 0
#                         Ground_Truth_Word_Dict[word]["left"][left_word] += 1
#
#                     elif index-1 < 0 and index + 1 < len(cleaned_word):
#                         right_index = index+1
#                         right_word = cleaned_word[right_index]
#                         if right_word not in Ground_Truth_Word_Dict[word]["right"]:
#                             Ground_Truth_Word_Dict[word]["right"][right_word] = 0
#                         Ground_Truth_Word_Dict[word]["right"][right_word] += 1
#
#     Searched_Word = Searched_Word + 1
#     Bar_Searched = '.' * int(Searched_Word*Progress_Bar_Length/Total_Words)
#     Bar_unsearched = ' ' * (Progress_Bar_Length-int(Searched_Word*Progress_Bar_Length/Total_Words))
#     Bar = Bar_Searched + Bar_unsearched
#     sys.stdout.write('[{}] \033[92m{}% {}Words\033[0m\r'.format(Bar ,round(100.0*Searched_Word/ float(Total_Words),1), Searched_Word))
#     sys.stdout.flush()
#
