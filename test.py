from pygments.lexers import PythonLexer
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.lexers import PygmentsLexer

# Create a list of items to display
items = ['apple', 'banana', 'orange', 'grape', 'strawberry',"anaconda"]

# Define a custom completer class
class CustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        # Get the current word being typed by the user
        word_before_cursor = document.get_word_before_cursor(WORD=True)

        # Find all items that start with the current word
        matches = [item for item in items if item.startswith(word_before_cursor)]

        # Return a list of Completion objects for the matches
        return [Completion(match, start_position=-len(word_before_cursor)) for match in matches]

# Create a PromptSession object and pass it the custom completer and syntax highlighter
session = PromptSession(completer=CustomCompleter(), lexer=PygmentsLexer(PythonLexer))

# Read a line of input from the user
input_text = session.prompt('Enter a Python expression: ')

print(f'You entered: {input_text}')