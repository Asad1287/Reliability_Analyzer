from sklearn.decomposition import non_negative_factorization
import surpyval as surv



import csv 

class Loader:
    def __init__(self,use_fitted_params:bool=False) -> None:
        self.object_dict = {}
        self.use_fitted_params = use_fitted_params
        self.object_dict['Start'] = {'name':'Start','model':None, 'relationship':[]}
        self.parameter_list = []
        self.equipment_fail_times = {}
        self.fitted_models = {}
        
    
    def _load_and_fit_params(self,TTF_file:str) -> None:
        with open(TTF_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                #skip header
                if row[0] == "Equipment":
                    pass
                #skip empty rows
                
                if len(row)==0:
                    pass
                if self.equipment_fail_times.get(row[0]) == None:
                    self.equipment_fail_times[row[0]] = []
                self.equipment_fail_times[row[0]].append(float(row[1]))
        
        for key in self.equipment_fail_times.keys():
            self.fitted_models[key] = surv.Weibull.fit(self.equipment_fail_times[key])
        
        print(self.fitted_models['item1'])
      
        

    def _load_config_file(self,file:str) -> None:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            for row in csv_reader:
                if len(row)==0:
                    break 
            
                
                if row[1]=="Weibull":
                    if self.use_fitted_params:
                     
                        self.object_dict[row[0]] = {'name':row[0],'model':self.fitted_models[row[0]], 'relationship':[]}
                        self.parameter_list.append(float(row[2]))
                    
                    model = surv.Weibull.from_params([float(row[2]),float(row[3])])
                    self.parameter_list.append(float(row[2]))
                elif row[1]=="Exponential":
                    if self.use_fitted_params:
                        self.object_dict[row[0]] = {'name':row[0],'model':self.fitted_models[row[0]], 'relationship':[]}
                        self.parameter_list.append(float(row[2]))

                    model = surv.Exponential.from_params([float(row[2])])
                    self.parameter_list.append(float(row[2]))

                else:
                    raise Exception("Distribution not supported")
                    
                

                self.object_dict[row[0]] = {'name':row[0],'model':model, 'relationship':[]}
       

              
    def _load_relationship_file(self,file:str) -> None:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_cnt = 0
            first_element = None
            for row in csv_reader:
                if len(row)!=0 and line_cnt == 0:
                    first_element = row[0]
                    line_cnt+=1
                line_cnt += 1
                if len(row) == 1:
                    raise Exception("No relationship found")
                else:
                    
                   
                    for row_index in range(1,len(row)):
                        if row[0] not in list(self.object_dict.keys()):
                            
                            raise Exception("Item not found in config")
                        self.object_dict[row[0]]['relationship'].append(row[row_index])
        self.object_dict['Start']['relationship'].append(first_element)
        print(self.object_dict)
    
    def load(self,TTF_file:str,config_file:str,relationship_file:str) -> None:

        self._load_and_fit_params(TTF_file)
        self._load_config_file(config_file)
        self._load_relationship_file(relationship_file)

import unittest

class LoaderTestCase(unittest.TestCase):
    def test_load(self):
        loader = Loader()
        loader.load("item_config.csv","item_rel.csv")
        self.assertEqual(loader.object_dict['Start']['name'],"Start")
        self.assertEqual(loader.object_dict['Start']['model'],None)
        self.assertEqual(loader.object_dict['Start']['relationship'],[])
        self.assertEqual(loader.object_dict['item1']['name'],"item1")
       
        self.assertEqual(loader.object_dict['item1']['relationship'],['item2'])
        self.assertEqual(loader.object_dict['item2']['name'],"item2")
       
        self.assertEqual(loader.object_dict['item2']['relationship'],['item3'])
        self.assertEqual(loader.object_dict['item3']['name'],"item3")
        
        self.assertEqual(loader.object_dict['item3']['relationship'],['item4'])
        self.assertEqual(loader.object_dict['item4']['name'],"item4")
      
        self.assertEqual(loader.object_dict['item4']['relationship'],['Terminal'])
      
    
loader = Loader(use_fitted_params=True)
loader.load("TTF.csv","item_config.csv","item_rel.csv")