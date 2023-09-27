import re

names = ['@rrr', '@fsgafgDDDf', '@asfgw56wF', '@dfD_435fda',
         '@rrr$%!', '@fsgafgDDDf!', '@asfgw56wF_п', '@asfgw56wF_', '@asfgw56wF__',
         'q@asfgw56wF', '@asfgw56w F', '@a sfgw56w', '@_______________',
         '@dfD_435fdadddddddddddddddddddddd', '@dfD_435fdaddddddddddddddddddddddd',

         ]

# pattern = re.compile(r'^@(?=\w{5,}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*')
# pattern = re.compile(r'^@(?=\w{5,}\b)[a-zA-Z0-9]*')
pattern = re.compile(r'^(?:@[a-zA-Z0-9_]{5,}$)')
# result = re.match(r'^@(?=\w{5,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*')

for name in names:
    result = pattern.search(name)
    print(name, '-', result if result is None else result.group())

