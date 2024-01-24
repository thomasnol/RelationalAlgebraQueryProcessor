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


def select(relation, condition):
    filtered_data = [row for row in relation.data if condition(row)]
    return Relation(relation.columns, filtered_data)


def project(relation, columns):
    index_mapping = [relation.columns.index(col) for col in columns]
    projected_data = [[row[i] for i in index_mapping] for row in relation.data]
    projected_columns = columns
    return Relation(projected_columns, projected_data)

while 1:
    # Example Relational Algebra Query
    query = input("""Type in a query: 
    For example:
    Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
    Employees(ID, Name) = {(1, 'John'), (2, 'Alice'), (3, 'Bob')}
    select age>30(employees)
    project ID, Name(employees)
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

        # Filtering the employees_data based on the query
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

        # Filtering the employees_data based on the query
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

    elif 'quit' in query:
        break

    else:
        # create a new relation
        newRelation = Relation.from_query(query)
        relations[newRelation.name] = newRelation

        # Applying the query and printing the result
        print(f"Result for query: {query}")
        # print(employees)
