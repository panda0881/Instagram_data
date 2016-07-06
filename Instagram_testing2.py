from instagram.client import InstagramAPI


# class defined for the client stuff - standard code from instagram
class client_packet:
    def __init__(self, client_id, client_secret, redirect_uri, begin_user_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.begin_user_id = begin_user_id
        print('creating new client...')

    def Access_token(self, flag):
        if flag:
            scope = []
            self.api = InstagramAPI(client_id=self.client_id, client_secret=self.client_secret,
                                    redirect_uri=self.redirect_uri)
            redirect_uri = self.api.get_authorize_login_url(scope=scope)

            print("Visit this page and authorize access in your browser:\n", redirect_uri)

            code = input("Paste in code in query string after redirect: ").strip()
            print('client_id: ' + self.api.client_id)
            print('client_secret: ' + self.api.client_secret)
            self.access_token = self.api.exchange_code_for_access_token(code)
            print(self.access_token)
        else:
            self.access_token = 'Insert Your actual Client Access token to not repeath this again and again'

        return self.access_token


# Visit the user node
def visit_user(user_id, stack, api, verbose=False):
    print("\n\n\n\n\n\n\n#########+++++++++=========+++++++++#########")
    # Collect User Data
    try:
        user = api.user(user_id)
    except:
        if verbose:
            print(user_id + " is private")
            print("#########+++++++++=========+++++++++#########\n\n\n\n\n\n\n")
            print("Current Stack Size : " + str(len(stack)))
        return stack

    print("Initialized user :" + user.username)
    print("User Id :" + user.id)
    print("User Full Name: " + user.full_name)
    print("Number of Images Posted : " + str(user.counts['media']))
    print("Number of Followers : " + str(user.counts['followed_by']))
    print("Number Follows: " + str(user.counts['follows']))


def main():
    client = client_packet(client_id='923490f7659a44fb8a83db1a4134992f',
                           client_secret='58999a8bbb0c42e78213585de310cafe', redirect_uri='https://192.168.0.82',
                           begin_user_id='190353205')
    # access_token = client.Access_token(True)
    # api = InstagramAPI(client_id=client.client_id, client_secret=client.client_secret, access_token=access_token[0])
    api = InstagramAPI(client_id=client.client_id, client_secret=client.client_secret)
    print('start searching')
    popular_media = api.media_popular(count=20)
    print('finish searching')
    for media in popular_media:
        print(media.images['standard_resolution'].url)
    user = api.user('190353205')
    # print("Initialized user :" + user.username)
    # print("User Id :" + user.id)
    # print("User Full Name: " + user.full_name)
    # print("Number of Images Posted : " + str(user.counts['media']))
    # print("Number of Followers : " + str(user.counts['followed_by']))
    # print("Number Follows: " + str(user.counts['follows']))


if __name__ == '__main__':
    main()
