import pytest
from models import User, db  # Assuming your models are in the 'models.py' file


# Test the User model
def test_user_creation(test_client):
    user = User(
        role="admin",
        username="testuser",
        email="testuser@example.com",
        password_hash="password123"
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Fetch the user from the database
    fetched_user = User.query.filter_by(username="testuser").first()
    
    assert fetched_user is not None  # Ensure the user is created and exists in the database
    assert fetched_user.username == "testuser"  # Ensure the username matches
    assert fetched_user.email == "testuser@example.com"  # Ensure the email matches


def test_user_email_validation():
    # Test for invalid email without '@'
    with pytest.raises(ValueError, match="Please include \"@\""):
        user = User(
            role="admin",
            username="testuser",
            email="testuserexample.com",  # Invalid email
            password_hash="password123"
        )
        db.session.add(user)
        db.session.commit()


def test_user_password_hashing():
    user = User(
        role="admin",
        username="testuser",
        email="testuser@example.com",
        password_hash="password123"
    )

    db.session.add(user)
    db.session.commit()

    # Check if the password is hashed correctly
    assert user.password_hash != "password123"  # Ensure password is hashed
    assert user.authenticate("password123")  # Ensure authentication works
