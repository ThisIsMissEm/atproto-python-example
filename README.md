# ATProto Python Example

This is an example showing how to properly authenticate a user given their handle and password, possibly prompting for the email-based OTP code if necessary. It takes care of resolving the handle to the DID Document, and then extracts the PDS Endpoint from that document, such that it would work with non-bluesky hosted PDSes.

> [!NOTE]
> This isn't the recommended way to authenticate now that OAuth exists, for an example using OAuth, see: https://github.com/bluesky-social/cookbook/tree/main/python-oauth-web-app
