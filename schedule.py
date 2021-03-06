from tabulate import tabulate
import pandas as pd
import datetime
import os, pdb

# Initial Variables
user_name = 'Kevin Mathews'
os_type = 'Linux'

# find data_folder given OS
if os_type == 'Windows':
	# location of data windows
	data_folder = '\\'.join(os.path.abspath(__file__).split('\\')[:~1]) + '\\'
else:
	# location of data linux
	data_folder = '/'.join(os.path.abspath(__file__).split('/')[:~1]) + '//'

# function to print available commands
def print_commands():
	print('\nAvaliable Commands:')
	print('functions: print_normal(), print_school(), print_data(df_name), terminate_prog()')
	print('data: df_dict, processed_dict, tomorrowpad_dict, available_dfs, get_raw_data(df_name), tomorrowpad_keys(), write_sorted_data()')

# function to apply correct class given table name
def create_table(df, df_name, file_name, date_str):
    table_type_dict = {'Normal Table':[''], # default table
                       'Bills Table':['[Bills Monthly]',
                                      '[Bills Yearly]',
                                      '[Bills Auto]'],
                       'Birthday Table':['[Scheduled Birthdays]',
                                         '[Scheduled Holidays]'],
                       'Event Table':['[Normal Events]'],
                       'Weekly Event Table':['[Scheduled Daily]'],
                       'Small Tasks Table':['[To Do List]',
                                            '[To Do Alerts]',
                                            '[To Do Buy]',
                                            '[To Do Groceries]']}

    # detect type of data stored in dataframe
    def detect_table(df_name, table_type_dict=table_type_dict):
        # https://jaxenter.com/implement-switch-case-statement-python-138315.html
        # cycle through dictionary and find table type
        out_type = list(table_type_dict.keys())[0]
        for table_type in table_type_dict.keys():
            table_list = table_type_dict.get(table_type)
            if df_name in table_list:
                out_type = table_type
        return out_type

    table_type = detect_table(df_name)
    if table_type == 'Normal Table':
        table_obj = normal_table(df, df_name, file_name, date_str)

    if table_type == 'Small Tasks Table':
        table_obj = small_tasks(df, df_name, file_name, date_str)

    if table_type == 'Bills Table':
        table_obj = bills_table(df, df_name, file_name, date_str)

    if table_type == 'Birthday Table':
        table_obj = birthday_table(df, df_name, file_name, date_str)

    if table_type == 'Event Table':
        table_obj = event_table(df, df_name, file_name, date_str)

    if table_type == 'Weekly Event Table':
        table_obj = weekly_event_table(df, df_name, file_name, date_str)

    return table_obj

# Table Blueprints
class tomorrow_pad:

    def padprint(self):
        output_df = self.dict.get(self.date_str)

        if output_df is None:
            output_df = pd.DataFrame(['None'])
        else:
            output_df = ' - ' + output_df

        return output_df

    def padkeys(self):
        return sorted(self.dict.keys(), reverse=True)

    def __init__(self, tomorrowpad_dict, file_name, date_str):
        self.dict = tomorrowpad_dict; self.date_str = date_str
        self.table_type = 'Tomorrowpad'
        self.file_name = file_name

