import matplotlib.pyplot as plt
import networkx as nx
Met_type={'invertebrate':9.7,'ectotherm vertebrate':8.9,'endotherm vertebrate':89.2,'photo-autotroph':0.0,'heterotrophic bacteria':0.15}
def Add_met_rate(sp_dict,mets):
        for sp in sp_dict.keys():
                sp_dict[sp].add_met_rate(mets)


def Open_and_read(path1,path2,path3,path4):
        a=open(path1,'r')
        b=[line.split('\t') for line in a.readlines()]
        sp_dict={}
        Pred_dict={}
        for t in range(1,len(b)):
                if b[t][10] not in Pred_dict.keys():
                        if b[t][10] not in sp_dict.keys():
                                sp_dict[b[t][10]]=Speci(b[t][10],b[t][11],b[t][9],float(b[t][17]),b[t][12])
                        Pred_dict[b[t][10]]=[]
                        if b[t][21] not in sp_dict.keys():
                                sp_dict[b[t][21]]=Speci(b[t][21],b[t][22],b[t][20],float(b[t][27]))
                        sp_dict[b[t][10]].add_preys(sp_dict[b[t][21]])
                        sp_dict[b[t][21]].add_pred(sp_dict[b[t][10]])
                else:
                        if b[t][21] not in sp_dict.keys():
                                sp_dict[b[t][21]]=Speci(b[t][21],b[t][22],b[t][20],float(b[t][27]))
                        sp_dict[b[t][10]].add_preys(sp_dict[b[t][21]])
                        sp_dict[b[t][21]].add_pred(sp_dict[b[t][10]])
        Add_met_rate(sp_dict,Met_type)
        p={}
        i_r={}
        sp_digit={}
        for i in range(len(sp_dict.keys())):
                sp_digit[sp_dict.keys()[i]]=str(i)
        
        for pred in Pred_dict:
                p[pred]=sp_dict[pred].preys
        writ_=open(path2,'w')
        write_2=open(path3,'w')
        write_3=open(path4,'w')
        for pre in p.keys():
                for prey in p[pre].keys():
                        writ_.write(sp_digit[pre]+'\t'+sp_digit[prey]+'\n')
                                
        for sp in sp_dict.keys():
                i_r[sp]=sp_dict[sp].met_rate
                write_2.write(sp_digit[sp] +'\t'+ sp+'\n')
                write_3.write(sp+'\t'+sp_dict[sp].met+'\t'+sp_dict[sp].life_stage+'\t'+str(sp_dict[sp].body_mass)+'\n')
        write_2.close()
        write_3.close()
        return sp_dict,p,sp_digit,i_r

class Speci(object):
        def __init__(self,name,metab,life_stage,body_mass,type_feed=None):
                self.name=name
                self.met=metab
                self.type_feed=type_feed
                self.life_stage=life_stage
                self.body_mass=body_mass
                self.preys={}
                self.preds={}
                self.met_rate=None
                self.vul_dict={}
        def add_preys(self,prey):
                self.preys[prey.name]=prey
        def add_pred(self,pred):
                self.preds[pred.name]=pred
        def add_met_rate(self,mets):
                self.met_rate=mets[self.met]*(self.body_mass*(10**-3))**(0.75)
        def __repr__(self):
                return self.name
        def get_vul(self):
                tot=sum([1.0/len(self.preds[i].preys) for i in self.preds.keys()])
                for pred in self.preds.keys():
                        self.vul_dict[pred]=(1.0/len(self.preds[pred].preys))/tot
def vul(sp_dict):
        for sp in sp_dict:
                sp_dict[sp].get_vul()
##def comp(sp_dict):
##        for sp in sp_dict:
##                sp_dict[sp].get_comp_hierarchy()
      

def draw_network(dict_,sp):
    network=nx.Graph(name='Prueba')
    for node in sp.keys():
        network.add_node(sp[node])
    for node in dict_.keys():
        for prey in dict_[node].keys():
            network.add_edge(sp[node],sp[prey])
    a=nx.random_layout(network)
    nx.draw_networkx(network,pos=a,node_size=150,font_size=0.0,width=0.7)
sp_dict,p,digits,ir=Open_and_read('C:\Users\Carlos\Documents\Proyecto Londres\simulation\Benguela\Benguela.txt','C:\Users\Carlos\Documents\Proyecto Londres\simulation\Benguela_links.txt',
                        'C:\Users\Carlos\Documents\Proyecto Londres\simulation\Benguela_index.txt','C:\Users\Carlos\Documents\Proyecto Londres\simulation\Benguela_met_size.txt')

