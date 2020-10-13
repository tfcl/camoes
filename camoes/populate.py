from library.models import Book, Publisher, Authors

b= Book(title='o amor é lindo',stock='1',year='2003',  classification='PQ2003', isbn='4544343', status='Disponivel')

Book.save()