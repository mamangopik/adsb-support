from datetime import datetime
from geopy.distance import geodesic

class adsb_to_distance():
    def __init__(self,target):
        self.target_coordinates = target
    # Function to calculate the distance between two sets of latitude and longitude coordinates
    def calculate_distance(self,coord1, coord2):
        """
        Calculate the distance in kilometers between two sets of latitude and longitude coordinates.

        Args:
        coord1: Tuple, representing the first coordinates as (latitude, longitude).
        coord2: Tuple, representing the second coordinates as (latitude, longitude).

        Returns:
        float: The distance between the two points in kilometers.
        """
        distance = geodesic(coord1, coord2).kilometers
        return distance

    # Function to parse ADS-B messages
    def parse_adsb_message(self,message):
        parts = message.split(',')
        if len(parts) >= 22 and parts[14] and parts[15]:
            return {
                'type': parts[1],
                'timestamp': str(datetime.strptime(parts[6] + ' ' + parts[7], '%Y/%m/%d %H:%M:%S.%f')),
                'latitude': float(parts[14]),
                'longitude': float(parts[15]),
                'ICAO':parts[4]
            }
        else:
            return None
    def get_distance(self,message):
        try:
            data = message
            if data.startswith("MSG"):
                message = self.parse_adsb_message(data)
                if message:
                    if 'latitude' in message:
                        coordinates = (message['latitude'], message['longitude'])
                        distance = self.calculate_distance(self.target_coordinates, coordinates)
                        # print(coordinates)
                        # print(distance)
                        return distance
                    else:
                        # print("data not contains location value or invalid")
                        return 0
                else:
                    # print("data not contains location value or invalid")
                    return 0
            else:
                # print("data not contains location value or invalid")
                return 0
        except:
            # print("data not contains location value or invalid")
            return 0



if __name__ == '__main__':
    target_coordinates = (-6.27831, 106.82939)
    extarctor  = adsb_to_distance(target_coordinates)
    data = "MSG,3,1,1,8A09A6,1,2023/09/27,11:33:53.224,2023/09/27,11:33:53.249,,7075,,,-6.24657,107.26738,,,0,,0,0"
    print(extarctor.get_distance(data))