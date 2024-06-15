echo OFF
"C:\Users\EEIA\AppData\Local\Programs\Python\Python310\python.exe" -m venv envYolo
echo.
echo -------------------------------------------------------------------------------------
echo ------------------------- ENV "envYolo" Sucessfully created------------------
echo -------------------------------------------------------------------------------------
echo.

CALL envYolo\Scripts\activate.bat
echo -------------------------------------------------------------------------------------
echo ------------------------- "envYolo" Sucessfully Activated -------------------
echo -------------------------------------------------------------------------------------
echo.

for %%x in (packages_tools\*.*) do python -m pip install --no-index --no-deps --upgrade %%x

echo.
echo -------------------------------------------------------------------------------------
echo ------------------------- Sucessfully install "packages tools" ----------------
echo -------------------------------------------------------------------------------------
echo.

for %%x in (yolov5-master\*.*) do python -m pip install --no-index --no-deps --upgrade %%x

echo.
echo -------------------------------------------------------------------------------------
echo ------------------------- Sucessfully install "requirementstxt" ----------------
echo -------------------------------------------------------------------------------------
echo.


PAUSE