class normal_table:

    # Step 1
    def sort_data(self):
        self.df_sorted = self.df.sort_values(['Done','Start','End'], ascending=[True, False, False])
        self.df_hr = self.df_sorted.copy()

    # Step 2
    # function to filter dataframe to relevant items
    def filter_data(self):
        df = self.df_hr.copy()
        date_str = self.date_str

        #df = self.df_sorted
        threshold_days = 30
        cols = self.clean_cols

        # sort to in progress items only
        df = df[df['Done'] == '0']

        for col_list in cols:
            cur_col = col_list[0]
            if cur_col == 'Start':

                # determine threshold
                threshold_date_str = threshold_date(date_str, threshold_days)

                # sort dataframe
                df = df[df[cur_col] <= threshold_date_str]

        self.df_hr = df.copy()

    # Step 3
    # add and drop needed columns from dataframe
    def process_data(self):
        df = self.df_hr.copy()
        date_str = self.date_str

        def gen_flag(diff_str, current_date):
            if diff_str < 0:
                out_str = 'LATE'
            elif diff_str == 0:
                out_str = 'TODAY'
            else:
                out_str = ''

            return out_str

        df.reset_index(drop=True, inplace=True)

        df.sort_values('Start', ascending=True, inplace=True)
        df.drop('Done', axis=1, inplace=True) # drop done column

        # Unique code for normal events
        df['Diff'] = df['End'].apply(gen_date_difference, args=(date_str,))
        df['Flag'] = df['Diff'].apply(gen_flag, args=(date_str,))
        df['Flag'] = df['Flag'].replace('nan','')

        self.df_hr = df.copy()[['Flag','Diff','Start','End','Item']]

    # Step 4
    # function to convert dataframe information to human readable format
    def clean_data(self):
        df = self.df_hr.copy()
        cols = self.clean_cols

        for col_list in cols:
            cur_col = col_list[0]
            cur_func = col_list[1]

            if cur_func == 'time':
                df[cur_col] = df[cur_col].apply(time_string)
            elif cur_func == 'mmmdd':
                df[cur_col] = df[cur_col].apply(date_mmmdd)
            elif cur_func == 'weekday':
                df[cur_col] = df[cur_col].apply(gen_date_string_yymmdd)
            else: # apply mmmdd
                df[cur_col] == df[cur_col].apply(date_mmmdd)

        self.df_hr = df.copy()

    # check to make sure dataframe is not empty
    def finalize_data(self):
        df = self.df_hr.copy()

        if df.shape[0] == 0:
            df = pd.DataFrame(['None'])
        else:
            pass

        self.df_hr = df.copy()

    def __init__(self, df, df_name, file_name, date_str):
        self.df = df; self.df_name = df_name; self.file_name = file_name; self.date_str = date_str
        self.table_type = 'Normal Table'
        self.clean_cols = [['Start','mmmdd'],['End','mmmdd']]

        # sort for writing later
        self.sort_data()

        # create human readable data
        self.filter_data()
        self.process_data()
        self.clean_data()
        self.finalize_data()

class small_tasks(normal_table):

    def sort_data(self):
        self.df_sorted = self.df.sort_values(['Done','Start'], ascending=[True, False])
        self.df_hr = self.df_sorted.copy()

    def process_data(self):
        df = self.df_hr.copy()
        date_str = self.date_str
        df.reset_index(drop=True, inplace=True)

        df.sort_values('Start', ascending=True, inplace=True)
        df.drop('Done', axis=1, inplace=True) # drop done column

        # Unique code for normal events
        df['Diff'] = df['Start'].apply(gen_date_difference, args=(date_str,))

        self.df_hr = df.copy()[['Diff','Start','Item']]

    def __init__(self, df, df_name, file_name, date_str):
        self.df = df; self.df_name = df_name; self.file_name = file_name; self.date_str = date_str
        self.table_type = 'Small Tasks Table'
        self.clean_cols = [['Start','mmmdd']]

        # sort for writing later
        self.sort_data()

        # create human readable data
        self.filter_data()
        self.process_data()
        self.clean_data()
        self.finalize_data()

class event_table(normal_table):

    def sort_data(self):
        self.df_sorted = self.df.sort_values(['Done','Day'], ascending=[True, False])
        self.df_hr = self.df_sorted.copy()

    def filter_data(self):
        df = self.df_hr.copy()
        date_str = self.date_str
        cols = self.clean_cols

        threshold_days = 30

        # sort to in progress items only
        df = df[df['Done'] == '0']

        for col_list in cols:
            cur_col = col_list[0]
            if cur_col == 'Day':

                # determine threshold
                threshold_date_str = threshold_date(date_str, threshold_days)

                # sort dataframe
                df = df[df[cur_col] <= threshold_date_str]

        self.df_hr = df.copy()

    # add and drop needed columns from dataframe
    def process_data(self):
        df = self.df_hr.copy()
        date_str = self.date_str

        def gen_flag(diff_str, current_date):
            if diff_str < 0:
                out_str = 'LATE'
            elif diff_str == 0:
                out_str = 'TODAY'
            else:
                out_str = ''

            return out_str

        df.reset_index(drop=True, inplace=True)

        df.sort_values(['Day','Time'], ascending=[True, True], inplace=True)
        df.drop('Done', axis=1, inplace=True) # drop done column

        # Unique code for normal events
        df['Diff'] = df['Day'].apply(gen_date_difference, args=(date_str,))
        df['Flag'] = df['Diff'].apply(gen_flag, args=(date_str,))
        df['Flag'] = df['Flag'].replace('nan','')

        self.df_hr = df.copy()[['Flag','Diff','Day','Time','Item']]

    def __init__(self, df, df_name, file_name, date_str):
        self.df = df; self.df_name = df_name; self.file_name = file_name; self.date_str = date_str
        self.table_type = 'Event Table'
        self.clean_cols = [['Day','weekday'],['Time','time']]

        # sort for writing later
        self.sort_data()

        # create human readable data
        self.filter_data()
        self.process_data()
        self.clean_data()
        self.finalize_data()

