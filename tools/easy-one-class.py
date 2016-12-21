from itertools import izip_longest
import subprocess, os
import numpy


owner_file='owner'
outlier_file='outlier'

owner_prefix = 'owner_'
outlier_prefix = 'outlier_'

nu = 0.1

grid_cmd = 'python ../../tools/grid.py %s > %s'
train_cmd = 'svm-train -t 2 -s 2 -n {0} %s'.format(nu)
train_cmd_c_gamma = 'svm-train -t 2 -s 2 -n {0} -c %f -g %f %s'.format(nu)
test_cmd = 'svm-predict %s  %s %s > %s'
test_outlier_cmd = 'svm-predict %s  %s %s > %s'

fold = 5
calcular_c_gamma = False

calculate_range = "svm-scale -l -1 -u 1 -s %s %s > %s"
scale_cmd = "svm-scale -r %s %s > %s"

def main():
  
  split_scale()
  for i in range(1,fold+1):
    file_name = owner_prefix+'not_'+str(i)
    range_name = 'range_'+file_name
    train_file = range_name+'.'+file_name+'.scale'	
    	
    if(calcular_c_gamma):	
      subprocess.call(grid_cmd%(train_file,range_name+'.grid.out'), shell=True, stdout=subprocess.PIPE)
      c, g = read_c_gamma(range_name+'.grid.out')
      subprocess.call(train_cmd_c_gamma%(c,g,train_file), shell=True, stdout=subprocess.PIPE)
    else:
      subprocess.call(train_cmd%(train_file), shell=True, stdout=subprocess.PIPE)
    
    file_name = owner_prefix+str(i)    
    test_file = range_name+'.'+file_name+'.scale'
    subprocess.call(test_cmd%(test_file,train_file+'.model',test_file+'.out','accuracy.'+test_file), shell=True, stdout=subprocess.PIPE)
    
    file_name = outlier_prefix+str(i)    
    test_outlier_file = range_name+'.'+file_name+'.scale'
    subprocess.call(test_outlier_cmd%(test_outlier_file,train_file+'.model',test_outlier_file+'.out','accuracy.'+test_outlier_file), shell=True, stdout=subprocess.PIPE)	
    
  mean_sd_rates()
  #mean_sd_numbers()
  #clean temp files
  subprocess.call('rm *.scale.model *.scale.out accuracy.* *.grid.out', shell=True, stdout=subprocess.PIPE)    
  subprocess.call('rm owner_* outlier_* range_*', shell=True, stdout=subprocess.PIPE)

def mean_sd_rates():
  arr=[]
  for i in range(1,fold+1):
    range_name = 'range_'+owner_prefix+'not_'+str(i)	
    file_name = 'accuracy.'+range_name+'.'+owner_prefix+str(i)+'.scale'
    crs = open(file_name, "r")

    for columns in ( raw.strip().split() for raw in crs ):
      arr.append([])	
      arr[i-1].append(float(columns[2].replace('%','')))

    outlier_file_name = 'accuracy.'+range_name+'.'+outlier_prefix+str(i)+'.scale'
    outlier_crs = open(outlier_file_name, "r")
    	
    for columns in ( raw.strip().split() for raw in outlier_crs ):
      #arr.append([])	
      arr[i-1].append(float(columns[2].replace('%','')))
	
  #print arr
  #http://stackoverflow.com/questions/15389768/standard-deviation-of-a-list#15389874  
  print '[mean1,mean2(outlier)]'
  print '[sd1,sd2(outlier)]'
  print numpy.mean(arr, axis=0)
  print numpy.std(arr, axis=0, ddof=1) #ddof=1 for samples

