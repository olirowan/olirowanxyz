from app import app

blog_admin_id = str(app.config['BLOG_ADMIN_ID'])
blog_admin_user = app.config['BLOG_ADMIN_USER']


def validate_if_admin_user(current_user):

    app.logger.info("Admin validation requested. ID: " + str(current_user.id) + " Username: " + current_user.username)

    if (current_user.id) == blog_admin_id and (current_user.username) == blog_admin_user:
        app.logger.info("Admin validation successful for user: " + current_user.username)
        return True
    else:
        app.logger.info("Admin validation failed for user: " + current_user.username)
        return False
