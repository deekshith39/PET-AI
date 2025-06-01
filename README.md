# 🧾 Bank Statement Parser

A privacy-first Python tool to parse and standardize bank statements (Excel/CSV), extract clean transaction data, and export user-specific outputs.  
Ideal for collaborative dataset building without sharing personal financial files.

---

## 🚀 Features

- Parses various bank statement formats
- Automatically detects headers like Date, Description, Credit, Debit
- Saves user-specific parsed output
- GUI input prompt when run via IDE
- CLI support for automated workflows
- Skips pushing sensitive raw files — only output is shared

---

## 🔧 How to Use

### ▶️ Option 1: Run via Terminal (CLI)

```bash
python main.py --user_name=<your_name>
```

✅ This will:
- Parse all files inside `../bank_statements/`
- Save output to: `../output/user_<your_name>_parsed.csv`

**Optional:** You can customize the input folder:

```bash
python main.py --user_name=deekshith --input_dir=../custom_folder
```

---

### 🖥 Option 2: Run via IDE (PyCharm, VSCode, Jupyter etc.)

If you run `main.py` without CLI arguments:

1. A GUI dialog will ask for your name.
2. All files from `../bank_statements/` will be parsed.
3. The output will be saved to `../output/user_<your_name>_parsed.csv`.

> ⚠️ If the GUI dialog fails (e.g. in headless mode), you'll be prompted in the terminal.

---

## 📁 Folder Structure

```
project_root/
│
├── bank_statement_parser/      # Core logic
│   ├── core/                   # Parser modules
│   └── __init__.py
│
├── main.py                     # Entry point
├── output/                     # [Ignored] Parsed user outputs
├── bank_statements/            # [Ignored] Raw input files
├── requirements.txt
└── README.md
```

---

## 🔒 Privacy & Collaboration

- ❌ Do **not** upload your real bank statements.
- ✅ Instead, run `main.py` and commit only your parsed output:
  ```
  output/user_<your_name>_parsed.csv
  ```

This way, everyone contributes clean, structured data without leaking private financial information.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/bank-statement-parser.git
cd bank-statement-parser
pip install -r requirements.txt
```

---

## 🤝 Contributing

We welcome contributions! To help:
- Create a fake/example bank statement (mimicking real format)
- Add it under a `sample_data/` folder
- Open a PR to enhance parsing logic or support new banks

---

## 🧠 Future Plans

- NLP-based transaction categorization
- PDF parsing support
- On-device ML model training
- Dashboard to visualize expenses

---

## 📄 License

MIT License © 2025 [Your Name]
