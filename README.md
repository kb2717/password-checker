Password Strength Checker — C Project

Overview
A C-based program that analyzes the strength of user-entered passwords and suggests a stronger one if required.  
It checks length, character variety, and repetition, then shows a **color-coded strength score** (Weak, Moderate, Strong).

---
Features
- Evaluates password strength (0–100)
- Detects lowercase, uppercase, digits, and special symbols
- Penalizes repeated characters
- Generates a strong random password if needed
- Color-coded terminal output

---
How to Run
1. Save as `password_strength.c`
2. Open terminal in the same folder
3. Compile:
   ```bash
   gcc password_strength.c -o password_strength
Run:
bash
Copy code
./password_strength

Example
Enter your password: abcd
Your Password: abcd
Strength: Weak (30%)
Suggested Stronger Password: G8!d#TqA
Strength: Strong (100%)

Logic
Check	Effect
Length ≥ 8	+20
Uppercase, Lowercase, Digit, Symbol	+20 each
Repeated chars	−5 each
Max score	100

Random Passwords
Strong passwords are created using:
Letters (A–Z, a–z)
Digits (0–9)
Symbols (!@#$%^&*)

Credits
ICS project GROUP 7:
-Khanak Bansal
-Boby
-Devansh Goyal
-Shaurya Pratap Singh
-Gugale Ninad Manoj

Conclusion
This project demonstrates:
Real-time password analysis
Random secure password generation
Application of string manipulation, character classification, and randomization in C

It’s a compact yet complete project showing practical use of C programming in cybersecurity
