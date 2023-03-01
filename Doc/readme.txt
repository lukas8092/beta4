Version 1.0 - brute force only
Project was developed on python 3.11
Run:
- install requirements.txt with pip
- launching directory must be set in root
To run app: python Src/main.py <parametr>
    -parametr:
        -path, for example 'Data/10.txt'
        n, for generation random situation of n cities, example for 10 cities '10'
Example run command: python Src/main.py data/p1.txt

Situation file:
1. first line is number of cities
2. second line number of start city
3. n-lines are lines for routes/costs table
    - values are separeted by ',' 
    - '-' mean empty, no route
Example of converting routes table to required format:
╔═══╤═══╤════╤════╤════╗
║   │ 0 │ 1  │ 2  │ 3  ║
╠═══╪═══╪════╪════╪════╣
║ 0 │ - │ 10 │ 11 │ 54 ║
╟───┼───┼────┼────┼────╢
║ 1 │ 5 │ -  │ 32 │ 41 ║  
╟───┼───┼────┼────┼────╢
║ 2 │ - │ 65 │ -  │ 17 ║
╟───┼───┼────┼────┼────╢
║ 3 │ 1 │ 78 │ 5  │ -  ║
╚═══╧═══╧════╧════╧════╝
           ↓
-,10,11,54
1,5,-,32,41
-,65,-,17
1,78,5,-

Full example of situation file with 4 cities and starting city 0 with table above:
""" Start of file """
4
0
-,10,11,54
1,5,-,32,41
-,65,-,17
1,78,5,-
""" End of file """