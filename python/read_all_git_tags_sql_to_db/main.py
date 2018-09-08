import urllib
from sqlalchemy import create_engine
import git
#custom module read_sql_files need to add to PYTHONPATH in Spyder IDE > Tools > "PYTHONPATH Manager" to GitHub\data-projects\python\lib\site-packages
import read_sql_files

#pyodbc connection params and engine creation for later df to sql
params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};SERVER=localhost,2017;DATABASE=schema_changes;UID=python_user;PWD=python_user")
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

#directory where the .sql files are
var_directory_to_sql = 'C:\\Users\\jong\\Documents\\GitHub\\Rave\\Medidata 5 RAVE Database Project'
#grab the current git tag from repo
var_directory_git_repo = 'C:\\Users\\jong\\Documents\\GitHub\\Rave'
repo = git.Repo(var_directory_git_repo)
g = git.Git(var_directory_git_repo)

#pull current tag if necessary
#current_tag = str(next((tag for tag in repo.tags if tag.commit == repo.head.commit), None))
first_run = True
for tag in repo.tags:
    g.clean('-xdf')
    g.checkout(tag)
    df = read_sql_files.read_sql_files_to_dataframe(var_directory_to_sql)
    df["tag"] = str(tag)

    if first_run == True:
        #write the dataframe to new table the first time
        df.to_sql('develop_branch_sql',engine,if_exists='replace')
        first_run = False
    else:
        #after the first time append to the table
        df.to_sql('develop_branch_sql',engine,if_exists='append')