class birthday_table(normal_table):

    def sort_data(self):
        self.df_sorted = self.df.sort_values('Day', ascending=True)
        self.df_hr = self.df_sorted.copy()

    # generate finalized dataframe (birthdays)
    def filter_data(self):

        df = self.df_hr.copy()
        date_str = self.date_str

        # add year to Day column
        df['Day'] = date_str[0:2] + df['Day']

        # get 30 day threshold
        threshold_date_str = threshold_date(date_str, 30)

        # get 15 day previous threshold
        previous_date_str = threshold_date(date_str, -15)

        # sort df to next month of birthdays
        df = df[(df['Day']>previous_date_str) & (df['Day']<threshold_date_str)].copy()

        self.df_hr = df.copy()

    # add and drop needed columns from dataframe
    def process_data(self):
        df = self.df_hr.copy()
        date_str = self.date_str

        def gen_flag(diff_str, current_date):
            if diff_str < 0:
                out_str = 'PAST'
            elif diff_str == 0:
                out_str = 'TODAY'
            else:
                out_str = ''

            return out_str

        df.reset_index(drop=True, inplace=True)

        df.sort_values(['Day'], ascending=True, inplace=True)

        # Unique code for normal events
        df['Diff'] = df['Day'].apply(gen_date_difference, args=(date_str,))
        df['Flag'] = df['Diff'].apply(gen_flag, args=(date_str,))
        df['Flag'] = df['Flag'].replace('nan','')

        self.df_hr = df.copy()[['Flag','Diff','Day','Name']]

    def __init__(self, df, df_name, file_name, date_str):
        self.df = df; self.df_name = df_name; self.file_name = file_name; self.date_str = date_str
        self.table_type = 'Birthday Table'
        self.clean_cols = [['Day','weekday']]

        # sort for writing later
        self.sort_data()

        # create human readable data
        self.filter_data()
        self.process_data()
        self.clean_data()
        self.finalize_data()

class bills_table(normal_table):
    def sort_data(self):
        self.df_sorted = self.df.sort_values(['Due'], ascending=True)
        self.df_hr = self.df_sorted.copy()

    def process_data(self):
        df = self.df_hr.copy()
        date_str = self.date_str
        date_obj = convert_date(date_str)

        year_str = str(date_obj.year)[2:]
        month_str = date_obj.month

        def gen_flag(diff_str, current_date):
            if diff_str < 0:
                out_str = 'PAST DUE'
            elif diff_str == 0:
                out_str = 'TODAY'
            else:
                out_str = ''

            return out_str

        if self.df_name == '[Bills Yearly]':
            df['Current_Due'] = year_str + df['Due']
            #df['Due'] = year_str + df['Due']

            for idx, row in df.iterrows():

                if int(row['Last']) >= int(year_str + row['Due']): # is the bill paid?
                    year_str = str(int(date_obj.year) + 1)[2:]
                    df.loc[idx,'Due'] = year_str + row['Due']
                else: # if not the bill is due in the current year
                    year_str = str(int(date_obj.year))[2:]
                    df.loc[idx,'Due'] = year_str + row['Due']

                year_str = str(date_obj.year)[2:]
                month_str = date_obj.month

            # drop done column
            df.drop('Current_Due', axis=1, inplace=True)

        elif self.df_name == '[Bills Auto]':
            df['Last'] = year_str + str(month_str).zfill(2) + df['Due']

            month_str += 1
            if month_str > 12:
                month_str = 1

            df['Due'] = year_str + str(month_str).zfill(2) + df['Due']

            #month_str = str(month_str).zfill(2)
            #df['Due'] = year_str + month_str + df['Due']

        elif self.df_name == '[Bills Monthly]':
            #df['Last'] = year_str + str(month_str).zfill(2) + df['Due']
            df['Last_Due'] = year_str + str(month_str).zfill(2) + df['Due']

            month_str += 1
            if month_str > 12:
                month_str = 1

            month_str = str(month_str).zfill(2)
            #df['Due'] = year_str + month_str + df['Due']
            df['Due'] = year_str + str(month_str).zfill(2) + df['Due']

            for idx, row in df.iterrows():
                last_paid = row['Last']
                last_due = row['Last_Due']

                if last_paid < last_due:
                    df.loc[idx, 'Due'] = last_due

        else: # bills monthly, bills auto
            #df['Last'] = year_str + str(month_str).zfill(2) + df['Due']

            month_str += 1
            if month_str > 12:
                month_str = 1

            month_str = str(month_str).zfill(2)
            df['Due'] = year_str + month_str + df['Due']

        df.reset_index(drop=True, inplace=True)
        df.sort_values('Due', ascending=True, inplace=True)

        # Unique code for normal events
        df['Diff'] = df['Due'].apply(gen_date_difference, args=(date_str,))
        df['Flag'] = df['Diff'].apply(gen_flag, args=(date_str,))
        df['Flag'] = df['Flag'].replace('nan','')

        # alter date
        #df['Due'] = df['Due'].apply(gen_date_string_yymmdd)
        df['Due'] = df['Due'].apply(date_mmmdd)
        df['Last Paid'] = df['Last'].apply(date_mmmdd)

        df['Amt'] = '$' + df['Amt']
        df = df[['Flag','Diff','Due','Last Paid','Item','Amt']]

        self.df_hr = df.copy()

    def __init__(self, df, df_name, file_name, date_str):
        self.df = df; self.df_name = df_name; self.file_name = file_name; self.date_str = date_str
        self.table_type = 'Bills Table'

        # sort for writing later
        self.sort_data()
        self.process_data()

