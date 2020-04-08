#!/usr/bin/env python

import os
from time import sleep

ENVAR_SEARCH_DIR = 'search_dir'
ENVAR_SEARCH_TEXT = 'search_text'
ENVAR_OUTPUT_FILE = 'output_file'

search_dir = os.environ.get(ENVAR_SEARCH_DIR)
search_texts = os.environ.get(ENVAR_SEARCH_TEXT).split('|')
output_file = os.environ.get(ENVAR_OUTPUT_FILE)

if search_dir is None or search_texts is None or len(search_texts) < 1 or output_file is None or search_texts[0] == 'none' or '00000' in output_file:
    print(f"No valid configuration for deployment. Please reconfigure envars:\n\n{ENVAR_SEARCH_TEXT}\n{ENVAR_OUTPUT_FILE}\n\n. Going to sleep...")
elif os.path.exists(output_file):
    print(f"Output file: {output_file} already exists. This search seems complete. Going to sleep...")
else:
    print(f"Searching for: {search_texts} in {search_dir} and printing results to {output_file}")
    results = []
    for dirpath, dirnames, files in os.walk(search_dir):
        for fname in files:
            filepath = os.path.join(dirpath, fname)
            with open(filepath) as f:
                try:
                    found = False
                    for line in f:
                        for search_text in search_texts:
                            if search_text in line:
                                print(f"+{filepath}")
                                results.append(filepath)
                                found = True
                                break
                    # if found is False:
                    #     print(f"-{filepath}")
                except Exception as e:
                    print(f"{filepath}: {e}")

    with open(output_file, 'w') as f:
        f.write(f"Search phrases: {search_texts}\nSearch directory: {search_dir}\nResults: {len(results)}\n-------------------------\n")
        f.write("\n".join(results))


    print(f"Job complete. Output file: {output_file} is ready for transfer. Going to sleep...")

while True:
    sleep(1)

