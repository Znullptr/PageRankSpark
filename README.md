# Page Rank Using Spark 
This project aims to rank web pages based on the google page rank algorithm utilizing big data technologies such as Apache Spark.

# Description
For this project we used PSXHAX website as an example. PSXHAX is a website that focus on bringing news about ps4 and ps5 jailbreaking scene and has around 444 pages in the time this repository is deployed, Every page contains several threads and in this context we are trying to extract and  rank all the threads that exists in the website using google page rank algorithm logic.

# Overview
 For simplicity, i splitted this project into two main parts. In the first part, we extracted useful informations about all the pages (threads) that exists in PSXHAX and saved them into a csv file.(see **psxhax_pages_extract.py**)  

The psxhax_pages_info.csv file consists of 4 columns: 

  page_id: the id of the page.  
  
  page_title: the title of the page.  
  
  page_url: the url of the page.  
  
  links: the existing pages links in every page.  

After that, we ran the google page rank algorithm and sorted all the pages based on their rank scores and saved them again into another csv file.(see **psxhax_pages_rank.py**)  

We obtained then the ranked_psxhax_pages.csv file with the following added column:  

pagerank: the rank of the page.  

In the second part, we are going to work with PySpark and graphframes to compute pages ranks and compare them with the obtained results.(see **Setup and Usage**)

# Prerequisites

In order to run this projet you need to have:  

   Working virtual machines with linux os installed on each one of them (i used lubuntu os).  
   
   Fully configured and installed hadoop in cluster mode (i used hadoop 3.3.4).  
   
   Apache Spark installed on top of hadoop (i used spark 3.4.1).  
   
   Python 3 or later installed.  
 

# Setup and Usage
To set up the project locally, follow these steps:  

1) Clone the repository: git clone <https://github.com/Znullptr/PageRankSpark>

2) Copy page_rank_spark.py script and psxhax_pages_info.csv to your hdfs.

3) Download graphframes latest jar version from this url <https://spark-packages.org/package/graphframes/graphframes> and copy it to the jars folder existing in the spark home installation directory.

4) Install graphframes dependency in all your cluster nodes using this command > sudo pip install graphframes. Alternatively, you can use --files option to copy dependencies to all nodes in the spark submit command.

5) Run the below command to start the spark job:
   > spark-submit --master yarn \
    --deploy-mode cluster \
    --driver-memory 512m \
    --executor-memory 512m \
    --executor-cores 1 \
    --num-executors 2 \
    hdfs://Master:9000/user/hadoop/py_scripts/page_rank_spark.py \
    inputs/psxhax_pages_info.csv

   Please modify this command in order to match your environnement resources and your hdfs path to your python script.
   
6) Open your yarn interface and visualize the spark job progress:
  <p>
   <img width="800" height="500" src="https://github.com/Znullptr/PageRankSpark/blob/main/images/yarn_interface_output.jpg">
  </p>  

7) Once it's successfully completed, open your hdfs interface and download the output csv file:
  <p>
   <img width="800" height="500" src="https://github.com/Znullptr/PageRankSpark/blob/main/images/hdfs_interface_output.jpg">
    </p>  

8) Compare the new results with your previous obtained results.


# Conclusion
   
