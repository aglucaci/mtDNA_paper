#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:21:56 2020

@author: Alexander G. Lucaci
"""

# =============================================================================
# Imports
# =============================================================================
import json, csv, os
import sys
import math

# =============================================================================
# Declares
# =============================================================================
# Path to directory holding the FEL fitter json files
path = "/Users/user/Documents/mtDNA_paper/data/FEL"

#Look for this ending.
file_ending = "FEL.json"
wrote_columns = False
# =============================================================================
# Helper functions
# =============================================================================

def read_json(filename, clade, gene):
    global wrote_columns
    #alphas = []
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    #end with

    
    MLE_Content =  json_data["MLE"]["content"]["0"]
    
    for n, item in enumerate(MLE_Content):
        #print(item[0])
        #try:
        alpha = item[0]
        if alpha == 0: alpha = 0.0001
        
        alpha = math.log10(alpha)
        
        #except: 
        #print(n, item)
            
        this_row = [clade, gene, str(n+1), str(alpha)] 
        writeto_csv(filename, this_row)
    #end for
    
#end method

# --- CSV --- #
def writeto_csv(filename, this_row):
    #file_output was set earlier based on the GENE
    global columns, wrote_columns, file_output
    #csv.writer(open(file_output, "a+"), delimiter=",") #MAC
    csv_writer = csv.writer(open(file_output, "a+"), delimiter=",", lineterminator='\n') #WINDOWS
    
    if wrote_columns == False:
        csv_writer.writerow(columns)
        wrote_columns = True
    #print([this_row])
    
    csv_writer.writerow(this_row)
#end method

# =============================================================================
# Main subroutine
# =============================================================================

files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(file_ending)]
print("## Starting ")
print("# --- details ---")
print()

print("# Found", str(len(files)), "files..")
print()

CLADES = []

#Make sure these are upper case
genes_dict = ["ATP6","ATP8", "COX1", "COX2", "COX3", "ND1", "ND2", "ND3", "ND5", "ND6", "CYTB", "ND4L"]

#Define columns for output csv
columns = ["Clade", "Gene", "Site_Number", "Alpha"]


for gene in genes_dict:
    wrote_columns = False
    
    # Create empty output file (csv)
    file_output = "mtdna_" + gene + "_alphas_log.csv"
    with open(file_output, "w") as f:
        f.write("")
    f.close()
    
    print("# Searching for files pertaining to gene:", gene)
    count = 0
    for n, file in enumerate(files):
    
    
        filename = file.split("/")[-1]
        if gene in filename.upper():
            count += 1
            #print(count, file)
            clade = filename.split("-")[0]
            print(count, clade.upper(), "\t\t\t", file)
            try:
                read_json(file, clade.upper(), gene)
            except:
                print("## ERROR")
                print(file, clade.upper(), gene)
                sys.exit(1)
        #end if
        # for Debugging
        #if count == 2: break
    #end inner for
    print()
#end outer for

# =============================================================================
# END OF FILE
# =============================================================================