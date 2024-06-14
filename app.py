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
        self.text = customtkinter.CTkLabel(self, text="Hold shift and scroll to move species left and right. This snake image by Sebastian Spindler, CC0, no rights reserved. Used without permission.")
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    def change_text(self, text):
        self.text.configure(text=text)

class bottomMidFrame(customtkinter.CTkFrame):
    def __init__(self, master, button_callbackL, button_callbackR):
        super().__init__(master)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_columnconfigure((0, 3), weight=2)
        self.buttonL = customtkinter.CTkButton(self, text="Guess Species/Subspecies", command=button_callbackL)
        self.buttonL.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")

        self.middle_frame = middleTextFrame(self)
        self.middle_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nesw", columnspan=2)

        self.buttonR = customtkinter.CTkButton(self, text="Next Image", command=button_callbackR)
        self.buttonR.grid(row=0, column=3, padx=10, pady=10, sticky="nesw")

class bottomFrame(customtkinter.CTkFrame):
    def __init__(self, master, button_callbackBL, button_callbackBM, button_callbackBR, mode):
        super().__init__(master)
        if mode == "species":
            self.grid_columnconfigure((0, 1), weight=1)

            self.buttonBL = customtkinter.CTkButton(self, text="Get a Hint: Genus", command=button_callbackBL)
            self.buttonBL.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")

            self.buttonBR = customtkinter.CTkButton(self, text="Get the Answer", command=button_callbackBR)
            self.buttonBR.grid(row=0, column=1, padx=10, pady=10, sticky="nesw")
        elif mode == "subspecies":
            self.grid_columnconfigure((0, 1, 2), weight=1)

            self.buttonBL = customtkinter.CTkButton(self, text="Get a Hint: Genus", command=button_callbackBL)
            self.buttonBL.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")

            self.buttonBM = customtkinter.CTkButton(self, text="Get a Hint: Species or Subspecies", command=button_callbackBM)
            self.buttonBM.grid(row=0, column=1, padx=10, pady=10, sticky="nesw")

            self.buttonBR = customtkinter.CTkButton(self, text="Get the Answer", command=button_callbackBR)
            self.buttonBR.grid(row=0, column=2, padx=10, pady=10, sticky="nesw")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Grab the second line of mode.txt to determine the mode
        with open("mode.txt", "r") as f:
            self.mode = f.readlines()[1].strip()
        self.getSnakeList()
        self.getValues()
        self.commonNamePlusSciNameList = self.inclCommonNames()
        self.alignSpeciesListAndCommonNameListWithMode()
        self.buttonsDisabled = True
        self.usedHint = False

        self.title("Snake ID Quiz")
        self.geometry("1600x1000")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = leftFrame(self, values=self.commonNamePlusSciNameList)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")

        self.center_image_frame = centerImageFrame(self)
        self.center_image_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", columnspan=3)

        self.bottom_middle_frame = bottomMidFrame(self, button_callbackL=self.button_callbackL, button_callbackR=self.button_callbackR)
        self.bottom_middle_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nesw", columnspan=4)

        self.bottom_frame = bottomFrame(self, button_callbackBL=self.button_callbackBL, button_callbackBM=self.button_callbackBM, button_callbackBR=self.button_callbackBR, mode=self.mode)
        self.bottom_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nesw", columnspan=4)

        self.correct_species = None
    def button_callbackL(self):
        # Get the species the user guessed
        if self.buttonsDisabled:
            return
        guessed_species_with_common_name = self.left_frame.get()
        self.number_of_guesses += 1
        # Remove everything within parentheses
        guessed_species = re.sub(r"\(.*\)", "", guessed_species_with_common_name).strip()
        print("User guessed: " + guessed_species)
        if self.mode == "species":
            modeText = "species"
        elif self.mode == "subspecies":
            modeText = "species/subspecies"
        if guessed_species == self.correct_species:
            if self.number_of_guesses == 1:
                if self.usedHint:
                    self.bottom_middle_frame.middle_frame.change_text("Correct! The " + modeText + " is " + self.correct_species + ". You guessed it on the first try, but used a hint.")
                else:
                    self.bottom_middle_frame.middle_frame.change_text("Correct! The " + modeText + " is " + self.correct_species + ". You guessed it on the first try without hints!")
            else:
                if self.usedHint:
                    self.bottom_middle_frame.middle_frame.change_text("Correct! The " + modeText + " is " + self.correct_species + ". You guessed it in " + str(self.number_of_guesses) + " tries, but used a hint.")
                else:
                    self.bottom_middle_frame.middle_frame.change_text("Correct! The " + modeText + " is " + self.correct_species + ". You guessed it in " + str(self.number_of_guesses) + " tries, and used no hints.")
            self.buttonsDisabled = True
        else:
            if self.number_of_guesses == 1:
                self.bottom_middle_frame.middle_frame.change_text("Incorrect. The " + modeText + " is not " + guessed_species + ". You have guessed " + str(self.number_of_guesses) + " time.")
            else:
                self.bottom_middle_frame.middle_frame.change_text("Incorrect. The " + modeText + " is not " + guessed_species + ". You have guessed " + str(self.number_of_guesses) + " times.")

    def button_callbackBL(self):
        if self.buttonsDisabled:
            return
        elif self.correct_species == None:
            self.bottom_middle_frame.middle_frame.change_text("Advance to the next image to begin.")
            return
        else:
            genus = self.correct_species.split()[0]
            self.bottom_middle_frame.middle_frame.change_text("The genus is " + genus + ".")
            self.usedHint = True

    def button_callbackBM(self):
        if self.buttonsDisabled:
            return
        elif self.correct_species == None:
            self.bottom_middle_frame.middle_frame.change_text("Advance to the next image to begin.")
            return
        else:
            if len(self.correct_species.split()) == 2:
                self.bottom_middle_frame.middle_frame.change_text("The current image is identifiable to species level.")
            elif len(self.correct_species.split()) == 3:
                self.bottom_middle_frame.middle_frame.change_text("The current image is identifiable to subspecies level.")
            else:
                self.bottom_middle_frame.middle_frame.change_text("ERROR")
            self.usedHint = True

    def button_callbackBR(self):
        if self.buttonsDisabled:
            return
        self.buttonsDisabled = True
        if self.correct_species == None:
            self.bottom_middle_frame.middle_frame.change_text("Advance to the next image to begin.")
            return
        if self.mode == "species":
            modeText = "species"
        elif self.mode == "subspecies":
            modeText = "species/subspecies"
        self.bottom_middle_frame.middle_frame.change_text("The " + modeText + " is " + str(self.correct_species) + ".")

    def button_callbackR(self):
        print("Next Image")
        self.number_of_guesses = 0
        self.buttonsDisabled = False
        self.usedHint = False
        # Order of events: pick random species, pick random image of that species, download it, display it
        while True:
            self.correct_species = random.choice(self.species_list)
            image_url_list = self.genListOfImagesURLsFromSpecies(self.correct_species)
            try:
                image_info = random.choice(image_url_list)
                break
            except:
                print("Error: No images found for " + self.correct_species + ". Trying different species.")
                continue
        image_url = image_info["image_url"]
        image_path = "cur_image"
        with open(image_path, "wb") as f:
            f.write(requests.get(image_url).content)
        self.center_image_frame.change_image(image_path)
        if self.mode == "species":
            newtext = "What species is this snake?"
        elif self.mode == "subspecies":
            newtext = "What species (or subspecies, if identifiable) is this snake?"
        newtext += " Image by " + image_info["creator"] + ", licensed under " + image_info["license"] + ". Reference: " + image_info["reference"]
        self.bottom_middle_frame.middle_frame.change_text(newtext)
        
    def genListOfImagesURLsFromSpecies(self, species):
        # Function to get image urls from species
        #print("Attempting to get image for species: " + species)
        if not os.path.isfile("image_urls/" + species + ".json"):
            url = "https://api.gbif.org/v1/occurrence/search?basisOfRecord=HUMAN_OBSERVATION&limit=300&scientificName=" + species
            response = requests.get(url)
            results = response.json()["results"]
            image_urls = []
            for result in results:
                try:
                    for media_entry in result["media"]:
                        image_info = {
                            "image_url": media_entry["identifier"],
                            "license": media_entry["license"],
                            "creator": media_entry["rightsHolder"],
                            "reference": media_entry["references"]
                        }
                        image_urls.append(image_info)
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
            commonNamePlusSciNameList = []
            for scientific_name in self.species_list:
                common_name_str = ""
                # Sometimes the common name lookup errors becaues the species is not in the database
                try:
                    common_name_list = pytaxize.itis.terms(scientific_name)[0]["commonNames"]
                    print("Got common name for " + scientific_name)
                except:
                    # If this haoppens, we have to remove the species from the list
                    print("Error getting common name for " + scientific_name)
                    common_name_list = [None]
                if common_name_list == [None]:
                    commonNamePlusSciNameList.append(scientific_name)
                    continue
                for common_name in common_name_list:
                    common_name_str += common_name + ", "
                common_name_str = common_name_str[:-2]
                commonNamePlusSciNameList.append(scientific_name + " (" + common_name_str + ")" )
            with open("locations/location_common_name_dict_" + location + ".json", "w") as f:
                json.dump(commonNamePlusSciNameList, f)
        else:
            with open("locations/location_common_name_dict_" + location + ".json", "r") as f:
                commonNamePlusSciNameList = json.load(f)
        commonNamePlusSciNameList.sort()
        return commonNamePlusSciNameList

    def getValues(self):
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

    def alignSpeciesListAndCommonNameListWithMode(self):
        # If the mode is "species", remove the subspecies from the species list and common name list
        if self.mode == "species":
            self.species_list = [species for species in self.species_list if len(species.split()) == 2]
            self.commonNamePlusSciNameList = [species for species in self.commonNamePlusSciNameList if len(re.sub(r"\(.*\)", "", species).split()) == 2]
            return
        elif self.mode == "subspecies":
            return
        else:
            print("Error: mode.txt is not set to 'species' or 'subspecies'.")
            raise ValueError

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
            raise FileNotFoundError

app = App()
app.mainloop()
