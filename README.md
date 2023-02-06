#  MeTeoR: a Metric Temporal Reasoner

This repository contains code, datasets and other related resources in support of our paper "MeTeoR: a Metric Temporal Reasoner", which is currently under review at TPLP.

<span id='overview'/>

### Overview:
* <a href='#data'>1. Programs and Datasets </a>
* <a href='#generator'>2. Program Generation </a>
* <a href='#generator'>3. Data Generation </a>
     * <a href="#lubm">LUBM Benchmark</a>
     * <a href="#itemporal">iTemporal Benchmark</a>
     * <a href="#weather">Weather Benchmark</a>
* <a href='#experiments'>4. Repeating our Experiments </a>
* <a href='#meteor'>5. Installation and Examples for MeTeoR</a>



****

<span id="data"/>

#### 1. Programs and Datasets </a>
We put in the **programs** and **datasets** folders all the programs and datasets used in our evaluation apart from the datasets in Figure 4, which 
exceed the size limit of GitHub folders. Subfolders  
fig1_left, fig1_right, fig2, fig3, and fig4 correspond to figure1(left), figure1(right), figure2, figure3, and figure4 in our paper, respectively.
As such, users can easily locate the datasets and programs used in
our experiments according to the folder and file names. For example, the 10 related datasets and 10 related  
programs for the experimental results presented in figure 1(left) can be found in **datasets/fig1_left** and **programs/fig1_left**. 

For large datasets excluded in this repo, we encourage interested users to generate 
these datasets themselves according to the generation methods provided in the subsequent section. 

<span id="generator"/>

