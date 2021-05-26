import happybase
import pandas as pd

connection = happybase.Connection('localhost', autoconnect=False)
connection.open()
def retriveDataFrame(connection,tableName):
    try:
        data = connection.table(tableName)  #get the table with tableName and connection
        data=list(data.scan())  #gives the list to tuples which contains row index and dict of column names and values
        columns=list(data[0][1].keys())  #grab the first tuple from list of index 1 which gives the dict to get the column names
        columns=[col.decode().split(":")[1] for col in columns] #decode the names and name the list of columns
        index=[row[0].decode() for row in data]  #getting the row index iterating through the whole list of tuple pairs and encode the,
        index=pd.to_numeric(index)  #converting the data to numberic as the data type is string
        #now iterate through each row which has tuple and with index one grad dict and get the values from dict.items() and store as list of lists
        rowData=[[value.decode() for key,value in row[1].items()] for row in data] 
        df=pd.DataFrame(rowData,columns=columns,index=index) #make the data Frame with rowData ,columns and index values
        for column in df.columns:
            try:
                df[column]=pd.to_numeric(df[column]) #as the data stored as object if the data for specific column is numric using try,except to convert it
            except:
                pass
        df.sort_index(inplace=True)
        return df
    except :
        "Error while creating the data frame"

print(retriveDataFrame(connection,'youtubeComments'))