class weekly_event_table(normal_table):

    def sort_data(self):
        self.df_sorted = self.df.sort_values(['Start'], ascending=True)
        self.df_hr = self.df_sorted.copy()

    def __init__(self, df, df_name, file_name, date_str):
        self.df = df; self.df_name = df_name; self.file_name = file_name; self.date_str = date_str
        self.table_type = 'Weekly Event Table'
        self.clean_cols = [['Start','mmmdd'],['End','mmmdd']]

        # sort for writing later
        self.sort_data()

# print data from specific dataframe
def get_raw_data(df_name, available_dfs, df_dict):
    file_name =  available_dfs[available_dfs[0].str.contains(df_name)][1].iloc[0]
    df_name = available_dfs[available_dfs[0].str.contains(df_name)][0].iloc[0]
    df_out = df_dict.get(file_name).get(df_name)
    return df_out

# generate table string
def table_string(df, format_str='plain'): # simple plain

    if df.shape[1] == 1 and df.shape[0] == 1 and df.iloc[0,0] == 'None': # df.shape[1] == 1 or
        return 'None' #tabulate(pd.DataFrame(['None']), showindex=False, tablefmt=format_str)

    #return tabulate(df, showindex=False, tablefmt=format_str)
    return tabulate(df, headers="keys", showindex=False, tablefmt=format_str)

# print dataframe using tabulate
def table_print(df):
    print(table_string(df))

# function to clear and end program
def terminate_prog():
    clear()
    exit()

def current_time():
    now = datetime.datetime.now()
    #output = now.weekday()
    return now.strftime("%H%M")

def current_date():
    now = datetime.datetime.now() - datetime.timedelta(hours=5)
    #output = now.weekday()
    return now.strftime("%y%m%d")

# function to generate weekday string
def gen_date_string(date_obj):
    weekday = date_obj.strftime("%w")

    weekday_dict = {'0':'Sunday',
		    '1':'Monday',
		    '2':'Tuesday',
		    '3':'Wednesday',
		    '4':'Thursday',
		    '5':'Friday',
		    '6':'Saturday'}

    out_string = ''
    out_string += weekday_dict.get(weekday) + date_obj.strftime(", %B %d %Y %H:%M")
    return out_string

# function to generate weekday string
def gen_date_string_yymmdd(date_str):
    date_obj = datetime.datetime.strptime(date_str, '%y%m%d')
    return gen_date_string(date_obj)[:~5]

# function to generate weekday string
def gen_date_difference(date_str, current_date_str):
    date_obj_1 = datetime.datetime.strptime(date_str, '%y%m%d')
    date_obj_2 = datetime.datetime.strptime(current_date_str, '%y%m%d')
    return (date_obj_1 - date_obj_2).days

