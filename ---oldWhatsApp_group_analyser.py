import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

#To test the algorithm, just change the file path of the path of the WhatsApp text you downloaded....
#'''To download the whatsApp text of your group, click on the ... button at the top right corner of you group chat,
#click and and then click on email chat. Send the chat to your mail without the media and download to your system from your mail'''

filename = "C:\\Users\\Ede\\Desktop\\WhatsApp Chat with CYAA Member   Probation (3).txt"
with open(filename, encoding="utf-8") as f:
    file_read = f.read()

#declare the re to be used
pieces = [x.strip('\n') for x in file_read.split('\n')]
beg_pattern = r'\d+/\d+/\d+,\s+\d+:\d+\s+\w+\.\w+\.'
pattern = r'\d+/(\d+/\d+),\s+\d+:\d+\s+\w+\.\w+\.\s+-\s+(\w+|\w+\s+\w+|\w+\s+\w+\s+\w+|\w+\s+\w+\.\s+\w+|\w+\s+\w+-\w+|\w+\'\w+\s+\w+|\+\d+\s+\(\W+\d+\)\s+\d+-\d+\W+|\W+\+\d+\s+\d+\s+\d+\s+\d+\W+|\W+\+\d+\s+\d+\w+\W+):(.*)'
#compile the re
reg = re.compile(beg_pattern)
regex = re.compile(pattern)

remove_blanks = [x for x in pieces if reg.match(x)]
blanks = [x for x in pieces if not reg.match(x)]

grouped_data = []
for x in remove_blanks:
    grouped_data.extend(regex.findall(x))

grouped_data_list = [list(x) for x in grouped_data]

#convert the list to a numpy array for ease convertion to DataFrame
#splitting to 3 to avoid memoryError

numpy_data = np.array(grouped_data_list)

#turn the numpy array to DataFrame
pd_data = pd.DataFrame(numpy_data, columns=['Date', 'User', 'Message'])


#compute for most active member
most_active_user = pd_data.User.value_counts()
most_active_date = pd_data.Date.value_counts(sort=False)
pd_date = pd.DataFrame({'Date':most_active_date.index, 'Occur':most_active_date.values}, index=None)
#pd_date.Date = pd.to_datetime(pd_date['Date'],format='%d/%m%/Y, %H:%M')

message_list = pd_data.Message.tolist()
message_list.extend(blanks)
message_list_lower = [x.strip().lower() for x in message_list]
word_list = []
for x in message_list_lower:
    word_list.extend(x.split(" "))

rem_sym = re.compile(r'(\w+\W+|\W+\w+|\W+)')

cln_list = []
uncln_list = []
for x in word_list:
    if not rem_sym.match(x):
        cln_list.append(x)
    else:
        uncln_list.append(x)

cln_uncl = []
left_over = []
cln_patrn = re.compile(r'(\w+)\W+|\W+(\w+)')
for x in uncln_list:
    if cln_patrn.match(x):
        cln_uncl.extend(cln_patrn.match(x).groups())
    else:
        left_over.append(x)

cln_list.extend(cln_uncl)
adverbs = ['','u','media','4','d','3','omitted','that','this','then','an','there','2','at','me','by','so','do','or','if','all','but','can','are','as','your','was','will','we','from','have','they','the','to','and','of','a','is','in','i','you','it','for','be','he','on']
rem_adv = [x for x in cln_list if x not in adverbs]

cln_list_sr = pd.Series(rem_adv)

most_used = cln_list_sr.value_counts()


###Plot graphs
#plt.figure()
#fig, axes = plt.subplots(2,2)
#ax2 = fig.add_subplot(2,2,2)
#ax3 = fig.add_subplot(2,2,3)
most_active_user[:20].plot(kind='barh')
plt.show()
most_active_date.plot(kind='bar')
plt.show()
most_used[:20].plot(kind='bar')
plt.show()















