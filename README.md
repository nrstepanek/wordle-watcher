# wordle-watcher
Keeps tabs on the wordle word lists (possible guesses and answers).

Running check.py (python3) grabs the wordle game script from the website, parses the guess and answer word lists, and then compares them against the most recent lists saved from previous runs of the script. If any differences are found a diff file will appear in the top level directory.

Don't look at the answer lists if you don't want spoilers.
