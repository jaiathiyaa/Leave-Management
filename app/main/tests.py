from django.test import TestCase, Client
from django.urls import reverse
from .mongo_models import User, Leave
import datetime

class LeavePortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Clean up any potential leftover test data
        User.objects(email__in=[
            "test_student@example.com",
            "test_staff@example.com",
            "test_advisor@example.com",
            "test_hod@example.com",
            "another_student@example.com",
            "new_student@example.com",
            "ece_student@example.com"
        ]).delete()
        Leave.objects(email__in=["test_student@example.com", "another_student@example.com", "ece_student@example.com"]).delete()

        # Create test student
        self.student = User(
            full_name="Test Student",
            email="test_student@example.com",
            password="testpassword",
            address="Test Address",
            register_number="REG12345",
            phone_number="1234567890",
            role="student",
            department="computer-science"
        )
        self.student.save()

        # Create test staff (tutor)
        self.tutor = User(
            full_name="Test Tutor",
            email="test_staff@example.com",
            password="testpassword",
            address="Test Staff Address",
            register_number="STAFF123",
            phone_number="0987654321",
            role="staff",
            staff_type="tutor",
            department="computer-science"
        )
        self.tutor.save()

        # Create test advisor
        self.advisor = User(
            full_name="Test Advisor",
            email="test_advisor@example.com",
            password="testpassword",
            address="Test Advisor Address",
            register_number="STAFF456",
            phone_number="0987654322",
            role="staff",
            staff_type="advisor",
            department="computer-science"
        )
        self.advisor.save()

        # Create test HOD
        self.hod = User(
            full_name="Test HOD",
            email="test_hod@example.com",
            password="testpassword",
            address="Test HOD Address",
            register_number="STAFF789",
            phone_number="0987654323",
            role="staff",
            staff_type="hod",
            department="computer-science"
        )
        self.hod.save()

    def tearDown(self):
        # Clean up after tests run
        User.objects(email__in=[
            "test_student@example.com",
            "test_staff@example.com",
            "test_advisor@example.com",
            "test_hod@example.com",
            "another_student@example.com",
            "new_student@example.com",
            "ece_student@example.com"
        ]).delete()
        Leave.objects(email__in=["test_student@example.com", "another_student@example.com", "ece_student@example.com"]).delete()

    def test_login_success(self):
        """Test successful login and redirect"""
        response = self.client.post(reverse('login'), {
            'email': 'test_student@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('leave'))
        # Check session variables
        session = self.client.session
        self.assertEqual(session['user_email'], 'test_student@example.com')
        self.assertEqual(session['user_name'], 'Test Student')
        self.assertEqual(session['role'], 'student')

    def test_login_invalid(self):
        """Test login failure with invalid password"""
        response = self.client.post(reverse('login'), {
            'email': 'test_student@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Renders login page again
        session = self.client.session
        self.assertNotIn('user_email', session)

    def test_signup_student(self):
        """Test student sign up"""
        # Delete the student first to avoid duplicate email key error
        User.objects(email="test_student@example.com").delete()
        response = self.client.post(reverse('signup'), {
            'fullname': 'Test Student',
            'email': 'test_student@example.com',
            'phone_number': '1234567890',
            'register_number': 'REG12345',
            'password': 'testpassword',
            'address': 'Test Address',
            'role': 'student',
            'department': 'computer-science'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        user = User.objects(email='test_student@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.role, 'student')

    def test_apply_leave_success(self):
        """Test applying for leave"""
        # Log in first
        self.client.post(reverse('login'), {
            'email': 'test_student@example.com',
            'password': 'testpassword'
        })
        # Post leave application
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        day_after = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        response = self.client.post(reverse('leave'), {
            'leave_type': 'Casual',
            'from_date': tomorrow,
            'to_date': day_after,
            'reason': 'Family function'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('leave'))
        
        # Verify leave saved in DB
        leave = Leave.objects(email='test_student@example.com').first()
        self.assertIsNotNone(leave)
        self.assertEqual(leave.leave_type, 'Casual')
        self.assertEqual(leave.reason, 'Family function')

    def test_teacher_approval_dashboard_and_action(self):
        """Test staff login, viewing dashboard and approving leave"""
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        day_after = datetime.date.today() + datetime.timedelta(days=2)
        # Create a leave application for student first
        leave = Leave(
            full_name=self.student.full_name,
            email=self.student.email,
            register_number=self.student.register_number,
            department=self.student.department,
            leave_type="Casual",
            from_date=tomorrow,
            to_date=day_after,
            reason="Sick leave test"
        )
        leave.save()

        # Log in as tutor
        self.client.post(reverse('login'), {
            'email': 'test_staff@example.com',
            'password': 'testpassword'
        })

        # View dashboard
        response = self.client.get(reverse('teacher'))
        self.assertEqual(response.status_code, 200)

        # Approve the leave application
        response = self.client.post(reverse('teacher'), {
            'action': 'approve',
            'leave_id': str(leave.id),
            'comment': 'Approved by tutor'
        })
        self.assertEqual(response.status_code, 200)

        # Refresh leave object and check status
        leave.reload()
        self.assertEqual(leave.tutor_approved, True)
        self.assertEqual(leave.tutor_comment, 'Approved by tutor')

    def test_delete_leave_application(self):
        """Test student deleting their own pending leave application"""
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        day_after = datetime.date.today() + datetime.timedelta(days=2)
        # Create a leave application
        leave = Leave(
            full_name=self.student.full_name,
            email=self.student.email,
            register_number=self.student.register_number,
            department=self.student.department,
            leave_type="Casual",
            from_date=tomorrow,
            to_date=day_after,
            reason="Temporary application"
        )
        leave.save()

        # Log in as student
        self.client.post(reverse('login'), {
            'email': 'test_student@example.com',
            'password': 'testpassword'
        })

        # Delete it
        response = self.client.post(reverse('delete_leave', args=[str(leave.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status'))

        # Verify deletion in DB
        db_leave = Leave.objects(id=leave.id).first()
        self.assertIsNone(db_leave)

    def test_apply_leave_past_date_fails(self):
        """Test applying for leave with past dates fails validation"""
        # Log in first
        self.client.post(reverse('login'), {
            'email': 'test_student@example.com',
            'password': 'testpassword'
        })
        # Post leave application with a past date
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.date.today().strftime("%Y-%m-%d")
        response = self.client.post(reverse('leave'), {
            'leave_type': 'Casual',
            'from_date': yesterday,
            'to_date': today,
            'reason': 'Past leave test'
        })
        # It should redirect back to the leave page due to validation error
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('leave'))
        
        # Verify no leave was saved in DB
        leave = Leave.objects(email='test_student@example.com').first()
        self.assertIsNone(leave)

    def test_staff_profile_page(self):
        """Test viewing staff profile page"""
        # Log in as tutor
        self.client.post(reverse('login'), {
            'email': 'test_staff@example.com',
            'password': 'testpassword'
        })
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Staff Profile")
        self.assertContains(response, "TUTOR Profile")
        self.assertContains(response, "Staff ID")

    def test_department_segregation_for_staff(self):
        """Test that a staff member only views leaves from their own department"""
        # Create a student in 'ece' department
        ece_student = User(
            full_name="ECE Student",
            email="ece_student@example.com",
            password="testpassword",
            address="ECE Address",
            register_number="ECE123",
            phone_number="1234567895",
            role="student",
            department="ece"
        )
        ece_student.save()

        # Create a leave application for ece student
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        day_after = datetime.date.today() + datetime.timedelta(days=2)
        ece_leave = Leave(
            full_name=ece_student.full_name,
            email=ece_student.email,
            register_number=ece_student.register_number,
            department=ece_student.department,
            leave_type="Casual",
            from_date=tomorrow,
            to_date=day_after,
            reason="ECE student leave"
        )
        ece_leave.save()

        # Tutor (self.tutor) is in 'computer-science' department.
        # Log in as tutor.
        self.client.post(reverse('login'), {
            'email': 'test_staff@example.com',
            'password': 'testpassword'
        })
        response = self.client.get(reverse('teacher'))
        self.assertEqual(response.status_code, 200)
        # Tutor should NOT see the ECE student's leave request
        self.assertNotContains(response, "ECE student leave")
        
        # Clean up
        ece_student.delete()
        ece_leave.delete()