def print_date_string(input_string):
    #now = datetime.datetime.now() - datetime.timedelta(hours=5)
    #out_string = ''
    #out_string += append_head
    #out_string += gen_date_string_yymmdd(date_str)
    #out_string += append_tail
    out_string = '-'*len(input_string) + '\n' + input_string + '\n' + '-'*len(input_string)
    return out_string

def print_date(input_string):
    out_string = print_date_string(input_string)
    #out_string = 'Schedule Assistant for ' + user_name + ':' + '\n' + out_string
    print(out_string)

# convert YYMMDD to datetime object
def convert_date(date_string):
    # https://stackabuse.com/converting-strings-to-datetime-in-python/
    date_time_obj = datetime.datetime.strptime(date_string, '%y%m%d')
    return date_time_obj

# calculate a date relative to supplied date
def threshold_date(date_string, threshold):
    date_time_obj = convert_date(date_string)
    date_time_obj = date_time_obj + datetime.timedelta(days=threshold)
    return date_time_obj.strftime("%y%m%d")

# clean six digit date information MM/DD/YY
def date_mmddyy(date_text):
    #get numbers
    year_num = date_text[:2]
    month_num = date_text[2:4]
    day_num = date_text[4:]
    year_num = "20" + year_num

    output = str(month_num + "/" + day_num + "/" + year_num)
    return output

# clean six digit date information MMM-DD
def date_mmmdd(date_text):
    #get numbers
    year_num = date_text[:2]
    month_num = date_text[2:4]
    day_num = date_text[4:]
    year_num = "20" + year_num

    month_dict = {'01':'Jan',
                  '02':'Feb',
                  '03':'Mar',
                  '04':'Apr',
                  '05':'May',
                  '06':'Jun',
                  '07':'Jul',
                  '08':'Aug',
                  '09':'Sep',
                  '10':'Oct',
                  '11':'Nov',
                  '12':'Dec'}

    month_text = month_dict.get(str(month_num))

    output = month_text + '-' + str(day_num) + '-' + str(year_num[2:])
    return output

# function to create time string
def time_string(time_text):
    hour_num = time_text[:2]
    min_num = time_text[2:]

    output = str(hour_num) + ':' + str(min_num)
    return output

# function to read file for tomorrowpad data
def load_data_tomorrowpad(tomorrow_file, tomorrow_folder):

    # generate finalized dataframe (tomorrowpad)
    def load_tomorrowpad(text_file):

        out_list = read_tomorrowpad(open(text_file))

        tomorrow_dict = {}
        for df in out_list[1:]:
            mid_list = interperet_tomorrowpad(df)
            tomorrow_dict[mid_list[0]] = mid_list[1]

        return tomorrow_dict

    # read textfile into list of dataframes
    def read_tomorrowpad(data):

        # read text data in
        data_list = data.readlines()
        data_df = pd.DataFrame(data_list)

        # remove carriage returns
        data_df[0] = data_df[0].str.replace('\r','')

        # determine available dataframes
        index_list = data_df[data_df[0].str.contains('^\d\d\d\d\d\d\n', regex=True)].index.tolist() # locate newlines in data
        index_list = [0] + index_list # add an initial zero

        pair_list = []
        # determine available pairs
        for i in range(0,len(index_list)-1): # intitial pairs
            pair = [index_list[i], index_list[i+1]-1]
            pair_list.append(pair)

        # last pair
        last_pair = [index_list[~0],]
        pair_list = pair_list + last_pair

        # gather all dataframes into list
        df_list = []
        for i in pair_list:
            try:
                data_filter = data_df.iloc[i[0]:i[1]]
            except:
                data_filter = data_df.iloc[i:]

            df_list.append(data_filter)

        return df_list

    # interperet schedule dataframe
    def interperet_tomorrowpad(data):

        # remove all newlines from data
        data = pd.DataFrame(data[0].str.replace('\n',''))

        # remove blank lines
        data = data[data[0]!='']

        # get title
        df_title = data.iloc[0].values[0]

        # get data
        df_data = data.iloc[1:]

        return [df_title, df_data]

    # print today's tomorrowpad
    tomorrowpad_dict = load_tomorrowpad(os.path.join(tomorrow_folder, tomorrow_file))
    return tomorrowpad_dict

