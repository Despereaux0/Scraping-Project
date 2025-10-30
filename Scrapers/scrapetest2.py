import requests

# Replace 'ACCESS_TOKEN' with your actual access token
ACCESS_TOKEN = 'EAAKsNs1XI4YBOzNobnXmIZCqHyjzKZCRLcBcWAdKqQXmoNaxLhQBn5nZCJYdpoh2mAYkkryL5O3Sp2crXzrbEnZCWaDmc9quL54s8KARYjyjc4MJbWR1flCZAucL8KZBAf4aI6z2Tj66ENsGiNK8cKN2H1LjuKcRmyUy0sbXVCO9IhgHJBo5CZAzPtT1wwccdsMhUfh3LWengQKkmL4Nw8xXpe1PFBFlRPdwrWDDiWJD7h75OrDaikWYxcK4vXMZCwZDZD'

# Replace 'PAGE_ID' with the ID of the Facebook page you want to scrape likes from
PAGE_ID = '100064712589264'

# URL for the Facebook Graph API to retrieve page likes
url = f"https://graph.facebook.com/v13.0/{100064712589264}?fields=likes&access_token={EAAKsNs1XI4YBOzNobnXmIZCqHyjzKZCRLcBcWAdKqQXmoNaxLhQBn5nZCJYdpoh2mAYkkryL5O3Sp2crXzrbEnZCWaDmc9quL54s8KARYjyjc4MJbWR1flCZAucL8KZBAf4aI6z2Tj66ENsGiNK8cKN2H1LjuKcRmyUy0sbXVCO9IhgHJBo5CZAzPtT1wwccdsMhUfh3LWengQKkmL4Nw8xXpe1PFBFlRPdwrWDDiWJD7h75OrDaikWYxcK4vXMZCwZDZD}"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    likes = data.get('likes', {}).get('summary', {}).get('total_count', 0)
    print(f"Likes: {likes}")
else:
    print("Failed to fetch data")
