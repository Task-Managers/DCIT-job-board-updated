from App.models import User, Company, Listing, Alumni, Admin
from App.database import db
from App.controllers import get_all_subscribed_alumni



def add_company(username, company_name, password, email, company_address, contact, company_website):
    # Check if there are no other users with the same username or email values in any other subclass
        if (
            Alumni.query.filter_by(username=username).first() is not None or
            Admin.query.filter_by(username=username).first() is not None or
            # Company.query.filter_by(username=username).first() is not None or

            # Company.query.filter_by(email=email).first() is not None or
            Admin.query.filter_by(email=email).first() is not None or
            Alumni.query.filter_by(email=email).first() is not None
            
        ):
            return None  # Return None to indicate duplicates

        newCompany= Company(username,company_name, password, email, company_address, contact, company_website)
        try: # safetey measure for trying to add duplicate 
            db.session.add(newCompany)
            db.session.commit()  # Commit to save the new  to the database
            return newCompany
        except:
            db.session.rollback()
            return None

def send_notification(job_categories=None):
    # get all the subscribed users who have the job categories
    subbed = get_all_subscribed_alumni()

    # turn the job categories into a set for intersection
    job_categories = set(job_categories)

    # list of alumni to be notified
    notif_alumni = []
    # print(job_categories)

    for alumni in subbed:
        # print('alumni')
        # get a set of all the job categories the alumni is subscribed for
        jobs = set(alumni.get_categories())
        common_jobs = []
        # perform an intersection of the jobs an alumni is subscribed for and the job categories of the listing
        common_jobs = list(jobs.intersection(job_categories))

        # if there are common jobs shared in the intersection, then add that alumni the list to notify
        if common_jobs:
            notif_alumni.append(alumni)
        # else:
        #     print('no commmon jobs: ', alumni, ' and ', job_categories)

    # do notification send here? use mail chimp?
    print(notif_alumni, job_categories)
    return notif_alumni, job_categories

def add_listing(title, description, company_name, #, job_categories=None
                salary, position, remote, ttnational, desiredcandidate, area, job_categories=None):

    # manually validate that the company actually exists
    company = get_company_by_name(company_name)
    if not company:
        return None

    newListing = Listing(title, description, company_name, job_categories,
                         salary, position, remote, ttnational, desiredcandidate, area)
    try:
        db.session.add(newListing)
        db.session.commit()

        # print('get_all_subscribed_alumn')
        # send_notification(job_categories)
        # send_notification(newListing.get_categories())

        # print('yah')
        return newListing
    except:
        # print('nah')
        db.session.rollback()
        return None

def get_company_by_name(company_name):
    return Company.query.filter_by(company_name=company_name).first()

def get_company_listings(company_name):
    # return Listing.query.filter_by(company_name=company_name)
    company = get_company_by_name(company_name)
    
    # for listing in company.listings:
    #     print(listing.get_json())
    return company.listings

def get_all_companies():
    return Company.query.all()

def get_all_companies_json():
    companies = get_all_companies()
    if not companies:
        return []
    companies = [company.get_json() for company in companies]
    return companies