# function to read files for normal data
def load_data_normal(text_file_list, data_folder):

    # populate dictionary with dataframes
    def pop_dict(text_file, data_folder):
        df_dict = {}
        df_list = read_textfile(open(data_folder + text_file))
        for i in df_list:
            data = interperet_df(i)
            #print(text_file, data[0], data[1].shape)
            df_dict[data[0]] = data[1]

        return df_dict

    # read textfile into list of dataframes
    def read_textfile(data, type='normal'):
        # read text data in
        data_list = data.readlines()

        if data_list[~0] == '\n':
            data_list = data_list[:~0]

        data_df = pd.DataFrame(data_list)

        # remove carriage returns
        data_df[0] = data_df[0].str.replace('\r','')

        # determine available dataframes
        index_list = data_df[data_df[0]=='\n'].index.tolist() # locate newlines in data

        index_list = [0] + index_list # add an initial zero

        pair_list = []
        # determine available pairs
        for i in range(0,len(index_list)-1): # intitial pairs
            pair = [index_list[i], index_list[i+1]]
            pair_list.append(pair)

        # last pair
        last_pair = [index_list[~0],]
        pair_list = pair_list + last_pair

        # gather all dataframes into list
        df_list = []
        for i in pair_list:
            try:
                data_filter = data_df.iloc[i[0]:i[1]]
            except:
                data_filter = data_df.iloc[i:]

            df_list.append(data_filter)

        return df_list

    # interperet schedule dataframe
    def interperet_df(data):
        # remove all newlines from data
        data = pd.DataFrame(data[0].str.replace('\n',''))

        # remove blank lines
        data = data[data[0]!='']

        # get title
        df_title = data.iloc[0].values[0]

        # get header
        df_header = data.iloc[1].values[0].split(' ')

        # get data
        df_data = data.iloc[2:]

        # split columns by header
        df_data = df_data[0].str.split(' ',n=len(df_header)-1, expand=True)

        # set column
        df_data.columns = df_header

        return [df_title, df_data]

    df_dict = {}
    for i in text_file_list:
        df_dict[i] = pop_dict(i, data_folder)

    return df_dict

# read df dict for available data
def get_dfs(df_dict):
    available_dfs = pd.DataFrame()
    file_names = list(df_dict.keys())
    for file_name in file_names:
        df_keys = list(df_dict.get(file_name).keys())
        for i in df_keys:
            #available_dfs = available_dfs.append([i, file_name])
            available_dfs = pd.concat([available_dfs, pd.DataFrame([i,file_name]).T])
    available_dfs = available_dfs.reset_index(drop=True)
    available_dfs.columns = ['dataframe','filename']
    return available_dfs

# function to write sorted data to files
def write_sorted_data(available_dfs, processed_dict):

    file_list = available_dfs['filename'].sort_values().drop_duplicates().tolist()
    for file_name in file_list:
        table_list = available_dfs[available_dfs['filename']==file_name]['dataframe'].tolist()
        output_string = ''
        for table_name in table_list: # file name
            mid_obj = processed_dict.get(table_name)
            assert file_name == mid_obj.file_name
            mid_df = mid_obj.df_sorted # data table

            # Create output string
            col_titles = [i for i in mid_df]
            output_df = mid_df[col_titles[0]] + ' ' + mid_df[col_titles[1]]

            # iterate through dataframe columns to create string
            for i in range(2, len(col_titles)):
                output_df = output_df + ' ' + mid_df[col_titles[i]]

            output_string = output_string + table_name + '\n' + ' '.join(col_titles) + '\n'
            output_string = output_string + '\n'.join(output_df.tolist()) + '\n\n'

        text_file = open(data_folder + file_name, "w")
        text_file.write(output_string)
        text_file.close()
        #print('printed:', file_name)'

    print('data sorted.')

# clear interpereter
clear = lambda: os.system('clear')

# Main Loop
print('loading data...')

# initial data
current_date_str = current_date()

# load tomorrowpad file
tomorrow_pad_name = '00_tomorrowpad.txt'
tomorrowpad_dict = load_data_tomorrowpad(tomorrow_pad_name, data_folder)

# load dataframes in text files
text_file_list = os.listdir(data_folder)
text_file_list = [i for i in text_file_list if '.txt' in i]
text_file_list.remove(tomorrow_pad_name)
df_dict = load_data_normal(text_file_list, data_folder)

# generate df index
available_dfs = get_dfs(df_dict)

# generate tomorrowpad object
tomorrowpad_obj = tomorrow_pad(tomorrowpad_dict, tomorrow_pad_name, current_date_str)

