from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            "username", "testuser@super.com", "usertype", "password"
        )
        self.assertEqual(super_user.username, "username")
        self.assertEqual(super_user.email, "testuser@super.com")
        self.assertEqual(super_user.usertype, "usertype")
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "username")

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                username="username1",
                email="testuser@super.com",
                usertype="usertype",
                password="password",
                is_superuser=False,
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                username="username2",
                email="testusers@super.com",
                usertype="usertype",
                password="password",
                is_staff=False,
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                username="username3",
                email="testuserss@super.com",
                usertype="usertype",
                password="password",
                is_active=False,
            )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            "username", "testuser@user.com", "usertype", "password"
        )
        self.assertEqual(user.username, "username")
        self.assertEqual(user.email, "testuser@user.com")
        self.assertEqual(user.usertype, "usertype")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                username="iris", email="", usertype="usertype", password="password"
            )


# Create your tests here.
