import os

filepath = r'c:\Users\840 g8\Desktop\mee\ayesha-portfolio\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'ÐŸ‘‹': '👋',
    'â€”': '—',
    'â€“': '–',
    'â€™': '’',
    'â€œ': '“',
    'â€ ': '”',
    'â€': '”',
    'â‹...': '•',
    'â†’': '→',
    'âœ´': '✦',
    'âœ“': '✓',
    'â˜°': '☰',
    'IÂ²C': 'I²C'
}

for k, v in replacements.items():
    content = content.replace(k, v)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Cleanup done.')
