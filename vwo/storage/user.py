class UserStorage(object):
    ''' UserStorage Class is used to store user-variation mapping.
    Override this class to implement your own functionality.
    SDK will ensure to use this while bucketing a user into a variation.'''

    def get(self, user_id, campaign_key):
        ''' To retrieve the stored variation for the user_id and
        campaign_key

        Args:
            user_id (str): User ID for which data needs to be retrieved.
            campaign_key (str): Campaign key to identify the campaign for
            which stored variation should be retrieved.

        Returns:
            user_data (dict): user-variation mapping
        '''
        pass

    def set(self, user_data):
        ''' To store the the user variation-mapping

        Args:
            user_data (dict): user-variation mapping
        '''
        pass
