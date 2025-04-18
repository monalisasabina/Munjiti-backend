from app import app
from models import db, User, Pastor, Project, ProjectImage, Ministry, MinistryProject, Notice, Downloads, ContactMessage, Notification, cipher

with app.app_context():
    print("Seeding database...")

    # Clear the database
    print("\nClearing the database...")
    db.session.query(User).delete()
    db.session.query(Pastor).delete()
    db.session.query(Project).delete()
    db.session.query(ProjectImage).delete()
    db.session.query(Ministry).delete()
    db.session.query(MinistryProject).delete()
    db.session.query(Notice).delete()
    db.session.query(Downloads).delete()
    db.session.query(ContactMessage).delete()
    db.session.query(Notification).delete()

    # Seeding Users
    print("Adding Users...")
    users = [
        User(role="admin", username="admin1", email="admin1@example.com", password_hash="password1"),
        User(role="editor", username="editor1", email="editor1@example.com", password_hash="password2"),
        User(role="user", username="user1", email="user1@example.com", password_hash="password3"),
        User(role="moderator", username="mod1", email="mod1@example.com", password_hash="password4"),
        User(role="admin", username="admin2", email="admin2@example.com", password_hash="password5"),
    ]
    db.session.add_all(users)

    # Seeding Pastors
    print("Adding Pastors...")
    pastors = [
        Pastor(firstname="John", lastname="Doe", image="pastor1.jpg", role="Senior Pastor", description="Leads the church."),
        Pastor(firstname="Jane", lastname="Smith", image="pastor2.jpg", role="Youth Pastor", description="Leads youth programs."),
        Pastor(firstname="Mark", lastname="Brown", image="pastor3.jpg", role="Worship Leader", description="Leads worship sessions."),
        Pastor(firstname="Emily", lastname="Johnson", image="pastor4.jpg", role="Assistant Pastor", description="Assists in church activities."),
        Pastor(firstname="Michael", lastname="Davis", image="pastor5.jpg", role="Outreach Coordinator", description="Handles community outreach."),
    ]
    db.session.add_all(pastors)

    # Seeding Projects
    print("Adding Projects...")
    projects = [
        Project(name="Church Renovation", description="Renovating the main church building."),
        Project(name="Community Feeding", description="Providing food to the less fortunate."),
        Project(name="Youth Empowerment", description="Training youth in skills development."),
        Project(name="Mission Outreach", description="Spreading the gospel to remote areas."),
        Project(name="Children's Ministry", description="Supporting children's education."),
    ]
    db.session.add_all(projects)

    # Seeding Project Images
    print("Adding Project Images...")
    project_images = [
        ProjectImage(project_id=1, image_url="renovation1.jpg"),
        ProjectImage(project_id=1, image_url="renovation2.jpg"),
        ProjectImage(project_id=2, image_url="feeding1.jpg"),
        ProjectImage(project_id=3, image_url="youth1.jpg"),
        ProjectImage(project_id=4, image_url="mission1.jpg"),
    ]
    db.session.add_all(project_images)

    # Seeding Ministries
    print("Adding Ministries...")
    ministries = [
        Ministry(name="Worship Ministry", description="Handles church worship and praise.", created_at="2024-01-01"),
        Ministry(name="Youth Ministry", description="Engages youth in church programs.", created_at="2024-01-02"),
        Ministry(name="Women Ministry", description="Supports women in the church.", created_at="2024-01-03"),
        Ministry(name="Men's Fellowship", description="Encourages men to be active in church.", created_at="2024-01-04"),
        Ministry(name="Children Ministry", description="Takes care of children in the church.", created_at="2024-01-05"),
    ]
    db.session.add_all(ministries)

    # Seeding Ministry-Project Relations
    print("Adding Ministry-Project Relations...")
    ministry_projects = [
        MinistryProject(ministry_id=1, project_id=1),
        MinistryProject(ministry_id=2, project_id=2),
        MinistryProject(ministry_id=3, project_id=3),
        MinistryProject(ministry_id=4, project_id=4),
        MinistryProject(ministry_id=5, project_id=5),
    ]
    db.session.add_all(ministry_projects)

    # Seeding Notices
    print("Adding Notices...")
    notices = [
        Notice(title="Sunday Service", notice_text="Join us for worship this Sunday.", image="notice1.jpg"),
        Notice(title="Prayer Meeting", notice_text="Weekly prayer meeting every Wednesday.", image="notice2.jpg"),
        Notice(title="Bible Study", notice_text="Deep dive into the scriptures.", image="notice3.jpg"),
        Notice(title="Community Outreach", notice_text="Serving the local community.", image="notice4.jpg"),
        Notice(title="Fundraiser", notice_text="Raising funds for church projects.", image="notice5.jpg"),
    ]
    db.session.add_all(notices)

    # Seeding Downloads
    print("Adding Downloads...")
    downloads = [
        Downloads(name="Sunday Bulletin", description="Weekly bulletin with updates.", file_url="bulletin.pdf"),
        Downloads(name="Church Constitution", description="Guidelines for church governance.", file_url="constitution.pdf"),
        Downloads(name="Worship Songs", description="Collection of church worship songs.", file_url="songs.pdf"),
        Downloads(name="Youth Program", description="Upcoming events for youth.", file_url="youth.pdf"),
        Downloads(name="Mission Report", description="Details of past mission trips.", file_url="mission.pdf"),
    ]
    db.session.add_all(downloads)

    # Seeding Contact Messages
    print("Adding Contact Messages...")
    messages = [
        ContactMessage(sender_firstname="Alice", sender_lastname="Brown", email="alice@example.com", _mobile_number=cipher.encrypt("1234567890".encode()), message="Need prayer support."),
        ContactMessage(sender_firstname="Bob", sender_lastname="Green", email="bob@example.com", _mobile_number=cipher.encrypt("0987654321".encode()), message="Want to volunteer."),
        ContactMessage(sender_firstname="Charlie", sender_lastname="Blue", email="charlie@example.com", _mobile_number=cipher.encrypt("1122334455".encode()), message="Looking for a church."),
        ContactMessage(sender_firstname="Diana", sender_lastname="Black", email="diana@example.com", _mobile_number=cipher.encrypt("6677889900".encode()), message="Inquiry about donations."),
        ContactMessage(sender_firstname="Ethan", sender_lastname="White", email="ethan@example.com", _mobile_number=cipher.encrypt("5566778899".encode()), message="Prayer request."),
    ]
    db.session.add_all(messages)

    # Seeding Notifications
    print("Adding Notifications...")
    notifications = [
        Notification(user_id=1, message="Welcome to the church website!"),
        Notification(user_id=2, message="Your request has been received."),
        Notification(user_id=3, message="Upcoming events this weekend."),
        Notification(user_id=4, message="New notice added to the board."),
        Notification(user_id=5, message="Thank you for your donation."),
    ]
    db.session.add_all(notifications)

    # Commit all changes
    db.session.commit()
    print("Database seeded successfully!")
