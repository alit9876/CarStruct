class Car:
    def __init__(self,serialNumber = None,name=None,model=None,color=None,manufacturer=None,Features=None,mileage=None,engineCC=None,price=None,Reviews=None):
        self.serialNumber =serialNumber
        self.name =name
        self.color =color
        self.model =model
        self.manufacturer =manufacturer
        self.mileage =mileage
        self.engineCC =engineCC
        self.Features =Features
        self.price =price
        self.Reviews =Reviews
        
    # to get the price in float type
    def get_numeric_price(self):
        try:
            return float(self.price)
        except ValueError:
            return None
        
    def to_list(self):
        # Convert car attributes to a list
        return [self.serialNumber, self.name, self.model, self.color, self.manufacturer,
                self.Features, self.mileage, self.engineCC, self.price, self.Reviews]