# generate table object for each dataframe & add to sorted dict
processed_dict = {}
for idx, row in available_dfs.iterrows():
    file_name = row.loc['filename']
    df_name = row.loc['dataframe']

    # get current table
    df_mid = df_dict.get(file_name).get(df_name)

    # apply correct table class given df information
    table_obj = create_table(df_mid, df_name, file_name, current_date_str)

    # add to dictionary
    processed_dict[table_obj.df_name] = table_obj

# write sorted data
write_sorted_data(available_dfs, processed_dict)

main_dict = {'tomorrowpad_obj': tomorrowpad_obj,
             'df_dict': df_dict,
             'available_dfs': available_dfs,
	         'table objects': processed_dict}

# print normal data
def execute_print_normal(main_dict, date_str):
    table_objects = main_dict.get('table objects')
    tomorrowpad_obj = main_dict.get('tomorrowpad_obj')
    date_str_output = gen_date_string_yymmdd(date_str)

    # bills df
    bills_df = pd.concat([table_objects.get('[Bills Monthly]').df_hr, table_objects.get('[Bills Yearly]').df_hr, table_objects.get('[Bills Auto]').df_hr])
    bills_df = bills_df.sort_values('Diff')

    # birthday df
    birthday_df = table_objects.get('[Scheduled Birthdays]').df_hr
    birthday_hbd_index = birthday_df[birthday_df['Name'].str.endswith('| HBD')].index
    birthday_df1 = birthday_df.loc[birthday_hbd_index]
    birthday_df1.loc[:,'Name'] = birthday_df1['Name'].str[:~5]

    clear()
    print('Schedule Assistant for ' + user_name)
    #print(''); print(birthday_df1) # [['Day','Name','Flag']]
    #print('')

    print('\nLatest Tomorrowpads: ' + ', '.join(tomorrowpad_obj.padkeys()[0:5]))
    print('Today\'s Pad: ' + date_str); table_print(tomorrowpad_obj.padprint())

    print('')
    print_date('Normal Events | ' + date_str_output + ':')
    print('\nNormal Events:'); table_print(table_objects.get('[Normal Events]').df_hr) # [['Day','Time','Item','Flag']]
    print('\nScheduled Holidays:'); table_print(table_objects.get('[Scheduled Holidays]').df_hr) # [['Day','Name','Flag']]
    print('\nScheduled Birthdays:'); table_print(birthday_df) # [['Day','Name','Flag']]

    print('')
    print_date('Normal Tasks | ' + date_str_output + ':')
    print('\nBills:'); table_print(bills_df)
    print('\nNormal Tasks:'); table_print(table_objects.get('[Normal Tasks]').df_hr)
    print('\nTo Do List:'); table_print(table_objects.get('[To Do List]').df_hr)

    print_commands()

def execute_print_school(main_dict, date_str):
    table_objects = main_dict.get('table objects')
    date_str_output = gen_date_string_yymmdd(date_str)

    clear(); print('')
    print_date('School Tasks |' + date_str_output + ':')
    print('\nSchool Alerts:'); table_print(table_objects.get('[School Alerts]').df_hr)
    print('\nSchool Exams:'); table_print(table_objects.get('[School Exams]').df_hr)
    print('\nSchool Homework:'); table_print(table_objects.get('[School Homework]').df_hr)
    print('\nSchool Reading:'); table_print(table_objects.get('[School Reading]').df_hr)
    print_commands()

