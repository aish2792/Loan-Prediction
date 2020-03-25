# Loan Approval Prediction

Loan prediction is a very common real-life problem that every retail bank faces in their lending operations. If the loan approval process is automated, it can save a lot of man hours and improve the speed of service to the customers. We made an application to automate the loan eligibility process (real time) based on customer detail provided while filling online application form. These details are Gender, Marital Status, Education, Number of Dependents, Income, Loan Amount, Credit History and others. We thereby, predict customers who are eligible to get a loan through this application.

Firstly, we did a comparative study on various algorithms to see which algorithm worked best for our dataset. After trying and testing 5 different algorithms, the best accuracy is achieved by Logistic Regression (80.61), followed by Naïve bayes (79.62), followed by Random Forest (77.35) and Decision Tree (73.30), while Support Vector Machine performed the worst (68.73).

This comparative study can found in the jupyter notebook in the folder we submitted called 'LoanPrediction.ipynb'.

We adopted Logistic Regression into our application. To run the application follow the steps below.

## Getting Started

We	will	be	using	Flask	as
our	web	framework.Flask	is	a	Python-based	framework. If	you	do	not	have	Python	3	on	your	local	machine,	we	recommend	that	you	look	through	the	Python	downloads	page	(https://www.python.org/downloads/) and	install	Python	3 in	whatever	way	is	appropriate	for	your	machine. In	the	end,	you	should	be	able	to	enter

```
> python3 --version
```
and	see	a	version	number	of	3.3	or	higher.

### Installing
Next,	you	will	need	to	install	the	Flask	package	within	the	Python	setup. This	is	easily	done
by	entering:

```
> pip3 install Flask
```
## Open the application

To	test	your	setup,	please	download	the	ZIP	package	available	as	part	of	this	project.
The	directory, ML_Project, includes	files	and
libraries	that	we	will	be	using.	In	a terminal	window,	please	navigate	to	the ML_Project/webdev4/app5/ directory	and
enter	the	following	command:

```
> python3 run.py
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
...
```

This	command	runs	the	included	Python	file,	which	in	turns	starts	a	Flask	web	server	on	a local	address	and	port	number	(http://127.0.0.1:5000).	Now,	open	a	web	browser	(Chrome,	Safari,	Firefox,	or	any	browser),	and	point	it	to	this	address;	when	you	do	so,
Flask	will	“serve”	the	web	page	provided	and	show	you	a	page just like the one we included in our paper.
