:: required

python SWAT_ParameterEdit.py


:: required

swat.exe


:: required

::python Extract_rch.py
::GLUE_extract_rch.exe
::copy model_rch.out   model.out

GLUE_extract_hru.exe
copy model_hru.out   model.out