# generate body for email, write attachment to summary.txt
def execute_html_message(main_dict, date_str):
    table_objects = main_dict.get('table objects')
    tomorrowpad_obj = main_dict.get('tomorrowpad_obj')
    date_str_output = gen_date_string_yymmdd(date_str)

    # bills df
    bills_df = pd.concat([table_objects.get('[Bills Monthly]').df_hr, table_objects.get('[Bills Yearly]').df_hr, table_objects.get('[Bills Auto]').df_hr])
    bills_df = bills_df.sort_values('Diff')
    bills_df1 = bills_df[bills_df['Diff']<=10]

    # birthday df
    birthday_df = table_objects.get('[Scheduled Birthdays]').df_hr
    birthday_hbd_index = birthday_df[birthday_df['Name'].str.endswith('| HBD')].index
    birthday_df1 = birthday_df.loc[birthday_hbd_index]
    birthday_df1.loc[:,'Name'] = birthday_df1['Name'].str[:~5]

    # Attachment
    out_string = 'Schedule Report for ' + user_name + ':'

    out_string += '\n\nToday\'s Pad: ' + date_str
    out_string += ' | Latest Tomorrowpads: ' + ', '.join(tomorrowpad_obj.padkeys()[0:5])
    out_string += '\n[Tomorrowpad]'; out_string += '\n' + table_string(tomorrowpad_obj.padprint())
    out_string += '\n\n[Normal Focus]'; out_string += '\n' + table_string(table_objects.get('[Normal Focus]').df_hr)
    out_string += '\n\n' + print_date_string('Normal Events | ' + date_str_output + ':')
    out_string += '\n\n[Normal Events]'; out_string += '\n' + table_string(table_objects.get('[Normal Events]').df_hr) # [['Day','Time','Item','Flag']]
    out_string += '\n\n[Scheduled Holidays]'; out_string += '\n' + table_string(table_objects.get('[Scheduled Holidays]').df_hr) # [['Day','Name','Flag']]
    out_string += '\n\n[Scheduled Birthdays]'; out_string += '\n' + table_string(birthday_df) # [['Day','Name','Flag']]

    out_string += '\n\n' + print_date_string('Normal Tasks | ' + date_str_output + ':')
    out_string += '\n\n[Bills]'; out_string += '\n' + table_string(bills_df)
    out_string += '\n\n[Normal Tasks]'; out_string += '\n' + table_string(table_objects.get('[Normal Tasks]').df_hr)
    out_string += '\n\n[To Do List]'; out_string += '\n' + table_string(table_objects.get('[To Do List]').df_hr)
    out_string += '\n\n[To Do Buy]'; out_string += '\n' + table_string(table_objects.get('[To Do Buy]').df_hr)
    out_string += '\n\n[To Do Groceries]'; out_string += '\n' + table_string(table_objects.get('[To Do Groceries]').df_hr)

    out_string += '\n\n' + print_date_string('School Tasks | ' + date_str_output + ':')
    out_string += '\n\n[School Alerts]'; out_string += '\n' + table_string(table_objects.get('[School Alerts]').df_hr)
    out_string += '\n\n[School Exams]'; out_string += '\n' + table_string(table_objects.get('[School Exams]').df_hr)
    out_string += '\n\n[School Homework]'; out_string += '\n' + table_string(table_objects.get('[School Homework]').df_hr)
    out_string += '\n\n[School Reading]'; out_string += '\n' + table_string(table_objects.get('[School Reading]').df_hr)

    writeFile = open(os.path.join(os.path.split(os.path.abspath(__file__))[0],'summary.txt'), 'w')
    writeFile.write(out_string)
    writeFile.close()

    # Email Body
    out_string = ''
    #out_string += '\n\n' + '<b>Tomorrowpad:</b>' + '\n' + table_string(tomorrowpad_obj.padprint(), 'plain')
    #out_string += '\n\n<b>Normal Small Tasks:</b>'; out_string += '\n' + table_string(table_objects.get('[Normal Small Tasks]').df_hr, 'plain')

    out_string += '\n\n' + '<b>Focus Goal:</b>' + '\n' + table_string(table_objects.get('[Normal Focus]').df_hr, 'plain')
    out_string += '\n\n' + '<b>Bills:</b>' + '\n' + table_string(bills_df1, 'plain')
    out_string += '\n\n' + '<b>Birthdays:</b>' + '\n' + table_string(birthday_df1, 'plain')
    out_string += '\n\n<b>Normal Events:</b>'; out_string += '\n' + table_string(table_objects.get('[Normal Events]').df_hr, 'plain')

    #out_string += '\n\n[Normal Events]'; out_string += '\n' + table_string(table_objects.get('[Normal Events]').df_hr, 'plain')
    #out_string += '\n\n' + '[Birthdays]' + '\n' + table_string(birthday_df1, 'plain')
    #out_string += '\n\n' + '[Bills]' + '\n' + table_string(bills_df1, 'plain')

    writeFile = open(os.path.join(os.path.split(os.path.abspath(__file__))[0],'summary_email.txt'), 'w')
    writeFile.write(out_string)
    writeFile.close()

# user functions
def print_normal(main_dict=main_dict, date_str=current_date_str):
	execute_print_normal(main_dict, date_str)

def print_school(main_dict=main_dict, date_str=current_date_str):
	execute_print_school(main_dict, date_str=current_date_str)

def html_message(main_dict=main_dict, date_str=current_date_str):
	execute_html_message(main_dict, date_str)