#### 2. Program Generation </a>
**iTemporal** programs are generated from the [iTemporal platform](https://github.com/kglab-tuwien/iTemporal) and we provide 
the related json files in the [folder](https://github.com/wdimmy/DatalogMTL_Practical_Reasoning/tree/main/programs/iTemporal).

**LUBM** programs are generated by extending the 56 plain Datalog rules obtained from the OWL 2 RL fragment of LUBM 
with 29 temporal rules involving recursion and mentioning all metric operators avail- able in DatalogMTL.

**Weather** programs are generated by adapting the DatalogMTL program used by Brandt et al. (2018) to 
reason with DatalogMTL about weather, which resulted in a a non-recursive program with 4 rules.


#### 3. Data Generation </a>

In this section we describe how the benchmark data was generated. We provide the relevant 
generators where possible in case users would like to generate new synthetic datasets by themselves. 


<span id="lubm"/>

##### 3.1 Lehigh University Benchmark (LUBM)

<span id="downloadlubm"/>

######  3.1.1 Download the LUBM data generator

You can download the data generator (UBA) from **SWAT Projects - Lehigh University Benchmark (LUBM)** [website](http://swat.cse.lehigh.edu/projects/lubm/). In particular,
we used [UBA1.7](http://swat.cse.lehigh.edu/projects/lubm/uba1.7.zip).

After downloading the UBA1.7 package, you need to add the package's path to CLASSPATH. For example,

```shell
export CLASSPATH="$CLASSPATH:path-to-your-package"
```

<span id="datalog"/>

###### 3.1.2 Generate the OWL files
```
==================
USAGES
==================

command:
   edu.lehigh.swat.bench.uba.Generator
      	[-univ <univ_num>]
	[-index <starting_index>]
	[-seed <seed>]
	[-daml]
	-onto <ontology_url>

options:
   -univ number of universities to generate; 1 by default
   -index starting index of the universities; 0 by default
   -seed seed used for random data generation; 0 by default
   -daml generate DAML+OIL data; OWL data by default
   -onto url of the univ-bench ontology
```

We found some naming and storage issues when using the above command provided 
by the official documentation. To make data generation more user-friendly, we 
wrote a script which can be directly used to generate the required OWL files
by passing some simple arguments. An example is shown as follows,

```python
from meteor_reasoner.datagenerator import generate_owl

univ_nume = 1 # the number of universities you want to generate
dir_name = "./data" # the directory path used for the generated OWL files.

generate_owl.generate(univ_nume, dir_name)

```
In  **./data**, you should obtain OWL files as below,
```
University0_0.owl 
University0_12.owl  
University0_1.owl
University0_4.owl
.....
```

Then, the OWL files need to be converted into unary and binary facts. We also prepared
a script that can be directly used to perform the conversion. 
```python
from meteor_reasoner.datagenerator import generate_datalog

owl_path = "owl_data" # the dir_path where the OWL files are located
out_dir = "./output" # the path for the converted facts

generate_datalog.extract_triplet(owl_path, out_dir)
```
In **./output**, you should see a **./output/owl_data** folder containing data
of the following form 
```
UndergraduateStudent(ID0)
undergraduateDegreeFrom(ID1,ID2)
takesCourse(ID3,ID4)
undergraduateDegreeFrom(ID5,ID6)
UndergraduateStudent(ID7)
name(ID8,ID9)
......
```
and **./output/statistics.txt** contains the statistics information
about the converted facts, for example, 
```
worksFor:540
ResearchGroup:224
....
AssistantProfessor:146
subOrganizationOf:239
headOf:15
FullProfessor:125
The number of unique entities:18092
The number of triplets:8604
```
<span id="datalogmtl"/>

###### 3.1.3 Add punctual intervals

Up to now, we have only constructed the atemporal data, so the final step will be adding temporal information
(intervals) to these atemporal data. In the stream reasoning scenario, we consider punctual intervals, i.e.,
the left endpint equals to the right endpoint (e.g., A@[1,1]). To be more specific, assuming that we have some facts in **datalog/datalog_data.txt**,
and we want to create a dataset containing 10000 temporal facts with each atemporal fact corresponding to at most 2 temporal facts with punctual intervals, and each of 
the time points is randomly chosen from the range [0, 300], we can run the following command (remember to add **--min_val=0, --max_val=300, --punctual**). 
```shell

python add_intervals.py --datalog_file_path datalog/datalog_data.txt --factnum 10000 --intervalnum 2 --min_val 0 --max_val 300 --punctual 

```

In the **datalog/10000.txt**, there should be 10000 facts, each of which in the form P(a,b)@\varrho, and 
some example facts are shown as follows,
```
undergraduateDegreeFrom(ID1,ID2)@[7,7]
takesCourse(ID34,ID4)@[46,46]
undergraduateDegreeFrom(ID5,ID6)@[21,21]
name(ID18,ID9)@[22,22]
......
```

<span id="itemporal"/>

##### iTemporal Benchmark

For the dataset generation based on the iTemporal platform, we refer readers to the 
[official github repository](https://github.com/kglab-tuwien/iTemporal), where a nice web-based  
interface and an easy-to-configure file have been provided for the data generation. A more technical
details about iTemporal can also be found in their [ICDE 2022](https://ieeexplore.ieee.org/document/9835220) paper. 


<span id="weather"/>

##### Weather Benchmark

The Weather Benchmark is based on a freely available dataset with meteorological observations. The original datasets  
could be downloaded from [here](https://www.engr.scu.edu/~emaurer/gridded_obs/index_gridded_obs.html). We have also uploaded our processed data to Google Drive [here](https://drive.google.com/file/d/1wS33E0T-g44FRVrf6QYfbPFquiAA8fFt/view?usp=share_link).


<span id="experiments"/>

#### 4. Repeating our Experiments

##### 4.1 Experiment 1 (Figure 1 (left) in Our Paper)
**An Example Command is as Follows**, in which the dataset path is: **datasets/fig1_left/itemporal_data_1**,
the program path is: **programs/fig1_left/itemporal_program_1**, and the fact path is: **facts/fig1_left/itemporal_data_1.txt**.
 
```shell
  bash run.sh datasets/fig1_left/itemporal_data_1 programs/fig1_left/itemporal_program_1   facts/fig1_left/itemporal_data_1.txt

```
--------------------------------------------------------------------------------

##### 4.2 Experiment 2 (Figure 1 (right) in Our Paper)
**An Example Command is as Follows**, in which the dataset path is: **datasets/fig1_right/itemporal_data_20000**,
the program path is: **programs/fig1_right/itemporal_program_E**, and the fact path is: **facts/fig1_right/itemporal_E_data_2000.txt**.
 
 
```shell
  bash run.sh datasets/fig1_right/itemporal_E_data_2000 programs/fig1_right/itemporal_program_E  facts/fig1_right/itemporal_E_data_2000.txt 
```

--------------------------------------------------------------------------------

##### 4.3 Experiment 3 (Figure 2 in Our Paper)
**An Example Command is as Follows**. You can change the dataset and the program paths (see datasets/fig2 and programs/fig2). By default, we use the naive materialisation and you
can change the mode by passing the argument **--mode**, in which we provide some kinds of choices: **naive**, **seminaive** and **opt**. 

```shell
   python run_1.py --datapath datasets/fig2/itemporal_E_data_100000 --rulepath programs/fig2/itemporal_program_E
```

--------------------------------------------------------------------------------

##### 4.4 Experiment 4 (Figure 3 in Our Paper)
This is the scalability test for the materailisation and it requires large datasets.
You need to prepare the datasets following the instructions provided in the **Data Generation** part.


```shell
 python run_1.py --datapath datasets/fig3/** --rulepath programs/fig3/***
```

--------------------------------------------------------------------------------

##### 4.5 Experiment 5 (Figure 4 in Our Paper)
**An Example Command is as Follows**. You can change the dataset and the program paths (see datasets/fig4 and programs/fig4). 

```shell
 python run_1.py --datapath datasets/fig4/lubm_100000 --rulepath programs/fig4/lubm_p1.txt
```

The code related to the query rewriting method can be found in the **Query_Rewriting** folder.

--------------------------------------------------------------------------------


<span id="meteor"/>

#### 5. Installation and Examples for MeTeoR 

##### 5.1 Installation
You can install MeTeoR using Python's package manager `pip`.

##### Requirements
 - Python>=3.7
 - Numpy>=1.16.0
 - pandas>=0.24.0
 - urllib3>=1.24.0
 - scikit-learn>=0.20.0
 - networkx
 - rdflib
 - outdated>=0.2.0

##### Pip install
The recommended way to install MeTeoR is using Python's package manager pip:
```bash
pip install - U meteor_reasoner
```

##### From source
You can also install MeTeoR from source. This is recommended if you want to contribute to MeTeoR.
```bash
git clone https://github.com/wdimmy/MeTeoR
cd MeTeoR
pip 
```


##### 5.2 Program Syntax
We define the following notations to represent the six MTL operators:
* Diamondminus[1,2] or SOMETIME[-2,-1]
* Boxminus[1,2] or ALWAYS[-2,-1]
* Diamondplus[1,2] or SOMETIME[1,2]
* Boxplus[1,2] or ALWAYS[1,2]
* Since[1,2]
* Until[1,2]

We use ":-" to separate the head and the body atoms and "," as the separator between different 
metric atoms in the body. In addition, the first letter of a constant should be **lowercase**; in contrast, the 
first letter of a variable should be **uppercase**.


As an example, a rule could be written as follows,
```
A(X):- B(a), SOMETIME[-1,0]C(X), Diamondminus[1,2]D(X)
```
##### 5.3 Dataset Syntax
We define the following format to represent a fact:

**F(c_1, ..., c_n)@<t1, t2>**, where **<** could be ( or [, and **>** could be ) or ]; t1 and t2 are two rational numbers with t1<=t2
and c_i with i in [1, ..., n] is a string starting with a **lowercase** letter. 

##### 5.4 An Example
###### Data parser
```python
from meteor_reasoner.utils.loader import load_dataset, load_program

data = ["A(a)@1", "B(a)@[1,2]", "C@(1,2]"]
program = ["A(X):-Diamondminus[1,2]A(X)", "D(X):- Boxminus[1,2]A(X), B(X)Since[1,2]C"]
D = load_dataset(data)
Program = load_program(program)

```


###### Materialisation
```python
from meteor_reasoner.materialization.materialize import materialize
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.utils.operate_dataset import print_dataset
data = ["A(a)@1", "B(a)@[1,2]", "C@(1,2]"]
program = ["A(X):-Diamondminus[1,2]A(X)", "D(X):- Boxminus[1,2]A(X), B(X)Since[1,2]C"]
D = load_dataset(data)
Program = load_program(program)
flag = materialize(D, Program, mode="naive", K=10) # mode could be "naive" or "seminiaive" or "opt" and K is the number of steps of rule application you want to  do
# using any mode and the same number of step, the following output should be the same
print_dataset(D)
````

The above code snippet shows how to run at most 10 rounds of rule applicatioins, and the flag represents whether 
the materialisation reaches the fixed point. The derived facts will be kept in D. 

###### Automata
```python
from meteor_reasoner.automata.buichi_automata import *
from meteor_reasoner.automata.automaton import consistency
data = ["Alive(adam)@0"]
program = ["ALWAYS[0,1]Alive(X) :- Alive(X)"]
D = load_dataset(data)
Program = load_program(program)
fact = parse_str_fact("Alive(adam)@[0,+inf)")
F = Atom(fact[0], fact[1], fact[2])
flag = consistency(D, program, F)
print("Consistency:", flag)
````

#### Contact
For any questions, please drop an email to Dingmin Wang (wangdimmy@gmail.com). 

