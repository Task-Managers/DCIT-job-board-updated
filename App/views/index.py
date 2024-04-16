from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
# from App.controllers import create_user

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


from App.controllers import(
    get_user_by_username,
    get_all_listings,
    get_company_listings,
    add_listing,
    apply_listing,
    add_alumni,
    add_admin,
    add_categories,
    subscribe_action,
    add_company,
    get_listing
)

from App.models import(
    Alumni,
    Company,
    Admin
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')



# @index_views.route('/', methods=['GET'])
@index_views.route('/app', methods=['GET'])
@jwt_required()
def index_page():
    # return render_template('index.html')
    jobs = get_all_listings()

    if isinstance(current_user, Alumni):
        return render_template('alumni.html', jobs=jobs )
    
    if isinstance(current_user, Company):
        jobs = get_company_listings(current_user.username)
        return render_template('company-view.html', jobs=jobs)

    if isinstance(current_user, Admin):
        return render_template('admin.html', jobs=jobs)
    
    return redirect('/login')


@index_views.route('/submit_application', methods=['POST'])
@jwt_required()
def submit_application_action():
    # get form data
    data = request.form

    response = None

    print(data)
    # print(current_user.alumni_id)

    try:
        alumni = apply_listing(current_user.alumni_id, data['job_id'])

        # print(alumni)
        response = redirect(url_for('index_views.index_page'))
        flash('Application submitted')

    except Exception:
        # db.session.rollback()
        flash('Error submitting application')
        response = redirect(url_for('auth_views.login_page'))

    return response

    # get the files from the form
    # print('testttt')
    # print(data)

# @index_views.route('/view_applications/<int:job_id>', methods=['GET'])
# @jwt_required()
# def view_applications_page(job_id):

#     # get the listing
#     listing = get_listing(job_id)

#     # applicants = listing.get_applicants()

#     response = None
#     print(listing)

#     try:
#         applicants = listing.get_applicants()
#         print(applicants)
#         return render_template('viewapp-company.html', applicants=applicants)

#     except Exception:
#         flash('Error receiving applicants')
#         response = redirect(url_for('index_views.index_page'))

#     return response

# @index_views.route('/add_listing', methods=['GET'])
# @jwt_required()
# def add_listing_page():
#     # username = get_jwt_identity()
#     # user = get_user_by_username(username)

#     return render_template('companyform.html')

# @index_views.route('/add_listing', methods=['POST'])
# @jwt_required()
# def add_listing_action():
#     # username = get_jwt_identity()
#     # user = get_user_by_username(username)
#     data = request.form

#     response = None

#     print(data)

#     try:
#         remote = False
#         national = False

#         if data['remote_option'] == 'Yes':
#             remote = True

#         if data['national_tt'] == 'Yes':
#             national = True

#         listing = add_listing(data['title'], data['description'], current_user.company_name, data['salary'], data['position_type'],
#                               remote, national, data['desired_candidate_type'], data['job_area'], None)
#         print(listing)
#         flash('Created job listing')
#         response = redirect(url_for('index_views.index_page'))
#     except Exception:
#         flash('Error creating listing')
#         response = redirect(url_for('index_views.add_listing_page'))
    
#     return response



# @index_views.route('/delete-exercise/<int:exercise_id>', methods=['GET'])
# @login_required
# def delete_exercise_action(exercise_id):
    
#     user = current_user

#     res = delete_exerciseSet(exercise_id)

#     if res == None:
#         flash('Invalid or unauthorized')
#     else:
#         flash('exercise deleted!')
#     return redirect(url_for('user_views.userInfo_page'))





@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    # create_user('bob', 'bobpass')

    # add in the first admin
    add_admin('bob', 'bobpass', 'bob@mail')

    # add in alumni
    add_alumni('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')

    # add_alumni('rooooob', 'robpass', 'roooooob@mail', '123456089')

    add_categories('123456789', ['Database'])
    # print('test')

    # remove_categories('123456789', ['N/A'])
    # remove_categories('123456789', ['Database'])
    

    # subscribe rob
    subscribe_action('123456789')

    # add in companies
    add_company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
    add_company('company2', 'company2', 'compass', 'company@mail2',  'company_address2', 'contact2', 'company_website2.com')

    # add in listings
    # listing1 = add_listing('listing1', 'job description', 'company2')
    # print(listing1, 'test')
    add_listing('listing1', 'job description1', 'company1',
                8000, 'Part-time', True, 'employmentTerm!', True, 'desiredCandidate?', 'Curepe', ['Database', 'Programming', 'butt'])

    add_listing('listing2', 'job description', 'company2',
                4000, 'Full-time', True, 'employmentTerm?', True, 'desiredCandidate?', 'Curepe', ['Database', 'Programming', 'butt'])

    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})