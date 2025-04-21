from mongoengine import Document, StringField, EmailField , DateField , BooleanField , FileField 

class User(Document):
    full_name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=6)  # Store hashed version ideally
    address = StringField(required=True)

    register_number = StringField(required=True, max_length=20)
    phone_number = StringField(required=True, max_length=15)
    
    role = StringField(required=True, choices=["student", "staff"])
    staff_type = StringField(choices=["hod", "advisor", "tutor"], null=True)
    department = StringField(required=True, choices=[
        "computer-science", "mechanical", "civil", "electrical"
    ])
    
    meta = {
        "collection": "users"
    }

class Leave(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    register_number = StringField(required=True)
    department = StringField(required=True)
    leave_type = StringField(required=True, choices=["Casual", "Sick", "OD"])
    from_date = DateField(required=True)
    to_date = DateField(required=True)
    reason = StringField(required=True)
    od_form = FileField()  # For OD uploads
    status = StringField(default='Pending')
    tutor_approved = BooleanField(default=None, null=True)
    advisor_approved = BooleanField(default=None, null=True)
    hod_approved = BooleanField(default=None, null=True)
    comment = StringField()  # Optional: Teacher comments

    meta = {
        "collection": "leave_applications"
    }


