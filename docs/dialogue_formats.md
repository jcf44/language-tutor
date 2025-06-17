# Dialogue Input Formats

The Language Tutor supports multiple file formats for importing dialogues. Each format has its own advantages and use cases.

## Supported Formats

### 1. **JSON** (`.json`)

Structured format with full metadata support.

```json
{
  "title": "At the Restaurant",
  "level": "intermediate",
  "context": "Ordering food at a French restaurant",
  "messages": [
    {"role": "user", "content": "Bonjour, une table pour deux, s'il vous plaît."},
    {"role": "assistant", "content": "Bien sûr ! Suivez-moi, s'il vous plaît."}
  ]
}
```

### 2. **CSV** (`.csv`)

Simple tabular format for quick dialogue creation.

```csv
speaker,message
user,"Excusez-moi, où est la gare ?"
assistant,"La gare est tout droit, à 200 mètres."
user,"Merci beaucoup !"
assistant,"De rien, bon voyage !"
```

### 3. **Markdown** (`.md`) ✨ **Enhanced**

Rich format with metadata, formatting, and easy readability.

```markdown
# Dialogue Title

**Level:** beginner  
**Context:** Description of the scenario

---

**User:** Bonjour ! Comment *allez-vous* ?

**Assistant:** Très bien, **merci** ! Et vous ?
```

### 4. **Plain Text** (`.txt`)

Simple format with automatic speaker detection.

```
User: Bonjour !
Assistant: Bonjour ! Comment puis-je vous aider ?
User: Je cherche la bibliothèque.
Assistant: Elle est dans la rue principale.
```

## Markdown Features ✨

The enhanced markdown parser supports:

### **Metadata Extraction**

- `**Level:**` - Sets dialogue difficulty (beginner/intermediate/advanced)
- `**Context:**` - Provides scenario description  
- `# Title` - Sets dialogue title from heading

### **Speaker Formats**

- `**Speaker:**` - Bold speaker names
- `*Speaker:*` - Italic speaker names
- `Speaker:` - Plain speaker names

### **Text Formatting Cleanup**

- **Bold text**: `**text**` → `text`
- *Italic text*: `*text*` → `text`
- `Code text`: `` `text` `` → `text`
- [Links](url): `[text](url)` → `text`

### **Smart Speaker Detection**

Automatically recognizes speaker roles based on keywords:

**User keywords:** user, utilisateur, client, étudiant, student  
**Assistant keywords:** assistant, tuteur, prof, teacher, tutor

### **Content Filtering**

Automatically skips:

- Headers (`# Title`)
- Metadata lines (`**Level:** beginner`)
- Separators (`---`)
- Empty lines

## Usage in Application

1. **Web Interface**: Upload any supported format via the file uploader
2. **Automatic Detection**: File extension determines the parser used
3. **Audio Generation**: Works with all formats - both speakers get audio
4. **Different Voices**: User and Assistant get different French accents

## Benefits by Format

| Format | Readability | Metadata | Formatting | Ease of Creation |
|--------|-------------|----------|------------|------------------|
| JSON   | ⭐⭐        | ⭐⭐⭐⭐⭐ | ⭐⭐       | ⭐⭐             |
| CSV    | ⭐⭐⭐      | ⭐        | ⭐         | ⭐⭐⭐⭐⭐       |
| Markdown| ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐         |
| Text   | ⭐⭐⭐⭐    | ⭐        | ⭐⭐       | ⭐⭐⭐⭐⭐       |

## Recommendation

**For new dialogues**: Use **Markdown** format for the best balance of readability, features, and ease of editing.

**For quick imports**: Use **CSV** format when you have dialogue data in spreadsheets.

**For integration**: Use **JSON** format when importing from other systems or APIs.
