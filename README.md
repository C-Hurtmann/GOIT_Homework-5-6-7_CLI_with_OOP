# GOIT_Homework-5_CLI_with_OOP
Console bot - phone book. Created with with OOP
main.py is a run file

DEFINITIONS:
Command - command word itself
Name - one word started from Capital letter
Birthday - date in format dd.mm.yyyy
Phone - accept most of kinds of phone records. Only UA domain

COMMANDS:
add - addition record to the address book. Required Command and Name. Optional Birthday and Phone

change - changing excisting phone in record to another phone. Able to do one to one, one to many, many to many changing. Reqired Command, Name, old Phone, new Phone and word 'to' that splits old and new Phones

search - show records containing searched substring. Required Command, substring needs to be searched

show all - shows all records in address book. Required Command

show - shows a certain numbers of records in address bool. Required Command and number

birthday - shows how many days left to birthday for certain record. Required Command, Name