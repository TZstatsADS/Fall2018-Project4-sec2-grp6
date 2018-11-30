import os
import string
import difflib
import collections


# Function to get the file end with .txt
def Get_FileNames(path):

    File_Lists = list()

    for ground_truth_file in os.listdir(path):
        if ground_truth_file.endswith(".txt"):
            File_Lists.append(ground_truth_file)

    return(File_Lists)

# Clean the words
def clean_word(w):
    out = []
    for c in w:
        c = c.lower()
        # searching set is faster than list: O(1) vs. O(n=26)
        if c.isalpha():
            out.append(c)
    return ''.join(out)


# Check the length of the words
def clean_word2(w):
    if len(w) < 21 and len(w) >1:
        return True
    else:
        return False

# Get the word with length n
def filter_word(n):
    def filter(word):
        if len(word) == n:
            return True
        else:
            return False
    return(filter)



Ground_Truth_Path = "./data/ground_truth/"

Tesseract_Path = "./data/tesseract/"

Ground_Truth_Files = Get_FileNames(Ground_Truth_Path)

File_Names = [filename[: -4] for filename in Ground_Truth_Files]

Ground_Truth_Words = set()

All_Ground_Truth_Words = list()

for FileName in File_Names:
    File_Dir = Ground_Truth_Path + FileName + ".txt"
    with open(File_Dir, 'r') as file:
        file_Content = file.read()
        uncleaned_word = file_Content.split()
        All_Ground_Truth_Words += list(map(clean_word,uncleaned_word))
        Ground_Truth_Words = Ground_Truth_Words.union(set(map(clean_word,uncleaned_word)))

All_Ground_Truth_Words = list(filter(clean_word2, All_Ground_Truth_Words))

Ground_Truth_Words = set(filter(clean_word2, Ground_Truth_Words))



# Intert the letter into specific position in the string
def Insert_Letter(String, Letter, Position):
    if Position <= 0:
        return(Letter + String)
    elif Position >= (len(String)-1):
        return(String + Letter)
    else:
        return(String[:Position] + Letter + String[Position:])


# Delete the letter from specific position in the string
def Delete_Letter(String, Position):
    if Position < 0 or Position > (len(String)-1):
        return(String)
    else:
        return(String[:Position] + String[Position+1:])

# Substitute the letter from specific position with new letter in the string
def Substitute_Letter(String, Letter, Position):
    if Position < 0 or Position > (len(String)-1) or Letter.isalpha() == False:
        return(String)
    else:
        return(String[:Position] + Letter.lower() + String[Position+1:])

# Reverse the letter between two specific positions in the string
def Reverse_Letter(String, Position1, Position2):
    pre_index = min(Position1, Position2)
    pos_index = max(Position1, Position2)
    if pre_index < 0 or pos_index < 0 or pre_index > (len(String)-1) or pos_index > (len(String)-1) or pre_index == pos_index:
        return(String)
    else:
        return(String[:pre_index] + String[pos_index] + String[pre_index+1:pos_index] + String[pre_index] + String[pos_index+1:])



# function for find the possibile candidates with inertation
def Find_Candidates_Insertion(Typo):
    '''

    '''
    Candidates = list()
    Candidates_Length = len(Typo) - 1
    PossibleWords = set(filter(filter_word(Candidates_Length), Ground_Truth_Words))
    for index in range(len(Typo)):
        for String in PossibleWords:
            Temp_String  = Insert_Letter(String, Typo[index], index)
            if Typo == Temp_String:
                Candidates.append((String, Typo[index], index))
    return(Candidates)



# function for find the possibile candidates with deletion
def Find_Candidates_Deletion(Typo):
    # Next create table dictionary for deletion for each words
    # Each element is (True Word, Position to delete)
    Deletion_Dic = dict()

    for ground_truth_word in Ground_Truth_Words:
        for index in range(len(ground_truth_word)):
            temp_typo = Delete_Letter(ground_truth_word, index)
            if temp_typo in Deletion_Dic:
                Deletion_Dic[temp_typo].append((ground_truth_word, index))
            else:
                Deletion_Dic[temp_typo] = list()
                Deletion_Dic[temp_typo].append((ground_truth_word, index))

    if Typo in Deletion_Dic:
        return(Deletion_Dic[Typo])
    else:
        return([])





# function for find the possibile candidates with Substitution
def Find_Candidates_Substitution(Typo):

    # Next create table dictionary for Substitute for each words
    # Each element is (True Word, First Position, Second Position)
    Substitution_Dic = dict()

    for ground_truth_word in Ground_Truth_Words:
        for index in range(len(ground_truth_word)):
            for substitution_letter in list(string.ascii_lowercase):
                temp_typo = Substitute_Letter(ground_truth_word, substitution_letter, index)
                if temp_typo in Substitution_Dic:
                    Substitution_Dic[temp_typo].append((ground_truth_word, substitution_letter, index))
                else:
                    Substitution_Dic[temp_typo] = list()
                    Substitution_Dic[temp_typo].append((ground_truth_word, substitution_letter, index))

    if Typo in Substitution_Dic:
        return(Substitution_Dic[Typo])
    else:
        return([])





