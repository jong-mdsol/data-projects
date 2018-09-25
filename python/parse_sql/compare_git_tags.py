"""
This module is intended to compare sql files in two tags in a git repository.

TAG1 should be an earlier git_tag.
TAG2 should be a later git_tag.

The results will return two dataframes with a special DDL column that shows
all DDL changes in the file.

DF_FILES_NEW_ALL
DF_FILES_CHANGED_ALL

Examples:
    compare_two_tags("v2017.2.0", "v2018.1.3")

"""
import urllib
import re
import pandas as pd
import sqlalchemy
import yaml
import db_ops

# Load the config yaml file
with open('config.yaml') as fp:
    MY_CONFIGURATION = yaml.load(fp)

# pyodbc connection PARAMS and ENGINE creation for later df to sql
DB_CONNECT_STRING = "DRIVER={%s};\
                     SERVER=%s;\
                     DATABASE=%s;\
                     UID=%s;\
                     PWD=%s" % (MY_CONFIGURATION['SQL_DRIVER'],
                                MY_CONFIGURATION['SQL_SERVER'],
                                MY_CONFIGURATION['SQL_DATABASE'],
                                MY_CONFIGURATION['SQL_LOGIN'],
                                MY_CONFIGURATION['SQL_PASSWORD'])
PARAMS = urllib.parse.quote_plus(DB_CONNECT_STRING)
ENGINE = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % PARAMS)
GIT_REPO = MY_CONFIGURATION['GIT_REPO_NAME']


def remove_empty_lists(the_list):
    """Remove empty lists removes any [] empty lists from a list of lists."""
    newlist = []
    # Loop over elements in list
    for i in the_list:
        # Is element a non-empty list? then call self on it.
        if isinstance(i, list) and i:
            newlist.append(remove_empty_lists(i))
        # If not a list.
        if not isinstance(i, list):
            newlist.append(i)
    return newlist