def get_link_index(pred_dict):
        link_index={}
        i=1
        for pred in pred_dict.keys():
                for prey in pred_dict[pred]:
                        link_index[str(pred)+','+str(prey)]=i
                        i+=1
        return link_index
Pred_dict={}
Prey_dict={}
for pred in p.keys():
        Pred_dict[pred]=[]
        keys=p[pred].keys()
        try:
                keys.remove(pred)
        except:
                pass
        for prey in keys:
                Pred_dict[pred].append(prey)
                new_keys=Prey_dict.keys()
                if prey not in new_keys:
                        if pred != prey:
                                Prey_dict[prey]=[[pred,len(sp_dict[pred].preys)]]
                else:
                        if pred != prey:
                                Prey_dict[prey].append([pred,len(sp_dict[pred].preys)])
index=get_link_index(Pred_dict)                                         
vul(sp_dict)
##comp(sp_dict)
##sp_dict,p,digits,ir=Open_and_read('C:\Users\Carlos\Documents\Proyecto Londres\simulation\Warren_Skipith.txt','C:\Users\Carlos\Documents\Proyecto Londres\simulation\warren_links.txt',
##                         'C:\Users\Carlos\Documents\Proyecto Londres\simulation\warren_index.txt','C:\Users\Carlos\Documents\Proyecto Londres\simulation\warren_met_size.txt')

##draw_network(p,sp_dict)
##plt.savefig('C:\Users\Carlos\Documents\Proyecto Londres\simulation\porfaa',dpi=800)
##plt.show()
ir_dict={0:{'Sharks': 3.1174269124539644, 'Other groundfish': 15.861781020890097, 'Kob': 54.463998304332826, 'Yellowtail': 62.69721729523808, 'Hakes': 24.15159481022579, 'Lightfish': 0.0419429298479679, 'Gelatinous zooplankton': 0.08891397050194615, 'Whales & Dolphins': 1496.0039276473171, 'Benthic carnivores': 0.015811388300841896, 'Anchovy': 0.08077021079005205, 'Horse mackerel': 7.811209129800217, 'Bacteria': 2.8117066259517455e-10, 'Round herring': 0.7267073224650402, 'Other pelagics': 4.647847727151747, 'Mesozooplankton': 8.891397050194615e-05, 'Tunas': 380.75950051368955, 'Chub mackerel': 5.579445953477171, 'Geelbek': 26.579679038086034, 'Microzooplankton': 2.8117066259517456e-06, 'Goby': 0.11584106568455015, 'Pilchard': 0.8853120175338038, 'Benthic filter feeders': 0.015811388300841896, 'Squid': 0.044721359549995794, 'Phytoplankton': 0.0, 'Lanternfish': 0.055063606639991595, 'Seals': 2186.3844289599415, 'Macrozooplankton': 0.0028117066259517455, 'Birds': 102.09911271660346, 'Snoek': 15.757538619732088},
         1:{'Sharks': 12.063086748191429, 'Other groundfish': 61.37819612431386, 'Kob': 210.7519934385053, 'Yellowtail': 242.61097127287783, 'Hakes': 93.45617122217807, 'Lightfish': 0.16230090245518014, 'Gelatinous zooplankton': 1.7249310277377552, 'Whales & Dolphins': 2430.665762224785, 'Benthic carnivores': 0.30674093303633276, 'Anchovy': 0.31254559827454925, 'Horse mackerel': 30.22598315444432, 'Bacteria': 8.435119877855236e-10, 'Round herring': 2.8120413782342863, 'Other pelagics': 17.98514990071763, 'Mesozooplankton': 0.001724931027737755, 'Tunas': 1473.3737193790598, 'Chub mackerel': 21.590029993889924, 'Geelbek': 102.8518014952025, 'Microzooplankton': 5.454710854346386e-05, 'Goby': 0.44825455851847673, 'Pilchard': 3.4257725895873286, 'Benthic filter feeders': 0.30674093303633276, 'Squid': 0.8675943752699183, 'Phytoplankton': 0.0, 'Lanternfish': 0.21307221699822837, 'Seals': 3552.376886397574, 'Macrozooplankton': 0.05454710854346386, 'Birds': 165.8878115541171, 'Snoek': 60.974823354615474}}

