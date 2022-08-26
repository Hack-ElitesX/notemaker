#!/usr/bin/env python3
import os
import pytube
from sys import exit
from sys import platform
PLATFORM:str = platform.lower()

class YouTube:
    def __init__(self, defaultSavePath:str = "Downloads", fileExtension:str = "mp4") -> None:
        self.defaultSavePath:str = defaultSavePath
        self.fileExtension:str = fileExtension

        if(os.path.isdir(self.defaultSavePath) == False):
            os.mkdir(self.defaultSavePath)

    def remove(self, fileName: str):
        try:
            os.remove(f"{self.defaultSavePath}/{fileName}")
            print("File Removed Successfully")
        except Exception as e:
            print("Unable to remove filel, can only remove file in default directory")

    # Downloads a single file
    def download(self, url:str, fileName:str = None, savePath:str = None) -> None:
        if(savePath is None):
            savePath = self.defaultSavePath
        if(not os.path.isdir(savePath)):
            os.mkdir(savePath)
        if(fileName is None):
            fileName = url.split("/")[-1]
        try:
            yt = pytube.YouTube(url)
            yt.streams.filter(progressive=True, file_extension=self.fileExtension).order_by('resolution').desc().first().download(savePath, filename=f"{fileName}.{self.fileExtension}")
            return 1
        except Exception as e:
            print(e)
            return 0

    # Downloads multiple file
    # Need path for the list of file links
    def downloadMultiple(self, filePath:str, savePath:str = None) -> None:
        if(savePath is None):
            savePath = self.defaultSavePath
        try:
            if(not os.path.isdir(savePath)):
                os.mkdir(savePath)
        except Exception as e:
            print(e)
        
        try:
            with open(filePath, "r") as f:
                for line in f:
                    try:
                        fileName = line.split("=")[0]
                        if(fileName == " " or fileName == "" or fileName == line):
                            fileName = line.split("/")[-1]
                    except:
                        fileName = line.split("/")[-1]
                    try:
                        url = line.split("=")[1]
                    except:
                        url = line
                    print(f"Downloading: \nUrl: {url} \tFileName: {fileName} \t savePath: {savePath}")
                    try:
                        fileName = fileName.strip()
                        self.download(url, fileName, savePath)
                    except:
                        print("Unable to download")
                        print(f"Url: {url} \tFileName: {fileName} \t savePath: {savePath}")
                        print("Skipping Download...\n")
        except FileNotFoundError:
            print("File Not Found!\n")

    def CLI(self):
        self.menu()
        while((user_input:=input(">> "))):
            try:
                user_input = int(user_input)
            except ValueError:
                print("Invalid Input, input should be an integer from the given list")
                continue
            if(user_input == 0): exit(0)
            elif(user_input == 1): self.list()
            elif(user_input == 2):
                url = input("Enter URL for the Youtube video: ")
                fileName = input("Enter FileName to save Video as(Default=None): ")
                fileName = None if fileName == "" else fileName
                savePath = input("Enter Save Path for the video(Default=None): ")
                savePath = None if savePath == "" else savePath
                print("Downloading...")
                status = self.download(url, fileName, savePath)
                print("Downloaded Successfully...") if status else print("Unable to download...")
            elif(user_input == 3):
                filePath = input("Enter File path for the list: ")
                if(filePath == ""):
                    print("File Path Cannot be None")
                    return 0
                savePath = input("Enter The Save Path for the file: ")
                savePath = None if savePath=="" else savePath
                self.downloadMultiple(filePath, savePath)
            elif(user_input == 4): 
                fileName = input("Enter File Name: ")
                self.open(fileName)
            elif(user_input == 5):
                fileName = input("Enter File Name: ")
                self.remove(fileName)
            elif(user_input == 99): self.menu()
            else: print("Invalid Input")