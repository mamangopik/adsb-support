from datetime import datetime
from geopy.distance import geodesic

class adsb_to_distance():
    def __init__(self,target):
        self.target_coordinates = target
        # Initialize variables
        self.unique_messages = {}
        self.result = []
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
                'timestamp': datetime.strptime(parts[6] + ' ' + parts[7], '%Y/%m/%d %H:%M:%S.%f'),
                'latitude': float(parts[14]),
                'longitude': float(parts[15]),
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
                        distance = self.calculate_distance(target_coordinates, coordinates)
                        print(coordinates)
                        print(distance)
                        return distance
                    else:
                        print("data not contains location value or invalid")
                        return -1
                else:
                    print("data not contains location value or invalid")
                    return -1
            else:
                print("data not contains location value or invalid")
                return -1
        except:
            print("data not contains location value or invalid")
            return -1

if __name__ == '__main__':
    # Coordinates for comparison
    target_coordinates = (-6.27831, 106.82939)
    extarctor  = adsb_to_distance(target_coordinates)
    data = "MSG,3,1,1,8A0516,1,2023/09/27,09:35:30.564,2023/09/27,09:35:30.618,,22525,,,-5.96241,108.01180,,,0,,0,0"
    print(extarctor.get_distance(data))
    # # Process each line
    # try:
    #     data = "MSG,3,1,1,8A0516,1,2023/09/27,09:35:30.564,2023/09/27,09:35:30.618,,22525,,,-5.96241,108.01180,,,0,,0,0"
    #     if data.startswith("MSG"):
    #         message = extarctor.parse_adsb_message(data)
    #         if message:
    #             if 'latitude' in message:
    #                 coordinates = (message['latitude'], message['longitude'])
    #                 distance = extarctor.calculate_distance(target_coordinates, coordinates)
    #                 print(coordinates)
    #                 print(distance)
    #             else:
    #                 print("data not contains location value or invalid")
    #         else:
    #             print("data not contains location value or invalid")
    #     else:
    #         print("data not contains location value or invalid")
    # except:
    #     print("data not contains location value or invalid")