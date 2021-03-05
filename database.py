# database.py

class Database:
    def __init__(self, filename):
        #initialize variables used in the database and load the file
        self.filename = filename
        self.items = []
        self.file = None
        self.load()

    def load(self):
        #read the file
        self.file = open(self.filename, "r")
        self.file.close()

    def add_item(self, item_name, category, expiration_date):
        # Take out all spaces
        item_name.strip()
        category.strip()
        expiration_date.strip()
        # Format the item
        new_item = {'Name': item_name, 'Category': category, 'Expiration Date': expiration_date}
        # Add the formatted item to the text file
        self.items.append(new_item)
        self.save()

    def remove_item(self, item_name, category, expiration_date):
        # Take out all spaces
        item_name.strip()
        category.strip()
        expiration_date.strip()
        for item in self.items:
            # If the item searched for exists, take out the item
            if item_name == item['Name']:
                existing_item = {'Name': item_name, 'Category': category, 'Expiration Date': expiration_date}
                try:
                    self.items.remove(existing_item)
                # Do not run if the item does not exist
                except:
                    return -1
        self.save()

    def save(self):
        #write file
        with open(self.filename, "w") as file:
            file.write(str(self.items))
