import textwrap
import maskpass

# This just silences a warning from the atproto package:
import sys
from pydantic.warnings import UnsupportedFieldAttributeWarning
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore", category=UnsupportedFieldAttributeWarning)
# End silencer

from atproto import Client, IdResolver, exceptions
from atproto_client.request import XrpcError

def main():
    handle = input("What is your handle? ")
    password = maskpass.askpass()

    resolver = IdResolver()
    did = resolver.handle.resolve(handle)
    if did is None:
      print("Unable to resolve handle: %s", handle)
      exit(1)

    did_doc = resolver.did.resolve_atproto_data(did)
    if did_doc.pds is None or did_doc.handle is None or did_doc.handle != handle:
      print("Error resolving handle, missing PDS or encountered mismatched handled")
      exit(1)

    client = Client(did_doc.pds)
    login(client, did_doc.handle, password)

    print("Authenticated!\n")

    profile = client.get_profile(did_doc.did)

    print("Handle: %s" % profile.handle)
    print("Display Name: %s" % profile.display_name)
    if profile.description:
      print("Description:\n\n%s\n" % textwrap.indent(profile.description, "\t"))
    print("Posts: %i" % profile.posts_count)
    print("Followers: %i" % profile.followers_count)
    print("Following: %i" % profile.follows_count)
    print("\n")

    exit(0)

def login(client, handle, password, otp=None):
  try:
    client.login(handle, password, None, otp)
  except exceptions.UnauthorizedError as error:
    if error.response is not None:
      if isinstance(error.response.content, XrpcError) and error.response.content.error == 'AuthFactorTokenRequired':
        otp = input("Please enter the 2FA Code sent via email: ")
        return login(client, handle, password, otp)
      else:
        raise error
    else:
      raise error

if __name__ == '__main__':
    main()