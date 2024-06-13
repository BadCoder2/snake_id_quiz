# Snake ID Quiz App

Written in python using customtkinter. Tested only on Windows 10, will maybe work on others.

## Setup

1. Download the repository, unzip into a folder.
2. Create an empty folder named "image_urls" and an empty folder named "locations" in the main folder (the directory containing app.py).
3. Create a venv and enter it:
   1. Open command prompt, cd into main folder
   2. Run `python -m venv venv`
   3. Run `venv\Scripts\Activate`
4. Run `pip install -r requirements.txt`
5. Change the contents of location.txt to a custom name that represents the area you want snakes to be picked from (1 word only.)
6. Get the species list for that area:
   1. Go to [this link](https://www.gbif.org/occurrence/download?dataset_key=50c9509d-22c7-4a22-a47d-8c48425ef4a7&taxon_key=11592253&occurrence_status=present&gadm_gid=USA.43_1) and sign in if needed.
   2. Change the area to your desired area.
   3. Download the species list into the same directory as app.py.
   4. Extract the csv file; delete the zip file that contained the csv file
   5. Rename the csv file to "location_species.csv"
7. Run the app! (`python app.py`)

### Creating a new location

To create a new location, simply repeat steps 5 and 6. Don't forget that you can change location.txt to any previously used word and it will use the generated data (no need to redownload GBIF species list.)

### Running again, after setup

1. cd into the main folder
2. Run `venv\Scripts\Activate`
3. Run `python app.py`
