# Chess-Tournament
Power Shell: commande = env/Scripts/Activate.ps1 (However, you might run into the following error when you try to run the script

venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies

You may use Set-Execution Policy to allow the current user to execute scripts as follows:

commande = Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser)

otherwise Git Bash (MINGW64):
commande = source env/Scripts/activate
