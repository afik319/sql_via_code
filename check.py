from SQLViaCode.SQLViaCode import get_query_from_db, exec_procedure_from_db

pName = "checkProcedure"
dict1 = {"caml_id": 17590}  # The key matches the parameter in the query
print(exec_procedure_from_db(pName, "coopapartmentmonthlyloans" , None , dict1))