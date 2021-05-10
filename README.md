# Covid_Data-withGUIOpt

This is the final product of the Covid data with a GUI  
#-If you want to use the GUI run the gui.py file 
#-IF you want to use CLI run the covid_main.py file  

This Python program:        
    · Read a config file to get the location of an excel file        
    · Read the excel file. The excel contains data with two columns: “date” and “iso”.  “date” is in “YYYY-MM-DD” format. “Iso” is the 3 digit ISO code of the country.        
    · Make an API request to https://covid-api.com/api/reports/ for each combination of date and iso in the excel        
    · Produce a table containing the following columns from parameters queried and the results returned: “date” “iso” “num_confirmed” “num_deaths” “num_recovered”        
    · Write the table to an excel on disk.        
    · The script should be production- ready (i.e. proper error handling, logging, read_me.txt and etc.)        
    · include script for unit testing.