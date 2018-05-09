# Assignment 4: Music Recommender

# Github link
You can also access our file here (you need TA's handle to access)
https://github.com/yw778/COMS6998_Chatbot_AWS

# Team(11) member
- Danwen Yang (dy2349)
- Jiachen Yang (jy2865)
- Yu Wang (yw3025)
- Ke Yin (ky2372)

# version 
We are using spark version 1.6 (same as the one specified in the aws instructions on github).
 
# Source Files
- `spark.py`: .py file for music recommendation (used in aws)
- `spark_VM.py`: py file for music recommendation (used in virtualbox linux terminal)


# Log Files
- `virtual_box_consoleout.txt` output logs in virtual box linux terminal, use `tail` to see
the recommendation result 

# Screen Shots
- `aws_step_add`: add step parameters.
- `aws_step_running`: step running after add
- `aws_step_complete`:  step successful complete
- `aws_console_output`:  output result in aws console output stdout

# Result output in AWS_EMR (top 10 recommendations)
- 2Pac
- 50 Cent
- The Game
- Snoop Dogg
- Jay-Z
- Dr. Dre
- Ludacris
- Nas
- Kanye West
- Eminem
Our AWS_EMR result contains the top five recommendations as in the book(50 Cent, Jay-Z, Kanye West, 2Pac, The Game)


# Result output in virtual_box_VM (top 10 recommendations)
- 50 Cent
- 2Pac
- The Game
- Kanye West
- Ludacris
- Jay-Z
- Snoop Dogg
- Dr. Dre
- Nelly
- Nas
Our virtual_box_VM result contains the top five recommendations as in the book(50 Cent, Jay-Z, Kanye West, 2Pac, The Game)

Note the result is slightly different from aws output since virtual box VM use spark 1.3 and aws use spark 1.6.
Also, the algorithm may use different random seed to initiate but all of them contains the top 5 recommendations in the book.