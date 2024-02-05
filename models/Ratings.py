class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coffee_rating = db.Column(db.String, nullable=False)
    wifi_rating = db.Column(db.String, nullable=False)
    power = db.Column(db.String, nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey('caffees.id'))

    def __repr__(self):
        return f'<Rating for Cafe {self.cafe_id}>'