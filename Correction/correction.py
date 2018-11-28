from correction_lib import Get_FileNames, clean_word, clean_word2, filter_word, Find_Candidates_Insertion

# First we need to create dictionary which help us find the possible candidates

Ground_Truth_Path = "../data/ground_truth/"

Tesseract_Path = "../data/tesseract/"

Ground_Truth_Files = Get_FileNames(Ground_Truth_Path)

File_Names = [filename[: -4] for filename in Ground_Truth_Files]

Ground_Truth_Words = set()

for FileName in File_Names:
    File_Dir = Ground_Truth_Path + FileName + ".txt"
    with open(File_Dir, 'r') as file:
        file_Content = file.read()
        uncleaned_word = file_Content.split()
        Ground_Truth_Words = Ground_Truth_Words.union(set(map(clean_word,uncleaned_word)))


Ground_Truth_Words = set(filter(clean_word2, Ground_Truth_Words))




print(Find_Candidates_Insertion("avoidded", Ground_Truth_Words))
