class Caffees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cafe = db.Column(db.String(250), nullable=False, unique=True)
    location = db.Column(db.String(250), nullable=False)
    open = db.Column(db.String, nullable=False)
    close = db.Column(db.String, nullable=False)
    ratings = db.relationship('Rating', backref='cafe')

    def __repr__(self):
        return f'<Caffee {self.cafe}>'