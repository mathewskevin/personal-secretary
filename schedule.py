from tabulate import tabulate
import pandas as pd
import datetime
import os

# user name
user_name = 'Kevin Mathews'

# data cleaning dictionary
clean_dict = {'[Exams]':[['Start','mmmdd'],['End','mmmdd']],
              '[Homework]':[['Start','mmmdd'],['End','mmmdd']],
              '[Reading]':[['Start','mmmdd'],['End','mmmdd']],
              '[Events]':[['Day','mmmdd'],['Time','time']],
              '[Tasks]':[['Start','mmmdd'],['End','mmmdd']],}

#data_folder = r'C:\Users\zbdxwr\Stuff\Product_Eng\Workspace\schedule_data\Schedule\\'
data_folder = os.getcwd() + '/Schedule/'

tomorrow_file = '0.0_Tomorrowpad.txt'
tomorrow_folder = os.getcwd()

# function to print available commands
def print_commands():
	print('\nAvaliable Commands:')
	print('functions: print_normal(), print_school(), print_data(df_name), terminate_prog()')
	print('data: df_dict, processed_dict, tomorrowpad_dict, available_dfs, get_raw_data(df_name), tomorrowpad_keys()')

# clear interpereter
clear = lambda: os.system('clear')

# print dataframe using tabulate
def table_print(df, format_str='plain'):
    print(tabulate(df, showindex=False, tablefmt=format_str))

# function to clear and end program
def terminate_prog():
    clear()
    exit()

def current_date():
    now = datetime.datetime.now() - datetime.timedelta(hours=5)
    #output = now.weekday()
    return now.strftime("%y%m%d")

current_date_str = current_date()

def print_date(append_string = '', user_name=user_name):
    now = datetime.datetime.now() - datetime.timedelta(hours=5)

    weekday = now.strftime("%w")

    weekday_dict = {'0':'Sunday',
					'1':'Monday',
					'2':'Tuesday',
					'3':'Wednesday',
					'4':'Thursday',
					'5':'Friday',
					'6':'Saturday'}

    out_string = weekday_dict.get(weekday) + now.strftime(", %B %d %Y %H:%M")
    out_string = out_string + append_string

    print('\nSchedule Assistant for ' + user_name + ':')
    print('-' * len(out_string))
    print(out_string)
    print('-' * len(out_string))

# generate finalized dataframe (scheduled tasks)
def print_scheduled(text_file, df_name):
    df = df_dict.get(text_file).get(df_name)
    data_mid = sort_df(df, df_name)
    data_mid = process_df(data_mid, df_name)
    data_mid = clean_df(data_mid, df_name)
    return data_mid

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

# generate finalized dataframe (tomorrowpad)
def load_tomorrowpad(text_file):
    out_list = read_tomorrowpad(open(text_file))

    tomorrow_dict = {}
    for df in out_list[1:]:
	    mid_list = interperet_tomorrowpad(df)
	    tomorrow_dict[mid_list[0]] = mid_list[1]

    return tomorrow_dict

tomorrowpad_dict = load_tomorrowpad(tomorrow_folder + '/' + tomorrow_file)

# print today's tomorrowpad
def print_tomorrowpad(current_date_str=current_date_str, tomorrowpad_dict=tomorrowpad_dict):
    output_df = tomorrowpad_dict.get(current_date_str)

    if output_df is None:
        output_df = pd.DataFrame(['None'])

    return output_df

def tomorrowpad_keys(tomorrowpad_dict=tomorrowpad_dict):
    return sorted(tomorrowpad_dict.keys(), reverse=True)

# generate finalized dataframe (birthdays)
def print_birthdays(text_file, df_name, current_date_str=current_date_str):
    df = df_dict.get(text_file).get(df_name)

    # add year to Day column
    df['Day'] = current_date_str[0:2] + df['Day']

    # get 30 day threshold
    threshold_date_str = threshold_date(current_date_str, 30)

    # sort df to next month of birthdays
    data_mid = df[(df['Day']>current_date_str) & (df['Day']<threshold_date_str)].copy()

    data_mid['Day'] = data_mid['Day'].apply(date_mmmdd)

    return data_mid

# generate finalized dataframe (normal structure)
def print_standard(text_file, df_name):
    df = df_dict.get(text_file).get(df_name).sort_values('Done', ascending=True)
    data_mid = sort_df(df, df_name)

    if data_mid.shape[0] == 0:
        return pd.DataFrame(['None'])
    else:
        data_mid = process_df(data_mid, df_name)
        data_mid = clean_df(data_mid, df_name)
        return data_mid

def load_data(folder_name):
    #text_file_list = ['tasks_school.txt','tasks_normal.txt','tasks_scheduled.txt']

    text_file_list = os.listdir(folder_name)
    text_file_list = [i for i in text_file_list if '.txt' in i]
    df_dict = {}
    for i in text_file_list:
        df_dict[i] = pop_dict(i, data_folder)

    return df_dict

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

def current_time():
    now = datetime.datetime.now()
    #output = now.weekday()
    return now.strftime("%H%M")

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

