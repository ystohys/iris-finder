# IrisFinder

This tool has been developed for:
	- Simple visualisation of Iris flowers datasets
	- Obtaining of historical samples that are the most similar to a new Iris flower in terms of its measurements

Development was done entirely in a MacOS environment, but this should still run on other operating systems. However, if you encounter any issues, kindly raise an issue here (with a description of the problem and your operating system) and I will take a look at it.

# Setup

1. Install Python (any version above 3.7), if you have yet to done so.

2. Navigate to the directory containing the code (where main.py, data_utils.py,... are located) using Terminal (Linux/MacOS) or PowerShell/Command Prompt (Windows)

3. Create and activate a virtual environment using venv or Anaconda/Miniconda. Instructions can be found at the links below:
	> venv: https://docs.python.org/3/library/venv.html
	> conda: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands

4. Install the following packages in the virtual environment:
	> numpy==1.22.4
	> pandas==1.4.2
	> matplotlib==3.5.2
	> seaborn==0.11.2
	> scikit-learn==1.1.1

	** you can also run "pip install -r requirements.txt" for convenience

5. Once installed, start the program by running main.py:
	> run this command: python3 main.py

6. The program's GUI should be launched and ready for use.

# Usage instructions

1. Upon start, you should be in the "Load Data" tab. If not, click on the "Load Data" tab.

2. In the "Path to CSV file" field, type in the path to the csv file containing the historical Iris dataset. If the dataset is named "iris_data.csv" and located in your current working directory, you only need to key in "iris_data.csv".

3. Tick the corresponding checkboxes if you wish to perform data cleaning when the data is loaded in.

4. Under 'Data Overview', select "Overall" if you wish to see the distribution of the numerical variables in the overall dataset. Select "Stratified" if you wish to see the distribution of the numerical variables across each flower type. 

4. Click on the "Click here to load data" button to load in your data and plot the distributions.

5. Once done, navigate to the "Find Similar Flowers" tab. 

6. Key in the input measurements of the new Iris flower under each corresponding field (Sepal Length, Sepal Width etc). 

7. Click on the "Click here to obtain data of similar flowers" button to generate:
	> A table containing the 10 historical data observations that are most similar to the new Iris flower
	> A scatterplot showing the distribution of the numerical variables of the similar observations, compared to the new observation (indicated by a red "x")