## PasswordPal
A tool to store emails and passwords with a modern interface.

## Features
- Master password protection
- Show/hide passwords
- Copy to clipboard
- Clean, easy-to-use interface

## How to Use
1. Install Python 3
2. Download PasswordPal
3. Change the master password in `main.py` (line 23: `access = 'password'`)
4. Navigate to the PasswordPal folder in Terminal
5. Run: `python3 main.py`

## Security Note
This uses basic character shifting for encoding. For sensitive data, consider using a more robust password manager.

## Files
- `main.py` - Main application
- `emails.txt` - Encrypted storage file (auto-generated)