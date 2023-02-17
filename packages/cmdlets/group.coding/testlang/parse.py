import re
from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import *

keywords = {
    'if': Keyword,
    'True': Keyword.Constant,
    'False': Keyword.Constant,
    r'\b\d+(\.\d+)?\b': Number,
    r'\bvar\w+\b': Name.Variable,
    r'print': Name.Builtin,
}

class KeywordLexer(RegexLexer):
    name = 'KeywordLexer'
    tokens = {
        'root': [
            # match keywords defined as strings
            (r'\b({})\b'.format('|'.join(k for k in keywords if isinstance(k, str))),
             keywords[match.group()]),
            # match keywords defined as regular expressions
            (k, keywords[k]) for k in keywords if isinstance(k, type(re.compile('')))
        ],
    }

# Use the custom lexer to lex code
code = '''
if True:
    var123 = 5
    print(var123)
'''

tokens = list(lex(code, KeywordLexer()))

for token in tokens:
    print(token)
