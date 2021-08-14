from app.extensions import marshmallow as ma


class TermSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("term", "date_added", "date_updated", "id")

    # Smart hyperlinking
    # _links = ma.Hyperlinks(
    #     {
    #         "self": ma.URLFor("terms_info", values=dict(id="<id>")),
    #         "collection": ma.URLFor("terms"),
    #     }
    # )


term_schema = TermSchema()
