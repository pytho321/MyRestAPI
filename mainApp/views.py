from django.shortcuts import render
from .serializers import EmployeeSerializer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
import io

# Create your views here.
def home(request):
    return render(request, 'index.html')

@csrf_exempt
def employeeAPI(request):
    if(request.method=="GET"):
        jdata = request.body
        stream = io.BytesIO(jdata)
        pdata = JSONParser().parse(stream)
        id = pdata.get("id",None)
        name = pdata.get("name",None)
        email = pdata.get("email",None)
        dsg = pdata.get("dsg",None)
        city = pdata.get("city",None)
        state = pdata.get("state",None)
        salary = pdata.get("salary",None)
        if(id is not None):
            emp = Employee.objects.filter(id=id)
            serializer = EmployeeSerializer(emp,many=True)
        elif(name is not None):
            emp = Employee.objects.filter(name=name)
            serializer = EmployeeSerializer(emp,many=True)
        elif(email is not None):
            emp = Employee.objects.filter(email=email)
            serializer = EmployeeSerializer(emp,many=True)
        elif(dsg is not None):
            emp = Employee.objects.filter(dsg=dsg)
            serializer = EmployeeSerializer(emp,many=True)
        elif(city is not None):
            emp = Employee.objects.filter(city=city)
            serializer = EmployeeSerializer(emp,many=True)
        elif(state is not None):
            emp = Employee.objects.filter(state=state)
            serializer = EmployeeSerializer(emp,many=True)
        elif(salary is not None):
            emp = Employee.objects.filter(salary=salary)
            serializer = EmployeeSerializer(emp,many=True)
        else:
            emp = Employee.objects.all()
            serializer = EmployeeSerializer(emp,many=True)
        jsonData = JSONRenderer().render(serializer.data)
        return HttpResponse(jsonData,content_type="application/json")
    elif(request.method=="POST"):
        jdata = request.body
        stream = io.BytesIO(jdata)
        pdata = JSONParser().parse(stream)
        serializer = EmployeeSerializer(data=pdata)
        if(serializer.is_valid()):
            serializer.save()
            res = {"msg":"Record Inserted"}
        else:
            res = {"msg":"Record is not Valid"}
        jsonData = JSONRenderer().render(res)
        return HttpResponse(jsonData,content_type="application/json")
    elif(request.method=="PUT"):
        jdata = request.body
        stream = io.BytesIO(jdata)
        pdata = JSONParser().parse(stream)
        id = pdata.get("id",None)
        if(id is not None):
            emp = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(emp,data=pdata,partial=True)
            if(serializer.is_valid()):
                serializer.save()
                res = {"msg":"Record Updated"}
            else:
                res = {"msg":"Record is not Valid"}
        else:  
            res = {"msg":"No Record Found to Update"}
        
        jsonData = JSONRenderer().render(res)
        return HttpResponse(jsonData,content_type="application/json")
    elif(request.method=="DELETE"):
        jdata = request.body
        stream = io.BytesIO(jdata)
        pdata = JSONParser().parse(stream)
        id = pdata.get("id",None)
        if(id is not None):
            emp = Employee.objects.get(id=id)
            emp.delete()
            res = {"msg":"Record Deleted"}
        else:  
            res = {"msg":"No Record Found to Delete"}
        
        jsonData = JSONRenderer().render(res)
        return HttpResponse(jsonData,content_type="application/json")