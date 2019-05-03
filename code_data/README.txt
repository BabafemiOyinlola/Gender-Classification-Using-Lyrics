1) The main file to run is the Jupiter notebook - LyricsBasedGenderClassification.ipynb 

2) The scraper used for gathering data (scraper.py) is run separately.

3) Data files are combined into a single document with combine.py by passing the files to combine and a destination path to save the combined files. (Files have been combined and labelled in the Data folder)

4) Preprocessing.py is imported into the notebook and functions called directly.

5) create_embedding.py is also imported into the notebook. This file generates a word embeddings file if it does not exist.