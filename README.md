# Snake ID Quiz App

Written in python using customtkinter. Tested only on Windows 10, will likely work on others.

**WARNING: Due to the nature of the dataset images are scraped from, injured or dead snakes may be shown.**

## Setup from Source

These instructions assume you have Python 3 installed - download it [here](https://www.python.org/downloads/) if you don't
1. Download the repository, unzip into a folder.
2. Create an empty folder named "image_urls" and an empty folder named "locations" in the main folder (the directory containing app.py). Do not rename these folders.
3. Create a venv and enter it:
   1. Open command prompt, [cd into main folder](https://www.wikihow.com/Change-Directories-in-Command-Prompt) (see link for guide on how to do so)
   2. Run `python -m venv venv`
   3. Run `venv\Scripts\Activate`
4. Run `pip install -r requirements.txt`
5. Change the contents of location.txt to a custom name that represents the area you want snakes to be picked from (1 word only.) (For clarity purposes: I am referring to the *contents* of location.txt, e.g., what the file says when you double click it, not the name of the file.)
6. Get the species list for that area:
   1. Go to [this link](https://www.gbif.org/occurrence/download?dataset_key=50c9509d-22c7-4a22-a47d-8c48425ef4a7&taxon_key=11592253&occurrence_status=present&gadm_gid=USA.43_1) and sign in if needed.
   2. Change the area to your desired area.
   3. Download the species list into the same directory as app.py.
   4. Extract the csv file; delete the zip file that contained the csv file
   5. Rename the csv file to "location_species.csv"
7. Run the app! (`python app.py`). Expect a long startup the first time you run it.

### Creating a new location

To create a new location, simply repeat steps 5 and 6. Don't forget that you can change location.txt to any previously used word and it will use the generated data (no need to redownload GBIF species list.) **Do note that the contents of location.txt are case-sensitive.**

For example, when one first starts the app, they need to set location.txt to a word, say, Tennessee, and download the corresponding `location_species.csv`. Then, let's say they also want to try their hand at identification in California. They change `location.txt` to California and replace `location_species.csv` with a species list from California. Now, `location.txt` can be changed back to Tennessee without changing `location_species.csv` - the data for Tennessee has already been generated.

### Deleting a location

To delete a location, simply delete `location_[word-used-in-location.txt].json` and `location_common_name_dict_[word-used-in-location.txt].json`

### Running again, after setup

1. cd into the main folder
2. Run `venv\Scripts\Activate`
3. Run `python app.py`

## Setup from EXE (Not recommended, but if you aren't experienced with command prompt, it might be a good choice)

1. Download the zipped exe from the most recent release
2. Follow steps 5 and 6 of setting up from source (instead of "the same directory as app.py", put it in the same directory as app.exe).
3. Run app.exe. Expect to wait for a long period of time before a window appears. This should only happen the first time you run the app (and any time you run the app after making a new location).

### Creating a new location, exe

Follow the same steps for creating a location on source installations.

# Issues and Contributions

If I'm being completely honest, then this code probably sucks because I'm a self-taught, inexperienced coder. So, issues are very likely to occur. That being said, I'm happy to fix any issues that do arise! Just make an issue and I'll do my best to replicate it and fix it. **Please include as much detail as possible in issues**, including the settings you used for downloading `location_species.csv`, your operating system, the entire log (if available), etc. The more info you provide, the easier it'll be for me to get it fixed.

Additionally - feel free to create feature requests as issues! I'd love to make this better in ways that people actually want, so please make feature requests if you think you'd enjoy it.

As to contributing - if you feel you can make this project better in any way, and you have the free time to do it, then go nuts! Pull requests welcome.
