import pandas as pd
import numpy as np
import copy

def non_trivialCT(data_binary,itemset):
  items = list(itemset.keys())
  in_codeword = np.zeros(len(itemset)) #whether the codeword is used
  in_codeword_tmp = np.zeros(len(itemset))
  codeword = []
  usage = []
  
  index = 0
  for i in range(len(data_binary)):

    if (in_codeword.sum() == (len(items)-1)):
      break
    
    #find the first codeword(from the first itemset)
    codeword_tmp = []
    if (data_binary.iloc[i].sum()!=1):
      index = i
      for x in items:
        if(data_binary.iloc[i][x]==1):
          codeword_tmp += [x]
          in_codeword_tmp[items.index(x)] = 1
    
      #count how many transactions contian the codeword
      trans = 0
      for j in range(len(data_binary)):
        comtain_codeword = 0
        for item in codeword_tmp:
          if(data_binary.iloc[j][item]!=0):
            comtain_codeword += 1
        if (comtain_codeword == len(codeword_tmp)):
          trans += 1

      #if more than one transaction contian the codeword, consider it the real codeword
      if (trans > 1) :
        codeword += [codeword_tmp]
        in_codeword = in_codeword_tmp
  return codeword

def data_encode(data_encode,codeword):
  usage = []
  encode_CT = {}
  code_usage = {}

  for i in range(len(codeword)):
    usage_count = 0
    code = ".".join(sorted(codeword[i])) #sort codeword
    
    for j in range(len(data_encode)):
      codeword_encode = 0  
      encode = copy.deepcopy(data_encode.iloc[j])

      for item in codeword[i]:
        if(data_encode.iloc[j][item] == 1):
          codeword_encode += 1
          encode[item] = 0
     
      if (codeword_encode == len(codeword[i])):
        if j in encode_CT:
          encode_CT[j].append(code)
          
        else:
          encode_CT.setdefault(j,[]).append(code)

        usage_count += 1
        data_encode.iloc[j] = encode
    
    code_usage[code] = usage_count
  return code_usage,encode_CT     

def Lst(itemset,data_itemset):
  lst = 0
  total_items = sum(list(itemset.values()))
  for i in range(len(data_itemset)):
    for x in data_itemset[i]:
      count = itemset[x]
      lst += -(np.log2(count/total_items))
  return lst

def Lct(codeword_usage):
  lct = 0
  total_items = sum(list(codeword_usage.values()))
  for x in codeword_usage.values():
    if(x != 0):
      lct += -(np.log2(x/total_items))
  return lct

def LDM(codeword_usage):
  ldm = 0
  total_items = sum(list(codeword_usage.values()))
  for x in codeword_usage.values():
    if(x != 0):
      ldm += -(x * (np.log2(x/total_items)))
  return ldm

dataset = pd.read_csv('final_project.csv')
dataset_binary = dataset*1

items = list(dataset_binary.columns)
count_items = []
total_items = 0
for i in items:
  count_items += [dataset_binary[i].sum()]

itemset = list(sorted(zip(count_items,items),reverse = True ))
itemset = {itemset[i][1]:itemset[i][0] for i in range(len(itemset))}

#itemset_data : standard code table itemset
itemset_data = []
itemset_data += [[x] for x in itemset.keys()] 

#ST_codeword : dict of standard code table's codeword and usage {codeword:usage}
ST_codeword = itemset

dataset_binary_encode = copy.deepcopy(dataset_binary)

#Ntrivial_codeword_ : non-trivial code table's codeword
Ntrivial_codeword_ = non_trivialCT(dataset_binary,itemset)
Ntrivial_codeword_ += [[item] for item in list(itemset.keys())]

#Ntrivial_usage : dict of non-trivial code table's codeword and usage 
#Ntrivial_encode : data encoded with non-trivial CT
Ntrivial_usage,Ntrivial_encode = data_encode(dataset_binary_encode,Ntrivial_codeword_)

#sort in transactions order
Ntrivial_encode = dict(sorted(Ntrivial_encode.items()))

#drop A non-trivial code table usage is zero
i = 0
for x in Ntrivial_usage:
  if(Ntrivial_usage[x]==0):
    #print(i)
    Ntrivial_codeword_[i]=''
  i += 1
Ntrivial_codeword = list(filter(None,Ntrivial_codeword_))

#standard code table
LM_CT = Lst(itemset,itemset_data)+Lct(ST_codeword)
LDM_CT = LDM(ST_codeword)
length_CT = LM_CT + LDM_CT 

#non-trivial code table
LM_N = Lst(itemset,Ntrivial_codeword)+Lct(Ntrivial_usage)
LDM_N = LDM(Ntrivial_usage)
length_N = LM_N + LDM_N

#print('standard code table length is',length_CT)
#print('non-trivial code table length is',length_N)

print('Data encoded with standard code table')
for x in range(len(dataset_binary)):
  filter = (dataset_binary.iloc[x][dataset_binary.columns] == 1)
  encode = list(dataset_binary.iloc[x][filter].keys())
  print(x+1,"|"," ".join(encode))
print('standard code table length is',length_CT)

print('-----------------------------------------------')

print('Non-trivial code table')
print('codeword   usage')
for x in Ntrivial_usage.keys():
  print(x,' '*(8-len(x)),'|',Ntrivial_usage[x])

print('-----------------------------------------------')

#sort each eencoded transction
Ntrivial_encode_sort = []
for x in Ntrivial_encode.values():
  Ntrivial_encode_sort += [list(sorted(x))]
#print the result of data encoded 
print('Data encoded with non-trivial code table')
for x in range(len(Ntrivial_encode_sort)):
  print(x+1,"|","  ".join(Ntrivial_encode_sort[x]))
print('non-trivial code table length is',length_N)
