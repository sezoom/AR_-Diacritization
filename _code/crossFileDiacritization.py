import pandas as pd
import re

# Regular expression matching Arabic diacritical marks
arabic_diacritics = re.compile(r'[\u064B-\u0652]')

def remove_diacritics(text):
    """Remove Arabic diacritics from a text string."""
    return re.sub(arabic_diacritics, '', text)

# Build a dictionary mapping from normalized words to their correct diacritized form
# from the test file.
def buildDictionary(file1_df):
    mapping = {}
    for transcription in file1_df["annotated_transcription"]:
        # Tokenize the transcription (here simply splitting on whitespace)
        tokens = transcription.split()
        for token in tokens:
            norm_token = remove_diacritics(token)
            # In case multiple variants exist, the dictionary will be updated to the last occurrence.
            # Optionally, you could add frequency counting or choose the most common variant.
            try:
                if len(mapping[norm_token]) >1:
                    pass
            except:
                mapping[norm_token]=[]

            mapping[norm_token].append( token)
    return mapping


def exportRedundencyWords(mapping):
    counter1 = 0
    exportTmp={}
    for k,v in mapping.items():
        testDF=pd.DataFrame(mapping[k])
        if len(testDF[0].unique())>1:
            print(testDF[0].unique())
            exportTmp[k]=v[:]
            counter1+=1
        del testDF
    return counter1, exportTmp

def fix_diacritization(text,mapping):
    global counter_global
    counter=0
    """Replace words in the input text with the diacritized version from the mapping, if available."""

    tokens = text.split()
    fixed_tokens = []
    for token in tokens:
        norm_token = remove_diacritics(token)
        if norm_token in mapping:
            if (token != mapping[norm_token][0]):
                counter += 1
                counter_global += 1
            fixed_tokens.append(mapping[norm_token][0])
        else:
            fixed_tokens.append(token)
    if (counter>0):
        print(counter," Replacements completed.")
        print("Before:",tokens)
        print("After:",fixed_tokens)
    return " ".join(fixed_tokens)


counter_global=0

##############################CROSS FILE DIACTRIZATION ############################
##### Uncomment to use either section:
# # Read the Excel files
# #file1 used to build the dictionary
# file1_df = pd.read_excel("exp/f3_merged1and2.xlsx")
# #file2 to be annotated from words in file1
# file2_df = pd.read_excel("exp/train_cs_pt4o.xlsx")
# # output file
# outputfile_Name="exp/train_cs_manual_test2.xlsx"
#
# mapping = buildDictionary(file1_df)
# # Apply the fix to the annotated_transcription column of the train file.
# file2_df["annotated_transcription"] = file2_df["annotated_transcription"].apply(fix_diacritization, mapping=mapping)
#
# # Save the modified DataFrame to a new Excel file.
# file2_df.to_excel(f"{outputfile_Name}", index=False)

################################ OR DIACTRIZATION FROM DICTIONARY #################
## read the dictionary:
mapping=pd.read_excel("dictionary_current_fixed_words.xlsx").to_dict(orient="dict")
#file2 to be annotated from words in file1
file2_df = pd.read_excel("exp/train_cs_manual.xlsx")
# output file
outputfile_Name="exp/train_cs_manual_v2.xlsx"
# Apply the fix to the annotated_transcription column of the train file.
file2_df["annotated_transcription"] = file2_df["annotated_transcription"].apply(fix_diacritization, mapping=mapping)

# Save the modified DataFrame to a new Excel file.
file2_df.to_excel(f"{outputfile_Name}", index=False)
print(counter_global, "TOTAL words updated")



