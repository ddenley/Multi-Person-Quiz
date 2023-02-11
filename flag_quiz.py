# Author:   Andy Edmondson
# Date:     11 Feb 2023
# Purpose:  Flag question/option/answer triples for quiz.
#
# Contains: FlagQuiz class
#
# Could be improved by pre-processing the country code and name data file.

import numpy as np
import pandas as pd                 # CSV file I/O
import os                           # read data files
from pathlib import Path            # Paths to data
import random                       # Get random flags
from typing import Tuple


class FlagQuiz:
    """Provide a flag quiz."""

    def __init__(self):
        # Get list of image file names
        self.img_path = Path('static/data/Flags Dataset/')
        self.img_list = os.listdir(self.img_path)

        # Filenames contain country abbreviations, so create a list of these
        self.country_codes = [fname[0:2] for fname in self.img_list]

        # Create a lookup dict for the country codes
        self.name_df = pd.read_csv("static/data/codes_names.csv")     #, encoding="iso-8859-1")
        self.name_lookup = dict([(code, name) for code, name in
                                 zip(self.name_df["code2"], self.name_df["name"])])

    def get_new_question(self) -> Tuple[str, list, str]:
        """Returns the flag path, n options and the answer."""
        codes = self.get_random_codes(4)
        answer_code = codes[0]                   # Always choose the first option as the answer
        answer = self.name_lookup[answer_code]

        random.shuffle(codes)
        path = os.path.join(self.img_path, answer_code.lower() + ".png")
        options = []
        for code in codes:
            options.append(self.name_lookup[code])
        return path, options, answer

    def get_random_codes(self, n=4) -> list:
        """Get n country codes and return"""
        return np.random.choice(self.name_df["code2"], n, replace=False).tolist()


if __name__ == "__main__":

    quiz = FlagQuiz()
    img_path, options, answer = quiz.get_new_question()
    print(f"The path is {img_path} and the options are: \n{options}.")
    print(f"The answer is {answer}.")
