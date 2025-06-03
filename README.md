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

## 📦 Installation

```bash
git clone git@github.com:deekshith39/PET-AI.git
cd bank_statement_parser
pip install -r requirements.txt
```

## 🧠 Future Plans

- NLP-based transaction categorization
- PDF parsing support
- On-device ML model training
- Dashboard to visualize expenses

---