# function for find the possibile candidates with Reverse
def Find_Candidates_Reverse(Typo):

    # Next create table dictionary for Reverse for each words
    # Each element is (True Word, First Position, Second Position)
    Reverse_Dic = dict()

    for ground_truth_word in Ground_Truth_Words:
        for i in range(len(ground_truth_word)):
            for j in range(i+1, len(ground_truth_word)):
                temp_typo = Reverse_Letter(ground_truth_word, i, j)
                if temp_typo != ground_truth_word:
                    if temp_typo in Reverse_Dic:
                        Reverse_Dic[temp_typo].append((ground_truth_word, i, j))
                    else:
                        Reverse_Dic[temp_typo] = list()
                        Reverse_Dic[temp_typo].append((ground_truth_word, i, j))

    if Typo in Reverse_Dic:
        return(Reverse_Dic[Typo])
    else:
        return([])



# function to find all possible candidates for typo
def Find_Possible_Candidates(Typo):
    # First we need to create dictionary which help us find the possible candidates
    Typo = Typo.lower()

    Possible_Candidates = dict()

    Possible_Candidates["Insertion"] = Find_Candidates_Insertion(Typo)

    Possible_Candidates["Deletion"] = Find_Candidates_Deletion(Typo)

    Possible_Candidates["Reverse"] = Find_Candidates_Reverse(Typo)

    Possible_Candidates["Substitution"] = Find_Candidates_Substitution(Typo)

    return({"Typo" : Typo, "Possible_Candidates": Possible_Candidates})



# get the letter index in the matrix
def getLetterIndex(letter):

    if letter == " ":
        return(26)
    else:
        return(string.ascii_lowercase.index(letter))


# delete non letter single string in the list
def Delete_Non_Letter(Stringlist):
    ResultList = Stringlist
    while '—' in Stringlist:
        ResultList.remove('—')
    while '•' in Stringlist:
        ResultList.remove('•')
    while ',' in Stringlist:
        ResultList.remove(',')
    while '.' in Stringlist:
        ResultList.remove('.')

    return(ResultList)


# find the which letter is delete after the one letter
def find_deletion_letters(ground_truth_word, tesseract_word):

    SequenceList = difflib.SequenceMatcher(None, ground_truth_word, tesseract_word).get_opcodes()

    pre_letter = ""

    delete_letter = ""

    if len(SequenceList) == 3 or len(SequenceList) == 2:
        for tag, a1, a2, b1, b2 in SequenceList:
            if tag == 'delete':
                if a1-1 >= 0:
                    pre_letter = ground_truth_word[a1-1]
                    delete_letter = ground_truth_word[a1]
                else:
                    pre_letter = " "
                    delete_letter = ground_truth_word[a1]

    if pre_letter in string.ascii_lowercase+" " and delete_letter in string.ascii_lowercase+" ":
        return({"pre_letter" : pre_letter, "delete_letter": delete_letter})
    else:
        pre_letter = ""

        delete_letter = ""

        return({"pre_letter" : pre_letter, "delete_letter": delete_letter})



# find the which letter is intert after the one letter
def find_insertion_letters(ground_truth_word, tesseract_word):

    SequenceList = difflib.SequenceMatcher(None, ground_truth_word, tesseract_word).get_opcodes()

    pre_letter = ""

    insert_letter = ""

    if len(SequenceList) == 3 or len(SequenceList) == 2:
        for tag, a1, a2, b1, b2 in SequenceList:
            if tag == 'insert':
                if a1-1 >= 0:
                    pre_letter = ground_truth_word[a1-1]
                    insert_letter = tesseract_word[a1]
                else:
                    pre_letter = " "
                    insert_letter = tesseract_word[a1]

    if pre_letter in string.ascii_lowercase+" " and insert_letter in string.ascii_lowercase+" ":
        return({"pre_letter" : pre_letter, "insert_letter": insert_letter})
    else:
        pre_letter = ""

        insert_letter = ""

        return({"pre_letter" : pre_letter, "insert_letter": insert_letter})



# find the which letter is reverse with the letter after or substitute with other letter
def find_sub_rev_letters(ground_truth_word, tesseract_word):

    Differ_Index = [index for index in range(len(ground_truth_word)) if ground_truth_word[index] != tesseract_word[index]]

    pre_letter = ""

    changed_letter = ""

    tag = ""

    if len(Differ_Index) == 1:
        tag = "sub"

        pre_letter = ground_truth_word[Differ_Index[0]]

        changed_letter = tesseract_word[Differ_Index[0]]

    elif len(Differ_Index) == 2:
        ground_truth_pre_letter = ground_truth_word[Differ_Index[0]]
        tesseract_pre_letter = tesseract_word[Differ_Index[0]]
        ground_truth_pos_letter = ground_truth_word[Differ_Index[1]]
        tesseract_pos_letter = tesseract_word[Differ_Index[1]]

        if ground_truth_pre_letter == tesseract_pos_letter and ground_truth_pos_letter == tesseract_pre_letter:
            tag = "rev"
            pre_letter = ground_truth_word[Differ_Index[0]]
            changed_letter = tesseract_word[Differ_Index[0]]

    if pre_letter in string.ascii_lowercase+" " and changed_letter in string.ascii_lowercase+" ":
        return({"tag": tag, "pre_letter" : pre_letter, "changed_letter": changed_letter})
    else:
        tag = ""
        pre_letter = ""
        changed_letter = ""

        return({"tag": tag, "pre_letter" : pre_letter, "changed_letter": changed_letter})



