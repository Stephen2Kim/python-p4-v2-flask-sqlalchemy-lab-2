from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Define a one-to-many relationship with Review
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to get items directly from reviews
    items = association_proxy('reviews', 'item', creator=lambda item: Review(item=item))

    # Custom serialization method to avoid recursion
    def to_dict(self):
        items_dict = []
        if self.items:
            for item in self.items:
                if item:  # Ensure that the item is not None
                    items_dict.append(item.to_dict())
        # Include 'reviews' explicitly here
        reviews_dict = []
        if self.reviews:
            for review in self.reviews:
                reviews_dict.append(review.to_dict())

        return {
            'id': self.id,
            'name': self.name,
            'items': items_dict,  # Return the list only if it's not empty
            'reviews': reviews_dict,  # Explicitly include the reviews
        }




class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Define a one-to-many relationship with Review
    reviews = db.relationship('Review', back_populates='item')

    # Custom serialization method to avoid recursion
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.to_dict() for review in self.reviews] if self.reviews else [],
        }


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)

    # Define relationships to Customer and Item
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # Custom serialization method to avoid recursion
    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer': {'id': self.customer.id, 'name': self.customer.name} if self.customer else None,
            'item': {'id': self.item.id, 'name': self.item.name} if self.item else None,
        }

