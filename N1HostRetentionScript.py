import http.client, json
from datetime import UTC, datetime, timedelta

# Set connection site
conn = http.client.HTTPSConnection("app.ninjarmm.com")
# Get OAuth token
payload = "grant_type=client_credentials&client_id=[ID]&client_secret=[Secret]&scope=monitoring management control"
headers = { 'Content-Type': "application/x-www-form-urlencoded" }
conn.request("POST", "/ws/oauth/token", payload, headers)
res = conn.getresponse()
data = res.read()
token_response = data.decode("utf-8")
# Extract access token
token_json = json.loads(token_response)
access_token = token_json['access_token']
# Set headers for subsequent requests
headers = { 'Accept': "application/json", 'Authorization': "Bearer" + " " + access_token}
# Get list of devices from [] organizations
# Replace organization IDs as needed
# To get list of organizations and their IDs, comment out all lines below this one then uncomment the lines with /v2/organizations, res = conn.getresponse()
# data = res.read().decode("utf-8"), data = json.loads(data), and print(data)
conn.request("GET", "/v2/organization/4/devices?pageSize=400", headers=headers)
# conn.request("GET", "/v2/organizations", headers=headers)
res = conn.getresponse()
data = res.read().decode("utf-8")
data = json.loads(data)
conn.request("GET", "/v2/organization/5/devices?pageSize=400", headers=headers)
res = conn.getresponse()
data2 = res.read().decode("utf-8")
data2 = json.loads(data2)
conn.request("GET", "/v2/organization/7/devices?pageSize=400", headers=headers)
res = conn.getresponse()
data3 = res.read().decode("utf-8")
data3 = json.loads(data3)
data.extend(data2)
data.extend(data3)
# with open("N1Devices.json", "w") as f:
#     json.dump(data, f, indent=4)

# Identify stale devices with last contact older than 30 days
# Adjust cutoffDays to change the threshold
cutoffDays = 30
stale = []
for d in data:
    last_contact = d.get("lastContact")
    if not last_contact:
        print(d["systemName"]," has never checked in.")
    else:
        syetem_name = d["systemName"]
        last_seen = datetime.fromtimestamp(last_contact, UTC)
        now = datetime.now(UTC)
        cutoffDate= now - timedelta(days=cutoffDays)
        if last_seen < cutoffDate:
            last_seen = last_seen.date()
            # map orgID to name for stale devices - replace names and organization IDs 
            if d["organizationId"] == 4:
                stale.append({
                "id": d["id"],
                "name": d["systemName"],
                "organization" : "name1",
                "last_seen": last_seen
                })
            elif d["organizationId"] == 5:
                stale.append({
                "id": d["id"],
                "name": d["systemName"],
                "organization" : "name2",
                "last_seen": last_seen
                })
            elif d["organizationId"] == 7:  
                stale.append({
                "id": d["id"],
                "name": d["systemName"],
                "organization" : "name3",
                "last_seen": last_seen
                })
# Report stale devices by organization
print(f"Out of {len(data)} devices, {len(stale)} stale devices were found:")
name1Devices = []
name2Devices = []
name3Devices = []
# Sort stale devices into their respective organizations
for s in stale:
    if s['organization'] == "name1":
        name1Devices.append(s)
    elif s['organization'] == "name2":
        name2Devices.append(s)
    elif s['organization'] == "name3":
        name3Devices.append(s)
# Print stale devices by organization
print(f"\nname1 stale devices ({len(name1Devices)}):")
for s in name1Devices:
    print(f"{s['name']} last seen {s['last_seen']}")
print(f"\nname2 stale devices ({len(name2Devices)}):")
for s in name2Devices:
    print(f"{s['name']} last seen {s['last_seen']}")
print(f"\nname3 stale devices ({len(name3Devices)}):")
for s in name3Devices:
    print(f"{s['name']} last seen {s['last_seen']}")

# Delete stale devices
# Uncomment below to prompt user for confirmation before deletion
# NOT TESTED - USE AT YOUR OWN RISK

# decision = input('Enter "yes" to delete these devices: ')
# yes = "yes"
# yes = yes.casefold()
# if decision.casefold() != yes:
#     print("Aborting deletion.")
#     exit(0)
# else:
#     print("Proceeding with deletion.")
#     for s in stale:
#         device_id = s['id']
#         system_name = s['name']
#         path = f"/v2/devices/{device_id}"
#         conn.request("DELETE", path, headers)
#         res = conn.getresponse()
#         data = res.read().decode("utf-8")
#         if res.status in (200, 204):
#             print(f"Deleted {system_name} successfully")
#         else:
#             print(f"Failed to delete {system_name} ({res.status}): {data}")
 