def Create_Confusion_Matrix():

    # Next create confusion matrix for Deletion, Insertion, Substitution, Reversal
    Deletion_Confusion = [[0] * 26 for i in range(27)]
    Insertion_Confusion = [[0] * 26 for i in range(27)]
    Substitution_Confusion = [[0] * 26 for i in range(26)]
    Reversal_Confusion = [[0] * 26 for i in range(26)]

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
                    # Then we divided them into three different ways
                    # First if Ground_Truth_Line_Word is less than Tesseract_Line_Word, it should be Insertion
                    if len(Ground_Truth_Line_Word) < len(Tesseract_Line_Word):
                        Insertion_Result = find_insertion_letters(Ground_Truth_Line_Word, Tesseract_Line_Word)
                        pre_letter = Insertion_Result["pre_letter"]
                        insert_letter = Insertion_Result["insert_letter"]
                        if pre_letter != "" and insert_letter != "":
                            pre_letter_index = getLetterIndex(pre_letter)
                            insert_letter_index = getLetterIndex(insert_letter)
                            Insertion_Confusion[pre_letter_index][insert_letter_index] = Insertion_Confusion[pre_letter_index][insert_letter_index] + 1

                    # Second if Ground_Truth_Line_Word is larger than Tesseract_Line_Word, it should be Deletion
                    elif len(Ground_Truth_Line_Word) > len(Tesseract_Line_Word):
                        Deletion_Result = find_deletion_letters(Ground_Truth_Line_Word, Tesseract_Line_Word)
                        pre_letter = Deletion_Result["pre_letter"]
                        delete_letter = Deletion_Result["delete_letter"]
                        if pre_letter != "" and delete_letter != "":
                            pre_letter_index = getLetterIndex(pre_letter)
                            delete_letter_index = getLetterIndex(delete_letter)
                            Deletion_Confusion[pre_letter_index][delete_letter_index] = Deletion_Confusion[pre_letter_index][delete_letter_index] + 1

                    # Third if Ground_Truth_Line_Word is equal to Tesseract_Line_Word, it should be Substitution or Reversal
                    else:
                        sub_rev_result = find_sub_rev_letters(Ground_Truth_Line_Word, Tesseract_Line_Word)
                        tag = sub_rev_result["tag"]
                        if tag == "sub":
                            pre_letter = sub_rev_result["pre_letter"]
                            changed_letter = sub_rev_result["changed_letter"]
                            if pre_letter != "" and changed_letter != "":
                                pre_letter_index = getLetterIndex(pre_letter)
                                changed_letter_index = getLetterIndex(changed_letter)
                                Substitution_Confusion[pre_letter_index][changed_letter_index] = Substitution_Confusion[pre_letter_index][changed_letter_index] + 1
                        elif tag == "rev":
                            pre_letter = sub_rev_result["pre_letter"]
                            changed_letter = sub_rev_result["changed_letter"]
                            if pre_letter != "" and changed_letter != "":
                                pre_letter_index = getLetterIndex(pre_letter)
                                changed_letter_index = getLetterIndex(changed_letter)
                                Reversal_Confusion[pre_letter_index][changed_letter_index] = Reversal_Confusion[pre_letter_index][changed_letter_index] + 1

    return({"Deletion_Confusion": Deletion_Confusion, "Insertion_Confusion": Insertion_Confusion, "Substitution_Confusion": Substitution_Confusion, "Reversal_Confusion": Reversal_Confusion})


# Next function will compute the pr(c) which means the prior of the correct words

def Compute_Pr_c(correct_word):
    N = len(All_Ground_Truth_Words)
    V = len(Ground_Truth_Words)
    denominator = N + V/2

    word_freqs = collections.defaultdict(int)
    for word in All_Ground_Truth_Words:
        word_freqs[word] += 1

    corr_probs = collections.defaultdict(float)
    for word, freq in word_freqs.items():
        corr_probs[word] = (freq + 0.5)/denominator

    return(corr_probs[correct_word])



# This function is used to create chars[x] and chars[xy]

def CreateChars():
    charsX = [0] * 26

    charsXY = [[0] * 26 for i in range(26)]


    for word in All_Ground_Truth_Words:

        for letter_index1 in range(len(word)):
            charsX[getLetterIndex(word[letter_index1])] += 1

            for letter_index2 in range(letter_index1, len(word)):

                charsXY[getLetterIndex(word[letter_index1])][getLetterIndex(word[letter_index2])] += 1

    return({"charsX" : charsX, "charsXY": charsXY})
