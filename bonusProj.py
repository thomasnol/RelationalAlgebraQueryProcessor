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

while 1:
    # Example Relational Algebra Query
    query = input("Type in a query: Use 'info' for info, 'relations' for all the relations and 'quit' to quit\n").lower().strip()

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

    if 'relations' == query:
        # Print all relations
        print("All relations:")
        for key in relations:
            print(relations[key])
        continue

    if 'select' in query:
        # Parsing the Query
        query_parts = query.split('(')
        operation = query_parts[0].strip()  # 'select age>30'
        params = query_parts[1].replace(')', '').strip()  # 'employees'

        operation = operation.replace('select', '').strip() # 'age>30'

        # Extracting the field and condition from the operation
        if ('>' in operation):
            field, condition_value = operation.split(">")
            condition = '>'
        elif ('<' in operation):
            field, condition_value = operation.split("<")
            condition = '<'
        elif ('=' in operation):
            field, condition_value = operation.split("=")
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
        print(relation.columns)
        for row in results:
            print(row)

    elif 'project' in query: # project ID, Name(employees)
        # Parsing the Query
        query_parts = query.split('(')
        operation = query_parts[0].strip()  # 'project ID, Name'
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
        print(fields)
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
        print(rel1.columns)
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
        print(rel1.columns)
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
        print(rel1.columns)
        for row in results:
            print(row)

    elif 'inner join' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Assistants(JobID, JobType) = {(9, 'General'), (3, 'Manager'), (2, 'Supervisor')}
        # employees.ID inner join assistants.ID
        # Parsing the Query
        query_parts = query.split('inner join')
        r1 = query_parts[0].strip()  # 'employees.ID'
        r2 = query_parts[1].strip()  # 'assistants.ID'

        # Convert the params to a relation
        rel1 = relations[r1.split('.')[0]] # employees
        rel2 = relations[r2.split('.')[0]] # assistants
        merge_col1 = r1.split('.')[1] # 'ID'
        merge_col2 = r2.split('.')[1] # 'jobID'

        # Converting the field to the column number
        col1 = rel1.columns.index(merge_col1)
        col2 = rel2.columns.index(merge_col2)

        # Filtering the data based on the query
        results = []
        for row in rel1.data:
            # (1, 'John', 32), 2, 30
            # find the matching row in rel2
            for row2 in rel2.data:
                if row[col1] == row2[col2]: # if matching key column value found
                    # create new list with all columns from both relations
                    newRow = [row + row2]
                    results.append(newRow)
                    break

        # Printing the result
        print(f"Result for query: {query}")
        print(rel1.columns + rel2.columns)
        for row in results:
            print(row)

    elif 'left outer join' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Assistants(JobID, JobType) = {(9, 'General'), (3, 'Manager'), (2, 'Supervisor')}
        # employees.ID left outer join assistants.JobID
        # Parsing the Query
        query_parts = query.split('left outer join')
        r1 = query_parts[0].strip()  # 'employees.ID'
        r2 = query_parts[1].strip()  # 'assistants.JobID'

        # Convert the params to a relation
        rel1 = relations[r1.split('.')[0]] # employees
        rel2 = relations[r2.split('.')[0]] # assistants
        merge_col1 = r1.split('.')[1] # 'ID'
        merge_col2 = r2.split('.')[1] # 'jobID'

        # Converting the field to the column number
        col1 = rel1.columns.index(merge_col1)
        col2 = rel2.columns.index(merge_col2)

        # Filtering the data based on the query
        results = []
        matching_row_found = False
        for row in rel1.data:
            # (1, 'John', 32), 2, 30
            # find the matching row in rel2
            for row2 in rel2.data:
                if row[col1] == row2[col2]: # if matching key column value found
                    # create new list with all columns from both relations
                    newRow = [row + row2]
                    results.append(newRow)
                    matching_row_found = True
                    break
            if not matching_row_found:
                # if no matching row found in rel2
                newRow = list(row)
                newRow.extend([None] * len(rel2.columns))
                results.append(newRow)

        # Printing the result
        print(f"Result for query: {query}")
        print(rel1.columns + rel2.columns)
        for row in results:
            print(row)

    elif 'right outer join' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Assistants(JobID, JobType) = {(9, 'General'), (3, 'Manager'), (2, 'Supervisor')}
        # employees.ID right outer join assistants.JobID
        # Parsing the Query
        query_parts = query.split('right outer join')
        r1 = query_parts[0].strip()  # 'employees.ID'
        r2 = query_parts[1].strip()  # 'assistants.JobID'

        # Convert the params to a relation
        rel1 = relations[r1.split('.')[0]] # employees
        rel2 = relations[r2.split('.')[0]] # assistants
        merge_col1 = r1.split('.')[1] # 'ID'
        merge_col2 = r2.split('.')[1] # 'jobID'

        # Converting the field to the column number
        col1 = rel1.columns.index(merge_col1)
        col2 = rel2.columns.index(merge_col2)

        # Filtering the data based on the query
        results = []
        matching_row_found = False
        for row2 in rel2.data:
            # (1, 'John', 32), 2, 30
            # find the matching row in rel1
            for row1 in rel1.data:
                if row1[col1] == row2[col2]: # if matching key column value found
                    # create new list with all columns from both relations
                    newRow = [row1 + row2]
                    results.append(newRow)
                    matching_row_found = True
                    break
            if not matching_row_found:
                # if no matching row found in rel1
                newRow = [None] * len(rel1.columns)
                newRow.extend(list(row2))
                results.append(newRow)

        # Printing the result
        print(f"Result for query: {query}")
        print(rel1.columns + rel2.columns)
        for row in results:
            print(row)

    elif 'full outer join' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Assistants(JobID, JobType) = {(9, 'General'), (3, 'Manager'), (2, 'Supervisor')}
        # employees.ID full outer join assistants.JobID
        # Parsing the Query
        query_parts = query.split('full outer join')
        r1 = query_parts[0].strip()  # 'employees.ID'
        r2 = query_parts[1].strip()  # 'assistants.JobID'

        # Convert the params to a relation
        rel1 = relations[r1.split('.')[0]]  # employees
        rel2 = relations[r2.split('.')[0]]  # assistants
        merge_col1 = r1.split('.')[1]  # 'ID'
        merge_col2 = r2.split('.')[1]  # 'jobID'

        # Converting the field to the column number
        col1 = rel1.columns.index(merge_col1)
        col2 = rel2.columns.index(merge_col2)

        # keep track of which rows have not been matched yet within rel2
        remaining_rows = list(rel2.data)

        # Filtering the data based on the query
        results = []
        matching_row_found = False
        for row in rel1.data:
            # (1, 'John', 32), 2, 30
            # find the matching row in rel2
            for row2 in rel2.data:
                if row[col1] == row2[col2]:  # if matching key column value found
                    if row2 in remaining_rows:
                        remaining_rows.remove(row2)
                    # create new list with all columns from both relations
                    newRow = [row + row2]
                    results.append(newRow)
                    matching_row_found = True
                    break
            if not matching_row_found:
                # if no matching row found in rel2
                newRow = list(row)
                newRow.extend([None] * len(rel2.columns))
                results.append(newRow)
        # add remaining rows from rel2 that were not matched
        for row2 in remaining_rows:
            newRow = [None] * len(rel1.columns)
            newRow.extend(list(row2))
            results.append(newRow)
        # Printing the result
        print(f"Result for query: {query}")
        print(rel1.columns + rel2.columns)
        for row in results:
            print(row)

    elif 'cproduct' in query:
        # Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
        # Students(ID, Name, Age) = {(1, 'Johny', 32), (2, 'Alice', 28), (7, 'Bob', 29)}
        # employees cproduct students
        # Parsing the Query
        query_parts = query.split('cproduct')
        r1 = query_parts[0].strip() # 'employees'
        r2 = query_parts[1].strip() # 'students'

        # Convert the params to a relation
        rel1 = relations[r1]
        rel2 = relations[r2]

        # Filtering the data based on the query
        results = []
        for row in rel1.data:
            # (1, 'John', 32), 2, 30
            for row2 in rel2.data:
                results.append(row+row2)

        # Printing the result
        print(f"Result for query: {query}")
        print(rel1.columns+rel2.columns)
        for row in results:
            print(row)

    elif 'info' in query:
        print("""Examples of queries:
    Employees(ID, Name, Age) = {(1, 'John', 32), (2, 'Alice', 28), (3, 'Bob', 29)}
    Students(ID, Name, Age) = {(1, 'Johny', 32), (2, 'Alice', 28), (7, 'Bob', 29)}
    Assistants(jobID, JobType) = {(9, 'General'), (3, 'Manager'), (2, 'Supervisor')}
    select age>30(employees)
    project ID, Name(employees)
    employees intersect students
    students union employees
    employees minus students
    employees cproduct students
    employees.ID inner join assistants.JobID
    employees.ID left outer join assistants.JobID
    employees.ID right outer join assistants.JobID
    employees.ID full outer join assistants.JobID""")

    elif 'quit' in query:
        break

    else:
        # create a new relation
        newRelation = Relation.from_query(query)
        relations[newRelation.name] = newRelation

        # Applying the query and printing the result
        print("Relation successfully added")
