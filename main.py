import pandas

df = pandas.read_csv('hotels.csv')
df_cards = pandas.read_csv('cards.csv', dtype=str).to_dict(orient='records')
df_card_security = pandas.read_csv('card_security.csv', dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.hotel_name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def available(self):
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        if availability == 'yes':
            return True
        else:
            return False


class SpaHotelReservation(Hotel):
    def book_spa_packade(self):
        pass


class Reservation:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f'''
    Thank you for reservation. 
    Here are you booking data:
    Name: {self.customer_name}
    Hotel: {self.hotel.hotel_name}
    '''
        return content


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f'''
    Thank you for your SPA reservation. 
    Here are you SPA booking data:
    Name: {self.customer_name}
    Hotel: {self.hotel.hotel_name}
    '''
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {'number': self.number, 'expiration': expiration,
                     'holder': holder, 'cvc': cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security['number'] == self.number, 'password'].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
hotel_id = int(input('Enter the ID of the hotel: '))
hotel = SpaHotelReservation(hotel_id)
if hotel.available():
    credit_card = SecureCreditCard(number='1234567890123456')
    if credit_card.validate(expiration='12/26', holder='JOHN SMITH', cvc='123'):
        if credit_card.authenticate(given_password='mypass'):
            hotel.book()
            name = input('Enter your name: ')
            reservation_ticket = Reservation(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
            spa_reservation = input('Would you like to reserve Spa place in the hotel? (y/n): ')
            if spa_reservation == 'y':
                hotel.book_spa_packade()
                spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate())
            else:
                print('Thanks for letting us know.')
        else:
            print('The password is wrong. Authentication failed')
    else:
        print('There was a problem with your payment.')
else:
    print('Hotel is not free.')