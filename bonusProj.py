import ast


global relations
relations = {}


class Relation:
    def __init__(self, name, columns, data):
        self.name = name
        self.columns = columns
        self.data = data

    @classmethod
    def from_query(cls, query):
        # Extracting information from the query
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Employees(ID, Name) = {(1, 'John'), (2, 'Alice'), (3, 'Bob')}
        query_parts = query.split("=")
        name_and_columns = query_parts[0].strip() # Employees(ID, Name, Age)
        data_str = query_parts[1].strip().lstrip('{').rstrip('}') # (1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)

        # Extracting name and columns
        name, columns_str = name_and_columns.split("(")
        name = name.strip() # Employees
        columns = [col.strip() for col in columns_str.rstrip(')').split(',')] # ['ID', 'Name', 'Age']

        # Extracting data using module for programmatic string to list conversion
        # [(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)]
        data = ast.literal_eval(f"[{data_str}]")

        return cls(name, columns, data)

    def __str__(self):
        return f"Relation {self.name} with columns {self.columns} and data {self.data}"


# def select(relation, condition):
#     filtered_data = [row for row in relation.data if condition(row)]
#     return Relation(relation.columns, filtered_data)
#
#
# def project(relation, columns):
#     index_mapping = [relation.columns.index(col) for col in columns]
#     projected_data = [[row[i] for i in index_mapping] for row in relation.data]
#     projected_columns = columns
#     return Relation(projected_columns, projected_data)

while 1:
    # Example Relational Algebra Query
    query = input("""Type in a query: 
    For example:
    Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
    Students(ID, Name, Age) = {(1, 'Johny', 32), (2, 'Alice', 28), (7, 'Bob', 29)}
    Assistants(ID, JobType) = {(9, 'General'), (3, 'Manager'), (2, 'Supervisor')}
    select age>30(employees)
    project ID, Name(employees)
    employees intersect students
    students union employees
    employees minus students
    employees.ID inner join assistants.ID
    """).lower()

    # Performing the Query Operation
    def condition_check(row, column, condition, condition_value):
        if (condition == '='):
            if (row[column] == condition_value):
                results.append(row)
        elif (condition == '<'):
            if (row[column] < condition_value):
                results.append(row)
        elif (condition == '>'):
            if (row[column] > condition_value):
                results.append(row)
        else:
            print("Unsupported condition2")


    if 'select' in query:
        # Parsing the Query
        query_parts = query.split('(')
        operation = query_parts[0].strip()  # 'select age>30'
        params = query_parts[1].replace(')', '').strip()  # 'employees'

        # Extracting the field and condition from the operation
        if ('>' in operation):
            field, condition_value = operation.split(" ")[1].split(">")
            condition = '>'
        elif ('<' in operation):
            field, condition_value = operation.split(" ")[1].split("<")
            condition = '<'
        elif ('=' in operation):
            field, condition_value = operation.split(" ")[1].split("=")
            condition = '='
        else:
            print("Unsupported condition1")
        condition_value = int(condition_value)

        # Convert the params to a relation
        relation = relations[params]

        # Converting the field to the column number
        column = relation.columns.index(field)

        # Filtering the data based on the query
        results = []
        for row in relation.data:
            condition_check(row, column, condition, condition_value) # (1, 'John', 32), 2, 30

        # Printing the result
        print(f"Result for query: {query}")
        for row in results:
            print(row)

    elif 'project' in query: # project ID, Name(employees)
        # Parsing the Query
        query_parts = query.split('(')
        operation = query_parts[0].strip()  # 'select age>30'
        params = query_parts[1].replace(')', '').strip()  # 'employees'

        # Extracting the fields from the query
        operation = operation.replace('project', '').strip() # 'ID, Name'
        fields = [field.strip() for field in operation.split(',')] # ['ID', 'Name']

        # Convert the params to a relation
        relation = relations[params]

        # Converting the fields to the column numbers
        columns = [relation.columns.index(field) for field in fields]

        # Filtering the data based on the query
        results = []
        for row in relation.data: # row = (1, 'John', 32)
            # for col in columns:
            newRow = []
            for col in columns:
                newRow.append(row[col])
            results.append(newRow)
            # results.append([tuple(item[i] for i in columns)])
            # condition_check(row, column, condition, condition_value)  # (1, 'John', 32), 2, 30

        # Printing the result
        print(f"Result for query: {query}")
        for row in results:
            print(row)

    elif 'intersect' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Students(ID, Name, Age) = {(1, 'Johny', 32), (2, 'Alice', 28), (7, 'Bob', 29)}
        # employees intersect students
        # Parsing the Query
        query_parts = query.split('intersect')
        r1 = query_parts[0].strip() # 'employees'
        r2 = query_parts[1].strip() # 'students'

        # Convert the params to a relation
        rel1 = relations[r1]
        rel2 = relations[r2]

        # Filtering the data based on the query
        results = []
        for row in rel1.data:
            # (1, 'John', 32), 2, 30
            if (row in rel2.data):
                results.append(row)

        # Printing the result
        print(f"Result for query: {query}")
        for row in results:
            print(row)

    elif 'union' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Students(ID, Name, Age) = {(1, 'Johny', 32), (2, 'Alice', 28), (7, 'Bob', 29)}
        # students union employees
        # Parsing the Query
        query_parts = query.split('union')
        r1 = query_parts[0].strip() # 'students'
        r2 = query_parts[1].strip() # 'employees'

        # Convert the params to a relation
        rel1 = relations[r1]
        rel2 = relations[r2]

        # Filtering the data based on the query
        results = []
        for row in rel1.data:
            # (1, 'John', 32), 2, 30
            results.append(row)
        for row in rel2.data:
            if row not in rel1.data:
                results.append(row)

        # Printing the result
        print(f"Result for query: {query}")
        for row in results:
            print(row)

    elif 'minus' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Students(ID, Name, Age) = {(1, 'Johny', 32), (2, 'Alice', 28), (7, 'Bob', 29)}
        # employees minus students
        # Parsing the Query
        query_parts = query.split('minus')
        r1 = query_parts[0].strip() # 'employees'
        r2 = query_parts[1].strip() # 'students'

        # Convert the params to a relation
        rel1 = relations[r1]
        rel2 = relations[r2]

        # Filtering the data based on the query
        results = []
        for row in rel1.data:
            # (1, 'John', 32), 2, 30
            if row not in rel2.data:
                results.append(row)

        # Printing the result
        print(f"Result for query: {query}")
        for row in results:
            print(row)

    elif 'inner join' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Assistants(ID, JobType) = {(9, 'General'), (3, 'Manager'), (2, 'Supervisor')}
        # employees.ID inner join assistants.ID
        # Parsing the Query
        query_parts = query.split('inner join')
        r1 = query_parts[0].strip()  # 'employees.ID'
        r2 = query_parts[1].strip()  # 'assistants.ID'

        # Convert the params to a relation
        rel1 = relations[r1.split('.')[0]] # employees
        rel2 = relations[r2.split('.')[0]] # assistants
        merge_col1 = r1.split('.')[1]
        merge_col2 = r2.split('.')[1]

        # Filtering the data based on the query
        results = []
        for row in rel1.data:
            # (1, 'John', 32), 2, 30
            if row not in rel2.data:
                results.append(row)

        # Printing the result
        print(f"Result for query: {query}")
        for row in results:
            print(row)

    elif 'quit' in query:
        break

    else:
        # create a new relation
        newRelation = Relation.from_query(query)
        relations[newRelation.name] = newRelation

        # Applying the query and printing the result
        print(f"Result for query: {query}")
        # print(employees)
