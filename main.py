import argparse
import os
import sys
from bank_statement_parser.core.parser import BankStatementParser

def ask_username_gui():
    try:
        import tkinter as tk
        from tkinter import simpledialog

        root = tk.Tk()
        root.withdraw()  # Hide main window
        user_name = simpledialog.askstring("User Input", "Enter your name:")
        if not user_name:
            raise ValueError("No name entered.")
        return user_name
    except Exception as e:
        print("⚠️ GUI not available or input canceled. Falling back to terminal input.")
        return input("Enter your name: ")

def run_parser(input_dir: str, user_name: str):
    output_file = os.path.join("output", f"user_{user_name}_parsed.csv")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    parser = BankStatementParser(input_dir, output_file)
    parser.process()

    print(f"✅ Parsed output saved to: {output_file}")

if __name__ == "__main__":
    cli = len(sys.argv) > 1

    if cli:
        arg_parser = argparse.ArgumentParser(description="Bank Statement Parser")
        arg_parser.add_argument("--user_name", required=True, help="Your name or ID to tag your parsed file")
        arg_parser.add_argument("--input_dir", default="bank_statements", help="Path to your bank statements folder")
        args = arg_parser.parse_args()
        run_parser(args.input_dir, args.user_name)
    else:
        print("⚠️ No CLI args detected. Prompting for user name...")
        user_name = ask_username_gui()
        run_parser("bank_statements", user_name)
