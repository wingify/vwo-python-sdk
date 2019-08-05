class UserProfileService(object):
    ''' Abstract class encapsulating user profile service functionality.
    Override with your own implementation for storing
    and retrieving the user profile. '''

    def lookup(self, user_id):
        ''' Abstract method, must be defined to fetch the
        user profile dict corresponding to the user_id..

        Args:
            user_id (str): ID for user whose profile needs to be retrieved.

        Returns:
            user_profile_obj (dict): Object representing the user's profile.
        '''
        pass

    def save(self, user_profile_obj):
        ''' Abstract method, must be to defined to save
        the user profile dict sent to this method.

        Args:
            user_profile_obj (dict): Object representing the user's profile.
        '''
        pass
