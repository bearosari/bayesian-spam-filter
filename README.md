# bayesian-spam-filter

#specifications

Spam Filtering is a problem that may be modeled as a two-category classification problem. The first category represents
legitimate messages or Ham, and the other category represents junk e-mail also known as Spam. In this Software
Project, you are to implement a program that classifies emails into these two categories using the concepts of Conditional
Probability and Bayes’ Theorem. In order to implement a working implementation of a Spam Filter, you will need to
provide a foundation or basis on how your program will classify e-mails. Thus, the program has two phases of execution,
namely, Training and Testing. In the Training phase, your goal is to provide pre-classified e-mails to your program so
that it can use the information extracted from those e-mails as a basis for computing the probability of an e-mail being
classified as legitimate or unsolicited. You will classify e-mails as Spam of Ham solely based on the frequency
of words in Spam or Ham e-mails. Once your program has been trained with pre-classified information, you can then
input actual e-mail content into your program and classify them as Ham or Spam using the results from the Training
phase. However, to test the performance of your Spam Filter, you will feed a second set of pre-classified e-mails to your
program to check how well it classifies e-mails. You are to assess the performance of your Spam Filter quantitatively
using the Precision and Recall metrics. Note that this Software Project is completely solvable using only the Python3
math library, but you are free to use external libraries if you understand their usage.

In this Software Project, you are provided a .zip file named trec06p-eee111.zip. This is a dataset that holds a plethora
of e-mails, and was obtained from this website: https://plg.uwaterloo.ca/∼gvcormac/treccorpus06/about.html. Upon
extraction, you will see two files and one folder. The first file, named "labels" contains the true classification of all the
email files in the set. The second file, named "README.rtl" just tells you that the relevant emails that you will use
for the Training phase in the "data" folder are the content of folders 0 to 70, and the dataset for the Testing phase
are in folders 71 onwards. Finally, the "data" folder holds all the email files grouped into many folders as stated in the
README.rtl file. Note that each folder has 300 emails with a standard naming convention.

#Reading the E-mail Files

Your first objective in this Software Project is to extract the contents of the .zip folder to gain access to the uncompressed
e-mail files. Once uncompressed, you should not open these e-mail files using a browser or anything that can run
JavaScript code as some of the e-mails are nasty or possibly NSFW Spam e-mails. You should open the files via a regular
and properly updated text editor for inspection. Some of the files, or some of the e-mail contents are not using the
standard ASCII or UTF-8 character encodings used in English messages. We will ignore e-mail contents that do not use
ASCII or UTF-8 encoding as we are building a Spam Filter suited for those who use English as their primary language.
Creating a Spam Filter for Chinese messages or other languages not using Roman letters is out of scope for the project.
Another common source for non UTF-8 data are attached images, video, and other files. You can safely disregard those
data as we will only filter Spam e-mails based on the words in the e-mails alone. It will be up to you how you will handle
files or content that do not adhere to ASCII or UTF-8 encoding.

#Decomposing & Determining list of words

Your next objective is to decompose each and every e-mail in the Test Set (data/000 to data/070) into a list of
words. To simplify the process, we will define a word as any string with only alphabetical characters [a-z,A-Z].
Each word is separated by a whitespace (spaces, tabs, newlines, and similar characters) in front of the word (or nothing
if it is the first word), and by whitespace or a single symbol of any kind (periods, commas, and similar symbols). For
example, “Hello”, “ XDXB! ”, and “NBSP&” are words, but “Hello...”, “spicy_gil123”, or similar constructs are not. Again,
note that you can discard e-mails that are fully non UTF-8 compliant. Also note that the words “banana”, “BANANA”,
“bAnAnA”, or other forms of capitalization are considered the same word (i.e. treat every word as having the same case).

Once you decompose all of the emails in the Test Set, you will count the number of Ham and Spam e-mails that contain
each word. For example, the word “banana” appears in 1078 Ham e-mails and 10384 Spam e-mails, so you count the
occurrence as such. Note that you should not count the occurrence of a word more than once in a single e-mail. Based
on the word count, add up the occurrences for each word (e.g. “banana” occurs in 11462 test emails in total), and use
the total word count to determine the top 5000 words. Save the top 5000 words, their number of occurrences in Ham
emails, their number of occurrences in Spam emails, and their total occurrences in the Test Set in a file.

