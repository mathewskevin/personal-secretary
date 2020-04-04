from tabulate import tabulate
import pandas as pd
import datetime
import os

# user name
user_name = 'Kevin Mathews'

# data cleaning dictionary
clean_dict = {'[Alerts]':[['Start','mmmdd'],['End','mmmdd']],
              '[Exams]':[['Start','mmmdd'],['End','mmmdd']],
              '[Homework]':[['Start','mmmdd'],['End','mmmdd']],
              '[Reading]':[['Start','mmmdd'],['End','mmmdd']],
              '[Events]':[['Day','weekday'],['Time','time']], # gen_date_string_yymmdd, mmmdd
              '[Tasks]':[['Start','mmmdd'],['End','mmmdd']],}

#data_folder = r'C:\Users\zbdxwr\Stuff\Product_Eng\Workspace\schedule_data\Schedule\\'
#data_folder = os.getcwd() + '//'
data_folder = '/'.join(os.path.abspath(__file__).split('/')[:~0]) + '//' # location of python file

#tomorrow_file = '0.0_Tomorrowpad.txt'
summary_file = 'summary.txt'
tomorrow_file = 'tomorrow_pad.txt'
tomorrow_folder = data_folder
#tomorrow_folder = os.getcwd() + '/Notes/Schedule/'

# function to print available commands
def print_commands():
	print('\nAvaliable Commands:')
	print('functions: print_normal(), print_school(), print_data(df_name), terminate_prog()')
	print('data: df_dict, processed_dict, tomorrowpad_dict, available_dfs, get_raw_data(df_name), tomorrowpad_keys(), write_sorted_data()')

# clear interpereter
clear = lambda: os.system('clear')

# generate table string
def table_string(df, format_str='plain'):
    return tabulate(df, showindex=False, tablefmt=format_str)

# print dataframe using tabulate
def table_print(df):
    print(table_string(df))

# function to clear and end program
def terminate_prog():
    clear()
    exit()

def current_date():
    now = datetime.datetime.now() - datetime.timedelta(hours=5)
    #output = now.weekday()
    return now.strftime("%y%m%d")

current_date_str = current_date()

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

def print_date_string(append_string = '', user_name=user_name):
    now = datetime.datetime.now() - datetime.timedelta(hours=5)
    out_string = gen_date_string(now)
    out_string += append_string
    out_string = '-'*len(out_string) + '\n' + out_string + '\n' + '-'*len(out_string)
    return out_string

def print_date(append_string = '', user_name=user_name):
    out_string = print_date_string(append_string)
    out_string = 'Schedule Assistant for ' + user_name + ':' + '\n' + out_string
    print(out_string)

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

tomorrowpad_dict = load_tomorrowpad(tomorrow_folder + tomorrow_file)

# print today's tomorrowpad
def print_tomorrowpad(current_date_str=current_date_str, tomorrowpad_dict=tomorrowpad_dict):
    output_df = tomorrowpad_dict.get(current_date_str)

    if output_df is None:
        output_df = pd.DataFrame(['None'])
    else:
        output_df = ' - ' + output_df

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

    # get 15 day previous threshold
    previous_date_str = threshold_date(current_date_str, -15)

    # sort df to next month of birthdays
    df = df[(df['Day']>previous_date_str) & (df['Day']<threshold_date_str)].copy()

    #data_mid['Day'] = data_mid['Day'].apply(date_mmmdd)

    # add flag column
    flag_series = df.apply(add_flag_custom, axis=1)
    df.insert(0, 'Flag', pd.DataFrame(flag_series))
    df.sort_values('Flag', ascending=False, inplace=True)

    # convert flag column
    df['Flag'] = df['Flag'].astype(str)
    df['Flag'] = df['Flag'].str.replace('3','Past')
    df['Flag'] = df['Flag'].str.replace('2','TODAY!')
    df['Flag'] = df['Flag'].str.replace('1','')

    df['Day'] = df['Day'].apply(gen_date_string_yymmdd)

    return df

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

    text_file_list.remove(tomorrow_file)
    text_file_list.remove(summary_file)
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

# weekday string
#def date_dd_full(date_text):
#    dateObj = date_text
#    output = gen_date_string(dateObj)
#    return output

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
    df['Flag'] = df['Flag'].str.replace('1','Inactive')

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
        df = df.sort_values(['Start','End'], ascending=True)
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
        elif cur_func == 'weekday':
            df[cur_col] = df[cur_col].apply(gen_date_string_yymmdd)
        else: # apply mmmdd
            df[cur_col] == df[cur_col].apply(date_mmmdd)

    return df

# Main Loop
print('loading data...')
df_dict = load_data(data_folder)

