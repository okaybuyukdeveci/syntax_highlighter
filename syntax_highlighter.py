import tkinter as tk
from enum import Enum


# Token türleri (söz dizimi vurgulama için)
class TokenType(Enum):
    KEYWORD = "keyword"      # Anahtar 
    NUMBER = "number"        # Sayılar (10, 5, vb.)kelimeler (if, while, vb.)
    IDENTIFIER = "identifier" # Değişken isimleri (x, y, vb.)
    STRING = "string"        # Stringler ("test" gibi)
    OPERATOR = "operator"    # Operatörler (+, -, =, <=, >=, vb.)
    WHITESPACE = "whitespace" # Boşluklar
    UNKNOWN = "unknown"      # Tanımlanamayan karakterler


# Lexer: Girdi metnini token'lara ayırır
class Lexer:
    def __init__(self):
        # Anahtar kelimeler ve operatörler
        self.keywords = {"if", "else", "while", "then", "do", "end"}
        self.operators = {"+", "-", "=", "==", "<", ">", "!=", "<=", ">="}  # <= ve >= eklendi
        self.pos = 0
        self.text = ""
        self.length = 0

    def set_text(self, text):
        self.text = text
        self.length = len(text)
        self.pos = 0

    def next_token(self):
        if self.pos >= self.length:
            return None, None

        char = self.text[self.pos]

        # Boşlukları atla
        if char.isspace():
            start = self.pos
            while self.pos < self.length and self.text[self.pos].isspace():
                self.pos += 1
            return TokenType.WHITESPACE, self.text[start:self.pos]

        # Tanımlayıcılar ve anahtar kelimeler
        if char.isalpha() or char == '_':
            start = self.pos
            while self.pos < self.length and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
                self.pos += 1
            token = self.text[start:self.pos]
            token_type = TokenType.KEYWORD if token in self.keywords else TokenType.IDENTIFIER
            return token_type, token

        # Sayılar
        if char.isdigit():
            start = self.pos
            while self.pos < self.length and self.text[self.pos].isdigit():
                self.pos += 1
            return TokenType.NUMBER, self.text[start:self.pos]

        # Stringler (çift tırnak)
        if char == '"':
            start = self.pos
            self.pos += 1
            while self.pos < self.length and self.text[self.pos] != '"':
                self.pos += 1
            if self.pos < self.length:
                self.pos += 1
            return TokenType.STRING, self.text[start:self.pos]

        # Operatörler (çoklu karakterli olanlar dahil)
        for op in sorted(self.operators, key=lambda x: -len(x)):
            if self.text.startswith(op, self.pos):
                self.pos += len(op)
                return TokenType.OPERATOR, op

        # Tanımlanamayan karakterler
        self.pos += 1
        return TokenType.UNKNOWN, char

    def tokenize(self):
        tokens = []
        while self.pos < self.length:
            token_type, token_value = self.next_token()
            if token_type is None:
                break
            if token_type != TokenType.WHITESPACE:
                tokens.append((token_type, token_value))
        return tokens

# ------------------------------------------------------
# Parser: Token'ları analiz eder ve söz dizimini kontrol eder
# ------------------------------------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def consume(self, expected_type=None, expected_value=None):
        token_type, token_value = self.current_token()
        if (expected_type and token_type != expected_type) or (expected_value and token_value != expected_value):
            raise SyntaxError(f"Expected {expected_type or expected_value}, got {token_type} ({token_value})")
        self.pos += 1
        return token_value

    def parse(self):
        try:
            self.program()
            return True
        except SyntaxError as e:
            print("Söz Dizimi Hatası:", e)
            return False

    def program(self):
        while self.pos < len(self.tokens):
            self.statement()

    def statement(self):
        token_type, token_value = self.current_token()
        if token_type == TokenType.KEYWORD:
            if token_value == "if":
                self.if_statement()
            elif token_value == "while":
                self.while_statement()
            else:
                raise SyntaxError(f"Beklenmeyen anahtar kelime: {token_value}")
        else:
            self.assignment()

    def if_statement(self):
        self.consume(TokenType.KEYWORD, "if")
        self.expr()
        self.consume(TokenType.KEYWORD, "then")
        while self.current_token()[1] != "end":
            self.statement()
        self.consume(TokenType.KEYWORD, "end")

    def while_statement(self):
        self.consume(TokenType.KEYWORD, "while")
        self.expr()
        self.consume(TokenType.KEYWORD, "do")
        while self.current_token()[1] != "end":
            self.statement()
        self.consume(TokenType.KEYWORD, "end")

    def assignment(self):
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.OPERATOR, "=")
        self.expr()

    def expr(self):
        token_type, _ = self.current_token()
        if token_type in (TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.STRING):
            self.consume(token_type)
        else:
            raise SyntaxError("Sayı, tanımlayıcı veya string bekleniyor")

        # Operatör varsa, ikili ifadeyi işle
        token_type, token_value = self.current_token()
        if token_type == TokenType.OPERATOR:
            self.consume(TokenType.OPERATOR)
            # Operatörden sonra sayı, tanımlayıcı veya string bekle
            token_type, _ = self.current_token()
            if token_type in (TokenType.NUMBER, TokenType.IDENTIFIER, TokenType.STRING):
                self.consume(token_type)
            else:
                raise SyntaxError("Operatörden sonra sayı, tanımlayıcı veya string bekleniyor")

# -----------------------------------------------
# GUI: Gerçek zamanlı söz dizimi vurgulayıcı
# -----------------------------------------------
class SyntaxHighlighter:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerçek Zamanlı Söz Dizimi Vurgulayıcı")
        self.lexer = Lexer()
        self.text_widget = tk.Text(root, height=20, width=60)
        self.text_widget.pack(padx=10, pady=10)

        # Renk ayarları
        self.text_widget.tag_configure(TokenType.KEYWORD.value, foreground="blue")
        self.text_widget.tag_configure(TokenType.IDENTIFIER.value, foreground="black")
        self.text_widget.tag_configure(TokenType.NUMBER.value, foreground="green")
        self.text_widget.tag_configure(TokenType.STRING.value, foreground="purple")
        self.text_widget.tag_configure(TokenType.OPERATOR.value, foreground="red")
        self.text_widget.tag_configure(TokenType.UNKNOWN.value, foreground="orange")

        # Tuş bırakma olayına bağlama
        self.text_widget.bind("<KeyRelease>", self.highlight)

    def highlight(self, event=None):
        content = self.text_widget.get("1.0", tk.END).strip()
        self.lexer.set_text(content)
        tokens = self.lexer.tokenize()

        # Eski etiketleri kaldır
        for tag in TokenType:
            self.text_widget.tag_remove(tag.value, "1.0", tk.END)

        # Yeni token'lar için etiket uygula
        current_pos = "1.0"
        for token_type, token_value in tokens:
            idx = self.text_widget.search(token_value, current_pos, tk.END)
            if not idx:
                continue
            end = f"{idx}+{len(token_value)}c"
            self.text_widget.tag_add(token_type.value, idx, end)
            current_pos = end

        # Söz dizimi doğrulama
        parser = Parser(tokens)
        is_valid = parser.parse()
        status = "Valid Syntax" if is_valid else "Invalid Syntax"
        self.root.title(f"Real-Time Syntax Highlighter- {status}")

# -----------------------------------
# Ana uygulama
# -----------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlighter(root)
    root.mainloop()