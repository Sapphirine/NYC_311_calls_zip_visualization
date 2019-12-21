from django.shortcuts import render, HttpResponse
from . import mappingscript

# Create your views here.
def frontpage(request):
    return render(request, 'frontpage/frontpage.html')
    
def mapper(request):
#    import socket
#    s = socket.socket()
#    port = 8000
#    s.connect(('', port))
#    s.listen()
#    conn, addr = s.accept()
#    DATA = conn.recv(1024)
#    data = DATA.decode("utf-8")
#    splitdata = data[data.find('/?')+2:data.find(' HTTP')].split('&')
#    pairs = []
#    for i in range(len(splitdata)):
#        pairs.append(splitdata[i].split('='))
#    print(pairs)
    
    
    mapped = mappingscript.map_maker()
    return render(request, 'maps/the_map.html')

def form(request):
    from django import forms
    class SimpleForm(forms.Form):
        firstname = forms.CharField(max_length=100)
        lastname = forms.CharField(max_length=100)

    f = SimpleForm()
    f = "<HTML>"+str(f.as_p())+"</HTML>"
    with open("mapapp/templates/frontpage/form.html", "w") as file:
        file.write(f)
    return render(request, 'mapapp/frontpage/form.html')
