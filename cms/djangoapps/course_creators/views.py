"""
Methods for interacting programmatically with the user creator table.
"""

import time
import json
import base64
import hmac
import hashlib

from course_creators.models import CourseCreator
from student.roles import CourseCreatorRole
from student import auth

from django.http import HttpResponse
from django.shortcuts import render


def add_user_with_status_unrequested(user):
    """
    Adds a user to the course creator table with status 'unrequested'.

    If the user is already in the table, this method is a no-op
    (state will not be changed).

    If the user is marked as is_staff, this method is a no-op (user
    will not be added to table).
    """
    _add_user(user, CourseCreator.UNREQUESTED)


def add_user_with_status_granted(caller, user):
    """
    Adds a user to the course creator table with status 'granted'.

    If appropriate, this method also adds the user to the course creator group maintained by authz.py.
    Caller must have staff permissions.

    If the user is already in the table, this method is a no-op
    (state will not be changed).

    If the user is marked as is_staff, this method is a no-op (user
    will not be added to table, nor added to authz.py group).
    """
    if _add_user(user, CourseCreator.GRANTED):
        update_course_creator_group(caller, user, True)


def update_course_creator_group(caller, user, add):
    """
    Method for adding and removing users from the creator group.

    Caller must have staff permissions.
    """
    if add:
        auth.add_users(caller, CourseCreatorRole(), user)
    else:
        auth.remove_users(caller, CourseCreatorRole(), user)


def get_course_creator_status(user):
    """
    Returns the status for a particular user, or None if user is not in the table.

    Possible return values are:
        'unrequested' = user has not requested course creation rights
        'pending' = user has requested course creation rights
        'granted' = user has been granted course creation rights
        'denied' = user has been denied course creation rights
        None = user does not exist in the table
    """
    user = CourseCreator.objects.filter(user=user)
    if user.count() == 0:
        return None
    else:
        # User is defined to be unique, can assume a single entry.
        return user[0].state


def user_requested_access(user):
    """
    User has requested course creator access.

    This changes the user state to CourseCreator.PENDING, unless the user
    state is already CourseCreator.GRANTED, in which case this method is a no-op.
    """
    user = CourseCreator.objects.get(user=user)
    if user.state != CourseCreator.GRANTED:
        user.state = CourseCreator.PENDING
        user.save()


def _add_user(user, state):
    """
    Adds a user to the course creator table with the specified state.

    Returns True if user was added to table, else False.

    If the user is already in the table, this method is a no-op
    (state will not be changed, method will return False).

    If the user is marked as is_staff, this method is a no-op (False will be returned).
    """
    if not user.is_staff and CourseCreator.objects.filter(user=user).count() == 0:
        entry = CourseCreator(user=user, state=state)
        entry.save()
        return True

    return False
	
'''
    to make token
	added by gzc 20160404
	copyright from JING Xia
'''
def token(request):
    scope = 'zhishigang'
    access_key = 'TNryzbrrYvEgQJG46lttCc4Gpl_wx-t1ULH2QMs6'
    secret_key = 'yFQBoM5W2BoteMika-uogHDRHubUFXg6Bti_IBTk'

    policy = {
        'scope': scope,
        'deadline': int(time.time()+3600),
    }
    policy_string = json.dumps(policy).replace(' ', '')
    encoded_policy = base64.urlsafe_b64encode(policy_string)
    sign = hmac.new(secret_key, encoded_policy, hashlib.sha1).digest()
    encoded_sign = base64.urlsafe_b64encode(sign)
    token = access_key + ':' + encoded_sign + ':' + encoded_policy
#    print token
#    return HttpResponse(token)
    return HttpResponse(json.dumps({
        'uptoken': token,
    }), content_type = 'application/json')
'''
	test upload
	added by gzc 20160404
	just for test
'''
def test_upload(request):
    return render(request,'test_upload.html')