def mean_sd_numbers():
  arr=[]
  for i in range(1,fold+1):
    range_name = 'range_'+owner_prefix+'not_'+str(i)	
    file_name = 'accuracy.'+range_name+'.'+owner_prefix+str(i)+'.scale'
    crs = open(file_name, "r")

    for columns in ( raw.strip().split() for raw in crs ):
      arr.append([])	
      small_arr = map(int,columns[3].replace('(','').replace(')','').split('/')) 
      arr[i-1].append([small_arr[0], small_arr[1] - small_arr[0]])

    outlier_file_name = 'accuracy.'+range_name+'.'+outlier_prefix+str(i)+'.scale'
    outlier_crs = open(outlier_file_name, "r")
    	
    for columns in ( raw.strip().split() for raw in outlier_crs ):
      small_arr = map(int,columns[3].replace('(','').replace(')','').split('/')) 
      arr[i-1].append([small_arr[0], small_arr[1] - small_arr[0]])
	
  #print arr
  #http://stackoverflow.com/questions/15389768/standard-deviation-of-a-list#15389874  
  print '[[N_TP, N_FN]'
  print '[N_FP, N_TN]]'
  print '[[SD_TP, SD_FN]'
  print '[SD_FP, SD_TN]]'
  print numpy.mean(arr, axis=0)
  print numpy.std(arr, axis=0, ddof=1) #ddof=1 for samples

def read_c_gamma(file_name):
    #http://stackoverflow.com/a/18603065/403999    
    with open(file_name, "rb") as f:
      first = f.readline()      # Read the first line.
      f.seek(-2, 2)             # Jump to the second last byte.
      while f.read(1) != b"\n": # Until EOL is found...
        f.seek(-2, 1)         # ...jump back the read byte plus one more.
      last = f.readline()       # Read last line.
    
    arr = last.split(' ')	
    return float(arr[0]), float(arr[1])

def split_scale():
  split_for_cross_validation(owner_file,owner_prefix,fold)
  split(outlier_file,outlier_prefix,fold)
    
  for i in range(1,fold+1):  
    file_name = owner_prefix+'not_'+str(i)
    range_name = 'range_'+file_name		  
    output_file = range_name+'.'+file_name+'.scale'
    command_range = calculate_range % (range_name,file_name,output_file)
    subprocess.call(command_range, shell=True, stdout=subprocess.PIPE)
    
    file_name = owner_prefix+str(i)	
    output_file = range_name+'.'+file_name+'.scale'
    command_scale = scale_cmd % (range_name,file_name,output_file)
    subprocess.call(command_scale, shell=True, stdout=subprocess.PIPE)
    
    file_name = outlier_prefix+str(i)	
    output_file = range_name+'.'+file_name+'.scale'
    command_scale = scale_cmd % (range_name,file_name,output_file)
    subprocess.call(command_scale, shell=True, stdout=subprocess.PIPE)

#http://stackoverflow.com/q/845058/403999 
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1 
#http://stackoverflow.com/a/16289922/403999
def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)	
#http://stackoverflow.com/a/16289922/403999
def split(file,prefix,fold):
  n = file_len(file)//fold
  join = False
  with open(file) as f:
    for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
        if(i > fold):
            join = True		
        with open(prefix+'{0}'.format(i), 'w') as fout:
            fout.writelines(g)
  
  if(join):
    with open(prefix+'{0}'.format(i+1), 'w') as outfile:
      for j in [i-1,i]:
        with open(prefix+'{0}'.format(j)) as infile:	
          outfile.write(infile.read())
    os.remove(prefix+'{0}'.format(i-1))
    os.remove(prefix+'{0}'.format(i))
    os.rename(prefix+'{0}'.format(i+1), prefix+'{0}'.format(i-1))	

def split_for_cross_validation(file,prefix,fold):
  split(file,prefix,fold)
  #http://stackoverflow.com/a/13613375/403999
  for i in range(1,fold+1):       
    with open(prefix+'not_'+str(i), 'w') as outfile:
      for j in range(1,fold+1):
        if(j == i):
          continue
        with open(prefix+str(j)) as infile:
          outfile.write(infile.read())
	
if __name__ == "__main__":
  main();