from Setup import location, closest, bike, destination_bubi

# getting your starting point
coordinate1 = input('Where are you?: ')
print("Nearest Mol Bubi is :\n", closest.bubi(coordinate1)[0] + ',', str(closest.bubi(coordinate1)[1])[0:5], ' km far away')

print('---------------------*************-------------------------')
# getting your ending point
coordinate2 = input('Where do you go? ')
print("Nearest Mol Bubi is :\n", closest.bubi(coordinate2)[0] + ',', str(closest.bubi(coordinate2)[1])[0:5], ' km far away')
print('---------------------*************-------------------------', '\n')

closest1 = str(closest.bubi(coordinate1)[0])
closest2 = str(closest.bubi(coordinate2)[0])

bike1 = bike.info(closest1)
bike2 = bike.info(closest2)

print(closest1)
print('free bikes: ', bike1[1])
print('empty slots: ', bike1[0], '\n')

print(closest2)
print('empty slots: ', bike2[0])
print('free bikes: ', bike2[1], '\n')

lat1 = bike1[2] 
long1 = bike1[3] 
lat2 = bike2[2] 
long2 = bike2[3] 

print('Average Distance: ', destination_bubi.far_away(lat1, long1, lat2, long2)[0])
print('Average speed: 15 km/h on the shortest way.')
print('Average Duration: ', destination_bubi.far_away(lat1, long1, lat2, long2)[1], 'minutes')