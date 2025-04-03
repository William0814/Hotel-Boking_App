import pandas as pd


df = pd.read_csv("hotels.csv", dtype={"id":str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)
print(df_cards_security)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        
    def book(self):
     # Book a hotel by changing its avalibility to no
     df.loc[df["id"] == self.hotel_id, "available"] = "no"
     df.to_csv("hotels.csv", index=False)

    def available(self):
        # Check if hotel is available
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == 'yes':
            return True
        else:
            return False
        

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, cvc, holder):
        card_data = {"number": self.number, "expiration": expiration, "cvc": cvc, "holder": holder}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard():
    def __init__(self, number):
        self.number = number

    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


class ReservationTicket:
     def __init__(self, customer_name, hotel_object):
         self.customer_name = customer_name
         self.hotel = hotel_object

     def generate_ticket(self):
         content = f"""Thank you for you rreservation!
         Here are you booking data:
         Name: {self.customer_name}
         Hotel Name: {self.hotel.name} """
         return content
     

print(df)
while True:
    try:
        hotel_ID = input("Enter the id of the hotel: ")
        hotel = Hotel(hotel_ID)

        if hotel.available():
            card_number = CreditCard(number="1234")
            card_security = SecureCreditCard(number="1234567890123456")
            if card_number.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
                if card_security.authenticate(given_password="mypass"):
                    hotel.book()
                    name = input("Enter your name: ")
                    reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
                    print(reservation_ticket.generate_ticket())
                    break
                else:
                    print("Authentication failed.")
                    break
            else:
                print("card not found")
                break
        else:
            print("No reservation, hotel is not free")
            break
    except ValueError:
        print("-------------------------------- \n"
            "Please enter a hotel ID valid. \n"
            "--------------------------------")
        print(df)
        continue

            