# Find all ddl statements in a sql string.
def process_ddl(file_content):
    """Search a file string and outputs all found DDL as list of lists."""
    # Procedures
    find = []
    find = find + re.findall(r"CREATE\s+PROCEDURE\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"DROP\s+PROCEDURE\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"CREATE\s+PROC\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"DROP\s+PROC\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"ALTER\s+PROCEDURE\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    # Views
    find = find + re.findall(r"CREATE\s+VIEW\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"DROP\s+VIEW\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"ALTER\s+VIEW\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    # Tables
    find = find + re.findall(r"CREATE\s+TABLE\s*[a-zA-Z0-9_\[\].#]+",
                             file_content, re.I)
    find = find + re.findall(r"DROP\s+TABLE\s*[a-zA-Z0-9_\[\].#]+",
                             file_content, re.I)
    # Select into
    find = find + re.findall(r"INTO\s*[a-zA-Z0-9_\[\].#]+\s+FROM",
                             file_content, re.I)
    regex = r"ALTER\s+TABLE\s*[a-zA-Z0-9_\[\].#]+\s+ALTER\s+COLUMN.*"
    find = find + re.findall(regex, file_content, re.I)
    find = find + re.findall(r"ALTER\s+TABLE\s*[a-zA-Z0-9_\[\].#]+\s+ADD.*",
                             file_content, re.I)
    # INTO\s+[a-zA-Z0-9_\[\].#]+\s+FROM.*
    # Functions
    find = find + re.findall(r"CREATE\s+FUNCTION\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"DROP\s+FUNCTION\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"ALTER\s+FUNCTION\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    # Types
    find = find + re.findall(r"CREATE\s+TYPE\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"DROP\s+TYPE\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"ALTER\s+TYPE\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    # Triggers
    find = find + re.findall(r"CREATE\s+TRIGGER\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"DROP\s+TRIGGER\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"ALTER\s+TRIGGER\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    # Indexes
    regex = r"CREATE\s+INDEX\s*[a-zA-Z0-9_\[\].]+\s+ON\s+[a-zA-Z0-9_\[\].#]+"
    find = find + re.findall(regex, file_content, re.I)
    regex = r"CREATE\s+CLUSTERED\s*INDEX\s*[a-zA-Z0-9_\[\].]+\s+ON\s+[a-zA-Z0-9_\[\].#]+"  # noqa
    find = find + re.findall(regex, file_content, re.I)
    regex = r"CREATE\s+NONCLUSTERED\s+INDEX\s*[a-zA-Z0-9_\[\].]+\s+ON\s+[a-zA-Z0-9_\[\].#]+"  # noqa
    find = find + re.findall(regex, file_content, re.I)
    regex = r"CREATE\s+UNIQUE\s+INDEX\s*[a-zA-Z0-9_\[\].]+\s+ON\s+[a-zA-Z0-9_\[\].#]+"  # noqa
    find = find + re.findall(regex, file_content, re.I)
    find = find + re.findall(r"DROP\s+INDEX\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    find = find + re.findall(r"ALTER\s+INDEX\s*[a-zA-Z0-9_\[\].]+",
                             file_content, re.I)
    # Rename objects
    find = find + re.findall(r"sp_rename\s*[@A-Za-z0-9'._= ]+,\s*[@A-Za-z0-9'._= ]+",  # noqa
                             file_content, re.I)
    # Remove any temp tables from list
    find = [item for item in find if "#" not in item]
    find = remove_empty_lists(find)
    return find


def read_tag_to_dataframe(git_repo, git_tag):
    """Pull git tag from parse_sql table into a dataframe."""
    queryx = "select full_path,\
              dir_path,\
              file_name,\
              file_content,\
              file_content_hash,\
              file_size,\
              git_repo,\
              git_tag\
              from parse_sql where git_tag = '{git_tag}'\
              and git_repo = '{git_repo}'"
    queryx = queryx.format(git_tag=git_tag, git_repo=git_repo)
    dfx = pd.read_sql(queryx, ENGINE)
    # Delete the second duplicate file_content_hash values from each dataframe.
    dfx = dfx.drop_duplicates(subset='file_content_hash', keep='first')
    # Remove directory paths not like Rave_Viper_Lucy_Merged_DB_Scripts
    string_contains = 'Rave_Viper_Lucy_Merged_DB_Scripts'
    dfx = dfx[dfx['dir_path'].str.contains(string_contains)]
    # Remove certain directory paths the ~ is the opposite result set
    dfx = dfx[~dfx['dir_path'].str.contains('tSQLt_UnitTests')]
    dfx = dfx[~dfx['dir_path'].str.contains('Samples')]
    dfx = dfx[~dfx['dir_path'].str.contains('SolarWinds')]
    dfx = dfx[~dfx['dir_path'].str.contains('Registry1')]
    dfx = dfx[~dfx['dir_path'].str.contains('TSDV DB Install Scripts')]
    return dfx


def save_diff_normalize_ddl(df_diff):
    """Take the difference dataframe after comparing two git tags and the ddl.

    Uses this dataframe to split the ddl list into separate rows.
    Inserts into the parse_sql_ddl table.
    """
    datalist = []
    for row in df_diff.itertuples():
        for single_ddl in row.ddl:
            object_info = ddl_object_name_type(single_ddl)
            datalist.append({'change_type': row.change_type,
                             'ddl': single_ddl,
                             'dir_path': row.dir_path,
                             'file_name': row.file_name,
                             'full_path': row.full_path,
                             'git_repo': row.git_repo,
                             'git_tag': row.git_tag,
                             'object_action': object_info[0],
                             'object_name': object_info[1],
                             'object_type': object_info[2]})
    df_ddl = pd.DataFrame(datalist)
    df_ddl.to_sql('parse_sql_ddl',
                  ENGINE,
                  if_exists='append',
                  index=False,
                  chunksize=1000,
                  dtype={'change_type': sqlalchemy.types.NVARCHAR(length=50),
                         'ddl':  sqlalchemy.types.NVARCHAR(),
                         'dir_path': sqlalchemy.types.NVARCHAR(),
                         'file_name': sqlalchemy.types.NVARCHAR(length=255),
                         'full_path': sqlalchemy.types.NVARCHAR(),
                         'git_repo': sqlalchemy.types.NVARCHAR(length=255),
                         'git_tag': sqlalchemy.types.NVARCHAR(length=255),
                         'object_action': sqlalchemy.types.NVARCHAR(length=50),
                         'object_name': sqlalchemy.types.NVARCHAR(length=255),
                         'object_type': sqlalchemy.types.NVARCHAR(length=255)})


def compare_all_tags(git_repo):
    """Read all tags, attempts ordering by date, runs compare_two_tags.

    Previous tag is determined by the order in the query.
    Excludes tags in git_tag_exclusions table.
    """
    queryx = ("SELECT gtd.git_repo \
              , gtd.git_tag \
              , gtd.git_tag_date \
              FROM git_tag_dates gtd \
              LEFT OUTER JOIN git_tag_exclusions gte \
              ON gtd.git_repo = gte.git_repo and gtd.git_tag = gte.git_tag \
              WHERE gte.git_tag is null \
              AND gtd.git_repo = '{git_repo}' \
              ORDER BY gtd.git_tag_date")
    queryx = queryx.format(git_repo=git_repo)
    df_all_tags = pd.read_sql(queryx, ENGINE)
    previous_tag = None
    for rowi in df_all_tags.itertuples():
        current_tag = rowi.git_tag
        print(previous_tag)
        print(current_tag)
        # print("Comparing tag %s to %s.") % (previous_tag, current_tag)
        compare_two_tags(git_repo, previous_tag, current_tag)
        previous_tag = current_tag
    return df_all_tags


def compare_two_tags(git_repo, git_tag1, git_tag2):
    """Compare all sql in two git tags to find new or changed files."""
    df1 = read_tag_to_dataframe(git_repo, git_tag1)
    df2 = read_tag_to_dataframe(git_repo, git_tag2)
    # Get 2 columns from each df.
    df1part = df1.loc[:, ['full_path',
                          'dir_path',
                          'file_name',
                          'file_content_hash']]
    df2part = df2.loc[:, ['full_path',
                          'dir_path',
                          'file_name',
                          'file_content_hash']]
    # Get list of unchanged files based on exact hash match.
    df2_unchanged = pd.merge(df2part,
                             df1part,
                             how='inner',
                             left_on=['file_content_hash'],
                             right_on=['file_content_hash'])
    df2_unchanged.columns = ['full_path',
                             'dir_path',
                             'file_name',
                             'file_content_hash',
                             'full_path_y',
                             'dir_path_y',
                             'file_name_y']
    df2_unchanged = df2_unchanged.drop(columns=['full_path_y'])
    df2_unchanged = df2_unchanged.drop(columns=['dir_path_y'])
    df2_unchanged = df2_unchanged.drop(columns=['file_name_y'])
    # Get list of new files only.
    # Left join on file_name.
    df2_new = pd.merge(df2part, df1part, how='left', on='file_name')
    # Only return rows where they did not exist in git_tag1.
    df2_new = df2_new.loc[df2_new.notna()['file_content_hash_y'] == 0]
    # Rename the columns after join and drop file_content_hash_y column.
    df2_new = df2_new.drop(columns=['full_path_y'])
    df2_new = df2_new.drop(columns=['dir_path_y'])
    df2_new = df2_new.drop(columns=['file_content_hash_y'])
    df2_new.columns = ['full_path',
                       'dir_path',
                       'file_name',
                       'file_content_hash']
    # Finally make sure does not exist in the files unchanged list
    df2_new = pd.merge(df2_new,
                       df2_unchanged,
                       how='left',
                       left_on=['file_content_hash'],
                       right_on=['file_content_hash'])
    df2_new = df2_new.loc[df2_new.notna()['file_name_y'] == 0]
    df2_new = df2_new.drop(columns=['file_name_y'])
    df2_new = df2_new.drop(columns=['full_path_y'])
    df2_new = df2_new.drop(columns=['dir_path_y'])
    df2_new.columns = ['full_path',
                       'dir_path',
                       'file_name',
                       'file_content_hash']
    # Get list of files changed only by removing unchanged and new files.
    # Exclude unchanged files first.
    df2_changed = pd.merge(df2part,
                           df2_unchanged,
                           how='left',
                           left_on=['file_content_hash'],
                           right_on=['file_content_hash'])
    df2_changed = df2_changed.loc[df2_changed.notna()['file_name_y'] == 0]
    df2_changed = df2_changed.drop(columns=['full_path_y'])
    df2_changed = df2_changed.drop(columns=['dir_path_y'])
    df2_changed = df2_changed.drop(columns=['file_name_y'])
    df2_changed.columns = ['full_path',
                           'dir_path',
                           'file_name',
                           'file_content_hash']
    # Exclude new files.
    df2_changed = pd.merge(df2_changed,
                           df2_new,
                           how='left',
                           left_on=['file_content_hash'],
                           right_on=['file_content_hash'])
    df2_changed = df2_changed.loc[df2_changed.notna()['file_name_y'] == 0]
    df2_changed = df2_changed.drop(columns=['full_path_y'])
    df2_changed = df2_changed.drop(columns=['dir_path_y'])
    df2_changed = df2_changed.drop(columns=['file_name_y'])
    df2_changed.columns = ['full_path',
                           'dir_path',
                           'file_name',
                           'file_content_hash']
    # Join back to the original df2.
    df2_changed['change_type'] = "modified"
    df2_new['change_type'] = "new"
    # Combine dataframe of new and modified files
    df2_diff = df2_new.append(df2_changed, ignore_index=True)
    df2_diff_all = pd.merge(df2_diff, df2, how='inner')
    df2_diff_all['ddl'] = ""
    for index2, row2 in df2_diff_all.iterrows():
        # Read file contents, set ddl column to list of all ddl statements.
        df2_diff_all.at[index2, 'ddl'] = process_ddl(row2['file_content'])
        print(row2['full_path'])
        print(df2_diff_all.loc[index2, 'ddl'])
    df2_diff_all = df2_diff_all.drop(columns=['file_content'])
    df2_diff_all = df2_diff_all.drop(columns=['file_content_hash'])
    df2_diff_all = df2_diff_all.drop(columns=['file_size'])
    # Normalize the ddl column from and save the results to parse_sql_ddl.
    save_diff_normalize_ddl(df2_diff_all)
    return df2_diff_all


def ddl_object_name_type(ddl_string):
    """Return object_action, object name, object type as a tuple."""
    ddl_string = re.sub(r'\[dbo\]\.', '', ddl_string, flags=re.I)
    ddl_string = re.sub(r'dbo\.', '', ddl_string, flags=re.I)
    ddl_string = re.sub(r'\bNONCLUSTERED\b', '',
                        ddl_string,
                        flags=re.I)
    ddl_string = re.sub(r'\bCLUSTERED\b', '', ddl_string, flags=re.I)
    ddl_string = re.sub(r'\bUNIQUE\b', '', ddl_string, flags=re.I)
    select_into = False  # used to determine if this is a select into statement
    # First, identify the object ddl action.
    object_action = re.search(r"(\bcreate\b|\balter\b|\bdrop\b|\bsp_rename\b)",
                              ddl_string,
                              re.I)
    # If no create, alter, drop, or sp_rename found in DDL statement
    if object_action is None:  # select into case
        object_action = re.search(r"INTO\s+[a-zA-Z0-9_\[\].#]+\s+FROM",
                              ddl_string,
                              re.I)
        if object_action is not None:
            select_into = True
            object_action = "CREATE"
    else:  # create, alter, drop, sp_rename case
        object_action = object_action.group(0).upper()
        ddl_string = re.sub(r'\b%s\b' % object_action,
                            '',
                            ddl_string,
                            flags=re.I)
    if object_action is not None:
        object_action = object_action.upper()
    # Next, identify the object type.
    # sp_rename could be any object type so we can't be sure.
    if object_action == 'SP_RENAME':
        object_type = None
    elif select_into:
        object_type = "TABLE"
    else:
        object_type = re.search(r"[A-Za-z0-9]+", ddl_string, re.I).group(0)
        ddl_string = re.sub(r'\b%s\b' % object_type,
                            '',
                            ddl_string,
                            flags=re.I)
        object_type = re.sub(r'\bproc\b',
                             'PROCEDURE',
                             object_type,
                             flags=re.I)
    if object_type is not None:
            object_type = object_type.upper()
    # Lastly, identify the object name if possible.
    # SP_RENAME condition.
    if object_action == "SP_RENAME":
        print("In SP_RENAME loop")
        object_name = re.search(r"@newname[\s]*=[\s]*[N]*'[a-zA-Z0-9_\.']+",
                                ddl_string, re.I)
        if object_name is None:
            object_name = re.search(r",\s*N*'*[a-zA-Z0-9_]+",
                                    ddl_string,
                                    re.I)
    # CREATE, ALTER, DROP condition.
    else:
        # Replace word "into" if this is a select into x from ddl create table.
        ddl_string = re.sub(r'\binto\b',
                             '',
                             ddl_string,
                             flags=re.I)
        object_name = re.search(r"[\S]+", ddl_string, re.I)
    if object_name is not None:
        object_name = object_name.group(0)
        # Replace =N'
        object_name = re.sub("[=\s]+N'", "", object_name, flags=re.I)
        # Replace ='
        object_name = re.sub("[=\s]+'", "", object_name, flags=re.I)
        # Replace @newname
        object_name = re.sub(r'@newname[\s]*', '',
                             object_name, flags=re.I)
        # Replace other single characters ,' [ ]
        object_name = re.sub(r",", "", object_name, flags=re.I)
        object_name = re.sub(r"'", "", object_name, flags=re.I)
        object_name = re.sub(r"\[", "", object_name, flags=re.I)
        object_name = re.sub(r"\]", "", object_name, flags=re.I)
        object_name = object_name.strip()

    obj_info = (object_action,
                object_name,
                object_type)
    return obj_info


if __name__ == "__main__":
    db_ops.truncate_sql_table(DB_CONNECT_STRING, "parse_sql_ddl")
    # DF_DIFF = compare_two_tags(GIT_REPO, "v2017.2.0", "v2018.1.3")
    DF_ALL_TAGS = compare_all_tags(GIT_REPO)