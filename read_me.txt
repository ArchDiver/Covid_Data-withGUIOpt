Please make sure all relevant Excel documents are in the same folder as the program.

(optional)
    To Run in a Virtual Enviornment (keeps the installs from being global):
      In the command line on windows:
      > pip install virtualenv
      > mkdir venv && virtualenv venv/
      > venv\Scripts\activate.bat

    When you are DONE running and want to LEAVE the virtual Environment:
      >deactivate

!REQUIRED!
  Wether you use a Virtual Environment or not you MUST load the requirements to run the program:
    In the command line on windows:
    > pip install -r requirements.txt

#-If you want to use the GUI run the gui.py file
#-IF you want to use CLI run the covid_main.py file
    -if you are using the CLI you will need to add a .yaml file with the file path like the below example
      e.g. excel_path: C:\Covid_Data-withGUIOpt\covid_base.xlsx
    -the input file will also need to be added the same dir

The out put excel file will be added to ..\Covid_Data-withGUIOpt\OUTPUT
