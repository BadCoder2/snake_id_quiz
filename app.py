import customtkinter
from ctkdlib import *
from PIL import Image
import random
import os
import pandas as pd
import json
import requests
import re
import pytaxize
customtkinter.set_default_color_theme("dark-blue")


class leftFrame(CTkXYFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")
        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)
    def get(self):
        return self.variable.get()

class centerImageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.cur_image = customtkinter.CTkImage(light_image=Image.open("snake.jpg"), size=(1000, 850))
        self.image_label = customtkinter.CTkLabel(self, image=self.cur_image, text = "")
        self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    def change_image(self, image_path):
        self.cur_image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(1000, 850))
        self.image_label.configure(image=self.cur_image, text = "")

class middleTextFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.text = customtkinter.CTkLabel(self, text="Hold shift and scroll to move species left and right.")
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    def change_text(self, text):
        self.text.configure(text=text)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.getSnakeList()
        self.getvalues()

        self.title("Snake ID Quiz")
        self.geometry("1600x1000")
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure((1, 2), weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = leftFrame(self, values=self.inclCommonNames())
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")

        self.buttonL = customtkinter.CTkButton(self, text="Guess Species/Ssp.", command=self.button_callbackL)
        self.buttonL.grid(row=1, column=0, padx=10, pady=10, sticky="nesw")

        self.middle_frame = middleTextFrame(self)
        self.middle_frame.grid(row=1, column=1, padx=10, pady=10, sticky="esw", columnspan=2)

        self.buttonR = customtkinter.CTkButton(self, text="Next Image", command=self.button_callbackR)
        self.buttonR.grid(row=1, column=3, padx=10, pady=10, sticky="nesw")

        self.center_image_frame = centerImageFrame(self)
        self.center_image_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", columnspan=3)

        self.correct_species = None
    def button_callbackL(self):
        # Get the species the user guessed
        guessed_species_with_common_name = self.left_frame.get()
        # Remove everything within parentheses
        guessed_species = re.sub(r"\(.*\)", "", guessed_species_with_common_name).strip()
        print("User guessed: " + guessed_species)
        if guessed_species == self.correct_species:
            self.middle_frame.change_text("Correct! The species is " + self.correct_species + ".")
        else:
            self.middle_frame.change_text("Incorrect. The species is not " + guessed_species + ".")
    def button_callbackR(self):
        print("Next Image")
        # Order of events: pick random species, pick random image of that species, download it, display it
        self.correct_species = random.choice(self.species_list)
        image_url_list = self.genListOfImagesURLsFromSpecies(self.correct_species)
        image_url = random.choice(image_url_list)
        image_path = "cur_image"
        with open(image_path, "wb") as f:
            f.write(requests.get(image_url).content)
        self.center_image_frame.change_image(image_path)
        self.middle_frame.change_text("What species is this?")
        
    def genListOfImagesURLsFromSpecies(self, species):
        # Function to get image urls from species
        print("Attempting to get image for species: " + species)
        if not os.path.isfile("image_urls/" + species + ".json"):
            url = "https://api.gbif.org/v1/occurrence/search?basisOfRecord=HUMAN_OBSERVATION&limit=300&scientificName=" + species
            response = requests.get(url)
            results = response.json()["results"]
            image_urls = []
            for result in results:
                try:
                    for media_entry in result["media"]:
                        image_urls.append(media_entry["identifier"])
                except:
                    continue
            with open("image_urls/" + species + ".json", "w") as f:
                json.dump(image_urls, f)
        else:
            with open("image_urls/" + species + ".json", "r") as f:
                image_urls = json.load(f)
        return image_urls
    
    def inclCommonNames(self):
        with open("location.txt", "r") as f:
            location = f.read().strip()
        if not os.path.isfile("locations/location_common_name_dict_" + location + ".json"):
            commonNamePlusSciName = []
            for scientific_name in self.species_list:
                common_name_str = ""
                common_name_list = pytaxize.itis.terms(scientific_name)[0]["commonNames"]
                if common_name_list == [None]:
                    continue
                for common_name in common_name_list:
                    common_name_str += common_name + ", "
                common_name_str = common_name_str[:-2]
                commonNamePlusSciName.append(scientific_name + " (" + common_name_str + ")" )
            with open("locations/location_common_name_dict_" + location + ".json", "w") as f:
                json.dump(commonNamePlusSciName, f)
        else:
            with open("locations/location_common_name_dict_" + location + ".json", "r") as f:
                commonNamePlusSciName = json.load(f)
        commonNamePlusSciName.sort()
        return commonNamePlusSciName

    def getvalues(self):
        with open("location.txt", "r") as f:
            location = f.read().strip()
        if not os.path.isfile("locations/location_" + location + ".json"):
            self.ensureExistsFiles()
            self.species_list = []
            # Get species list from GBIF
            species_csv = pd.read_csv("location_species.csv", sep=None, engine="python")
            for index, row in species_csv.iterrows():
                # Grab first 2 words of the "acceptedScientificName" column
                acceptedScientificNameList = row["acceptedScientificName"].split()[:2]
                if len(acceptedScientificNameList) < 2:
                    continue
                acceptedScientificName = "".join(acceptedScientificNameList[0]) + " " + "".join(acceptedScientificNameList[1])
                # Sometimes this string ends in a comma, so remove it
                if acceptedScientificName[-1] == ",":
                    acceptedScientificName = acceptedScientificName[:-1]
                # If the first 2 words are in the list of snakes, add either the first two words or the first three words to the species list (depending on "taxonRank" column)
                if acceptedScientificName in self.snakes:
                    if row["taxonRank"] == "SPECIES":
                        self.species_list.append(acceptedScientificName)
                    elif row["taxonRank"] == "SUBSPECIES":
                        self.species_list.append(acceptedScientificName + " " + row["acceptedScientificName"].split()[2])
                    else:
                        print("Unknown taxonRank: " + row["taxonRank"])
                else:
                    print("Not a snake: " + acceptedScientificName)
            # Once done, save the species list to a json file so we don't have to do this again
            with open("locations/location_" + location + ".json", "w") as f:
                json.dump(self.species_list, f)
            print("Created location_" + location + ".json")
        else:
            # If the json file already exists, just load it :)
            with open("locations/location_" + location + ".json", "r") as f:
                self.species_list = json.load(f)

    def getSnakeList(self):
        # Function to get list of all snake species and load it into a list
        # This may not be needed - when we're done implementing GBIF, reevaluate
        with open("snake_list.txt", "r") as f:
            self.snakes = f.readlines()
            for i in range(len(self.snakes)):
                self.snakes[i] = self.snakes[i].strip()

    def ensureExistsFiles(self):
        # Check if GBIF dataset files exist, if not, tell user to download them
        if not os.path.isfile("location_species.csv"):
            print("location_species.csv does not exist. Please download it from GBIF. See the README for more information.")
            exit()

app = App()
app.mainloop()
