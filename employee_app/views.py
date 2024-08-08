
# Import necessary modules and functions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
import uuid
from django.db.models import Q
"""Create employee starts"""
# Define API view for creating an employee
@api_view(['POST'])
def createEmployee(request):
    # Use exception handling to catch potential errors
    try:
         # Check if the email provided already exists in the database
        email = request.data.get('email')
        if Employee.objects.filter(email=email).exists():
            return Response({'message': 'Employee already exists', 'success': False}, status=status.HTTP_200_OK)
         # Define expected data types for each field
        data_types = {
            'name': str,
            'email': str,
            'age': int,
            'gender': str,
            'phoneNo': str,
            'addressDetails': dict,
            'workExperience': list,
            'qualifications': list,
            'projects': list,
            'photo': str
        }

        for key, data_type in data_types.items():
            if key not in request.data or not isinstance(request.data[key], data_type):
                return Response({'message': 'Invalid body request', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        required_keys = ['name', 'email', 'age', 'gender', 'phoneNo', 'addressDetails', 'workExperience', 'qualifications', 'projects', 'photo']
        for key in required_keys:
            if key not in request.data:
                return Response({'message': 'Invalid body request', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Get the total number of employees created
            total_employees = Employee.objects.count()
            
            # Increment the total number of employees by 1 to get the next employee number
            employee_number = total_employees + 1
            
            # Generate the regid in the format EMP001, EMP002, ...
            regid = "EMP" + str(employee_number).zfill(3)  
            
            # Save the employee record
            serializer.save()
            
            # Return the response with the generated regid
            return Response({'message': 'Employee created successfully', 'regid': regid, 'success': True}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Invalid body request', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': 'Employee creation failed: {}'.format(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""Create  employee ends here"""

"""get all the employee starts from here"""
@api_view(['GET'])
def getEmployee(request, regid=None):
    # Use exception handling to catch potential errors
    try:
        if regid:
            # Extract the numeric part from the regid 
            regid_number = int(regid[3:])  
            
            # If regid is provided, retrieve details for a single employee
            try:
                # Retrieve the employee based on the regid number
                employee = Employee.objects.get(id=regid_number)
                serializer = EmployeeSerializer(employee)
                return Response({'message': 'Employee details found', 'success': True, 'employee': serializer.data}, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                # Return message if employee with the provided regid does not exist
                return Response({'message': 'Employee details not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no regid provided, retrieve details for all employees
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response({'message': 'Employee details found', 'success': True, 'employees': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Return error message if an exception occurs during employee retrieval
        return Response({'message': 'Error occurred while retrieving employee details: {}'.format(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""get all the employee ends from here"""


"""Update the employee starts from here"""
# Define API view for updating an employee
@api_view(['PUT'])
def updateEmployee(request, regid):
    # Use exception handling to catch potential errors
    try:
        # Retrieve the employee object with the provided regid
        try:
            # Extract the numeric part from the regid 
            regid_number = int(regid[3:])  
            employee = Employee.objects.get(id=regid_number)
        except ValueError:
            return Response({'message': 'Invalid regid format', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize the request data and perform the update (allow partial updates)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        
        # Check if the serializer is valid and save the updated data
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee updated successfully', 'success': True}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid body request', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    except Employee.DoesNotExist:
        # Return message if employee with the provided regid does not exist
        return Response({'message': 'Employee not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Return error message if an exception occurs during employee update
        return Response({'message': 'Employee update failed: {}'.format(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Update the employee ends here"""



"""Delete employee starts from here"""

@api_view(['DELETE'])
def deleteEmployee(request, regid):
    # Use exception handling to catch potential errors
    try:
        # Retrieve the employee object with the provided regid
        try:
            # Extract the numeric part from the regid 
            regid_number = int(regid[3:])  
            employee = Employee.objects.get(id=regid_number)
        except ValueError:
            return Response({'message': 'Invalid regid format', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete the retrieved employee object
        employee.delete()
        
        # Return success response
        return Response({'message': 'Employee deleted successfully', 'success': True}, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        # Return message if employee with the provided regid does not exist
        return Response({'message': 'Employee not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Return error message if an exception occurs during employee deletion
        return Response({'message': 'Employee deletion failed: {}'.format(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Delete employee ends here"""
