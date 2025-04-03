from app import app
from models import db, ProjectImage , User, Pastor, Project, Ministry, MinistryProject, Notice, Downloads, ContactMessage, Notification, cipher,Gallery


with app.app_context():

    print("Church sample data")

    # Deleting all the rows in tables
    print("\n Clearing the database")
    MinistryProject.query.delete()
    User.query.delete()
    Pastor.query.delete()
    Project.query.delete()
    Ministry.query.delete()
    Notice.query.delete()
    Downloads.query.delete()
    Notification.query.delete()
    ContactMessage.query.delete()
    ProjectImage.query.delete()
    Gallery.query.delete()


    # Seeding Users
    print('\nAdding users...')
    users = [
            User(role="admin", username="admin1", email="admin1@example.com", password_hash="password1"),
            User(role="editor", username="editor1", email="editor1@example.com", password_hash="password2"),
            User(role="user", username="user1", email="user1@example.com", password_hash="password3"),
            User(role="moderator", username="mod1", email="mod1@example.com", password_hash="password4"),
            User(role="admin", username="admin2", email="admin2@example.com", password_hash="password5"),
        ]
    db.session.add_all(users)

    db.session.commit()



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

    db.session.commit()


     # Seeding Projects
    print("Adding Projects")
    projects = [
        Project(name="Church Renovation", description="Renovating the main church building."),
        Project(name="Community Feeding", description="Providing food to the less fortunate."),
        Project(name="Youth Empowerment", description="Training youth in skills development."),
        Project(name="Mission Outreach", description="Spreading the gospel to remote areas."),
        Project(name="Children's Ministry", description="Supporting children's education."),
    ]
    db.session.add_all(projects)
    db.session.commit()  # Ensure projects are committed before proceeding

    # Seeding Project Images
    print("Adding project images...")
    project_images = [
        ProjectImage(project_id=projects[0].id, image_url="renovation1.jpg"),
        ProjectImage(project_id=projects[0].id, image_url="renovation2.jpg"),
        ProjectImage(project_id=projects[1].id, image_url="feeding1.jpg"),
        ProjectImage(project_id=projects[2].id, image_url="youth1.jpg"),
        ProjectImage(project_id=projects[3].id, image_url="mission1.jpg"),
    ]
    db.session.add_all(project_images)
    db.session.commit()

    # Seeding Ministries
    print('Adding ministries')
    ministries = [
            Ministry(name="Worship Ministry", description="Handles church worship and praise."),
            Ministry(name="Youth Ministry", description="Engages youth in church programs."),
            Ministry(name="Women Ministry", description="Supports women in the church."),
            Ministry(name="Men's Fellowship", description="Encourages men to be active in church."),
            Ministry(name="Children Ministry", description="Takes care of children in the church."),
        ]
    db.session.add_all(ministries)

    db.session.commit()


    # Seeding Notices
    print("Adding notices...")
    notices = [
            Notice(title="Sunday Service", notice_text="Join us for worship this Sunday.", image="notice1.jpg"),
            Notice(title="Prayer Meeting", notice_text="Weekly prayer meeting every Wednesday.", image="notice2.jpg"),
            Notice(title="Bible Study", notice_text="Deep dive into the scriptures.", image="notice3.jpg"),
            Notice(title="Community Outreach", notice_text="Serving the local community.", image="notice4.jpg"),
            Notice(title="Fundraiser", notice_text="Raising funds for church projects.", image="notice5.jpg"),
        ]
    db.session.add_all(notices)

    db.session.commit()


    # Seeding Downloads
    print("Adding downloads")
    downloads = [
            Downloads(name="Sunday Bulletin", description="Weekly bulletin with updates.", file_url="bulletin.pdf"),
            Downloads(name="Church Constitution", description="Guidelines for church governance.", file_url="constitution.pdf"),
            Downloads(name="Worship Songs", description="Collection of church worship songs.", file_url="songs.pdf"),
            Downloads(name="Youth Program", description="Upcoming events for youth.", file_url="youth.pdf"),
            Downloads(name="Mission Report", description="Details of past mission trips.", file_url="mission.pdf"),
        ]
    db.session.add_all(downloads)

    db.session.commit()


    # Seeding Contact Messages
    print("Adding contact messages")
    messages = [
            ContactMessage(sender_firstname="Alice", sender_lastname="Brown", email="alice@example.com", mobile_number=1234567890, message="Need prayer support."),
            ContactMessage(sender_firstname="Bob", sender_lastname="Green", email="bob@example.com", mobile_number=987654321, message="Want to volunteer."),
            ContactMessage(sender_firstname="Charlie", sender_lastname="Blue", email="charlie@example.com", mobile_number=1122334455, message="Looking for a church."),
            ContactMessage(sender_firstname="Diana", sender_lastname="Black", email="diana@example.com", mobile_number=6677889900, message="Inquiry about donations."),
            ContactMessage(sender_firstname="Ethan", sender_lastname="White", email="ethan@example.com", mobile_number=5566778899, message="Prayer request."),
        ]
    db.session.add_all(messages)

    db.session.commit()


    # Seeding Notifications
    print("Adding notifications...")
    notifications = [
            Notification(message="Welcome to the church website!", contact_message_id=messages[0].id, is_read=True),
            Notification(message="Your request has been received.", contact_message_id=messages[1].id, is_read=False ),
            Notification(message="Upcoming events this weekend.", contact_message_id=messages[2].id, is_read=True),
            Notification(message="New notice added to the board.", contact_message_id=messages[3].id, is_read=False),
            Notification(message="Thank you for your donation.",contact_message_id=messages[4].id, is_read=True),
        ]
    db.session.add_all(notifications)

    db.session.commit()

    # Seeding Gallery
    print("Adding gallery images...")
    gallery_items = [
          Gallery(image_url="https://example.com/images/gallery1.jpg", description="A beautiful sunset over the church."),
          Gallery(image_url="https://example.com/images/gallery2.jpg", description="Church building exterior during the day."),
          Gallery(image_url="https://example.com/images/gallery3.jpg", description="Congregation during Sunday service."),
          Gallery(image_url="https://example.com/images/gallery4.jpg", description="Close-up of the altar."),
          Gallery(image_url="https://example.com/images/gallery5.jpg", description="A community event in the church hall.")
        ]

    db.session.add_all(gallery_items)
    db.session.commit()


    # Fetch ministries and projects from the DB
    ministries = Ministry.query.all()
    projects = Project.query.all()

    # Manually associate Ministries with Projects
    print("Linking Ministries with Projects...")

    # Example links (modify as needed)
    ministry_project_links = [
    MinistryProject(ministry_id=ministries[0].id, project_id=projects[0].id),  # Worship Ministry → Church Renovation
    MinistryProject(ministry_id=ministries[1].id, project_id=projects[2].id),  # Youth Ministry → Youth Empowerment
    MinistryProject(ministry_id=ministries[2].id, project_id=projects[4].id),  # Women Ministry → Children's Ministry
    ]

    # Add to the session
    db.session.add_all(ministry_project_links)

    print("✅ Ministry-Project relationships added!")

    # Commit all changes
    db.session.commit()


    print("\nDatabase seeded successfully!")

    print("\nMinistries")
    print(ministries)
    print("\nProjects")
    print(projects)

   

