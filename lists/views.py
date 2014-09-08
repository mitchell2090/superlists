from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request) :
    return HttpResponse('''
<html>
<header>
  <title>To-Do lists</title>
</header>
<body>
  <h1>To-Do Damn it</h1>

</html>')
''')
