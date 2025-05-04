# Instagram Follow Checker

A Python script that logs into your Instagram account, retrieves your followers and following lists, compares them, and saves reports showing:

- Accounts that **follow you** but **you don’t follow back**
- Accounts **you follow** but **don’t follow you back**


The results are saved as plain `.txt` files for simple review.  


## 🚀 Features

- 🔐 Secure login using credentials from a `.env` file
- 🔄 Automatic session reuse with 2FA (two-factor authentication) support
- 📥 Uses Instagram’s private API via `instagrapi`
- 🧘 Behaves gently (rate limits built in) to reduce risk of being flagged by Instagram
- 💾 Saves outputs to:
    - `outputs/fans.txt`  
    - `outputs/not_following_back.txt`
  

## 📂 Project Structure  

```  
📁 outputs/                     # Contains output TXT reports
├── fans.txt
├── not_following_back.txt  
📄 .env                         # Your credentials (excluded from Git)
📄 .env.example                 # Template for environment variables
📄 .gitignore                   # Hides sensitive/session files
📄 requirements.txt             # Python package dependencies
📄 session.json                 # Cached session file to avoid repeated logins (excluded from Git)  
📄 instagram_follow_checker.py  # Main script
📄 README.md
```  


## 📦 Requirements

- Python 3.8+
- Instagram account with 2FA enabled (optional)
- Packages in `requirements.txt`

To install the required packages:
```bash
pip install -r requirements.txt
```


## 🔐 Setup

1. Clone the repository:
```bash
git clone https://github.com/loufakis/instagram-follow-checker.git
cd instagram-follow-checker
```

2. Create a `.env` file by copying the example:
```bash
cp .env.example .env
```

3. Fill in your Instagram credentials in `.env`:
```bash
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
```
Your `.env` and session file are ignored via `.gitignore`.  


## ▶️ Usage

Run the script:  
```bash
python instagram_follow_checker.py
```
If 2FA is enabled, you’ll be prompted to enter the verification code sent to your device.  


## 📁 Output

After running, you’ll get: 
- `outputs/fans.txt`: People who follow you but you don’t follow them back   
- `outputs/not_following_back.txt`: People you follow but who don’t follow you back  


Each file contains one username per line.






## ⚠️ Disclaimer
This project uses Instagram's private API via `instagrapi`.  
Use it responsibly to avoid violating Instagram's terms of service or triggering temporary restrictions.

