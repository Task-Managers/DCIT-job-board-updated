from App.database import db
from .user import User
from .listing import categories

# from .file import File

# categories = ['Software Engineering', 'Database', 'Programming', 'N/A']

class Alumni(User):
    # id = db.Column(db.Integer, primary_key = True)
    alumni_id = db.Column(db.Integer, nullable = False, unique = True)
    # insert other personal info later


    # relationship to companies 
    # company_name = db.Column(db.String(), db.ForeignKey('company.company_name'), nullable=False)
    # companies = db.relationship('Company', back_populates='applicants', overlaps="company")

    # Define relationship to listings
    listing = db.relationship('Listing', secondary='alumni_listings', back_populates='applicant')

    # relationship to listings to receive notifications?
    subscribed = db.Column(db.Boolean, default=False)

    # need to add in columns for:
    # -contact info i.e phone number
    contact = db.Column(db.String(30), nullable = False)

    #name
    firstname = db.Column(db.String(120), nullable = False)
    lastname = db.Column(db.String(120), nullable = False)

    # relationship with files?
    # files = db.relationship('File', back_populates='alumni', lazy=True)

    # categories = ['Software Engineering', 'Database', 'Programming', 'N/A']
    job_category = db.Column(db.String(120))

    def __init__(self, username, password, email, alumni_id, contact, firstname, lastname):
        super().__init__(username, password, email)
        self.alumni_id = alumni_id
        # self.job_category = 'N/A'
        self.job_category = None
        self.subscribed = False
        self.contact = contact
        self.firstname = firstname
        self.lastname = lastname

        # if job_categories is None:
        #     self.job_category = 'N/A'
        # else:
        #     self.validate_and_set_categories(job_categories)

        # if job_category is None:
        #     self.job_category = 'N/A'

        # if job_category in self.categories:
        #     self.job_category = job_category
        # else:
        #     self.job_category = 'N/A'

    # methods to support adding, removing, validating the job categories
    # def validate_and_set_categories(self, job_categories):
    #     valid_categories = [category for category in job_categories if category in categories]
    #     # for category in job_categories:
    #     #     if category not in categories:
    #     #         raise ValueError(f"Invalid job category: {category}")
    #     # self.job_category = '|'.join(job_categories)
    #     self.job_category = '|'.join(valid_categories)

    def get_categories(self):
        return self.job_category.split('|') if self.job_category else []

    # def add_category(self, category):
    #     categories = self.get_categories()
    #     if category not in categories:
    #         categories.append(category)
    #         self.job_category = '|'.join(categories)
    #     else:
    #         print(f"Category '{category}' already exists.")

    def add_category(self, category):
        self.job_category = category

        # if 'N/A' in categories:
            # print('na in categories')


    def remove_category(self, category):
        categories = self.get_categories()
        if category in categories:
            categories.remove(category)
            self.job_category = '|'.join(categories)
        else:
            print(f"Category '{category}' does not exist.")

    def get_alumni_id(self):
        return self.alumni_id

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'alumni_id': self.alumni_id,
            'subscribed': self.subscribed,
            'job_category': self.get_categories(),
            'contact':self.contact,
            'firstname':self.firstname,
            'lastname':self.lastname
        }