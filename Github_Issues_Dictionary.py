#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import requests
import os.path
import pandas as pd
import urllib.parse
import json
from io import StringIO
import numpy as np


# In[2]:


repos = pd.read_csv('repos_name.csv')
repos.head()


# ### Downloading Issues from Github

# In[3]:


count = 0
skip=0
issues = []
for repo in repos.repo_name.values:
    url = 'https://api.github.com/repos/' + repo +'/issues?state=all'
    r = requests.get(url, allow_redirects=True, auth = ('asad14789','7c9971ae53237d2b10c0609772f43c9ec0e6fc1d'))
    if r.status_code==200 : 
        try:
            issuess = json.loads(r.content)
            for i in issuess:
                issue = i['body']
                if ('exception' in issue) or ('Exception' in issue) or ('EXCEPTION' in issue): 
                    issues.append(issue)
                    
                    open('issues/exceptions/' + str(count), 'w').write(issue)
                    count +=1
                    print(count)
                else:
                    skip +=1
                    print('unrelated:- '+str(skip))
                    open('issues/' + str(skip), 'w').write(issue)
        except:
            print('request failed')


# ### Reading from Downloaded Files

# In[3]:


import glob
root_dir = 'issues/exceptions/'
issues = []
for filepath in glob.iglob(root_dir + '**/**', recursive=True):
     if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                issues.append(f.read())


# #### Filtering Java Issues

# In[116]:


java_issues = []
for issue in issues:
    if 'java.lang' in issue:
        java_issues.append(issue)
len(java_issues)


# ### Getting Errors and Exceptions

# In[117]:


import re
err = re.compile('java.lang.*')
excp = re.compile('java.lang.*')
Errors = []
Exceptions = []
miss_err = 0
miss_exception = 0
for  issue in java_issues:
    for i in issue.split(' '):
        if 'java.lang.' in i and ('Exception' in i or 'Error' in i):
            try:
                if 'Error' in i:
                    error = err.findall(issue)[0]
                    ind = error.find('Error')+5
                    Errors.append(error[:ind])
                    print(error[:ind])
            except:
                miss_err +=1
            try:
                if 'Exception' in i:
                    exception = excp.findall(issue)[0]
                    ind = exception.find('Exception')+9
                    Exceptions.append(exception[:ind])
                    print(exception[:ind])
            except:
                miss_exception +=1
        break

Total_Errors = Errors + Exceptions
len(Total_Errors)


# ### Saving into Dictionary

# In[122]:


values, counts = np.unique(Total_Errors, return_counts=True)
dictionary = dict(zip(values, counts))
dictionary


# In[123]:


### Dropping Garbage
dictionary.pop('java')
dictionary.pop('java.lan')


# ### Writing Dictionary into File

# In[126]:


with open('dictionary.txt','w+') as file:
    file.write(str(dictionary))