def add_flag_custom(row):

    try:
        start_date = row['Start']
        end_date = row['End']

        if current_date_str >= start_date and current_date_str <= end_date:
            flag_string = 2
        elif current_date_str > end_date:
            flag_string = 3
        else:
            flag_string = 1

    except:
        start_date = row['Day']

        if current_date_str == start_date:
            flag_string = 2
        elif current_date_str > start_date:
            flag_string = 3
        else:
            flag_string = 1

    return flag_string

# add and drop needed columns from dataframe
def process_df(df, df_name):

    # drop flag column if it exists
    try:
        df.drop('Flag', axis=1, inplace=True)
    except:
        pass

    # add flag column
    flag_series = df.apply(add_flag_custom, axis=1)
    df.insert(0, 'Flag', pd.DataFrame(flag_series))
    df.sort_values('Flag', ascending=False, inplace=True)

    # drop done column
    df.drop('Done', axis=1, inplace=True)

    # convert flag column
    df['Flag'] = df['Flag'].astype(str)
    df['Flag'] = df['Flag'].str.replace('3','LATE')
    df['Flag'] = df['Flag'].str.replace('2','!')
    df['Flag'] = df['Flag'].str.replace('1','')

    return df

# function to sort dataframe to relevant items
def sort_df(df, df_name, clean_dict=clean_dict, current_date_str=current_date_str):

    threshold_days = 30

    cols = clean_dict.get(df_name)

    # sort to in progress items only
    df = df[df['Done'] == '0']

    for col_list in cols:
        cur_col = col_list[0]
        if cur_col == 'Start' or cur_col == 'Day':
            # determine threshold
            threshold_date_str = threshold_date(current_date_str, threshold_days)

            # sort dataframe
            df = df[df[cur_col] <= threshold_date_str]

    try:
        df = df.sort_values('Start', ascending=True)
    except:
        df = df.sort_values('Day', ascending=True)

    return df

# function to convert dataframe information to human readable format
def clean_df(df, df_name, clean_dict=clean_dict):
    cols = clean_dict.get(df_name)

    for col_list in cols:
        cur_col = col_list[0]
        cur_func = col_list[1]

        if cur_func == 'time':
            df[cur_col] = df[cur_col].apply(time_string)
        elif cur_func == 'mmmdd':
            df[cur_col] = df[cur_col].apply(date_mmmdd)
        else: # apply mmmdd
            df[cur_col] == df[cur_col].apply(date_mmmdd)

    return df

# Main Loop
print('loading data...')
df_dict = load_data(data_folder)

# read df dict for available data
def get_dfs(df_dict=df_dict):
    available_dfs = pd.DataFrame()
    file_names = list(df_dict.keys())
    for file_name in file_names:
        df_keys = list(df_dict.get(file_name).keys())
        for i in df_keys:
            #available_dfs = available_dfs.append([i, file_name])
            available_dfs = pd.concat([available_dfs, pd.DataFrame([i,file_name]).T])
    return available_dfs.reset_index(drop=True)

available_dfs = get_dfs()

# populate dictionary with processed dataframes
def pop_processed_dict(available_dfs = available_dfs):
	df_dict = {}
	for idx, row in available_dfs.iterrows():
		df_name = row[0]
		file_name = row[1]

		if df_name == '[Birthdays]':
			df = print_birthdays(file_name, df_name)
		elif df_name == '[Daily]':
			df = 'None'
			#df = print_standard(file_name, df_name)
		else:
			df = print_standard(file_name, df_name)

		df_dict[df_name] = df

	return df_dict

processed_dict = pop_processed_dict()

# print data from specific dataframe
def get_raw_data(df_name, df_dict=df_dict, available_dfs=available_dfs):
    file_name =  available_dfs[available_dfs[0].str.contains(df_name)][1].iloc[0]
    df_name = available_dfs[available_dfs[0].str.contains(df_name)][0].iloc[0]
    df_out = df_dict.get(file_name).get(df_name)
    return df_out

#print available dataframes()
def print_data(df_name = '', available_dfs=available_dfs, processed_dict=processed_dict):
    clear()
    if df_name == '':
        print_date(' | Available Data:')
        print('\nAvailable Dataframes:')
        print(available_dfs)
        print('\nSupply argument to return data.')
        print_commands()

    else:
        print_date(' | Available Data:')
        print_commands()
        print('')
        return processed_dict.get(df_name)

# print normal data
def print_normal():
    clear()
    print_date(' | Normal Tasks:')

    print('\nLatest Tomorrowpads: ' + ', '.join(tomorrowpad_keys()[0:5]))
    print('Today\'s Pad: ' + current_date_str)
    table_print(print_tomorrowpad())

    print('\nEvents:')
    table_print(processed_dict.get('[Events]'))

    print('\nTasks:')
    table_print(processed_dict.get('[Tasks]'))

    print('\nBirthdays:')
    print(processed_dict.get('[Birthdays]'))

    print_commands()

def print_school():
    clear()
    print_date(' | School Tasks:')

    print('\nExams:')
    table_print(processed_dict.get('[Exams]'))

    print('\nHomework:')
    table_print(processed_dict.get('[Homework]'))

    print('\nReading:')
    table_print(processed_dict.get('[Reading]'))

    print_commands()

# print normal
print_normal()
