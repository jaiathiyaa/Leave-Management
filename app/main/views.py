from django.shortcuts import render, redirect
from .mongo_models import User , Leave
from django.contrib import messages
import datetime

# ✅ LOGIN VIEW
def login(request):
    if request.session.get("user_email"):
        # If already logged in, redirect based on role
        role = request.session.get("role")
        if role == "staff":
            return redirect("teacher")
        else:
            return redirect("leave")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects(email=email, password=password).first()

        if user:
            # ✅ Login successful — storing info in session
            request.session['user_email'] = user.email
            request.session['user_name'] = user.full_name
            request.session['role'] = user.role  # Add role to session
            messages.success(request, "Logged in successfully!")

            if user.role == "staff":
                return redirect("teacher")
            else:
                return redirect("leave")  # Student portal
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "login.html")


# ✅ HOME VIEW — redirect to login
def home(request):
    return redirect('login')


# ✅ LEAVE DASHBOARD
def leave(request):
    if not request.session.get("user_email"):
        messages.error(request, "Please log in to access the leave form.")
        return redirect("login")

    try:
        user = User.objects.get(email=request.session["user_email"])
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("login")

    if request.method == "POST":
        leave_type = request.POST.get("leave_type")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        reason = request.POST.get("reason")

        leave_obj = Leave(
            full_name=user.full_name,
            email=user.email,
            register_number=user.register_number,
            department=user.department,
            leave_type=leave_type,
            from_date=datetime.datetime.strptime(from_date, "%Y-%m-%d"),
            to_date=datetime.datetime.strptime(to_date, "%Y-%m-%d"),
            reason=reason,
        )

        # Only attach OD form if it's an OD leave
        if leave_type == "OD" and "od_form" in request.FILES:
            leave_obj.od_form.put(request.FILES["od_form"], content_type=request.FILES["od_form"].content_type)

        leave_obj.save()

        messages.success(request, "Leave application submitted successfully.")
        return redirect("leave")

    context = {
        "user_name": user.full_name,
        "register_number": user.register_number,
        "department": user.department,
    }
    return render(request, "leave.html", context)


# ✅ TEACHER PAGE
def teacher(request):
    if request.session.get("role") != "staff":
        return redirect("login")

    user_email = request.session.get("user_email")
    if not user_email:
        messages.error(request, "Please log in.")
        return redirect("login")

    try:
        user = User.objects.get(email=user_email)

        if request.method == "POST":
            action = request.POST.get("action")
            leave_id = request.POST.get("leave_id")
            comment = request.POST.get("comment", "")

            try:
                leave = Leave.objects.get(id=ObjectId(leave_id))

                staff_type = user.staff_type
                leave.comment = comment  # Save comment

                if action == "approve":
                    if staff_type == "tutor":
                        leave.tutor_approved = True
                    elif staff_type == "advisor":
                        leave.advisor_approved = True
                    elif staff_type == "hod":
                        leave.hod_approved = True
                    messages.success(request, f"Leave approved by {staff_type} for {leave.full_name}")

                elif action == "reject":
                    if staff_type == "tutor":
                        leave.tutor_approved = False
                    elif staff_type == "advisor":
                        leave.advisor_approved = False
                    elif staff_type == "hod":
                        leave.hod_approved = False
                    messages.warning(request, f"Leave rejected by {staff_type} for {leave.full_name}")

                leave.save()

            except Leave.DoesNotExist:
                messages.error(request, "Leave request not found.")

        leave_requests = Leave.objects.order_by('-from_date')

        context = {
            'name': user.full_name,
            'register_number': user.register_number,
            'department': user.department,
            'email': user.email,
            'phone': user.phone_number,
            'address': user.address,
            'leave_requests': leave_requests,
            'user': user  # Needed for staff_type in template
        }
        return render(request, 'teacher.html', context)

    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("login")

# ✅ STUDENT PROFILE PAGE
def profile(request):
        # Check if the user_email is stored in the session
    user_email = request.session.get("user_email")
    if not user_email:
        messages.error(request, "Please log in to view your leave status.")
        return redirect("login")
    
    try:
        # Fetch the user from the database using the email from the session
        user = User.objects.get(email=user_email)
        
        context = {
            'name': user.full_name,
            'register_number': user.register_number,
            'department': user.department,
            'email': user.email,
            'phone': user.phone_number,
            'address': user.address,
        }
        return render(request, 'profile.html', context)
    
    except User.DoesNotExist:
        # Handle case where user is not found
        messages.error(request, "User not found.")
        return redirect("login")

# ✅ STATUS PAGE
# ✅ STATUS PAGE
def status(request):
    if not request.session.get("user_email"):
        messages.error(request, "Please log in to view your leave status.")
        return redirect("login")

    try:
        user_email = request.session["user_email"]
        leave_entries = Leave.objects(email=user_email).order_by('-from_date')  # latest first
    except Exception as e:
        messages.error(request, "Error retrieving leave details.")
        leave_entries = []

    context = {
        "leave_entries": leave_entries,
    }
    return render(request, "status.html", context)



# ✅ SIGNUP VIEW
def signup(request):
    if request.method == "POST":
        full_name = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        role = request.POST.get("role")
        department = request.POST.get("department")
        staff_type = request.POST.get("staff_type")
        phone_number = request.POST.get("phone_number")
        register_number = request.POST.get("register_number")

        if User.objects(email=email).first():
            messages.error(request, "Email already exists!")
            return render(request, "signup.html")

        student = User(
            full_name=full_name,
            email=email,
            role=role,
            department=department,
            password=password,  # TODO: hash this for production
            address=address,
            staff_type=staff_type,
            phone_number=phone_number,
            register_number=register_number,
        )
        student.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")  # Make sure 'login' name is set correctly in urls.py

    return render(request, "signup.html")



def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect("login")


from django.http import HttpResponse
from bson import ObjectId

def download_od(request, leave_id):
    try:
        leave = Leave.objects.get(id=ObjectId(leave_id))
        if leave.od_form:
            file_data = leave.od_form.read()
            content_type = leave.od_form.content_type
            response = HttpResponse(file_data, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="OD_Form_{leave_id}.pdf"'
            return response
    except Leave.DoesNotExist:
        messages.error(request, "OD Form not found.")
    return redirect("status")

from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_leave(request, leave_id):
    if request.method == "POST" and request.session.get("user_email"):
        try:
            leave = Leave.objects.get(id=ObjectId(leave_id), email=request.session["user_email"])
            leave.delete()
            messages.success(request, "Leave application deleted successfully.")
        except Leave.DoesNotExist:
            messages.error(request, "Leave application not found.")
    else:
        messages.error(request, "Invalid request.")
    return redirect("status")


