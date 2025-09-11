# 🤓 DocNerd
An AI docstring generator because I find writing docstrings a big bore. Now has support for Python, Rust, C & it's header files, C++ & it's header files, JavaScript, TypeScript & Java.

# Installation
1. CLone the repository and create a `.env` file
```
git clone https://github.com/AalbatrossGuy/DocNerd.git
cd DocNerd
touch .env
```
2. Set `GROQ_API_KEY=<api-key>` in `.env` or `export GROQ_API_KEY=<api-key>`

# Instructions
1. Make sure the file is structured like this:
```python3
# DOCSTRING START
def func(a, b):
    <do-something>
# DOCSTRING END
```
2. If the file is called `python_file.py`, then do
```
python3 docnerd.py python_file.py
```
If you want to rewrite existing docstrings, do
```
python3 docnerd.py python_file.py --replace-existing-docstring
```
3. For knowing what other parameters are there, do `python3 docnerd.py --help`.

# Screenshots
<img width="479" height="302" alt="image" src="https://github.com/user-attachments/assets/927d796d-76f2-4ccc-9239-806c1a6ca6cc" /><br>
<img width="691" height="59" alt="image" src="https://github.com/user-attachments/assets/0c31d5ab-3d61-4641-bdf7-08b8c567541b" /><br>
<img width="532" height="443" alt="image" src="https://github.com/user-attachments/assets/3cb24bcf-fcc5-4582-92a7-0bb9282c6506" />