# sort raw data for writing back to notepad
def sort_data(df_dict=df_dict):
    # iterate through dictionary
    #file_list = []
    sorted_dict={}
    file_list = df_dict.keys()
    file_list = [i for i in file_list]
    file_list.remove('tasks_scheduled.txt')
    for file_name in file_list:
        mid_dict = df_dict.get(file_name)
        #df_list = []
        new_dict = {}
        for df_name in mid_dict.keys(): #df_list = iter(mid_dict.keys()):
            #else:
            # for each dataframe found, sort according to rules
            mid_df = mid_dict.get(df_name)
            #mid_df = mid_df.sort_values(['Done'], ascending=False)

            if df_name == '[Events]':
                mid_df = mid_df.sort_values(['Done', 'Day'], ascending=True)
                #print(file_name, df_name, mid_df.columns.values)
            else:
                mid_df = mid_df.sort_values(['Done', 'Start', 'End'], ascending=True)
                #print(file_name, df_name, mid_df.columns.values)

            new_dict[df_name] = mid_df
            #df_list.append(mid_df)


        sorted_dict[file_name] = new_dict

    return sorted_dict

data_sorted = sort_data() # sort raw data for writing back to file

# function to write sorted data to files
def write_sorted_data(data_sorted=data_sorted):
    for file_name in data_sorted.keys(): # file name
        table_df = data_sorted.get(file_name)
        output_string = ''
        for df_name in table_df.keys(): # dataframe name
            mid_df = table_df.get(df_name) # data table
            col_titles = [i for i in mid_df]
            output_df = mid_df[col_titles[0]] + ' ' + mid_df[col_titles[1]]
            # iterate through dataframe columns to create string
            for i in range(2, len(col_titles)):
                output_df = output_df + ' ' + mid_df[col_titles[i]]
                #print(file_name, df_name, len(col_titles))

            #output_df = output_df + '\n'
            output_string = output_string + df_name + '\n' + ' '.join(col_titles) + '\n'
            output_string = output_string + '\n'.join(output_df.tolist()) + '\n\n'

            text_file = open(data_folder + file_name, "w")
            text_file.write(output_string)
            text_file.close()
            #print('printed:', file_name)
    print('data sorted.')

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
    df_dict_new = {}
    for idx, row in available_dfs.iterrows():
    	df_name = row[0]
    	file_name = row[1]

    	if df_name == '[Birthdays]':
    		df = print_birthdays(file_name, df_name)
    	elif df_name == '[Daily]':
    		df = 'None'
    	else:
    		df = print_standard(file_name, df_name)

    	df_dict_new[df_name] = df

    return df_dict_new

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
    clear(); print('')
    print_date(' | Normal Tasks:')
    print('\nLatest Tomorrowpads: ' + ', '.join(tomorrowpad_keys()[0:5]))
    print('Today\'s Pad: ' + current_date_str); table_print(print_tomorrowpad())
    print('\nEvents:'); table_print(processed_dict.get('[Events]')[['Day','Time','Item','Flag']])
    print('\nTasks:'); table_print(processed_dict.get('[Tasks]'))
    print('\nBirthdays:'); print(processed_dict.get('[Birthdays]')[['Day','Name','Flag']])
    print_commands()

def print_school():
    clear(); print('')
    print_date(' | School Tasks:')
    print('\nAlerts:'); table_print(processed_dict.get('[Alerts]'))
    print('\nExams:'); table_print(processed_dict.get('[Exams]'))
    print('\nHomework:'); table_print(processed_dict.get('[Homework]'))
    print('\nReading:'); table_print(processed_dict.get('[Reading]'))
    print_commands()

# generate message for email, write to summary.txt
def html_message():
    out_string = 'Schedule Assistant for ' + user_name + ':' + '\n'
    out_string += '\nLatest Tomorrowpads: ' + ', '.join(tomorrowpad_keys()[0:5])
    out_string += '\nToday\'s Pad: ' + current_date_str; out_string += '\n' + table_string(print_tomorrowpad())

    out_string += '\n\n' + print_date_string(' | Normal Tasks:') + '\n'
    out_string += '\nEvents:'; out_string += '\n' + table_string(processed_dict.get('[Events]')[['Day','Time','Item','Flag']])
    out_string += '\n\nTasks:'; out_string += '\n' + table_string(processed_dict.get('[Tasks]'))
    out_string += '\n\nBirthdays:'; out_string += '\n' + table_string(processed_dict.get('[Birthdays]')[['Day','Name','Flag']])

    out_string += '\n\n' + print_date_string(' | School Tasks:')
    out_string += '\n\nAlerts:'; out_string += '\n' + table_string(processed_dict.get('[Alerts]'))
    out_string += '\n\nExams:'; out_string += '\n' + table_string(processed_dict.get('[Exams]'))
    out_string += '\n\nHomework:'; out_string += '\n' + table_string(processed_dict.get('[Homework]'))
    out_string += '\n\nReading:'; out_string += '\n' + table_string(processed_dict.get('[Reading]'))

    writeFile = open('summary.txt', 'w')
    writeFile.write(out_string)
    writeFile.close()

# write sorted data
write_sorted_data()
# print normal
#print_normal()
