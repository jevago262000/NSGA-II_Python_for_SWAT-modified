:: required
python "D:\GitHub\NSGA-II_Python_for_SWAT-modified\SWATModel\ExampleTest.py"
python "D:\GitHub\NSGA-II_Python_for_SWAT-modified\ExternalPythonScripts\CreateGlueFiles4VisualizationInSWAT-CUP.py"
python "D:\GitHub\NSGA-II_Python_for_SWAT-modified\ExternalPythonScripts\MoveGlueFilesInCorrespondingSWAT-CUPfolder.py"





:: required
::CALL Glue_pre.bat

:: required
::Glue06.exe






::
::
::
::
:: Remarks:
::
:: In this batch file the trk.txt file is initialized and all previous files in the GLUE.OUT are deleted before
:: starting a new run
::