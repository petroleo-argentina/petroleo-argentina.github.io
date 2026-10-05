with open('frontend/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

print('Lines:', len(code.splitlines()))
print('Chars:', len(code))
print('Braces:', code.count('{'), '/', code.count('}'))
print('Parens:', code.count('('), '/', code.count(')'))
print('Brackets:', code.count('['), '/', code.count(']'))
assert code.count('{') == code.count('}'), 'Braces mismatch!'
assert code.count('(') == code.count(')'), 'Parens mismatch!'
assert code.count('[') == code.count(']'), 'Brackets mismatch!'
print('Syntax balance is PERFECT!')
