# Covid_Data_ with GUI option
This is the final product of the Covid data with a GUI

## -If you want to use the GUI run the covid_gui_main.py file in the covid_GUI dir
## -IF you want to use CLI run the covid_main.py file in the covid_no_GUI dir
    ### -if you are using the CLI you will need to add a .yaml file with the file path like the below example
      e.g. excel_path: C:\Covid_Data-withGUIOpt\covid_base.xlsx
    ### -the input file will also need to be added to the same dir

## The out put excel file will be added to ..\Covid_Data-withGUIOpt\OUTPUT

This Python program can:

      · Read a config file to get the location of an excel file

      · Read the excel file. The excel contains data with two columns: “date” and “iso”.  “date” is in “YYYY-MM-DD” format. “Iso” is the 3 digit ISO code of the country.

      · Make an API request to https://covid-api.com/api/reports/ for each combination of date and iso in the excel

      · Produce a table containing the following columns from parameters queried and the results returned: “date” “iso” “num_confirmed” “num_deaths” “num_recovered”

      · Write the table to an excel on disk.

      · The script should be production- ready (i.e. proper error handling, logging, read_me.txt and etc.)

      · include script for unit testing.