# Real-Time Syntax Highlighter Project Report


## 1. Programming Language

The programming language chosen for this project is Python. Python was selected due to its simplicity, readability, and extensive support for GUI development through libraries like tkinter. Additionally, Python's dynamic nature and robust string manipulation capabilities make it suitable for implementing lexical and syntax analyzers without relying on external syntax highlighting libraries.

## 2. Syntax Analysis Process

The syntax analysis process is divided into two primary components: lexical analysis and syntax analysis (parsing). The lexical analyzer tokenizes the input text based on predefined rules, while the syntax analyzer validates the token stream against a context-free grammar. The process ensures real-time feedback by integrating with a GUI that updates as the user types.

### Lexical Analysis
    
**Approach**: State Diagram & Program Implementation

**Details** : The lexical analyzer (Lexer class) processes the input character by character using a state-driven
approach. It identifies tokens by checking the current character against predefined conditions (e.g., alphabetic for        identifiers, digits for numbers, quotes for strings). The lexer recognizes the following token types:

      KEYWORD: Reserved words like if, else, while, then, do, end.
      NUMBER: Integer values (e.g., 10, 5).
      IDENTIFIER: Variable names (e.g., x, y).
      STRING: Quoted strings (e.g., "test").
      OPERATOR: Operators like +, -, =, ==, <=, >=, etc.
      WHITESPACE: Spaces and tabs (ignored during parsing).
      UNKNOWN: Unrecognized characters.
    
**Implementation**: The Lexer class uses a position-based approach (self.pos) to iterate through the input text. It employs conditional checks to categorize characters and build tokens. Multi-character operators (e.g., <=, >=) are handled by sorting operators by length to prioritize longer matches.


### Syntax Analysis (Parsing)

**Approach**: Top-Down Parsing

**Details**: A recursive descent parser (Parser class) is implemented to validate the token stream. The parser follows a context-free grammar supporting:

**Program**: A sequence of statements.

**Statements**: if statements, while statements, or assignments.

**Expressions**: Simple expressions involving numbers, identifiers, strings, and operators.

**Grammar**:

        program → statement*
        statement → if_stmt | while_stmt | assignment
        if_stmt → "if" expr "then" statement* "end"
        while_stmt → "while" expr "do" statement* "end"
        assignment → IDENTIFIER "=" expr
        
expr → NUMBER | IDENTIFIER | STRING [OPERATOR (NUMBER | IDENTIFIER | STRING)]

**Implementation**: The parser uses a top-down approach, starting with the program rule and recursively descending through statements and expressions. It checks token types and values, raising SyntaxError for invalid constructs. The parser ensures that the token stream adheres to the defined grammar, providing real-time validation feedback.

## 3. Lexical Analysis Details

The lexical analyzer is implemented in the Lexer class without relying on external libraries. The state-driven approach processes input text as follows:

**Initialization**: The lexer stores the input text and tracks the current position (self.pos).

**Tokenization**: The next_token method examines the current character:

  **Whitespace**: Skips spaces and tabs.
  
  **Identifiers/Keywords**: Builds tokens for alphabetic sequences, checking against a predefined keyword set.
  
  **Numbers**: Accumulates consecutive digits.
  
  **Strings**: Captures text between double quotes.
  
  **Operators**: Matches single- or multi-character operators, prioritizing longer matches.
  
  **Unknown**: Captures unrecognized characters.
  
  **Output**: The tokenize method returns a list of (token_type, token_value) pairs, excluding whitespace.
  
## 4. Parsing Methodology
   
The parser employs top-down parsing (recursive descent) for its simplicity and suitability for the defined grammar. Key aspects:

**Token Consumption**: The consume method ensures the current token matches expected types or values, advancing the position.

**Error Handling**: Raises SyntaxError with descriptive messages for invalid token sequences.

**Recursive Structure**: Functions like program, statement, if_statement, while_statement, assignment, and expr mirror the grammar rules, ensuring hierarchical validation.

**Real-Time Validation**: The parser is invoked on every keypress, updating the GUI title to indicate valid or invalid syntax.

## 5. Highlighting Scheme

The syntax highlighter supports real-time highlighting of five distinct token types:

    -KEYWORD: Blue (e.g., if, while).
    -NUMBER: Green (e.g., 10, 5).
    -IDENTIFIER: Black (e.g., x, y).  
    -STRING: Purple (e.g., "test").
    -OPERATOR: Red (e.g., +, =).
    -UNKNOWN: Orange (for error highlighting).
    
**Implementation**: The SyntaxHighlighter class uses tkinter.Text widget tags to apply colors. The highlight method tokenizes the input, searches for each token in the text widget, and applies the corresponding tag from the token’s start to end position.
## 6. GUI Implementation

The GUI is built using tkinter, Python’s standard library for graphical interfaces. Key features:

**Text Widget**: A tkinter.Text widget captures user input and displays highlighted text.

**Real-Time Updates**: The <KeyRelease> event triggers the highlight method, which re-tokenizes the input, clears previous tags, and applies new ones.

**Syntax Validation Feedback**: The window title updates to "Valid Syntax" or "Invalid Syntax" based on parser output.

**Design**: The GUI is minimal, with a single text area (20x60) and padding for readability. Colors are chosen for clear visual distinction between token types.

## 7. Demo

**Demo**: A video demonstration has been recorded, showcasing the application’s real-time highlighting and syntax validation. The video is publicly accessible at https://youtu.be/_CdxkQzZqRs?si=C3k878xpW2DIzb-d 


## Conclusion
The project successfully implements a real-time syntax highlighter with a GUI, adhering to the specified requirements. The use of Python, a state-driven lexer, top-down parsing, and tkinter-based GUI ensures a robust and user-friendly solution. The highlighting scheme effectively distinguishes five token types, and the real-time feedback enhances usability.

