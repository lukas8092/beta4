Version 4.0 - Heuristics - branch and bound method with network paralization
Project was developed on python 3.11
Run:
- install requiments.txt with pip
- launching directory must be set in root
For Server:
    for server config file in Config folder is 'server-config.json'
        Parametrs:
            address, port
    Run command: python Src/ServerSide/main.py <parametr>
        -parametr:
            -path, for example 'Data/10.txt'
            n, for generation random situation of n cities, example for 10 cities '10'
        Server will wait to workers to connect, when somebody connect, it will print info about it
        Solving of the problem will start after pressing key ENTER
For Client:
    for client config file in Config folder is 'client-config.json'
    Parametrs:
        address = address of server
        port = port of server
        name = name of worker
    Run command: python Src/ClientSide/main.py
        Client will connect to server and wait until server start solving problem

To run app: python Src/main.py <parametr>

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