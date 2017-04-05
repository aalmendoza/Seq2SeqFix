from lexer.utilities import *
from pygments.lexers import get_lexer_for_filename
from pygments import lex
import re
import argparse

# Keep Lines?
def get_tokenization(lexedWoComments):
    res = ''
    curr_line_empty = True
    for t in lexedWoComments:
        token = t[1]
        token_stripped = token.strip()

        if '\n' in token:
            if curr_line_empty:
                if t[0] != Token.Text and token_stripped != '':
                    res += token_stripped + "\n"
            else:
                res += token_stripped + "\n"
            curr_line_empty = True
        elif t[0] == Token.Text:
            continue
        else:
            curr_line_empty = False
            res += token + ' '

    return res

def tokenize(sourcePath, strFlag, keepLines=False):    
    fileContents = ""
    with open(sourcePath, 'r') as f:
        fileContents = ''.join(f.readlines())

    lexer = get_lexer_for_filename(sourcePath)
    tokens = lex(fileContents, lexer) # returns a generator of tuples
    tokensList = list(tokens)
    language = languageForLexer(lexer)

    # Strip comments and alter strings
    lexedWoComments = tokensExceptTokenType(tokensList, Token.Comment)
    lexedWoComments = tokensExceptTokenType(lexedWoComments, Token.Literal.String.Doc)
    lexedWoComments = fixTypes(lexedWoComments, language) #Alter the pygments lexer types to be more comparable between our languages
    lexedWoComments = convertNamespaceTokens(lexedWoComments, language)

    if(strFlag == 0):
        lexedWoComments = modifyStrings(lexedWoComments, underscoreString)
    elif(strFlag == 1):
        lexedWoComments = modifyStrings(lexedWoComments, singleStringToken)
    elif(strFlag == 2):
        lexedWoComments = modifyStrings(lexedWoComments, spaceString)
    elif(strFlag == 3):
        lexedWoComments = modifyStrings(lexedWoComments, singleStringToken)
        lexedWoComments = collapseStrings(lexedWoComments)
        lexedWoComments = modifyNumbers(lexedWoComments, singleNumberToken)

    if(len(lexedWoComments) == 0):
        return ""
    else:
        return get_tokenization(lexedWoComments)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--source_file', type=str,
                       help='source file to be tokenized')
    parser.add_argument('--literal_handle', type=int, default=3,
                       help="0 -> replace all spaces in strings with _\n"
                            "1 -> replace all strings with a <str> tag\n"
                            "2 -> add spaces to the ends of the strings\n"
                            "3 -> collapse strings to <str> and collapses numbers to a type as well.\n")

    args = parser.parse_args()
    lexed = tokenize(args.source_file, args.literal_handle)
    print(lexed)